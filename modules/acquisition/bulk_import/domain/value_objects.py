"""Value objects for the Bulk Import domain."""

from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class BulkImportStatus(str, Enum):
    """Lifecycle status of a bulk import operation."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"
    FAILED = "FAILED"


@dataclass(frozen=True)
class BulkImportId:
    """Unique identifier for a bulk import operation."""

    value: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise ValueError(
                "BulkImportId must contain a valid UUID."
            )

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class BulkImportFileCount:
    """Validated number of files in a bulk import."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(
                "File count cannot be negative."
            )


@dataclass(frozen=True)
class BulkImportSuccessCount:
    """Number of successfully imported files."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(
                "Successful file count cannot be negative."
            )


@dataclass(frozen=True)
class BulkImportDuplicateCount:
    """Number of duplicate files detected."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(
                "Duplicate file count cannot be negative."
            )


@dataclass(frozen=True)
class BulkImportFailureCount:
    """Number of files that failed during import."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(
                "Failed file count cannot be negative."
            )


@dataclass(frozen=True)
class BulkImportFileName:
    """Validated file name associated with a bulk import item."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError(
                "File name cannot be empty."
            )

        if len(self.value) > 255:
            raise ValueError(
                "File name cannot exceed 255 characters."
            )

        if "/" in self.value or "\\" in self.value:
            raise ValueError(
                "File name cannot contain path separators."
            )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class BulkImportSummary:
    """Summary of files processed during a bulk import."""

    total: BulkImportFileCount
    successful: BulkImportSuccessCount
    duplicates: BulkImportDuplicateCount
    failed: BulkImportFailureCount

    def __post_init__(self) -> None:
        calculated_total = (
            self.successful.value
            + self.duplicates.value
            + self.failed.value
        )

        if calculated_total != self.total.value:
            raise ValueError(
                "Bulk import summary counts do not match total."
            )