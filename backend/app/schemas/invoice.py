from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class InvoiceItem(BaseModel):
    description: str
    quantity: int = 1
    rate: float
    amount: float

class InvoiceBase(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    visit_id: Optional[int] = None
    items: List[InvoiceItem] = []
    discount: float = 0
    gst_percent: float = 0
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(BaseModel):
    id: int
    invoice_id: str
    patient_id: int
    doctor_id: Optional[int] = None
    items: List[dict] = []
    subtotal: float
    discount: float
    gst_percent: float
    gst_amount: float
    total: float
    paid: float
    balance: float
    status: str
    notes: Optional[str] = None
    invoice_date: datetime
    
    class Config:
        from_attributes = True

class InvoiceListResponse(BaseModel):
    id: int
    invoice_id: str
    patient_id: int
    patient_name: Optional[str] = None
    total: float
    paid: float
    balance: float
    status: str
    invoice_date: datetime
    
    class Config:
        from_attributes = True
