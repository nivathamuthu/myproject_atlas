"""Authentication API routes."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from modules.auth.application.otp_service import (
    create_otp,
    verify_otp,
)
from modules.auth.application.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from modules.auth.infrastructure.models import UserModel
from modules.auth.presentation.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ResendOTPRequest,
    ResendOTPResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
)
from modules.shared.database.connection import session_factory


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
) -> RegisterResponse:
    """Register a new Atlas user."""

    async with session_factory() as session:
        result = await session.execute(
            select(UserModel).where(
                UserModel.email == request.email.lower()
            )
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        user = UserModel(
            email=request.email.lower(),
            password_hash=hash_password(request.password),
            is_email_verified=False,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

    await create_otp(user.id)

    return RegisterResponse(
        message="Registration successful. Please verify your email.",
        email=user.email,
    )


@router.post(
    "/verify-otp",
    response_model=VerifyOTPResponse,
)
async def verify_email_otp(
    request: VerifyOTPRequest,
) -> VerifyOTPResponse:
    """Verify a user's email address using OTP."""

    verified = await verify_otp(
        email=request.email,
        otp=request.otp,
    )

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code.",
        )

    return VerifyOTPResponse(
        message="Email verified successfully.",
    )


@router.post(
    "/resend-otp",
    response_model=ResendOTPResponse,
)
async def resend_otp(
    request: ResendOTPRequest,
) -> ResendOTPResponse:
    """Generate a new OTP for an unverified user."""

    async with session_factory() as session:
        result = await session.execute(
            select(UserModel).where(
                UserModel.email == request.email.lower()
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found.",
            )

        if user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified.",
            )

        user_id = user.id

    await create_otp(user_id)

    return ResendOTPResponse(
        message="A new verification code has been generated.",
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
) -> LoginResponse:
    """Authenticate a verified Atlas user."""

    async with session_factory() as session:
        result = await session.execute(
            select(UserModel).where(
                UserModel.email == request.email.lower()
            )
        )

        user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before signing in.",
        )

    if not verify_password(
        request.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        user_id=str(user.id),
        email=user.email,
    )

    return LoginResponse(
        message="Login successful.",
        access_token=access_token,
        token_type="bearer",
    )