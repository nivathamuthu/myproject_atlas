"""Domain entities for Bulk Import."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from .value_objects import (
    BulkImportDuplicateCount,
    BulkImportFailureCount,
    BulkImportFileCount,
    BulkImportId,
    BulkImportStatus,
    BulkImportSuccessCount,
)


@dataclass
class BulkImport:
    """Domain entity representing a bulk import operation."""

    import_id: BulkImportId

    status: BulkImportStatus = BulkImportStatus.PENDING

    total_files: BulkImportFileCount = field(
        default_factory=lambda: BulkImportFileCount(0)
    )

    successful_files: BulkImportSuccessCount = field(
        default_factory=lambda: BulkImportSuccessCount(0)
    )

    duplicate_files: BulkImportDuplicateCount = field(
        default_factory=lambda: BulkImportDuplicateCount(0)
    )

    failed_files: BulkImportFailureCount = field(
        default_factory=lambda: BulkImportFailureCount(0)
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    started_at: datetime | None = None

    completed_at: datetime | None = None

    def start(self) -> None:
        """Start processing the bulk import."""

        if self.status != BulkImportStatus.PENDING:
            raise ValueError(
                "Only a pending bulk import can be started."
            )

        self.status = BulkImportStatus.PROCESSING
        self.started_at = datetime.now(timezone.utc)

    def record_success(self) -> None:
        """Record one successfully imported file."""

        self._ensure_processing()

        self.successful_files = BulkImportSuccessCount(
            self.successful_files.value + 1
        )

    def record_duplicate(self) -> None:
        """Record one duplicate file."""

        self._ensure_processing()

        self.duplicate_files = BulkImportDuplicateCount(
            self.duplicate_files.value + 1
        )

    def record_failure(self) -> None:
        """Record one failed file."""

        self._ensure_processing()

        self.failed_files = BulkImportFailureCount(
            self.failed_files.value + 1
        )

    def complete(self) -> None:
        """Complete the bulk import based on processing results."""

        self._ensure_processing()

        processed_files = (
            self.successful_files.value
            + self.duplicate_files.value
            + self.failed_files.value
        )

        if processed_files != self.total_files.value:
            raise ValueError(
                "Bulk import cannot be completed until "
                "all files have been processed."
            )

        if self.failed_files.value > 0:
            self.status = (
                BulkImportStatus.COMPLETED_WITH_ERRORS
            )
        else:
            self.status = BulkImportStatus.COMPLETED

        self.completed_at = datetime.now(timezone.utc)

    def fail(self) -> None:
        """Mark the entire bulk import as failed."""

        if self.status not in (
            BulkImportStatus.PENDING,
            BulkImportStatus.PROCESSING,
        ):
            raise ValueError(
                "Only a pending or processing bulk import "
                "can be marked as failed."
            )

        self.status = BulkImportStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)

    def _ensure_processing(self) -> None:
        """Ensure the import is currently being processed."""

        if self.status != BulkImportStatus.PROCESSING:
            raise ValueError(
                "Bulk import must be in PROCESSING state."
            )

    @property
    def processed_files(self) -> int:
        """Return the number of files already processed."""

        return (
            self.successful_files.value
            + self.duplicate_files.value
            + self.failed_files.value
        )

    @property
    def remaining_files(self) -> int:
        """Return the number of files still waiting to be processed."""

        return max(
            self.total_files.value - self.processed_files,
            0,
        )

    @property
    def progress_percentage(self) -> float:
        """Return bulk import processing progress."""

        if self.total_files.value == 0:
            return 0.0

        return (
            self.processed_files
            / self.total_files.value
        ) * 100