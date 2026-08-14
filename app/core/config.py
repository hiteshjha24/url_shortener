from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI URL Shortener"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./url_shortener.db"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    RATE_LIMIT_DEFAULT: str = "5/minute"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()