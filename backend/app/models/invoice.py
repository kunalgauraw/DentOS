from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String(20), unique=True, index=True)  # INV-000001
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    visit_id = Column(Integer, ForeignKey("visits.id"))
    
    # Line Items (stored as JSON array)
    # [{"description": "Consultation", "quantity": 1, "rate": 500, "amount": 500}]
    items = Column(JSON, default=[])
    
    # Amounts
    subtotal = Column(Numeric(10, 2), default=0)
    discount = Column(Numeric(10, 2), default=0)
    gst_percent = Column(Numeric(5, 2), default=0)
    gst_amount = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    paid = Column(Numeric(10, 2), default=0)
    balance = Column(Numeric(10, 2), default=0)
    
    # Status
    status = Column(String(20), default="pending")  # pending, partial, paid
    
    # Notes
    notes = Column(Text)
    
    # Metadata
    invoice_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="invoices")
    doctor = relationship("User")
    payments = relationship("Payment", back_populates="invoice")
