from abc import ABC, abstractmethod

from .metadata import ParsedMetadata


class FileParser(ABC):
    """Base interface for all file parsers."""

    @abstractmethod
    def parse(
        self,
        file_name: str,
        mime_type: str,
        file_content: bytes,
    ) -> ParsedMetadata:
        """Parse a file and return its metadata."""
        raise NotImplementedError