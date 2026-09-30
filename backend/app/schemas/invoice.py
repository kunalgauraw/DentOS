from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime

class InvoiceItem(BaseModel):
    description: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(1, ge=1)
    rate: float = Field(..., ge=0)
    amount: float = Field(..., gt=0)  # INV-003

    @field_validator("description")
    @classmethod
    def strip_description(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Item description is required")
        return v

    @model_validator(mode="after")
    def amount_matches(self):
        # Server is the source of truth for line totals
        self.amount = round(self.quantity * self.rate, 2)
        if self.amount <= 0:
            raise ValueError("Line item amount must be greater than zero")
        return self

class InvoiceBase(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    visit_id: Optional[int] = None
    items: List[InvoiceItem] = Field(..., min_length=1)  # INV-002
    discount: float = Field(0, ge=0)
    gst_percent: float = Field(0, ge=0, le=100)
    notes: Optional[str] = None

    @model_validator(mode="after")
    def discount_within_subtotal(self):
        # INV-004
        subtotal = sum(i.amount for i in self.items)
        if self.discount > subtotal:
            raise ValueError("Discount cannot exceed subtotal")
        return self

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_id: str
    patient_id: int
    doctor_id: Optional[int] = None
    visit_id: Optional[int] = None
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

class InvoiceListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_id: str
    patient_id: int
    visit_id: Optional[int] = None
    patient_name: Optional[str] = None
    total: float
    paid: float
    balance: float
    status: str
    invoice_date: datetime
