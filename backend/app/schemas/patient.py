from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class PatientBase(BaseModel):
    full_name: str
    mobile: str
    gender: str
    age: Optional[int] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    alternate_phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    current_medications: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    mobile: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    alternate_phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    current_medications: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    patient_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PatientListResponse(BaseModel):
    id: int
    patient_id: str
    full_name: str
    mobile: str
    gender: str
    age: Optional[int] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    
    class Config:
        from_attributes = True
