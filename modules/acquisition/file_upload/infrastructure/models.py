"""SQLAlchemy models for file upload persistence."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Integer, String,Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy.orm import Mapped, mapped_column

from modules.shared.database.base import Base

class FileUploadModel(Base):
    """PostgreSQL representation of a file upload."""

    __tablename__ = "file_uploads"

    upload_id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sha256_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    # Parsed metadata
    file_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    page_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    sheet_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    slide_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    author: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    parsed_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    storage_reference: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    
class FileUploadAuditLogModel(Base):
    """PostgreSQL representation of a file upload audit event."""

    __tablename__ = "file_upload_audit_logs"

    audit_id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    upload_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    file_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    file_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    event: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    result: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    sha256: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    reason: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )



