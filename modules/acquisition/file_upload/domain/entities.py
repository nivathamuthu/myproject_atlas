"""Domain entities for file uploads."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .value_objects import (
    ContentType,
    FileHash,
    FileName,
    FileSize,
    FileUploadStatus,
    StorageReference,
)


def utc_now() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.utcnow()


@dataclass
class FileUpload:
    """Domain entity representing an uploaded file."""

    upload_id: UUID
    file_name: FileName
    file_size: FileSize
    content_type: ContentType
    sha256_hash: FileHash

    # Parsed metadata
    file_type: str | None = None
    page_count: int | None = None
    sheet_count: int | None = None
    slide_count: int | None = None
    title: str | None = None
    author: str | None = None
    parsed_status: str = "PENDING"

    # Upload status
    status: FileUploadStatus = FileUploadStatus.PENDING
    storage_reference: StorageReference | None = None

    # Timestamps
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def mark_stored(
        self,
        storage_reference: StorageReference,
    ) -> None:
        """Mark the upload as successfully stored."""

        self.storage_reference = storage_reference
        self.status = FileUploadStatus.STORED
        self.updated_at = utc_now()

    def mark_failed(self) -> None:
        """Mark the upload as failed."""

        self.status = FileUploadStatus.FAILED
        self.updated_at = utc_now()