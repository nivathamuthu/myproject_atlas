"""Commands for Bulk Import application use cases."""

from dataclasses import dataclass
from typing import Sequence

from modules.acquisition.file_upload.application.commands import (
    UploadFileCommand,
)


@dataclass(frozen=True)
class BulkImportCommand:
    """Request to process multiple files as one bulk import."""

    files: Sequence[UploadFileCommand]

    def __post_init__(self) -> None:
        if not self.files:
            raise ValueError(
                "Bulk import must contain at least one file."
            )