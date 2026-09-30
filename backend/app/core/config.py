from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "DentOS"
    VERSION: str = "0.1.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./dentos.db"
    
    # JWT
    SECRET_KEY: str = "dentos-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours
    
    # Clinic Info (defaults, can be changed in settings)
    CLINIC_NAME: str = "Gauravam Denta Clinic"
    CLINIC_ADDRESS: str = "Jagdam College Road, Chapra, Bihar - 841301"
    CLINIC_PHONE: str = "98525 00001"
    DENTIST_NAME: str = "Dr. Aditya Gaurav"
    DENTIST_REG_NO: str = "BDC/2020/12345"
    
    class Config:
        env_file = ".env"

settings = Settings()
