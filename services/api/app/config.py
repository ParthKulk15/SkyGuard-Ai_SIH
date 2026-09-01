from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SkyGuard API"
    environment: str = Field(default="local", alias="SKYGUARD_ENV")
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"],
        validation_alias="SKYGUARD_CORS_ORIGINS",
    )
    repo_root: Path = Path(__file__).resolve().parents[3]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)

    @property
    def ml_root(self) -> Path:
        return self.repo_root / "packages" / "ml"

    @property
    def ml_models_dir(self) -> Path:
        return self.ml_root / "models"


@lru_cache
def get_settings() -> Settings:
    return Settings()
