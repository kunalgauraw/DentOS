from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional
from datetime import date, datetime
import re

MOBILE_RE = re.compile(r"^\d{10}$")
GENDERS = {"male", "female", "other"}


def _clean_mobile(v: Optional[str]) -> Optional[str]:
    if v is None:
        return v
    digits = re.sub(r"\D", "", v)
    if not MOBILE_RE.match(digits):
        raise ValueError("Mobile number must be exactly 10 digits")
    return digits


class PatientBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    mobile: str
    gender: str
    age: Optional[int] = Field(None, ge=0, le=120)
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

    @field_validator("full_name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Full name must be at least 2 characters")
        return v

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        return _clean_mobile(v)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        v = v.lower()
        if v not in GENDERS:
            raise ValueError("Gender must be male, female or other")
        return v


class PatientCreate(PatientBase):
    @model_validator(mode="after")
    def age_or_dob(self):
        # PAT-006: either age or DOB must be provided
        if self.age is None and self.date_of_birth is None:
            raise ValueError("Either age or date of birth is required")
        # PAT-005: derive age from DOB if not supplied
        if self.age is None and self.date_of_birth is not None:
            today = date.today()
            dob = self.date_of_birth
            self.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return self


class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    mobile: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
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

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: Optional[str]) -> Optional[str]:
        return _clean_mobile(v)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.lower()
        if v not in GENDERS:
            raise ValueError("Gender must be male, female or other")
        return v


class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: str
    created_at: datetime


class PatientListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: str
    full_name: str
    mobile: str
    gender: str
    age: Optional[int] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
