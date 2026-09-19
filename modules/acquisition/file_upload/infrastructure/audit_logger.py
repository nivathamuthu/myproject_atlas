"""Audit logging for file upload security events."""

import logging


logging.basicConfig(
    level=logging.INFO,
)


logger = logging.getLogger("atlas.file_upload.audit")


def audit_log(
    event: str,
    *,
    file_name: str | None = None,
    file_size: int | None = None,
    upload_id: str | None = None,
    sha256: str | None = None,
    result: str | None = None,
    reason: str | None = None,
) -> None:
    """Write a structured security audit event."""

    details = {
        "event": event,
        "file_name": file_name,
        "file_size": file_size,
        "upload_id": upload_id,
        "sha256": sha256,
        "result": result,
        "reason": reason,
    }

    logger.info(
        "FILE_UPLOAD_AUDIT %s",
        details,
    )