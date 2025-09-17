from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, UniqueConstraint, Enum
from app.database import Base
from datetime import datetime
import enum


class ApplicationStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    L1_APPROVED = "L1_APPROVED"
    L1_REJECTED = "L1_REJECTED"
    L2_APPROVED = "L2_APPROVED"
    L2_REJECTED = "L2_REJECTED"


class DecisionEnum(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ODApplication(Base):
    __tablename__ = "od_applications"

    application_id = Column(String(36), primary_key=True)
    registration_number = Column(
        String(20),
        ForeignKey("students.registration_number", ondelete="CASCADE"),
        nullable=False,
    )
    event_id = Column(
        String(36),
        ForeignKey("events.event_id", ondelete="CASCADE"),
        nullable=False,
    )

    status = Column(Enum(ApplicationStatusEnum), default=ApplicationStatusEnum.PENDING)
    level1_approver_id = Column(
        String(20), ForeignKey("faculty.faculty_id", ondelete="SET NULL")
    )
    level1_decision = Column(Enum(DecisionEnum), default=DecisionEnum.PENDING)
    level1_decision_at = Column(TIMESTAMP)

    level2_approver_id = Column(
        String(20), ForeignKey("faculty.faculty_id", ondelete="SET NULL")
    )
    level2_decision = Column(Enum(DecisionEnum), default=DecisionEnum.PENDING)
    level2_decision_at = Column(TIMESTAMP)

    applied_at = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("registration_number", "event_id", name="unique_student_event"),
    )
