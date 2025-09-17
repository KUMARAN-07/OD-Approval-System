# app/utils/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import getenv
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = int(getenv("EMAIL_PORT", 587))
EMAIL_USER = getenv("EMAIL_USER")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")


def send_otp_email(recipient: str, otp: str):
    subject = "Your OTP for OD Portal"
    body = f"""
    Dear user,

    Your OTP for logging into the OD Portal is: {otp}
    This OTP is valid for 5 minutes. Please do not share it with anyone.

    Regards,
    OD System
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, recipient, msg.as_string())
        print(f"✅ OTP sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
