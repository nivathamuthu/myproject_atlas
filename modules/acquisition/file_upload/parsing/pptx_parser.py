from datetime import datetime, timezone
from io import BytesIO

from pptx import Presentation

from .base import FileParser
from .metadata import ParsedMetadata


class PPTXParser(FileParser):
    """Parse PPTX files and extract presentation metadata."""

    def parse(
        self,
        file_name: str,
        mime_type: str,
        file_content: bytes,
    ) -> ParsedMetadata:
        """Parse a PPTX file and return its metadata."""

        presentation = Presentation(BytesIO(file_content))

        properties = presentation.core_properties

        title = properties.title or None
        author = properties.author or None

        slide_count = len(presentation.slides)

        return ParsedMetadata(
            file_name=file_name,
            file_type="PPTX",
            mime_type=mime_type,
            file_size=len(file_content),
            slide_count=slide_count,
            title=title,
            author=author,
            created_at=datetime.now(timezone.utc),
            parsed_status="SUCCESS",
        )