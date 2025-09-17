# app/schemas/event_request.py

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum


class RequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class EventRequestCreate(BaseModel):
    name: str
    description: Optional[str] = None
    date: date


class EventRequestResponse(BaseModel):
    request_id: str
    registration_number: str
    name: str
    description: Optional[str] = None
    date: date
    status: RequestStatus
    reviewed_by: Optional[str] = None
    created_at: datetime
    decision_at: Optional[datetime] = None

    class Config:
        orm_mode = True
