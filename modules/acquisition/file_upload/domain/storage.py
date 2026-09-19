"""Storage contract for uploaded file content."""

from abc import ABC, abstractmethod


class FileStorage(ABC):
    """Contract for storing and managing file content."""

    @abstractmethod
    def store(
        self,
        file_name: str,
        content: bytes,
    ) -> str:
        """Store file content and return a storage reference."""
        raise NotImplementedError

    @abstractmethod
    def retrieve(
        self,
        storage_reference: str,
    ) -> bytes:
        """Retrieve file content using a storage reference."""
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        storage_reference: str,
    ) -> None:
        """Delete stored file content."""
        raise NotImplementedError

    @abstractmethod
    def move(
        self,
        storage_reference: str,
        destination_bucket: str,
    ) -> str:
        """Move a file to another storage bucket."""
        raise NotImplementedError