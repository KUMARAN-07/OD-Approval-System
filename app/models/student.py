# app/models/student.py
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from app.database import Base
from datetime import datetime

class Student(Base):
    __tablename__ = "students"

    registration_number = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(100))
    year_of_study = Column(Integer)
    is_password_reset = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
