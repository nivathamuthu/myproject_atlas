"""File upload API endpoints."""

import os
from typing import Annotated
from fastapi import APIRouter, File, HTTPException, UploadFile
from minio import Minio

from modules.acquisition.file_upload.application.commands import (
    UploadFileCommand,
)
from modules.acquisition.file_upload.application.use_cases import (
    UploadFileUseCase,
)
from modules.acquisition.file_upload.infrastructure.audit_repository import (
    PostgreSQLAuditLogRepository,
)
from modules.acquisition.file_upload.infrastructure.clamav_scanner import (
    ClamAVScanner,
    MalwareDetectedError,
)
from modules.acquisition.file_upload.infrastructure.repository import (
    PostgreSQLFileUploadRepository,
)
from modules.acquisition.file_upload.infrastructure.storage import (
    MinIOFileStorage,
)
from modules.shared.database.connection import session_factory


router = APIRouter(
    prefix="/api/files",
    tags=["File Upload"],
)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_FILE_SIZE = 100 * 1024 * 1024
MAX_BULK_FILES = 50

MINIO_ENDPOINT = os.getenv(
    "MINIO_ENDPOINT",
    "localhost:9000",
)

MINIO_ACCESS_KEY = os.getenv(
    "MINIO_ACCESS_KEY",
    "minioadmin",
)

MINIO_SECRET_KEY = os.getenv(
    "MINIO_SECRET_KEY",
    "minioadmin",
)

MINIO_SECURE = (
    os.getenv(
        "MINIO_SECURE",
        "false",
    ).lower()
    == "true"
)

QUARANTINE_BUCKET = os.getenv(
    "MINIO_BUCKET_QUARANTINE",
    "atlas-quarantine",
)

TRUSTED_BUCKET = os.getenv(
    "MINIO_BUCKET_TRUSTED",
    "atlas-trusted",
)

CLAMAV_HOST = os.getenv(
    "CLAMAV_HOST",
    "127.0.0.1",
)

CLAMAV_PORT = int(
    os.getenv(
        "CLAMAV_PORT",
        "3310",
    )
)


# ============================================================
# MINIO CLIENT
# ============================================================

def get_minio_client() -> Minio:
    """Create a MinIO client."""

    return Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE,
    )


def ensure_bucket(
    client: Minio,
    bucket_name: str,
) -> None:
    """Create the bucket if it does not already exist."""

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


# ============================================================
# GET UPLOADED FILES
# ============================================================

@router.get("")
async def get_uploaded_files(
    limit: int = 50,
):
    """
    Retrieve recent uploaded files.

    Also returns total document count and
    total storage occupied by all uploaded documents.
    """

    if limit < 1:
        limit = 1

    if limit > 100:
        limit = 100

    repository = PostgreSQLFileUploadRepository(
        session_factory=session_factory,
    )

    try:
        uploads = await repository.get_all(
            limit=limit,
        )

        total_count, total_size = (
            await repository.get_storage_stats()
        )

    except Exception as exc:
        print(
            "GET FILES ERROR:",
            repr(exc),
        )

        print(
            "ERROR TYPE:",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve uploaded files.",
        ) from exc

    return {
        "count": total_count,
        "total_size": total_size,
        "files": [
            {
                "upload_id": str(
                    upload.upload_id
                ),

                "file_name": (
                    upload.file_name.value
                ),

                "file_size": (
                    upload.file_size.value
                ),

                "content_type": (
                    upload.content_type.value
                ),

                "file_type": (
                    upload.file_type
                ),

                "page_count": (
                    upload.page_count
                ),

                "sheet_count": (
                    upload.sheet_count
                ),

                "slide_count": (
                    upload.slide_count
                ),

                "title": (
                    upload.title
                ),

                "author": (
                    upload.author
                ),

                "parsed_status": (
                    upload.parsed_status
                ),

                "status": (
                    upload.status.value
                ),

                "storage_reference": (
                    upload.storage_reference.value
                    if upload.storage_reference
                    else None
                ),

                "created_at": (
                    upload.created_at.isoformat()
                    if upload.created_at
                    else None
                ),

                "updated_at": (
                    upload.updated_at.isoformat()
                    if upload.updated_at
                    else None
                ),
            }
            for upload in uploads
        ],
    }


# ============================================================
# CREATE UPLOAD USE CASE
# ============================================================

