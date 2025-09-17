# app/repositories/od_applications.py

import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.od_application import ODApplication, ApplicationStatusEnum
from app.models.faculty_student_mapping import FacultyStudentMapping
from app.schemas.od_application import ODApplicationCreate


def create_od_application(
    db: Session,
    student_reg_no: str,
    application: ODApplicationCreate
) -> ODApplication:
    # 1) Find the counsellor assigned to this student
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

    # 2) Create the OD application with level-1 approver set
    new_app = ODApplication(
        application_id=str(uuid.uuid4()),
        registration_number=student_reg_no,
        event_id=application.event_id,
        status=ApplicationStatusEnum.PENDING,
        level1_approver_id=mapping.counsellor_id
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app


def get_student_applications(db: Session, student_reg_no: str):
    return (
        db.query(ODApplication)
          .filter(ODApplication.registration_number == student_reg_no)
          .all()
    )


def get_application_by_id(
    db: Session,
    application_id: str,
    student_reg_no: str
):
    return (
        db.query(ODApplication)
          .filter(
              ODApplication.application_id == application_id,
              ODApplication.registration_number == student_reg_no
          )
          .first()
    )


def delete_application(
    db: Session,
    application_id: str,
    student_reg_no: str
) -> bool:
    app_record = get_application_by_id(db, application_id, student_reg_no)
    if app_record and app_record.status == ApplicationStatusEnum.PENDING:
        db.delete(app_record)
        db.commit()
        return True
    return False
