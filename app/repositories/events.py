from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate  # ✅ Import EventUpdate
import uuid

def get_faculty_events(db: Session, faculty_id: str):
    return db.query(Event).filter(Event.created_by == faculty_id).all()

def create_event(db: Session, faculty_id: str, event_data: EventCreate):
    new_event = Event(
        event_id=str(uuid.uuid4()),
        name=event_data.name,
        description=event_data.description,
        date=event_data.date,
        location=event_data.location,
        seat_limit=event_data.seat_limit,
        created_by=faculty_id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def get_event_by_id(db: Session, event_id: str):
    return db.query(Event).filter(Event.event_id == event_id).first()

def delete_event(db: Session, event: Event):
    db.delete(event)
    db.commit()

def update_event(db: Session, event: Event, data: EventUpdate):  # ✅ Now uses imported EventUpdate
    for field, value in data.dict(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event

def update_event_status_if_filled(db: Session, event_id: str):
    """Check applications count and update event status if seat limit reached"""
    from app.models.od_application import ODApplication  # avoid circular import
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        return
    count = db.query(ODApplication).filter(ODApplication.event_id == event_id).count()
    if count >= event.seat_limit and event.status != "FILLED":
        event.status = "FILLED"
        db.commit()
