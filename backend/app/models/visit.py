from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Visit(Base):
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(String(20), unique=True, index=True)  # VIS-000001
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    
    # Visit Info
    visit_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Vitals
    bp = Column(String(10))  # e.g., "120/80"
    blood_sugar = Column(String(10))  # e.g., "110"
    pulse = Column(String(10))  # e.g., "72"
    
    # Clinical Notes
    chief_complaint = Column(Text)
    examination_findings = Column(Text)
    advice = Column(Text)
    
    # Follow-up
    follow_up_date = Column(Date)
    follow_up_reason = Column(String(200))
    
    # Status
    status = Column(String(20), default="completed")  # in_progress, completed
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="visits")
    doctor = relationship("User")
    prescriptions = relationship("Prescription", back_populates="visit")
