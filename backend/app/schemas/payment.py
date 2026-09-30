from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    invoice_id: int
    patient_id: int
    amount: float
    payment_mode: str  # cash, upi, card, bank_transfer
    reference_no: Optional[str] = None
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    received_by: Optional[int] = None

class PaymentResponse(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    receipt_id: str
    payment_date: datetime
    received_by: Optional[int] = None
