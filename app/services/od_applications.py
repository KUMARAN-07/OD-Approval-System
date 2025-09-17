# app/services/od_applications.py

from uuid import uuid4
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.od_application import (
    ODApplication,
    ApplicationStatusEnum,
    DecisionEnum,
)
from app.models.faculty_student_mapping import FacultyStudentMapping
from app.schemas.od_application import ODApplicationCreate
from app.models.event import Event


def apply_for_od(
    db: Session,
    student_reg_no: str,
    application: ODApplicationCreate
) -> ODApplication:
    # 1) Check event exists & seat availability
    event = db.query(Event).filter_by(event_id=application.event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    if event.remaining_seats <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No seats available for this event"
        )

    # 2) Prevent duplicate applications
    existing = (
        db.query(ODApplication)
          .filter_by(
              registration_number=student_reg_no,
              event_id=application.event_id
          )
          .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already applied for this event"
        )

    # 3) Find counsellor mapping
    mapping = (
        db.query(FacultyStudentMapping)
          .filter_by(registration_number=student_reg_no)
          .first()
    )
    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No counsellor assigned to this student"
        )

    # 4) Create the OD application
    new_app = ODApplication(
        application_id=str(uuid4()),
        registration_number=student_reg_no,
        event_id=application.event_id,
        status=ApplicationStatusEnum.PENDING,
        level1_approver_id=mapping.counsellor_id,
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def list_student_applications(
    db: Session,
    student_reg_no: str
) -> List[ODApplication]:
    return db.query(ODApplication)\
             .filter_by(registration_number=student_reg_no)\
             .all()


def get_application_status(
    db: Session,
    application_id: str,
    student_reg_no: str
) -> ODApplication:
    app = db.query(ODApplication)\
            .filter_by(
                application_id=application_id,
                registration_number=student_reg_no
            )\
            .first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Application not found")
    return app


def cancel_application(
    db: Session,
    application_id: str,
    student_reg_no: str
):
    app = db.query(ODApplication)\
            .filter_by(
                application_id=application_id,
                registration_number=student_reg_no
            )\
            .first()

    if not app or app.status != ApplicationStatusEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel (either not found or already processed)"
        )

    db.delete(app)
    db.commit()
    return {"detail": "Application cancelled successfully"}


# ----------------------------------------
# Level 1 (Counsellor) workflows
# ----------------------------------------

def list_pending_l1(
    db: Session,
    counsellor_id: str
) -> List[ODApplication]:
    return db.query(ODApplication)\
             .filter_by(
                 level1_approver_id=counsellor_id,
                 level1_decision=DecisionEnum.PENDING
             )\
             .all()


def decide_l1(
    db: Session,
    application_id: str,
    counsellor_id: str,
    approve: bool
) -> ODApplication:
    od = db.query(ODApplication)\
           .filter_by(
               application_id=application_id,
               level1_approver_id=counsellor_id
           )\
           .first()
    if not od:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending application assigned to you"
        )
    if od.level1_decision != DecisionEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already decided at Level 1"
        )

    od.level1_decision = DecisionEnum.APPROVED if approve else DecisionEnum.REJECTED
    od.level1_decision_at = datetime.utcnow()
    od.status = (
        ApplicationStatusEnum.L1_APPROVED
        if approve else
        ApplicationStatusEnum.L1_REJECTED
    )
    db.commit()
    db.refresh(od)
    return od


# ----------------------------------------
# Level 2 (Academic Head) workflows
# ----------------------------------------

def list_pending_l2(
    db: Session
) -> List[ODApplication]:
    return db.query(ODApplication)\
             .filter_by(
                 status=ApplicationStatusEnum.L1_APPROVED,
                 level2_decision=DecisionEnum.PENDING
             )\
             .all()


def decide_l2(
    db: Session,
    application_id: str,
    academic_head_id: str,
    approve: bool
) -> ODApplication:
    # 1) Load the OD application and validate state
    od = (
        db.query(ODApplication)
          .filter_by(
              application_id=application_id,
              status=ApplicationStatusEnum.L1_APPROVED
          )
          .first()
    )
    if not od:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No L1-approved application found"
        )
    if od.level2_decision != DecisionEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already decided at Level 2"
        )

    # 2) Fetch event to check/decrement seats
    event = db.query(Event).filter_by(event_id=od.event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated event not found"
        )
    if approve and event.remaining_seats <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No seats available for this event"
        )

    # 3) Apply the Level-2 decision
    od.level2_approver_id = academic_head_id
    od.level2_decision     = DecisionEnum.APPROVED if approve else DecisionEnum.REJECTED
    od.level2_decision_at  = datetime.utcnow()
    od.status              = (
        ApplicationStatusEnum.L2_APPROVED
        if approve else
        ApplicationStatusEnum.L2_REJECTED
    )

    # 4) Decrement the seat counter on final approval
    if approve:
        event.remaining_seats -= 1
        db.add(event)

    # 5) Persist all changes
    db.commit()
    db.refresh(od)
    return od