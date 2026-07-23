from functools import lru_cache 
#  Without lru_cache: Every import
# ↓
# Read .env again
# ↓
# Create new Settings object

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Kingdom Simulator"
    API_PREFIX: str = "/api/v1"
    APP_VERSION:str = "1.0.0"
    APP_ENV: str = "development"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
    )

    DATABASE_NAME: str = "ai_kingdom_simulator"

    SECRET_KEY: str
    LOG_LEVEL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    lru_cache ensures the .env file is read only once
    during the application's lifetime.
    """
    return Settings()


settings = get_settings()