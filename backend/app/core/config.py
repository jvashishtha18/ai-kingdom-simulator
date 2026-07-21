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

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    SECRET_KEY: str = Field(...)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MONGODB_URL: str
    DATABASE_NAME: str

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
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