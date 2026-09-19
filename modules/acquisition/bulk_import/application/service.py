"""Application service for Bulk Import."""

from dataclasses import dataclass
from uuid import uuid4

from modules.acquisition.file_upload.application.use_cases import (
    UploadFileUseCase,
)
from modules.acquisition.file_upload.application.dto import (
    UploadResult,
)

from ..domain.entities import BulkImport
from ..domain.exceptions import (
    BulkImportEmptyError,
    BulkImportProcessingError,
)
from ..domain.value_objects import (
    BulkImportFileCount,
    BulkImportId,
)
from .commands import BulkImportCommand


@dataclass(frozen=True)
class BulkImportFileResult:
    """Result of processing one file."""

    file_name: str
    status: str
    upload_id: str | None = None
    message: str | None = None


@dataclass(frozen=True)
class BulkImportResult:
    """Result of the complete bulk import operation."""

    import_id: str
    status: str
    total: int
    successful: int
    duplicates: int
    failed: int
    results: list[BulkImportFileResult]


class BulkImportService:
    """Orchestrate multiple files through the secure upload pipeline."""

    def __init__(
        self,
        upload_file_use_case: UploadFileUseCase,
    ) -> None:
        self._upload_file_use_case = (
            upload_file_use_case
        )

    async def execute(
        self,
        command: BulkImportCommand,
    ) -> BulkImportResult:
        """Process all files independently."""

        if not command.files:
            raise BulkImportEmptyError(
                "Bulk import must contain at least one file."
            )

        bulk_import = BulkImport(
            import_id=BulkImportId(uuid4()),
            total_files=BulkImportFileCount(
                len(command.files)
            ),
        )

        bulk_import.start()

        results: list[BulkImportFileResult] = []

        for file_command in command.files:
            result = await self._process_file(
                file_command,
                results,
            )

            results.append(result)

            if result.status == "SUCCESS":
                bulk_import.record_success()

            elif result.status == "DUPLICATE":
                bulk_import.record_duplicate()

            else:
                bulk_import.record_failure()

        bulk_import.complete()

        return BulkImportResult(
            import_id=str(
                bulk_import.import_id
            ),
            status=bulk_import.status.value,
            total=bulk_import.total_files.value,
            successful=(
                bulk_import.successful_files.value
            ),
            duplicates=(
                bulk_import.duplicate_files.value
            ),
            failed=(
                bulk_import.failed_files.value
            ),
            results=results,
        )

    async def _process_file(
        self,
        file_command,
        results: list[BulkImportFileResult],
    ) -> BulkImportFileResult:
        """Process one file without stopping the bulk operation."""

        try:
            upload_result: UploadResult = (
                await self._upload_file_use_case.execute(
                    file_command
                )
            )

            return BulkImportFileResult(
                file_name=file_command.file_name,
                status="SUCCESS",
                upload_id=str(
                    upload_result.upload_id
                ),
            )

        except ValueError as exc:
            message = str(exc)

            if (
                "same content" in message.lower()
                or "duplicate" in message.lower()
            ):
                return BulkImportFileResult(
                    file_name=file_command.file_name,
                    status="DUPLICATE",
                    message=message,
                )

            return BulkImportFileResult(
                file_name=file_command.file_name,
                status="FAILED",
                message=message,
            )

        except Exception as exc:
            return BulkImportFileResult(
                file_name=file_command.file_name,
                status="FAILED",
                message=str(exc),
            )