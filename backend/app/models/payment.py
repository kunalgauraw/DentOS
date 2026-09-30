from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(String(20), unique=True, index=True)  # RCP-000001
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # Payment Details
    amount = Column(Numeric(10, 2), nullable=False)
    payment_mode = Column(String(20), nullable=False)  # cash, upi, card, bank_transfer
    reference_no = Column(String(100))  # UPI ref, card last 4 digits, etc.
    
    # Notes
    notes = Column(Text)
    
    # Metadata
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    received_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    patient = relationship("Patient")
    receiver = relationship("User")
