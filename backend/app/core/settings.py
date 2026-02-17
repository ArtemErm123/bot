from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from env vars."""

    app_name: str = Field(default="Concrete Lab API")
    app_version: str = Field(default="1.0.0")
    app_description: str = Field(
        default="API for concrete projects, variants, mixes and engineering calculations"
    )
    api_v1_prefix: str = Field(default="/api/v1")
    jwt_secret_key: str = Field(default="change-me")
    jwt_algorithm: str = Field(default="HS256")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
