from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from app.core import get_db
from app.models import Payment, Invoice, Patient
from app.schemas import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["Payments"])

def generate_receipt_id(db: Session) -> str:
    last_payment = db.query(Payment).order_by(Payment.id.desc()).first()
    if last_payment:
        last_num = int(last_payment.receipt_id.split("-")[1])
        return f"RCP-{str(last_num + 1).zfill(6)}"
    return "RCP-000001"

@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    patient_id: Optional[int] = Query(None),
    invoice_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Payment)
    if patient_id:
        query = query.filter(Payment.patient_id == patient_id)
    if invoice_id:
        query = query.filter(Payment.invoice_id == invoice_id)
    if date_from:
        query = query.filter(Payment.payment_date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(Payment.payment_date <= datetime.combine(date_to, datetime.max.time()))
    
    payments = query.order_by(Payment.payment_date.desc()).offset(skip).limit(limit).all()
    return payments

@router.get("/today-collection")
def get_today_collection(db: Session = Depends(get_db)):
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    
    payments = db.query(Payment).filter(
        Payment.payment_date >= start,
        Payment.payment_date <= end
    ).all()
    
    total = sum(float(p.amount) for p in payments)
    by_mode = {}
    for p in payments:
        mode = p.payment_mode
        if mode not in by_mode:
            by_mode[mode] = 0
        by_mode[mode] += float(p.amount)
    
    return {
        "date": today.isoformat(),
        "total": total,
        "count": len(payments),
        "by_mode": by_mode,
        "payments": [PaymentResponse.model_validate(p) for p in payments]
    }

@router.post("/", response_model=PaymentResponse)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    # Verify invoice exists
    invoice = db.query(Invoice).filter(Invoice.id == payment_data.invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Check if payment amount is valid
    if payment_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be positive")
    if payment_data.amount > float(invoice.balance):
        raise HTTPException(status_code=400, detail="Payment amount exceeds balance")
    
    receipt_id = generate_receipt_id(db)
    
    payment = Payment(
        receipt_id=receipt_id,
        invoice_id=payment_data.invoice_id,
        patient_id=payment_data.patient_id,
        amount=payment_data.amount,
        payment_mode=payment_data.payment_mode,
        reference_no=payment_data.reference_no,
        notes=payment_data.notes,
        received_by=payment_data.received_by
    )
    db.add(payment)
    
    # Update invoice
    invoice.paid = float(invoice.paid) + payment_data.amount
    invoice.balance = float(invoice.total) - float(invoice.paid)
    if invoice.balance <= 0:
        invoice.status = "paid"
    else:
        invoice.status = "partial"
    
    db.commit()
    db.refresh(payment)
    return payment
