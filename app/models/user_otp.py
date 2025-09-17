# app/models/user_otp.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, TIMESTAMP
from app.database import Base
from datetime import datetime
import enum

class UserRoleEnum(str, enum.Enum):
    STUDENT = "STUDENT"
    FACULTY = "FACULTY"

class UserOTP(Base):
    __tablename__ = "user_otps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    role = Column(Enum(UserRoleEnum), nullable=False)
    otp_code = Column(String(6), nullable=False)
    otp_expiry = Column(TIMESTAMP, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
