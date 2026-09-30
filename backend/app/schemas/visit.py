from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class VisitBase(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    bp: Optional[str] = None
    blood_sugar: Optional[str] = None
    pulse: Optional[str] = None
    chief_complaint: Optional[str] = None
    examination_findings: Optional[str] = None
    advice: Optional[str] = None
    follow_up_date: Optional[date] = None
    follow_up_reason: Optional[str] = None

class VisitCreate(VisitBase):
    pass

class VisitUpdate(BaseModel):
    bp: Optional[str] = None
    blood_sugar: Optional[str] = None
    pulse: Optional[str] = None
    chief_complaint: Optional[str] = None
    examination_findings: Optional[str] = None
    advice: Optional[str] = None
    follow_up_date: Optional[date] = None
    follow_up_reason: Optional[str] = None
    status: Optional[str] = None

class VisitResponse(VisitBase):
    id: int
    visit_id: str
    visit_date: datetime
    status: str
    
    class Config:
        from_attributes = True
