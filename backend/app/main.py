from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings, Base, engine, SessionLocal, get_password_hash
from app.models import User, UserRole
from app.routes import (
    auth_router,
    patients_router,
    visits_router,
    prescriptions_router,
    invoices_router,
    payments_router,
    dashboard_router
)

# Create tables
Base.metadata.create_all(bind=engine)


def create_default_user():
    """Create default admin user if not exists"""
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == "admin").first()
        if not existing_user:
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                full_name="Dr. Aditya Gaurav",
                role=UserRole.ADMIN,
                mobile="98525 00001",
                registration_no="BDC/2020/12345",
                qualification="BDS, MDS"
            )
            db.add(admin_user)
            db.commit()
            print("Default admin user created: admin / admin123")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_default_user()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Dental Practice Management System",
    lifespan=lifespan,
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(visits_router)
app.include_router(prescriptions_router)
app.include_router(invoices_router)
app.include_router(payments_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
