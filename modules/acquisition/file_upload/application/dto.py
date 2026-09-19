"""Data transfer objects for file upload use cases."""

from dataclasses import dataclass
from uuid import UUID

from ..domain.value_objects import FileUploadStatus


@dataclass(frozen=True)
class UploadResult:
    """Result returned after a file upload operation."""

    upload_id: UUID
    file_name: str
    status: FileUploadStatus
    storage_reference: str | None = None