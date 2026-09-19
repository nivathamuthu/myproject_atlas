"""Domain entity for file upload audit events."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class AuditLog:
    """Domain entity representing a file upload audit event."""

    audit_id: UUID
    upload_id: UUID
    event: str
    result: str
    file_name: str | None = None
    file_size: int | None = None
    sha256: str | None = None
    reason: str | None = None
    created_at: datetime | None = None

    @classmethod
    def create(
        cls,
        upload_id: UUID,
        event: str,
        result: str,
        *,
        file_name: str | None = None,
        file_size: int | None = None,
        sha256: str | None = None,
        reason: str | None = None,
    ) -> "AuditLog":
        """Create a new audit event."""

        return cls(
            audit_id=uuid4(),
            upload_id=upload_id,
            event=event,
            result=result,
            file_name=file_name,
            file_size=file_size,
            sha256=sha256,
            reason=reason,
            created_at=datetime.now(),
        )
