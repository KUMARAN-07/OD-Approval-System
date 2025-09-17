# app/services/event_requests.py

from uuid import uuid4
from typing import Optional
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.event_request import EventRequest, RequestStatusEnum
from app.schemas.event_request import EventRequestCreate


def create_event_request(
    db: Session,
    registration_number: str,
    request: EventRequestCreate
) -> EventRequest:
    # 1) Instantiate EventRequest
    new_req = EventRequest(
        request_id=str(uuid4()),
        registration_number=registration_number,
        name=request.name,
        description=request.description,
        date=request.date,
        status=RequestStatusEnum.PENDING,
        created_at=datetime.utcnow()
    )

    # 2) Persist to DB
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req

def list_pending_requests(
    db: Session
) -> List[EventRequest]:
    """
    Return all EventRequest rows still in PENDING status.
    """
    return (
        db.query(EventRequest)
          .filter_by(status=RequestStatusEnum.PENDING)
          .all()
    )

def review_event_request(
    db: Session,
    faculty_id: str,
    request_id: str,
    approve: bool
) -> EventRequest:
    """
    Set reviewed_by, status and decision_at on a pending EventRequest.
    """
    # 1) Load the pending request
    ev_req: Optional[EventRequest] = (
        db.query(EventRequest)
          .filter_by(request_id=request_id,
                     status=RequestStatusEnum.PENDING)
          .first()
    )
    if not ev_req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pending event request not found"
        )

    # 2) Apply decision
    ev_req.reviewed_by = faculty_id
    ev_req.status      = (
        RequestStatusEnum.APPROVED
        if approve else
        RequestStatusEnum.REJECTED
    )
    ev_req.decision_at = datetime.utcnow()

    # 3) Persist
    db.add(ev_req)
    db.commit()
    db.refresh(ev_req)
    return ev_req