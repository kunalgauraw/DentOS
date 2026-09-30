from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core import get_db
from app.models import Visit, Patient
from app.schemas import VisitCreate, VisitUpdate, VisitResponse

router = APIRouter(prefix="/visits", tags=["Visits"])

def generate_visit_id(db: Session) -> str:
    last_visit = db.query(Visit).order_by(Visit.id.desc()).first()
    if last_visit:
        last_num = int(last_visit.visit_id.split("-")[1])
        return f"VIS-{str(last_num + 1).zfill(6)}"
    return "VIS-000001"

@router.get("/", response_model=List[VisitResponse])
def get_visits(
    patient_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Visit)
    if patient_id:
        query = query.filter(Visit.patient_id == patient_id)
    visits = query.order_by(Visit.visit_date.desc()).offset(skip).limit(limit).all()
    return visits

@router.get("/{visit_id}", response_model=VisitResponse)
def get_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit

@router.post("/", response_model=VisitResponse)
def create_visit(visit_data: VisitCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == visit_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    visit_id = generate_visit_id(db)
    
    visit = Visit(
        visit_id=visit_id,
        **visit_data.model_dump()
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit

@router.put("/{visit_id}", response_model=VisitResponse)
def update_visit(visit_id: int, visit_data: VisitUpdate, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    update_data = visit_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(visit, field, value)
    
    db.commit()
    db.refresh(visit)
    return visit
