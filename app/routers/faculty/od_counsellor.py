# app/routers/od_counsellor.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.deps.auth import get_current_faculty
from app.models.faculty import Faculty
from app.schemas.od_application import ODApplicationResponse
from app.services.od_applications import (
    list_pending_l1,
    decide_l1,
)

router = APIRouter(
    prefix="/faculty/od/counsellor",
    tags=["Counsellor OD"]
)

@router.get(
    "/pending",
    response_model=List[ODApplicationResponse],
    summary="List pending OD applications for this counsellor"
)
def list_pending(
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    # 1) Confirm this user is a counsellor
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty or faculty.designation != "Counsellor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not a counsellor"
        )

    # 2) Fetch pending applications assigned to them
    return list_pending_l1(db, faculty_id)


@router.post(
    "/{app_id}/approve",
    response_model=ODApplicationResponse,
    summary="Counsellor approves an OD application"
)
def approve(
    app_id: str,
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    # Confirm counsellor role
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty or faculty.designation != "Counsellor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not a counsellor"
        )

    # Approve at Level-1
    return decide_l1(db, app_id, faculty_id, approve=True)


@router.post(
    "/{app_id}/reject",
    response_model=ODApplicationResponse,
    summary="Counsellor rejects an OD application"
)
def reject(
    app_id: str,
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    # Confirm counsellor role
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty or faculty.designation != "Counsellor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not a counsellor"
        )

    # Reject at Level-1
    return decide_l1(db, app_id, faculty_id, approve=False)
