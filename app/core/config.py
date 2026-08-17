# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI URL Shortener"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./url_shortener.db"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    RATE_LIMIT_DEFAULT: str = "5/minute"

    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION_32_BYTES"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()