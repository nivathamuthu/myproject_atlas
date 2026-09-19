"""Application use cases for file uploads."""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4
from datetime import datetime
from ..domain.audit import AuditLog
from ..domain.entities import FileUpload
from ..domain.repository import (
    AuditLogRepository,
    FileUploadRepository,
)
from ..domain.storage import FileStorage
from ..domain.value_objects import (
    ContentType,
    FileHash,
    FileName,
    FileSize,
    StorageReference,
)
from ..security.signature_validator import (
    is_supported_file_type,
    validate_file_signature,
)
from ..parsing.factory import ParserFactory
from ..infrastructure.audit_logger import audit_log
from ..infrastructure.clamav_scanner import (
    ClamAVScanner,
    MalwareDetectedError,
)
from .commands import UploadFileCommand
from .dto import UploadResult


class UploadFileUseCase:
    """Handle secure file upload validation and storage."""

    def __init__(
        self,
        repository: FileUploadRepository,
        audit_repository: AuditLogRepository,
        storage: FileStorage,
        trusted_storage: FileStorage,
        antivirus_scanner: ClamAVScanner,
        trusted_bucket: str,
    ) -> None:
        self._repository = repository
        self._audit_repository = audit_repository
        self._storage = storage
        self._trusted_storage = trusted_storage
        self._antivirus_scanner = antivirus_scanner
        self._trusted_bucket = trusted_bucket

    async def _audit(
        self,
        upload_id: UUID,
        event: str,
        result: str,
        *,
        file_name: str | None = None,
        file_size: int | None = None,
        sha256: str | None = None,
        reason: str | None = None,
    ) -> None:
        """Write an audit event to terminal logs and PostgreSQL."""

        audit_log(
            event,
            file_name=file_name,
            file_size=file_size,
            upload_id=str(upload_id),
            sha256=sha256,
            result=result,
            reason=reason,
        )

        audit_entity = AuditLog.create(
            upload_id=upload_id,
            event=event,
            result=result,
            file_name=file_name,
            file_size=file_size,
            sha256=sha256,
            reason=reason,
        )

        await self._audit_repository.save(
            audit_entity
        )

    async def execute(
        self,
        command: UploadFileCommand,
    ) -> UploadResult:
        """Process an uploaded file through the secure pipeline."""

        # --------------------------------------------------
        # 1. GENERATE UPLOAD ID
        # --------------------------------------------------

        upload_id = uuid4()

        # --------------------------------------------------
        # 2. UPLOAD STARTED
        # --------------------------------------------------

        await self._audit(
            upload_id,
            "UPLOAD_STARTED",
            "STARTED",
            file_name=command.file_name,
            file_size=command.file_size,
        )

        # --------------------------------------------------
        # 3. CHECK FILE EXTENSION
        # --------------------------------------------------

        if not is_supported_file_type(
            command.file_name
        ):
            await self._audit(
                upload_id,
                "UPLOAD_REJECTED",
                "REJECTED",
                file_name=command.file_name,
                file_size=command.file_size,
                reason="Unsupported file type",
            )

            raise ValueError(
                "Unsupported file type."
            )

        # --------------------------------------------------
        # 4. GENERATE UNIQUE STORAGE KEY
        # --------------------------------------------------

        extension = Path(
            command.file_name
        ).suffix.lower()

        storage_key = (
            f"{uuid4().hex}{extension}"
        )

        # --------------------------------------------------
        # 5. STORE IN QUARANTINE
        # --------------------------------------------------

        storage_reference = self._storage.store(
            storage_key,
            command.file_content,
        )

        await self._audit(
            upload_id,
            "QUARANTINE_STORED",
            "SUCCESS",
            file_name=command.file_name,
            file_size=command.file_size,
        )

        trusted_reference: str | None = None

        try:
            # --------------------------------------------------
            # 6. FILE SIGNATURE VALIDATION
            # --------------------------------------------------

            if not validate_file_signature(
                command.file_name,
                command.file_content,
            ):
                await self._audit(
                    upload_id,
                    "SIGNATURE_VALIDATION_FAILED",
                    "REJECTED",
                    file_name=command.file_name,
                    file_size=command.file_size,
                    reason=(
                        "File content does not "
                        "match file type"
                    ),
                )

                raise ValueError(
                    "File content does not match "
                    "the file type."
                )

            await self._audit(
                upload_id,
                "SIGNATURE_VALIDATED",
                "SUCCESS",
                file_name=command.file_name,
                file_size=command.file_size,
            )

            # --------------------------------------------------
            # 7. CLAMAV MALWARE SCAN
            # --------------------------------------------------

            try:
                self._antivirus_scanner.scan(
                    command.file_content,
                )

                await self._audit(
                    upload_id,
                    "MALWARE_SCAN",
                    "CLEAN",
                    file_name=command.file_name,
                    file_size=command.file_size,
                )

            except MalwareDetectedError as exc:
                await self._audit(
                    upload_id,
                    "MALWARE_DETECTED",
                    "REJECTED",
                    file_name=command.file_name,
                    file_size=command.file_size,
                    reason=str(exc),
                )

                raise

            # --------------------------------------------------
            # 8. CALCULATE SHA-256
            # --------------------------------------------------

            sha256_hash = hashlib.sha256(
                command.file_content
            ).hexdigest()

            await self._audit(
                upload_id,
                "HASH_CALCULATED",
                "SUCCESS",
                file_name=command.file_name,
                file_size=command.file_size,
                sha256=sha256_hash,
            )

            # --------------------------------------------------
            # 9. DUPLICATE CHECK
            # --------------------------------------------------

            existing_upload = (
                await self._repository.get_by_sha256(
                    sha256_hash
                )
            )

            if existing_upload is not None:
                await self._audit(
                    upload_id,
                    "DUPLICATE_DETECTED",
                    "REJECTED",
                    file_name=command.file_name,
                    file_size=command.file_size,
                    sha256=sha256_hash,
                    reason=(
                        "File with same SHA-256 "
                        "already exists"
                    ),
                )

                raise ValueError(
                    "A file with the same content "
                    "already exists."
                )

            await self._audit(
                upload_id,
                "DUPLICATE_CHECK",
                "NOT_FOUND",
                file_name=command.file_name,
                file_size=command.file_size,
                sha256=sha256_hash,
            )

            # --------------------------------------------------
            # 10. SELECT PARSER
            # --------------------------------------------------

            parser = ParserFactory.get_parser(
                command.file_name
            )

            # --------------------------------------------------
            # 11. PARSE FILE
            # --------------------------------------------------

            parsed_metadata = parser.parse(
                file_name=command.file_name,
                mime_type=command.content_type,
                file_content=command.file_content,
            )

            await self._audit(
                upload_id,
                "PARSING_COMPLETED",
                parsed_metadata.parsed_status,
                file_name=command.file_name,
                file_size=command.file_size,
                sha256=sha256_hash,
            )

            # --------------------------------------------------
            # 12. MOVE TO TRUSTED STORAGE
            # --------------------------------------------------

            trusted_reference = self._storage.move(
                storage_reference=storage_reference,
                destination_bucket=self._trusted_bucket,
            )

            await self._audit(
                upload_id,
                "MOVED_TO_TRUSTED",
                "SUCCESS",
                file_name=command.file_name,
                file_size=command.file_size,
                sha256=sha256_hash,
            )

            # --------------------------------------------------
            # 13. CREATE DOMAIN ENTITY
            # --------------------------------------------------

            now = datetime.utcnow()

            upload = FileUpload(
                upload_id=upload_id,
                file_name=FileName(
                    command.file_name
                ),
                file_size=FileSize(
                    command.file_size
                ),
                content_type=ContentType(
                    command.content_type
                ),
                sha256_hash=FileHash(
                    sha256_hash
                ),
                file_type=parsed_metadata.file_type,
                page_count=parsed_metadata.page_count,
                sheet_count=parsed_metadata.sheet_count,
                slide_count=parsed_metadata.slide_count,
                title=parsed_metadata.title,
                author=parsed_metadata.author,
                parsed_status=parsed_metadata.parsed_status,
                created_at=now,
                updated_at=now,
            )

            # --------------------------------------------------
            # 14. MARK FILE AS STORED
            # --------------------------------------------------

            upload.mark_stored(
                StorageReference(
                    trusted_reference
                ),
            )

            # --------------------------------------------------
            # 15. SAVE METADATA
            # --------------------------------------------------

            await self._repository.save(
                upload
            )

            # --------------------------------------------------
            # 16. UPLOAD COMPLETED
            # --------------------------------------------------

            await self._audit(
                upload_id,
                "UPLOAD_COMPLETED",
                "SUCCESS",
                file_name=command.file_name,
                file_size=command.file_size,
                sha256=sha256_hash,
            )

            return UploadResult(
                upload_id=upload.upload_id,
                file_name=upload.file_name.value,
                status=upload.status,
                storage_reference=trusted_reference,
            )

        except Exception as exc:
            # --------------------------------------------------
            # 17. CLEANUP
            # --------------------------------------------------

            if trusted_reference is None:
                self._storage.delete(
                    storage_reference,
                )

                await self._audit(
                    upload_id,
                    "QUARANTINE_CLEANUP",
                    "SUCCESS",
                    file_name=command.file_name,
                    file_size=command.file_size,
                    reason=type(exc).__name__,
                )

            else:
                self._trusted_storage.delete(
                    trusted_reference,
                )

                await self._audit(
                    upload_id,
                    "TRUSTED_STORAGE_CLEANUP",
                    "SUCCESS",
                    file_name=command.file_name,
                    file_size=command.file_size,
                    reason=type(exc).__name__,
                )

            await self._audit(
                upload_id,
                "UPLOAD_REJECTED",
                "REJECTED",
                file_name=command.file_name,
                file_size=command.file_size,
                reason=str(exc),
            )

            raise

