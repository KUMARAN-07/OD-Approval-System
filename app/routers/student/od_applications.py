from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.od_application import (
    ODApplicationCreate,
    ODApplicationResponse,
)
from app.services import od_applications as service
from app.deps.auth import get_current_student

router = APIRouter(prefix="/student/od", tags=["Student OD"])


@router.post("/apply", response_model=ODApplicationResponse)
def apply_for_od(
    application: ODApplicationCreate,
    registration_number: str = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    od = service.apply_for_od(db, registration_number, application)
    return ODApplicationResponse.from_orm(od)



@router.get("/applications", response_model=List[ODApplicationResponse])
def list_applications(
    registration_number: str = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    ods = service.list_student_applications(db, registration_number)
    return [ODApplicationResponse.from_orm(o) for o in ods]


@router.get("/applications/{application_id}", response_model=ODApplicationResponse)
def get_application_status(
    application_id: str,
    registration_number: str = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    od = service.get_application_status(db, application_id, registration_number)
    return ODApplicationResponse.from_orm(od)


@router.delete("/applications/{application_id}")
def cancel_application(
    application_id: str,
    registration_number: str = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    # This returns a dict, so it’s fine as-is
    return service.cancel_application(db, application_id, registration_number)
