"""Domain exceptions for Bulk Import."""


class BulkImportError(Exception):
    """Base exception for Bulk Import domain errors."""


class InvalidBulkImportStateError(BulkImportError):
    """Raised when an invalid state transition is attempted."""


class BulkImportNotFoundError(BulkImportError):
    """Raised when a requested bulk import does not exist."""


class BulkImportAlreadyCompletedError(BulkImportError):
    """Raised when an operation is attempted on a completed import."""


class BulkImportEmptyError(BulkImportError):
    """Raised when a bulk import contains no files."""


class BulkImportFileLimitExceededError(BulkImportError):
    """Raised when the maximum number of files is exceeded."""


class BulkImportProcessingError(BulkImportError):
    """Raised when bulk import processing fails."""