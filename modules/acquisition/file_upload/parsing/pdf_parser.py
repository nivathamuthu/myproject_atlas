"""PDF parser implementation."""

from datetime import datetime, timezone
from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError, PdfStreamError

from .base import FileParser
from .metadata import ParsedMetadata


class PDFParser(FileParser):
    """Parse PDF files and extract document metadata."""

    def parse(
        self,
        file_name: str,
        mime_type: str,
        file_content: bytes,
    ) -> ParsedMetadata:
        """Parse a PDF file and return its metadata."""

        try:
            reader = PdfReader(
                BytesIO(file_content)
            )

            page_count = len(reader.pages)

            metadata = reader.metadata

        except (PdfReadError, PdfStreamError) as exc:
            raise ValueError(
                "The uploaded PDF is corrupted or unreadable."
            ) from exc

        title = None
        author = None

        if metadata:
            title = metadata.title
            author = metadata.author

        # Remove default/anonymous metadata values.
        if title == "(anonymous)":
            title = None

        if author == "(anonymous)":
            author = None

        return ParsedMetadata(
            file_name=file_name,
            file_type="PDF",
            mime_type=mime_type,
            file_size=len(file_content),
            page_count=page_count,
            title=title,
            author=author,
            created_at=datetime.now(timezone.utc),
            parsed_status="SUCCESS",
        )

