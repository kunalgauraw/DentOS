from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core import get_db
from app.models import Invoice, Patient, Visit, User
from app.schemas import InvoiceCreate, InvoiceResponse, InvoiceListResponse
from app.routes.auth import get_current_user

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
    dependencies=[Depends(get_current_user)],
)

def generate_invoice_id(db: Session) -> str:
    last_inv = db.query(Invoice).order_by(Invoice.id.desc()).first()
    if last_inv:
        last_num = int(last_inv.invoice_id.split("-")[1])
        return f"INV-{str(last_num + 1).zfill(6)}"
    return "INV-000001"

@router.get("/", response_model=List[InvoiceListResponse])
def get_invoices(
    patient_id: Optional[int] = Query(None),
    visit_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Invoice, Patient.full_name).join(Patient, Patient.id == Invoice.patient_id)
    if patient_id:
        query = query.filter(Invoice.patient_id == patient_id)
    if visit_id:
        query = query.filter(Invoice.visit_id == visit_id)
    if status:
        query = query.filter(Invoice.status == status)
    rows = query.order_by(Invoice.invoice_date.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": inv.id,
            "invoice_id": inv.invoice_id,
            "patient_id": inv.patient_id,
            "visit_id": inv.visit_id,
            "patient_name": patient_name,
            "total": float(inv.total),
            "paid": float(inv.paid),
            "balance": float(inv.balance),
            "status": inv.status,
            "invoice_date": inv.invoice_date,
        }
        for inv, patient_name in rows
    ]

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.post("/", response_model=InvoiceResponse)
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == invoice_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    visit = None
    if invoice_data.visit_id:
        visit = db.query(Visit).filter(Visit.id == invoice_data.visit_id).first()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        if visit.patient_id != invoice_data.patient_id:
            raise HTTPException(status_code=400, detail="Visit does not belong to this patient")
    
    invoice_id = generate_invoice_id(db)
    
    # Calculate amounts (INV-005)
    items_data = [item.model_dump() for item in invoice_data.items]
    subtotal = round(sum(item["amount"] for item in items_data), 2)
    discount = invoice_data.discount
    after_discount = subtotal - discount
    gst_amount = round(after_discount * (invoice_data.gst_percent / 100), 2)
    total = round(after_discount + gst_amount, 2)
    
    # Attribute to the treating dentist for collection-by-doctor reporting
    doctor_id = invoice_data.doctor_id or (visit.doctor_id if visit else None) or current_user.id
    
    invoice = Invoice(
        invoice_id=invoice_id,
        patient_id=invoice_data.patient_id,
        doctor_id=doctor_id,
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
