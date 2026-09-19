from datetime import datetime, timezone
from io import BytesIO

from docx import Document

from .base import FileParser
from .metadata import ParsedMetadata


class DOCXParser(FileParser):
    """Parse DOCX files and extract document metadata."""

    def parse(
        self,
        file_name: str,
        mime_type: str,
        file_content: bytes,
    ) -> ParsedMetadata:
        """Parse a DOCX file and return its metadata."""

        document = Document(BytesIO(file_content))

        properties = document.core_properties

        title = properties.title or None
        author = properties.author or None

        return ParsedMetadata(
            file_name=file_name,
            file_type="DOCX",
            mime_type=mime_type,
            file_size=len(file_content),
            title=title,
            author=author,
            created_at=datetime.now(timezone.utc),
            parsed_status="SUCCESS",
        )