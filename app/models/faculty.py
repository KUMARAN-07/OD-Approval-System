# app/models/faculty.py
from sqlalchemy import Column, String, Boolean, TIMESTAMP
from app.database import Base
from datetime import datetime

class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    designation = Column(String(100))
    department = Column(String(100))
    is_password_reset = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
