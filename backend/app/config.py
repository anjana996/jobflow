"""Application configuration loaded from environment variables."""

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """JobFlow settings; secrets are masked in representations and errors."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: SecretStr

    @field_validator("database_url")
    @classmethod
    def require_postgresql(cls, value: SecretStr) -> SecretStr:
        url = value.get_secret_value()
        if not url.startswith(("postgresql+psycopg://", "postgresql://")):
            raise ValueError("DATABASE_URL must use PostgreSQL")
        return value


def get_settings() -> Settings:
    """Load settings at the point of use so configuration failures stay explicit."""

    return Settings()  # type: ignore[call-arg]
