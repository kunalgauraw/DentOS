from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(String(20), unique=True, index=True)  # RX-000001
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    
    # Medicines (stored as JSON array)
    # [{"name": "Amoxicillin", "dosage": "500mg", "frequency": "1-0-1", "duration": "5 days", "instructions": "After food"}]
    medicines = Column(JSON, default=[])
    
    # Additional
    notes = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    visit = relationship("Visit", back_populates="prescriptions")
    patient = relationship("Patient")
    doctor = relationship("User")
