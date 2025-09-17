from sqlalchemy import Column, String, Text, Date, Integer, Enum as SAEnum, ForeignKey, TIMESTAMP
from app.database import Base
from datetime import datetime
from enum import Enum  # ✅ Use Python Enum for the status values

# ✅ Define Python Enum for statuses
class EventStatusEnum(str, Enum):
    OPEN = "OPEN"
    FILLED = "FILLED"
    CLOSED = "CLOSED"

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    date = Column(Date, nullable=False)
    location = Column(String(255))
    seat_limit = Column(Integer, nullable=False)
    remaining_seats = Column(Integer, nullable=False)
    # ✅ Use SQLAlchemy Enum with alias SAEnum
    status = Column(SAEnum(EventStatusEnum, name="event_status_enum"), default=EventStatusEnum.OPEN)

    created_by = Column(String(20), ForeignKey("faculty.faculty_id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
