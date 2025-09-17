# app/routers/student/event_requests.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps.auth import get_current_student
from app.schemas.event_request import (
    EventRequestCreate,
    EventRequestResponse,
)
from app.services.event_requests import create_event_request

router = APIRouter(
    prefix="/student/event-requests",
    tags=["Student Event Requests"]
)


@router.post(
    "/",
    response_model=EventRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new event request"
)
def submit_event_request(
    request: EventRequestCreate,
    registration_number: str = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    A student submits an event request.
    """
    new_req = create_event_request(db, registration_number, request)
    return new_req

