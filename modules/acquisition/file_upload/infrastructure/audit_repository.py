"""PostgreSQL repository for file upload audit logs."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..domain.audit import AuditLog
from ..domain.repository import AuditLogRepository
from .models import FileUploadAuditLogModel


class PostgreSQLAuditLogRepository(AuditLogRepository):
    """Persist file upload audit events in PostgreSQL."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory = session_factory

    async def save(
        self,
        audit_log: AuditLog,
    ) -> None:
        """Save an audit event."""

        async with self._session_factory() as session:
            model = FileUploadAuditLogModel(
                audit_id=audit_log.audit_id,
                upload_id=audit_log.upload_id,
                file_name=audit_log.file_name,
                file_size=audit_log.file_size,
                event=audit_log.event,
                result=audit_log.result,
                sha256=audit_log.sha256,
                reason=audit_log.reason,
                created_at=audit_log.created_at,
            )

            session.add(model)
            await session.commit()

    async def get_by_upload_id(
        self,
        upload_id: UUID,
    ) -> list[AuditLog]:
        """Retrieve audit events for an upload."""

        async with self._session_factory() as session:
            result = await session.execute(
                select(FileUploadAuditLogModel)
                .where(
                    FileUploadAuditLogModel.upload_id
                    == upload_id,
                )
                .order_by(
                    FileUploadAuditLogModel.created_at.asc(),
                )
            )

            models = result.scalars().all()

            return [
                AuditLog(
                    audit_id=model.audit_id,
                    upload_id=model.upload_id,
                    event=model.event,
                    result=model.result,
                    file_name=model.file_name,
                    file_size=model.file_size,
                    sha256=model.sha256,
                    reason=model.reason,
                    created_at=model.created_at,
                )
                for model in models
            ]

