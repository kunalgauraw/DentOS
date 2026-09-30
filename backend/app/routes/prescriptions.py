from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core import get_db
from app.models import Prescription, Visit, Patient
from app.schemas import PrescriptionCreate, PrescriptionResponse

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

def generate_prescription_id(db: Session) -> str:
    last_rx = db.query(Prescription).order_by(Prescription.id.desc()).first()
    if last_rx:
        last_num = int(last_rx.prescription_id.split("-")[1])
        return f"RX-{str(last_num + 1).zfill(6)}"
    return "RX-000001"

@router.get("/", response_model=List[PrescriptionResponse])
def get_prescriptions(
    patient_id: Optional[int] = Query(None),
    visit_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Prescription)
    if patient_id:
        query = query.filter(Prescription.patient_id == patient_id)
    if visit_id:
        query = query.filter(Prescription.visit_id == visit_id)
    prescriptions = query.order_by(Prescription.created_at.desc()).offset(skip).limit(limit).all()
    return prescriptions

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@router.post("/", response_model=PrescriptionResponse)
def create_prescription(rx_data: PrescriptionCreate, db: Session = Depends(get_db)):
    # Verify visit exists
    visit = db.query(Visit).filter(Visit.id == rx_data.visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    prescription_id = generate_prescription_id(db)
    
    # Convert medicines to dict for JSON storage
    medicines_data = [med.model_dump() for med in rx_data.medicines]
    
    prescription = Prescription(
        prescription_id=prescription_id,
        visit_id=rx_data.visit_id,
        patient_id=rx_data.patient_id,
        doctor_id=rx_data.doctor_id,
        medicines=medicines_data,
        notes=rx_data.notes
    )
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription
