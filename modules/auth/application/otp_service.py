"""OTP generation and verification services."""

import secrets
from datetime import datetime, timedelta

from pwdlib import PasswordHash
from sqlalchemy import select

from modules.auth.application.email_service import send_otp_email
from modules.auth.infrastructure.models import (
    EmailVerificationOTPModel,
    UserModel,
)
from modules.shared.database.connection import session_factory


password_hash = PasswordHash.recommended()

OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 5


def generate_otp() -> str:
    """Generate a cryptographically secure 6-digit OTP."""
    return f"{secrets.randbelow(1_000_000):06d}"


async def create_otp(user_id) -> str:
    """Create, securely store, and email a new OTP."""

    otp = generate_otp()
    otp_hash = password_hash.hash(otp)

    expires_at = datetime.utcnow() + timedelta(
        minutes=OTP_EXPIRY_MINUTES
    )

    async with session_factory() as session:
        result = await session.execute(
            select(EmailVerificationOTPModel).where(
                EmailVerificationOTPModel.user_id == user_id,
                EmailVerificationOTPModel.used.is_(False),
            )
        )

        existing_otps = result.scalars().all()

        for existing_otp in existing_otps:
            existing_otp.used = True

        new_otp = EmailVerificationOTPModel(
            user_id=user_id,
            otp_hash=otp_hash,
            expires_at=expires_at,
            attempts=0,
            used=False,
        )

        session.add(new_otp)
        await session.commit()

        result = await session.execute(
            select(UserModel).where(
                UserModel.id == user_id
            )
        )

        user = result.scalar_one()

    await send_otp_email(
        recipient_email=user.email,
        otp=otp,
    )

    return otp


async def verify_otp(
    email: str,
    otp: str,
) -> bool:
    """Verify an email OTP."""

    async with session_factory() as session:
        result = await session.execute(
            select(UserModel).where(
                UserModel.email == email.lower()
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            return False

        if user.is_email_verified:
            return True

        result = await session.execute(
            select(EmailVerificationOTPModel)
            .where(
                EmailVerificationOTPModel.user_id == user.id,
                EmailVerificationOTPModel.used.is_(False),
            )
            .order_by(
                EmailVerificationOTPModel.created_at.desc()
            )
        )

        otp_record = result.scalars().first()

        if not otp_record:
            return False

        if datetime.utcnow() > otp_record.expires_at:
            otp_record.used = True
            await session.commit()
            return False

        if otp_record.attempts >= MAX_OTP_ATTEMPTS:
            otp_record.used = True
            await session.commit()
            return False

        otp_record.attempts += 1

        if not password_hash.verify(
            otp,
            otp_record.otp_hash,
        ):
            await session.commit()
            return False

        otp_record.used = True
        user.is_email_verified = True
        user.updated_at = datetime.utcnow()

        await session.commit()

        return True