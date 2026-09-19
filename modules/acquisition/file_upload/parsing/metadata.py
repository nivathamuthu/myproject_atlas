from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ParsedMetadata:
    file_name: str
    file_type: str
    mime_type: str
    file_size: int

    page_count: int | None = None
    sheet_count: int | None = None
    slide_count: int | None = None

    title: str | None = None
    author: str | None = None

    created_at: datetime | None = None
    parsed_status: str = "SUCCESS"