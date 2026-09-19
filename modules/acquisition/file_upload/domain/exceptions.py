"""Domain-specific exceptions for file uploads."""


class FileUploadError(Exception):
    """Base exception for file upload domain errors."""


class EmptyFileError(FileUploadError):
    """Raised when an uploaded file is empty."""


class UnsupportedFileTypeError(FileUploadError):
    """Raised when the uploaded file type is not supported."""


class FileTooLargeError(FileUploadError):
    """Raised when the uploaded file exceeds the allowed size."""