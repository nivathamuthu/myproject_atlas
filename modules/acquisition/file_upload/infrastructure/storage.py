"""MinIO implementation of file content storage."""

from io import BytesIO

from minio import Minio
from minio.commonconfig import CopySource
from minio.error import S3Error

from ..domain.storage import FileStorage


class MinIOFileStorage(FileStorage):
    """Store and manage file content in MinIO."""

    def __init__(
        self,
        client: Minio,
        bucket_name: str,
    ) -> None:
        self._client = client
        self._bucket_name = bucket_name

    def store(
        self,
        file_name: str,
        content: bytes,
    ) -> str:
        """Store file content and return its storage reference."""

        self._client.put_object(
            self._bucket_name,
            file_name,
            BytesIO(content),
            length=len(content),
        )

        return file_name

    def retrieve(
        self,
        storage_reference: str,
    ) -> bytes:
        """Retrieve file content from MinIO."""

        response = self._client.get_object(
            self._bucket_name,
            storage_reference,
        )

        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    def delete(
        self,
        storage_reference: str,
    ) -> None:
        """Delete file content from MinIO."""

        try:
            self._client.remove_object(
                self._bucket_name,
                storage_reference,
            )
        except S3Error as exc:
            raise RuntimeError(
                f"Failed to delete object from MinIO: "
                f"{storage_reference}"
            ) from exc

    def move(
        self,
        storage_reference: str,
        destination_bucket: str,
    ) -> str:
        """Move a file from the current bucket to another MinIO bucket."""

        source = CopySource(
            self._bucket_name,
            storage_reference,
        )

        self._client.copy_object(
            destination_bucket,
            storage_reference,
            source,
        )

        self._client.remove_object(
            self._bucket_name,
            storage_reference,
        )

        return storage_reference