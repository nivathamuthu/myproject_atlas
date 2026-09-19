from pathlib import Path

from .base import FileParser
from .docx_parser import DOCXParser
from .pdf_parser import PDFParser
from .pptx_parser import PPTXParser
from .text_parser import TextParser
from .xlsx_parser import XLSXParser


class ParserFactory:
    """Create the appropriate parser for a file."""

    _parsers: dict[str, type[FileParser]] = {
        ".pdf": PDFParser,
        ".docx": DOCXParser,
        ".pptx": PPTXParser,
        ".xlsx": XLSXParser,
        ".csv": TextParser,
        ".json": TextParser,
        ".xml": TextParser,
        ".html": TextParser,
        ".htm": TextParser,
        ".md": TextParser,
        ".markdown": TextParser,
        ".txt": TextParser,
        ".eml": TextParser,
    }

    @classmethod
    def get_parser(cls, file_name: str) -> FileParser:
        """Return the parser matching the file extension."""

        extension = Path(file_name).suffix.lower()

        parser_class = cls._parsers.get(extension)

        if parser_class is None:
            raise ValueError(
                f"No parser available for file type: {extension}"
            )

        return parser_class()