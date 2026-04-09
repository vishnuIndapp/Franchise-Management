from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # 🔹 App
    PROJECT_NAME: str = "Franchise API"
    ENV: str = "dev"

    # 🔹 Database
    DATABASE_URL: str

    # 🔹 JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 🔹 Redis
    REDIS_URL: str = "redis://localhost:6379"

    # 🔹 SMTP
    EMAIL_FROM: str = ""
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    

    # 🔹 Pagination
    DEFAULT_PAGE: int = 1
    DEFAULT_LIMIT: int = 10
    MAX_LIMIT: int = 100


    CACHE_EXPIRY:int = 300  # 5 minutes
    OTP_EXPIRATION_SECONDS: int = 300  # 5 minutes

    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

    CORS_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()   