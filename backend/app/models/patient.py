from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(20), unique=True, index=True)  # PAT-000001
    
    # Basic Info
    full_name = Column(String(100), nullable=False, index=True)
    mobile = Column(String(15), nullable=False, index=True)
    gender = Column(String(10), nullable=False)
    age = Column(Integer)
    date_of_birth = Column(Date)
    blood_group = Column(String(5))
    
    # Contact
    alternate_phone = Column(String(15))
    email = Column(String(100))
    address = Column(Text)
    
    # Emergency Contact
    emergency_contact_name = Column(String(100))
    emergency_contact_relation = Column(String(50))
    emergency_contact_phone = Column(String(15))
    
    # Medical Info
    allergies = Column(Text)
    medical_conditions = Column(Text)
    current_medications = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    visits = relationship("Visit", back_populates="patient")
    invoices = relationship("Invoice", back_populates="patient")
