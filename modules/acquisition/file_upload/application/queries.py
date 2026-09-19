"""Queries for the file upload application layer."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetUploadStatusQuery:
    """Request the status of an uploaded file."""

    upload_id: UUID