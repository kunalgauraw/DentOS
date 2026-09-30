from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from app.core import get_db
from app.models import Invoice, Patient
from app.schemas import InvoiceCreate, InvoiceResponse, InvoiceListResponse

router = APIRouter(prefix="/invoices", tags=["Invoices"])

def generate_invoice_id(db: Session) -> str:
    last_inv = db.query(Invoice).order_by(Invoice.id.desc()).first()
    if last_inv:
        last_num = int(last_inv.invoice_id.split("-")[1])
        return f"INV-{str(last_num + 1).zfill(6)}"
    return "INV-000001"

@router.get("/", response_model=List[InvoiceListResponse])
def get_invoices(
    patient_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Invoice)
    if patient_id:
        query = query.filter(Invoice.patient_id == patient_id)
    if status:
        query = query.filter(Invoice.status == status)
    invoices = query.order_by(Invoice.invoice_date.desc()).offset(skip).limit(limit).all()
    
    # Add patient name to response
    result = []
    for inv in invoices:
        patient = db.query(Patient).filter(Patient.id == inv.patient_id).first()
        inv_dict = {
            "id": inv.id,
            "invoice_id": inv.invoice_id,
            "patient_id": inv.patient_id,
            "patient_name": patient.full_name if patient else None,
            "total": float(inv.total),
            "paid": float(inv.paid),
            "balance": float(inv.balance),
            "status": inv.status,
            "invoice_date": inv.invoice_date
        }
        result.append(inv_dict)
    return result

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == invoice_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    invoice_id = generate_invoice_id(db)
    
    # Calculate amounts
    items_data = [item.model_dump() for item in invoice_data.items]
    subtotal = sum(item["amount"] for item in items_data)
    discount = invoice_data.discount
    after_discount = subtotal - discount
    gst_amount = after_discount * (invoice_data.gst_percent / 100)
    total = after_discount + gst_amount
    
    invoice = Invoice(
        invoice_id=invoice_id,
        patient_id=invoice_data.patient_id,
        doctor_id=invoice_data.doctor_id,
        visit_id=invoice_data.visit_id,
        items=items_data,
        subtotal=subtotal,
        discount=discount,
        gst_percent=invoice_data.gst_percent,
        gst_amount=gst_amount,
        total=total,
        paid=0,
        balance=total,
        status="pending",
        notes=invoice_data.notes
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice
