"""Storage abstractions for Bulk Import."""

from abc import ABC, abstractmethod


class BulkImportStorage(ABC):
    """Contract for Bulk Import related storage operations."""

    @abstractmethod
    def store_batch_reference(
        self,
        import_id: str,
    ) -> str:
        """Create or return a storage reference for a bulk import."""
        raise NotImplementedError

    @abstractmethod
    def delete_batch_reference(
        self,
        storage_reference: str,
    ) -> None:
        """Delete a bulk import storage reference."""
        raise NotImplementedError