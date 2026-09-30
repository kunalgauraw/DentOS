from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
from typing import Optional

from app.core import get_db
from app.models import Patient, Visit, Invoice, Payment

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    # Today's stats
    today_visits = db.query(Visit).filter(
        Visit.visit_date >= start_of_day,
        Visit.visit_date <= end_of_day
    ).count()
    
    today_payments = db.query(Payment).filter(
        Payment.payment_date >= start_of_day,
        Payment.payment_date <= end_of_day
    ).all()
    
    today_collection = sum(float(p.amount) for p in today_payments)
    
    # Overall stats
    total_patients = db.query(Patient).count()
    
    # Outstanding
    total_outstanding = db.query(func.sum(Invoice.balance)).filter(
        Invoice.balance > 0
    ).scalar() or 0
    
    # Follow-ups due
    follow_ups_due = db.query(Visit).filter(
        Visit.follow_up_date <= today + timedelta(days=7),
        Visit.follow_up_date >= today
    ).count()
    
    return {
        "today": {
            "visits": today_visits,
            "collection": float(today_collection),
            "payments_count": len(today_payments)
        },
        "overall": {
            "total_patients": total_patients,
            "outstanding": float(total_outstanding),
            "follow_ups_due": follow_ups_due
        }
    }

@router.get("/recent-patients")
def get_recent_patients(limit: int = 10, db: Session = Depends(get_db)):
    patients = db.query(Patient).order_by(Patient.created_at.desc()).limit(limit).all()
    return [
        {
            "id": p.id,
            "patient_id": p.patient_id,
            "full_name": p.full_name,
            "mobile": p.mobile,
            "created_at": p.created_at
        }
        for p in patients
    ]

@router.get("/pending-payments")
def get_pending_payments(limit: int = 10, db: Session = Depends(get_db)):
    invoices = db.query(Invoice).filter(
        Invoice.balance > 0
    ).order_by(Invoice.invoice_date.desc()).limit(limit).all()
    
    result = []
    for inv in invoices:
        patient = db.query(Patient).filter(Patient.id == inv.patient_id).first()
        result.append({
            "id": inv.id,
            "invoice_id": inv.invoice_id,
            "patient_id": inv.patient_id,
            "patient_name": patient.full_name if patient else None,
            "total": float(inv.total),
            "paid": float(inv.paid),
            "balance": float(inv.balance),
            "invoice_date": inv.invoice_date
        })
    return result
