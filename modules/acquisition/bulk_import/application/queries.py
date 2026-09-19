"""Queries for Bulk Import application use cases."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetBulkImportQuery:
    """Request details of a specific bulk import."""

    import_id: UUID


@dataclass(frozen=True)
class GetRecentBulkImportsQuery:
    """Request recent bulk import operations."""

    limit: int = 50

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise ValueError(
                "Limit must be at least 1."
            )

        if self.limit > 100:
            raise ValueError(
                "Limit cannot exceed 100."
            )