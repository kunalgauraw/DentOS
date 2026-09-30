from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# <repo>/data/dentos.db regardless of the current working directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "DentOS"
    VERSION: str = "0.1.0"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{(DATA_DIR / 'dentos.db').as_posix()}"
    
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


settings = Settings()
