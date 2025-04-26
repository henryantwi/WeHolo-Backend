from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./weholo.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # API Keys
    AKOOL_API_KEY: Optional[str] = None
    SOUL_MACHINES_API_KEY: Optional[str] = None
    
    # Project directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()