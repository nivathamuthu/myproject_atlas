"""File type and signature validation for uploaded files."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".csv",
    ".xml",
    ".json",
    ".html",
    ".htm",
    ".md",
    ".markdown",
    ".eml",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".zip",
}


FILE_SIGNATURES: dict[str, list[bytes]] = {
    ".pdf": [
        b"%PDF-",
    ],
    ".jpg": [
        b"\xff\xd8\xff",
    ],
    ".jpeg": [
        b"\xff\xd8\xff",
    ],
    ".png": [
        b"\x89PNG\r\n\x1a\n",
    ],
    ".gif": [
        b"GIF87a",
        b"GIF89a",
    ],
    ".webp": [
        b"RIFF",
    ],
    ".zip": [
        b"PK\x03\x04",
        b"PK\x05\x06",
        b"PK\x07\x08",
    ],
    ".docx": [
        b"PK\x03\x04",
        b"PK\x05\x06",
        b"PK\x07\x08",
    ],
    ".xlsx": [
        b"PK\x03\x04",
        b"PK\x05\x06",
        b"PK\x07\x08",
    ],
    ".pptx": [
        b"PK\x03\x04",
        b"PK\x05\x06",
        b"PK\x07\x08",
    ],
}


def get_file_extension(file_name: str) -> str:
    """Return the normalized file extension."""
    return Path(file_name).suffix.lower()


def is_supported_file_type(file_name: str) -> bool:
    """Check whether the uploaded file type is supported."""
    extension = get_file_extension(file_name)

    return extension in SUPPORTED_EXTENSIONS


def _validate_json(file_content: bytes) -> bool:
    """Validate JSON content."""
    try:
        json.loads(file_content.decode("utf-8"))
        return True
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False


def _validate_xml(file_content: bytes) -> bool:
    """Validate XML content."""
    try:
        ET.fromstring(file_content)
        return True
    except (UnicodeDecodeError, ET.ParseError):
        return False


def _validate_text(file_content: bytes) -> bool:
    """Validate UTF-8 text content."""
    try:
        file_content.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _validate_webp(file_content: bytes) -> bool:
    """Validate WebP RIFF container."""
    return (
        len(file_content) >= 12
        and file_content[:4] == b"RIFF"
        and file_content[8:12] == b"WEBP"
    )


def _validate_zip_signature(file_content: bytes) -> bool:
    """Validate ZIP file signature."""
    return any(
        file_content.startswith(signature)
        for signature in FILE_SIGNATURES[".zip"]
    )


def validate_file_signature(
    file_name: str,
    file_content: bytes,
) -> bool:
    """
    Validate uploaded file type and content.

    Returns True only when the file matches the expected
    supported file format.
    """

    extension = get_file_extension(file_name)

    # Step 1: Extension whitelist.
    if extension not in SUPPORTED_EXTENSIONS:
        return False

    # Empty files are rejected.
    if not file_content:
        return False

    # Step 2: Binary signature validation.
    signatures = FILE_SIGNATURES.get(extension)

    if signatures:
        if extension == ".webp":
            return _validate_webp(file_content)

        return any(
            file_content.startswith(signature)
            for signature in signatures
        )

    # Step 3: Text-based formats.
    if extension == ".json":
        return _validate_json(file_content)

    if extension == ".xml":
        return _validate_xml(file_content)

    if extension in {
        ".csv",
        ".html",
        ".htm",
        ".md",
        ".markdown",
        ".eml",
        ".txt",
    }:
        return _validate_text(file_content)

    return False

