from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.deps.auth import get_current_faculty
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services import events as service

router = APIRouter(
    prefix="/faculty/events",
    tags=["Faculty Events"]
)

@router.get(
    "/",
    response_model=List[EventResponse],
    summary="List all events created by this faculty"
)
def get_faculty_events(
    db: Session = Depends(get_db),
    faculty_id: str = Depends(get_current_faculty),
):
    events = service.list_faculty_events(db, faculty_id)
    return [EventResponse.from_orm(evt) for evt in events]

@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event"
)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    faculty_id: str = Depends(get_current_faculty),
):
    event = service.create_new_event(db, faculty_id, event_data)
    return EventResponse.from_orm(event)

@router.patch(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update an existing event"
)
def update_event(
    event_id: str,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
    faculty_id: str = Depends(get_current_faculty),
):
    event = service.edit_faculty_event(db, faculty_id, event_id, event_data)
    return EventResponse.from_orm(event)

@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an event"
)
def delete_event(
    event_id: str,
    db: Session = Depends(get_db),
    faculty_id: str = Depends(get_current_faculty),
):
    service.delete_faculty_event(db, faculty_id, event_id)
    return None
