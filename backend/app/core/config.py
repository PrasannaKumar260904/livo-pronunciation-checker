from functools import cached_property
from pathlib import Path
from tempfile import gettempdir

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LOCAL_CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"


class Settings(BaseSettings):
    app_name: str = "Livo Pronunciation Checker API"
    app_env: str = "development"
    backend_cors_origins: str = Field(default=LOCAL_CORS_ORIGINS)
    max_upload_size_mb: int = 25
    upload_dir: Path = Path(gettempdir()) / "livo-pronunciation-checker" / "uploads"
    transcription_model_size: str = "base"
    transcription_device: str = "cpu"
    transcription_compute_type: str = "int8"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @cached_property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    def validate_production_config(self) -> None:
        if not self.is_production:
            return

        local_origins = {"http://localhost:3000", "http://127.0.0.1:3000"}
        configured_origins = set(self.cors_origins)

        if not configured_origins:
            raise RuntimeError("BACKEND_CORS_ORIGINS must be set in production.")

        if configured_origins.intersection(local_origins):
            raise RuntimeError(
                "BACKEND_CORS_ORIGINS must not include localhost in production."
            )


settings = Settings()
