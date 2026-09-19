"""Commands for file upload use cases."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UploadFileCommand:
    """Request to upload a file."""

    file_name: str
    file_size: int
    content_type: str
    file_content: bytes