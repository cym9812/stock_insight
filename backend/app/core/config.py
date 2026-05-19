from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enum import LogLevel

PROJECT_ROOT = Path(__file__).resolve().parents[3]

BASE_CONFIG = SettingsConfigDict(
    env_file=PROJECT_ROOT / ".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
)


def _parse_csv_list(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


StringList = Annotated[list[str], BeforeValidator(_parse_csv_list)]


class AppSettings(BaseSettings):
    model_config = BASE_CONFIG

    project_name: str = Field(default="Stock Insight", alias="PROJECT_NAME")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=18000, ge=0, le=65535, alias="APP_PORT")
    reload: bool = Field(default=False, alias="APP_RELOAD")


class StorageSettings(BaseSettings):
    model_config = BASE_CONFIG

    root_dir: Path = Field(default=PROJECT_ROOT / "local_data", alias="STORAGE_ROOT_DIR")


class CorsSettings(BaseSettings):
    model_config = BASE_CONFIG

    origins: StringList = Field(default_factory=lambda: ["http://localhost:5173"], alias="CORS_ORIGINS")
    allow_credentials: bool = Field(default=True, alias="CORS_ALLOW_CREDENTIALS")
    allow_methods: StringList = Field(default_factory=lambda: ["*"], alias="CORS_ALLOW_METHODS")
    allow_headers: StringList = Field(default_factory=lambda: ["*"], alias="CORS_ALLOW_HEADERS")


class LogSettings(BaseSettings):
    model_config = BASE_CONFIG

    dir: Path = Field(default=PROJECT_ROOT / "logs", alias="LOG_DIR")
    console_log_level: LogLevel = Field(default="INFO", alias="CONSOLE_LOG_LEVEL")
    file_log_level: LogLevel = Field(default="INFO", alias="FILE_LOG_LEVEL")
    retention: str = Field(default="14 days", alias="LOG_RETENTION")
    rotation: str = Field(default="00:00", alias="LOG_ROTATION")
    diagnose: bool = Field(default=False, alias="LOG_DIAGNOSE")


class Settings(BaseModel):
    app: AppSettings = Field(default_factory=AppSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    cors: CorsSettings = Field(default_factory=CorsSettings)
    log: LogSettings = Field(default_factory=LogSettings)


settings = Settings()
