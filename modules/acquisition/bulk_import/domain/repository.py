"""Repository contracts for the Bulk Import domain."""

from abc import ABC, abstractmethod
from uuid import UUID

from .entities import BulkImport


class BulkImportRepository(ABC):
    """Repository contract for Bulk Import persistence."""

    @abstractmethod
    async def save(
        self,
        bulk_import: BulkImport,
    ) -> None:
        """Persist a bulk import operation."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        import_id: UUID,
    ) -> BulkImport | None:
        """Retrieve a bulk import by its identifier."""
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        bulk_import: BulkImport,
    ) -> None:
        """Update an existing bulk import operation."""
        raise NotImplementedError

    @abstractmethod
    async def get_recent(
        self,
        limit: int = 50,
    ) -> list[BulkImport]:
        """Retrieve recent bulk import operations."""
        raise NotImplementedError