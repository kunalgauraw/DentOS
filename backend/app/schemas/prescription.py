from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class Medicine(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None  # e.g., "1-0-1"
    duration: Optional[str] = None   # e.g., "5 days"
    instructions: Optional[str] = None  # e.g., "After food"

class PrescriptionBase(BaseModel):
    visit_id: int
    patient_id: int
    doctor_id: Optional[int] = None
    medicines: List[Medicine] = []
    notes: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionResponse(PrescriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prescription_id: str
    created_at: datetime
