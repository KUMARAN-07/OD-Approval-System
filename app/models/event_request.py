# app/models/event_request.py
from sqlalchemy import Column, String, Text, Date, Enum, ForeignKey, TIMESTAMP
from app.database import Base
from datetime import datetime
import enum

class RequestStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class EventRequest(Base):
    __tablename__ = "event_requests"

    request_id = Column(String(36), primary_key=True)
    registration_number = Column(String(20), ForeignKey("students.registration_number", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    date = Column(Date, nullable=False)
    status = Column(Enum(RequestStatusEnum), default=RequestStatusEnum.PENDING)
    reviewed_by = Column(String(20), ForeignKey("faculty.faculty_id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    decision_at = Column(TIMESTAMP)
