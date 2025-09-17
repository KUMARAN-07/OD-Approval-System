from pydantic import BaseModel, constr
from datetime import date
from typing import Optional


class EventBase(BaseModel):
    name: constr(min_length=3, max_length=255)
    description: Optional[str]
    date: date
    location: Optional[str]
    seat_limit: int


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    date: Optional[date]
    location: Optional[str]
    seat_limit: Optional[int]


class EventResponse(EventBase):
    event_id: str
    status: str
    created_by: str

    class Config:
        orm_mode = True   # ✅ Pydantic v1 uses orm_mode instead of from_attributes