def create_upload_use_case() -> UploadFileUseCase:
    """
    Create the existing secure file upload use case.

    This is shared by both single and bulk uploads.
    """

    client = get_minio_client()

    ensure_bucket(
        client,
        QUARANTINE_BUCKET,
    )

    ensure_bucket(
        client,
        TRUSTED_BUCKET,
    )

    repository = PostgreSQLFileUploadRepository(
        session_factory=session_factory,
    )

    audit_repository = PostgreSQLAuditLogRepository(
        session_factory=session_factory,
    )

    quarantine_storage = MinIOFileStorage(
        client=client,
        bucket_name=QUARANTINE_BUCKET,
    )

    trusted_storage = MinIOFileStorage(
        client=client,
        bucket_name=TRUSTED_BUCKET,
    )

    antivirus_scanner = ClamAVScanner(
        host=CLAMAV_HOST,
        port=CLAMAV_PORT,
    )

    return UploadFileUseCase(
        repository=repository,
        audit_repository=audit_repository,
        storage=quarantine_storage,
        trusted_storage=trusted_storage,
        antivirus_scanner=antivirus_scanner,
        trusted_bucket=TRUSTED_BUCKET,
    )


# ============================================================
# UPLOAD FILE
# ============================================================

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
):
    """
    Upload a document through the secure Atlas pipeline.
    """

    # --------------------------------------------------------
    # 1. Validate filename
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required.",
        )

    # --------------------------------------------------------
    # 2. Read file
    # --------------------------------------------------------

    contents = await file.read()

    file_size = len(contents)

    # --------------------------------------------------------
    # 3. Validate size
    # --------------------------------------------------------

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=(
                "File size exceeds the maximum "
                "allowed size of 100 MB."
            ),
        )

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # --------------------------------------------------------
    # 4. Create upload use case
    # --------------------------------------------------------

    try:
        use_case = create_upload_use_case()

    except Exception as exc:
        print(
            "MINIO CONNECTION ERROR:",
            repr(exc),
        )

        print(
            "ERROR TYPE:",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "Object storage is currently "
                "unavailable."
            ),
        ) from exc

    # --------------------------------------------------------
    # 5. Create command
    # --------------------------------------------------------

    command = UploadFileCommand(
        file_name=file.filename,
        file_size=file_size,
        content_type=(
            file.content_type
            or "application/octet-stream"
        ),
        file_content=contents,
    )

    # --------------------------------------------------------
    # 6. Execute secure upload pipeline
    # --------------------------------------------------------

    try:
        result = await use_case.execute(
            command,
        )

        return {
            "upload_id": str(
                result.upload_id
            ),
            "file_name": result.file_name,
            "status": result.status.value,
            "storage_reference": (
                result.storage_reference
            ),
        }

    except MalwareDetectedError as exc:
        print(
            "MALWARE DETECTED:",
            repr(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        message = str(exc)

        print(
            "UPLOAD VALIDATION ERROR:",
            repr(exc),
        )

        if (
            "same content" in message.lower()
            or "duplicate" in message.lower()
        ):
            raise HTTPException(
                status_code=409,
                detail=message,
            ) from exc

        raise HTTPException(
            status_code=400,
            detail=message,
        ) from exc

    except Exception as exc:
        print(
            "UPLOAD ERROR:",
            repr(exc),
        )

        print(
            "ERROR TYPE:",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "The uploaded file could not "
                "be processed."
            ),
        ) from exc


# ============================================================
# BULK UPLOAD FILES
# ============================================================

@router.post("/bulk")
async def bulk_upload_files(
    files: Annotated[list[UploadFile], File(...)],
):
    """
    Upload multiple documents through the
    existing secure Atlas upload pipeline.

    Each file is processed independently.
    A failed or duplicate file does not stop
    the remaining files.
    """

    # --------------------------------------------------------
    # 1. Validate bulk request
    # --------------------------------------------------------

    if not files:
        raise HTTPException(
            status_code=400,
            detail="At least one file is required.",
        )

    if len(files) > MAX_BULK_FILES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Maximum {MAX_BULK_FILES} files "
                "can be uploaded at once."
            ),
        )

    # --------------------------------------------------------
    # 2. Create shared upload use case
    # --------------------------------------------------------

    try:
        upload_use_case = create_upload_use_case()

    except Exception as exc:
        print(
            "BULK MINIO CONNECTION ERROR:",
            repr(exc),
        )

        print(
            "ERROR TYPE:",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "Object storage is currently "
                "unavailable."
            ),
        ) from exc

    # --------------------------------------------------------
    # 3. Result counters
    # --------------------------------------------------------

    results = []

    successful = 0
    duplicates = 0
    failed = 0

    # --------------------------------------------------------
    # 4. Process every file independently
    # --------------------------------------------------------

    for file in files:

        file_name = (
            file.filename
            or "unknown"
        )

        try:
            # ------------------------------------------------
            # Filename validation
            # ------------------------------------------------

            if not file.filename:
                results.append(
                    {
                        "file_name": file_name,
                        "status": "FAILED",
                        "message": (
                            "File name is required."
                        ),
                    }
                )

                failed += 1
                continue

            # ------------------------------------------------
            # Read file
            # ------------------------------------------------

            contents = await file.read()

            file_size = len(contents)

            # ------------------------------------------------
            # Empty file
            # ------------------------------------------------

            if file_size == 0:
                results.append(
                    {
                        "file_name": file_name,
                        "status": "FAILED",
                        "message": (
                            "The uploaded file "
                            "is empty."
                        ),
                    }
                )

                failed += 1
                continue

            # ------------------------------------------------
            # File size
            # ------------------------------------------------

            if file_size > MAX_FILE_SIZE:
                results.append(
                    {
                        "file_name": file_name,
                        "status": "FAILED",
                        "message": (
                            "File size exceeds "
                            "the maximum allowed "
                            "size of 100 MB."
                        ),
                    }
                )

                failed += 1
                continue

            # ------------------------------------------------
            # Create command
            # ------------------------------------------------

            command = UploadFileCommand(
                file_name=file.filename,
                file_size=file_size,
                content_type=(
                    file.content_type
                    or "application/octet-stream"
                ),
                file_content=contents,
            )

            # ------------------------------------------------
            # Run existing secure pipeline
            # ------------------------------------------------

            result = await upload_use_case.execute(
                command
            )

            # ------------------------------------------------
            # Success
            # ------------------------------------------------

            results.append(
                {
                    "file_name": result.file_name,
                    "status": "SUCCESS",
                    "upload_id": str(
                        result.upload_id
                    ),
                    "storage_reference": (
                        result.storage_reference
                    ),
                }
            )

            successful += 1

        # ----------------------------------------------------
        # Malware
        # ----------------------------------------------------

        except MalwareDetectedError as exc:

            print(
                "BULK MALWARE DETECTED:",
                repr(exc),
            )

            results.append(
                {
                    "file_name": file_name,
                    "status": "FAILED",
                    "message": str(exc),
                }
            )

            failed += 1

        # ----------------------------------------------------
        # Validation / duplicate
        # ----------------------------------------------------

        except ValueError as exc:

            message = str(exc)

            print(
                "BULK VALIDATION ERROR:",
                repr(exc),
            )

            if (
                "same content" in message.lower()
                or "duplicate" in message.lower()
            ):
                results.append(
                    {
                        "file_name": file_name,
                        "status": "DUPLICATE",
                        "message": message,
                    }
                )

                duplicates += 1

            else:
                results.append(
                    {
                        "file_name": file_name,
                        "status": "FAILED",
                        "message": message,
                    }
                )

                failed += 1

        # ----------------------------------------------------
        # Unexpected error
        # ----------------------------------------------------

        except Exception as exc:

            print(
                "BULK FILE ERROR:",
                repr(exc),
            )

            print(
                "ERROR TYPE:",
                type(exc).__name__,
            )

            results.append(
                {
                    "file_name": file_name,
                    "status": "FAILED",
                    "message": (
                        "The uploaded file "
                        "could not be processed."
                    ),
                }
            )

            failed += 1

    # --------------------------------------------------------
    # 5. Final bulk status
    # --------------------------------------------------------

    total = len(files)

    if failed > 0:
        overall_status = "COMPLETED_WITH_ERRORS"
    else:
        overall_status = "COMPLETED"

    # --------------------------------------------------------
    # 6. Return bulk summary
    # --------------------------------------------------------

    return {
        "status": overall_status,
        "total": total,
        "successful": successful,
        "duplicates": duplicates,
        "failed": failed,
        "results": results,
    }