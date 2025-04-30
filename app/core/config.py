from pydantic_settings import BaseSettings
from typing import Optional, List, Union
import secrets
from pathlib import Path

from icecream import ic

ic.disable()

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = "postgresql://weholo:weholo@db:5432/weholo"
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], List[None]] = ["*"]
    
    # API Keys
    AKOOL_API_KEY: Optional[str] = None
    SOUL_MACHINES_API_KEY: Optional[str] = None
    
    # Project directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Environment
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

ic(settings.BACKEND_CORS_ORIGINS)
