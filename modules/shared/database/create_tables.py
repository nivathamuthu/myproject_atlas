"""Create database tables."""

import asyncio

from modules.acquisition.file_upload.infrastructure.models import (
    FileUploadAuditLogModel,
    FileUploadModel,
)
from modules.auth.infrastructure.models import (
    EmailVerificationOTPModel,
    UserModel,
)
from modules.shared.database.base import Base
from modules.shared.database.connection import engine


async def create_tables() -> None:
    """Create all registered database tables."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())