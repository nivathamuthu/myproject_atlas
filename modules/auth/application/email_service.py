"""Email sending service for Atlas authentication."""

import os
from email.message import EmailMessage

import aiosmtplib
from dotenv import load_dotenv


load_dotenv()


async def send_otp_email(
    recipient_email: str,
    otp: str,
) -> None:
    """Send an email verification OTP."""

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from_email = os.getenv(
        "SMTP_FROM_EMAIL",
        smtp_username,
    )
    smtp_from_name = os.getenv(
        "SMTP_FROM_NAME",
        "Atlas",
    )

    if not smtp_host:
        raise RuntimeError("SMTP_HOST is not configured.")

    if not smtp_username:
        raise RuntimeError("SMTP_USERNAME is not configured.")

    if not smtp_password:
        raise RuntimeError("SMTP_PASSWORD is not configured.")

    if not smtp_from_email:
        raise RuntimeError("SMTP_FROM_EMAIL is not configured.")

    message = EmailMessage()

    message["From"] = f"{smtp_from_name} <{smtp_from_email}>"
    message["To"] = recipient_email
    message["Subject"] = "Atlas Email Verification Code"

    message.set_content(
        f"""Hello,

Your Atlas verification code is:

{otp}

This code will expire in 5 minutes.

If you did not create an Atlas account, you can safely ignore this email.

Regards,
Atlas Team
"""
    )

    await aiosmtplib.send(
        message,
        hostname=smtp_host,
        port=smtp_port,
        username=smtp_username,
        password=smtp_password,
        start_tls=True,
    )