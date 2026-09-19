"""Repository contracts for file upload metadata and audit logs."""

from abc import ABC, abstractmethod
from uuid import UUID

from .audit import AuditLog
from .entities import FileUpload


class FileUploadRepository(ABC):
    """Persistence contract for file upload metadata."""

    @abstractmethod
    async def save(self, upload: FileUpload) -> None:
        """Save upload metadata."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        upload_id: str,
    ) -> FileUpload | None:
        """Retrieve an upload by its identifier."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        limit: int = 50,
    ) -> list[FileUpload]:
        """Retrieve recent uploaded files."""
        raise NotImplementedError


class AuditLogRepository(ABC):
    """Persistence contract for file upload audit events."""

    @abstractmethod
    async def save(self, audit_log: AuditLog) -> None:
        """Save an audit event."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_upload_id(
        self,
        upload_id: UUID,
    ) -> list[AuditLog]:
        """Retrieve audit events for an upload."""
        raise NotImplementedError

