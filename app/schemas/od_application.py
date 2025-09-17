from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ✅ Base class (shared fields)
class ODApplicationBase(BaseModel):
    event_id: str


# ✅ When student applies
class ODApplicationCreate(ODApplicationBase):
    pass


# ✅ Response schema (when returning data to student)
class ODApplicationResponse(BaseModel):
    application_id: str
    registration_number: str
    event_id: str
    status: str
    level1_approver_id: Optional[str]
    level1_decision: str
    level1_decision_at: Optional[datetime]
    level2_approver_id: Optional[str]
    level2_decision: str
    level2_decision_at: Optional[datetime]
    applied_at: datetime

    class Config:
        orm_mode = True
