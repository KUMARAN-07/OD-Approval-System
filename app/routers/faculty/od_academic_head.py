from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.deps.auth import get_current_faculty
from app.models.faculty import Faculty
from app.schemas.od_application import ODApplicationResponse
from app.services.od_applications import list_pending_l2, decide_l2

router = APIRouter(
    prefix="/faculty/od/academic-head",
    tags=["Academic Head OD"]
)

@router.get(
    "/pending",
    response_model=List[ODApplicationResponse],
    summary="List OD applications approved by counsellors (awaiting Academic Head approval)"
)
def list_pending(
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    # 1) Ensure this user is an Academic Head
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty or faculty.designation != "Academic Head":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not an Academic Head"
        )

    # 2) Return all L1-approved, L2-pending applications
    return list_pending_l2(db)

@router.post(
    "/{app_id}/approve",
    response_model=ODApplicationResponse,
    summary="Academic Head approves an OD application"
)
def approve(
    app_id: str,
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    # verify Academic Head role
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty or faculty.designation != "Academic Head":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not an Academic Head"
        )

    # perform Level-2 approval
    return decide_l2(db, app_id, faculty_id, approve=True)


@router.post(
    "/{app_id}/reject",
    response_model=ODApplicationResponse,
    summary="Academic Head rejects an OD application"
)
def reject(
    app_id: str,
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    # verify Academic Head role
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty or faculty.designation != "Academic Head":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not an Academic Head"
        )

    # perform Level-2 rejection
    return decide_l2(db, app_id, faculty_id, approve=False)
