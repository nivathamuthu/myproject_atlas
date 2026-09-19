"""Authentication request and response schemas."""

from pydantic import BaseModel, EmailStr, Field
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    """Registration request."""

    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class RegisterResponse(BaseModel):
    """Registration response."""

    message: str
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    """OTP verification request."""

    email: EmailStr
    otp: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
    )


class VerifyOTPResponse(BaseModel):
    """OTP verification response."""

    message: str


class ResendOTPRequest(BaseModel):
    """OTP resend request."""

    email: EmailStr


class ResendOTPResponse(BaseModel):
    """OTP resend response."""

    message: str