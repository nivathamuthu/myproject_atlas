from uuid import UUID

from modules.acquisition.file_upload.application.commands import UploadFileCommand
from modules.acquisition.file_upload.application.use_cases import UploadFileUseCase
from modules.acquisition.file_upload.domain.entities import FileUpload
from modules.acquisition.file_upload.domain.repository import FileUploadRepository
from modules.acquisition.file_upload.domain.storage import FileStorage


class FakeStorage(FileStorage):
    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}

    def store(self, file_name: str, content: bytes) -> str:
        self.files[file_name] = content
        return file_name

    def retrieve(self, storage_reference: str) -> bytes:
        return self.files[storage_reference]

    def delete(self, storage_reference: str) -> None:
        del self.files[storage_reference]


class FakeRepository(FileUploadRepository):
    def __init__(self) -> None:
        self.uploads: dict[UUID, FileUpload] = {}

    async def save(self, upload: FileUpload) -> None:
        self.uploads[upload.upload_id] = upload

    async def get_by_id(self, upload_id: str) -> FileUpload | None:
        return self.uploads.get(UUID(upload_id))


async def test_upload_file() -> None:
    storage = FakeStorage()
    repository = FakeRepository()

    use_case = UploadFileUseCase(
        repository=repository,
        storage=storage,
    )

    command = UploadFileCommand(
        file_name="sample.pdf",
        file_size=4,
        content_type="application/pdf",
        file_content=b"test",
    )

    result = await use_case.execute(command)

    assert result.file_name == "sample.pdf"
    assert result.status.value == "STORED"
    assert result.storage_reference == "sample.pdf"
    assert storage.files["sample.pdf"] == b"test"
    assert len(repository.uploads) == 1