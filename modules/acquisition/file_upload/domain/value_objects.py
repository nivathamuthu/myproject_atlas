"""Value objects for the file upload domain."""

from dataclasses import dataclass
from enum import StrEnum
import re


class FileUploadStatus(StrEnum):
    """Possible states of a file upload."""

    PENDING = "PENDING"
    STORED = "STORED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class FileName:
    """Validated file name."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("File name cannot be empty.")

        if "/" in self.value or "\\" in self.value:
            raise ValueError("File name must not contain path separators.")


@dataclass(frozen=True)
class FileSize:
    """Validated file size in bytes."""

    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("File size must be greater than zero.")


@dataclass(frozen=True)
class ContentType:
    """Validated MIME content type."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Content type cannot be empty.")


@dataclass(frozen=True)
class StorageReference:
    """Reference to the file stored in object storage."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Storage reference cannot be empty.")


@dataclass(frozen=True)
class FileHash:
    """Validated SHA-256 hash of file content."""

    value: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", self.value):
            raise ValueError(
                "SHA-256 hash must be exactly 64 hexadecimal characters."
            )

        object.__setattr__(self, "value", self.value.lower())