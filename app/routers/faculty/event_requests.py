# app/routers/faculty/event_requests.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.services.event_requests import review_event_request
from app.database import get_db
from app.deps.auth import get_current_faculty
from app.models.faculty import Faculty
from app.schemas.event_request import EventRequestResponse
from app.services.event_requests import list_pending_requests

router = APIRouter(
    prefix="/faculty/event-requests",
    tags=["Faculty Event Requests"] 
)


@router.get(
    "/pending",
    response_model=List[EventRequestResponse],
    summary="List all student event requests awaiting review"
)
def list_pending_event_requests(
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    # Optional: restrict to only certain faculty roles
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return list_pending_requests(db)

@router.post(
    "/{request_id}/approve",
    response_model=EventRequestResponse,
    summary="Approve a student event request",
    status_code=status.HTTP_200_OK
)
def approve_event_request(
    request_id: str,
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    return review_event_request(db, faculty_id, request_id, approve=True)


@router.post(
    "/{request_id}/reject",
    response_model=EventRequestResponse,
    summary="Reject a student event request",
    status_code=status.HTTP_200_OK
)
def reject_event_request(
    request_id: str,
    faculty_id: str = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    return review_event_request(db, faculty_id, request_id, approve=False)