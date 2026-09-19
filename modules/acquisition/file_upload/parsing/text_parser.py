from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from io import BytesIO
import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from .base import FileParser
from .metadata import ParsedMetadata


class TextParser(FileParser):
    """Parse text-based and structured file formats."""

    def parse(
        self,
        file_name: str,
        mime_type: str,
        file_content: bytes,
    ) -> ParsedMetadata:
        """Parse a text-based file and return its metadata."""

        extension = Path(file_name).suffix.lower()

        # Default metadata
        title = Path(file_name).stem
        author = "Atlas"

        if extension == ".json":
            data = json.loads(file_content.decode("utf-8"))

            if isinstance(data, dict):
                title = data.get("title") or title
                author = data.get("author") or author

        elif extension == ".xml":
            ET.fromstring(file_content)

        elif extension == ".csv":
            self._parse_csv(file_content)

        elif extension == ".eml":
            title, author = self._parse_eml(
                file_content,
                title,
                author,
            )

        elif extension in {
            ".txt",
            ".md",
            ".markdown",
            ".html",
            ".htm",
        }:
            file_content.decode("utf-8")

        else:
            raise ValueError(
                f"Unsupported text format: {extension}"
            )

        return ParsedMetadata(
            file_name=file_name,
            file_type=extension.lstrip(".").upper(),
            mime_type=mime_type,
            file_size=len(file_content),
            title=title,
            author=author,
            created_at=datetime.now(timezone.utc),
            parsed_status="SUCCESS",
        )

    @staticmethod
    def _parse_csv(file_content: bytes) -> None:
        """Validate that CSV content can be read."""

        text = file_content.decode("utf-8")

        reader = csv.reader(
            BytesIO(text.encode("utf-8"))
            .read()
            .decode("utf-8")
            .splitlines()
        )

        for _ in reader:
            pass

    @staticmethod
    def _parse_eml(
        file_content: bytes,
        default_title: str,
        default_author: str,
    ) -> tuple[str, str]:
        """Parse EML metadata."""

        message = BytesParser(
            policy=policy.default
        ).parsebytes(file_content)

        title = message.get("subject") or default_title
        author = message.get("from") or default_author

        return title, author