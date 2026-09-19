"""PostgreSQL repository for file uploads."""
from modules.acquisition.file_upload.domain.value_objects import (
    ContentType,
    FileHash,
    FileName,
    FileSize,
    FileUploadStatus,
    StorageReference,
)
from uuid import UUID

from sqlalchemy import func, select

from modules.acquisition.file_upload.domain.entities import FileUpload
from modules.acquisition.file_upload.domain.repository import (
    FileUploadRepository,
)

from .models import FileUploadModel


class PostgreSQLFileUploadRepository(
    FileUploadRepository
):
    """PostgreSQL implementation of the file upload repository."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def save(
        self,
        upload: FileUpload,
    ) -> None:
        """Save file upload metadata."""

        async with self._session_factory() as session:
            model = FileUploadModel(
                upload_id=upload.upload_id,
                file_name=upload.file_name.value,
                file_size=upload.file_size.value,
                content_type=upload.content_type.value,
                sha256_hash=upload.sha256_hash.value,
                file_type=upload.file_type,
                page_count=upload.page_count,
                sheet_count=upload.sheet_count,
                slide_count=upload.slide_count,
                title=upload.title,
                author=upload.author,
                parsed_status=upload.parsed_status,
                status=upload.status.value,
                storage_reference=(
                    upload.storage_reference.value
                    if upload.storage_reference
                    else None
                ),
                created_at=upload.created_at,
                updated_at=upload.updated_at,
            )

            session.add(model)
            await session.commit()

    async def get_by_id(
        self,
        upload_id: str,
    ) -> FileUpload | None:
        """Retrieve an upload by its identifier."""

        async with self._session_factory() as session:
            result = await session.execute(
                select(FileUploadModel).where(
                    FileUploadModel.upload_id
                    == UUID(upload_id)
                )
            )

            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_entity(model)

    async def get_all(
        self,
        limit: int = 50,
    ) -> list[FileUpload]:
        """Retrieve recent uploaded files."""

        async with self._session_factory() as session:
            result = await session.execute(
                select(FileUploadModel)
                .order_by(
                    FileUploadModel.created_at.desc()
                )
                .limit(limit)
            )

            models = result.scalars().all()

            return [
                self._to_entity(model)
                for model in models
            ]

    async def get_storage_stats(
        self,
    ) -> tuple[int, int]:
        """
        Return total uploaded file count and
        total uploaded storage in bytes.
        """

        async with self._session_factory() as session:
            result = await session.execute(
                select(
                    func.count(
                        FileUploadModel.upload_id
                    ),
                    func.coalesce(
                        func.sum(
                            FileUploadModel.file_size
                        ),
                        0,
                    ),
                )
            )

            total_count, total_size = result.one()

            return (
                int(total_count),
                int(total_size),
            )

    async def get_by_sha256(
        self,
        sha256: str,
    ) -> FileUpload | None:
        """Retrieve an upload using its SHA-256 hash."""

        async with self._session_factory() as session:
            result = await session.execute(
                select(FileUploadModel).where(
                    FileUploadModel.sha256_hash
                    == sha256
                )
            )

            model = result.scalar_one_or_none()

            if model is None:
                return None

            return self._to_entity(model)

    @staticmethod
    def _to_entity(
        model: FileUploadModel,
    ) -> FileUpload:
        """Convert a database model into a domain entity."""

        return FileUpload(
            upload_id=model.upload_id,
            file_name=FileName(model.file_name),
            file_size=FileSize(model.file_size),
            content_type=ContentType(model.content_type),
            sha256_hash=FileHash(model.sha256_hash),
            file_type=model.file_type,
            page_count=model.page_count,
            sheet_count=model.sheet_count,
            slide_count=model.slide_count,
            title=model.title,
            author=model.author,
            parsed_status=model.parsed_status,
            status=FileUploadStatus(model.status),
            storage_reference=(
                StorageReference(model.storage_reference)
                if model.storage_reference
                else None
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
