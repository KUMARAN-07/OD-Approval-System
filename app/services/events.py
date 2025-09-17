from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from app.repositories import events as repo
from app.schemas.event import EventCreate, EventUpdate  # ✅ Import EventUpdate

def list_faculty_events(db: Session, faculty_id: str):
    return repo.get_faculty_events(db, faculty_id)

def create_new_event(db: Session, faculty_id: str, event_data: EventCreate):
    if event_data.date < date.today():
        raise HTTPException(status_code=400, detail="Event date cannot be in the past")
    return repo.create_event(db, faculty_id, event_data)

def delete_faculty_event(db: Session, faculty_id: str, event_id: str):
    event = repo.get_event_by_id(db, event_id)
    if not event or event.created_by != faculty_id:
        raise HTTPException(status_code=404, detail="Event not found or not owned by you")
    repo.delete_event(db, event)

def edit_faculty_event(db: Session, faculty_id: str, event_id: str, data: EventUpdate):
    event = repo.get_event_by_id(db, event_id)
    if not event or event.created_by != faculty_id:
        raise HTTPException(status_code=404, detail="Event not found or not owned by you")
    if data.date and data.date < date.today():
        raise HTTPException(status_code=400, detail="Event date cannot be in the past")
    return repo.update_event(db, event, data)

def check_and_update_event_status(db: Session, event_id: str):
    repo.update_event_status_if_filled(db, event_id)
