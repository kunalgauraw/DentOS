from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.core import get_db
from app.models import Visit, Patient, User, UserRole
from app.schemas import VisitCreate, VisitUpdate, VisitResponse
from app.routes.auth import get_current_user

router = APIRouter(
    prefix="/visits",
    tags=["Visits"],
    dependencies=[Depends(get_current_user)],
)

DENTIST_ROLES = {UserRole.ADMIN, UserRole.DENTIST, UserRole.VISITING_DENTIST}

def generate_visit_id(db: Session) -> str:
    last_visit = db.query(Visit).order_by(Visit.id.desc()).first()
    if last_visit:
        last_num = int(last_visit.visit_id.split("-")[1])
        return f"VIS-{str(last_num + 1).zfill(6)}"
    return "VIS-000001"

def _is_same_day(dt: datetime) -> bool:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone().date() == datetime.now().date()

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
def create_visit(
    visit_data: VisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == visit_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    visit_id = generate_visit_id(db)
    data = visit_data.model_dump()
    # VIS-004: capture the dentist from the session unless explicitly provided
    if not data.get("doctor_id"):
        data["doctor_id"] = current_user.id if current_user.role in DENTIST_ROLES else None
    
    visit = Visit(visit_id=visit_id, **data)
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit

@router.put("/{visit_id}", response_model=VisitResponse)
def update_visit(
    visit_id: int,
    visit_data: VisitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    # VIS-006/007: only same-day edits, unless admin
    if current_user.role != UserRole.ADMIN and not _is_same_day(visit.visit_date):
        raise HTTPException(status_code=403, detail="Visits can only be edited on the day they were created")
    
    update_data = visit_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(visit, field, value)
    
    db.commit()
    db.refresh(visit)
    return visit
