from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.core import get_db
from app.models import Patient
from app.schemas import PatientCreate, PatientUpdate, PatientResponse, PatientListResponse
from app.routes.auth import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])

def generate_patient_id(db: Session) -> str:
    last_patient = db.query(Patient).order_by(Patient.id.desc()).first()
    if last_patient:
        last_num = int(last_patient.patient_id.split("-")[1])
        return f"PAT-{str(last_num + 1).zfill(6)}"
    return "PAT-000001"

@router.get("/", response_model=List[PatientListResponse])
def get_patients(
    search: Optional[str] = Query(None, description="Search by name or mobile"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Patient)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Patient.full_name.ilike(search_term),
                Patient.mobile.ilike(search_term),
                Patient.patient_id.ilike(search_term)
            )
        )
    patients = query.order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()
    return patients

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=PatientResponse)
def create_patient(patient_data: PatientCreate, db: Session = Depends(get_db)):
    # Check for duplicate mobile number
    existing = db.query(Patient).filter(Patient.mobile == patient_data.mobile).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient with this mobile number already exists")
    
    # Generate patient ID
    patient_id = generate_patient_id(db)
    
    patient = Patient(
        patient_id=patient_id,
        **patient_data.model_dump()
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient_data: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    from app.models import Visit, Prescription, Invoice, Payment
    
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Delete related records first (cascade)
    db.query(Payment).filter(Payment.patient_id == patient_id).delete()
    db.query(Prescription).filter(Prescription.patient_id == patient_id).delete()
    db.query(Invoice).filter(Invoice.patient_id == patient_id).delete()
    db.query(Visit).filter(Visit.patient_id == patient_id).delete()
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
