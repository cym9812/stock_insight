from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _parse_cors_origins(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [origin.strip() for origin in value.split(",") if origin.strip()]
    return value


CorsOrigins = Annotated[list[str], BeforeValidator(_parse_cors_origins)]


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    project_name: str = Field(default="Stock Insight", alias="PROJECT_NAME")
    environment: Literal["local", "development", "test", "production"] = Field(default="local", alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=18000, ge=0, le=65535, alias="APP_PORT")
    reload: bool = Field(default=True, alias="APP_RELOAD")

    cors_origins: CorsOrigins = Field(default_factory=lambda: ["*"], alias="CORS_ORIGINS")

    data_root_path: Path = Field(default=PROJECT_ROOT / "local_data", alias="DATA_ROOT_PATH")

    log_dir: Path = Field(default=PROJECT_ROOT / "logs", alias="LOG_DIR")
    log_level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = Field(default="INFO", alias="LOG_LEVEL")
    log_to_file: bool = Field(default=True, alias="LOG_TO_FILE")
    log_retention: str = Field(default="14 days", alias="LOG_RETENTION")
    log_rotation: str = Field(default="00:00", alias="LOG_ROTATION")
    log_diagnose: bool = Field(default=False, alias="LOG_DIAGNOSE")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
