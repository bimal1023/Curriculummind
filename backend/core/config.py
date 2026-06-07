"""
core/config.py
Centralised settings loaded from environment / .env file.
All other modules import from here — never from os.environ directly.
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Azure AI Foundry
    foundry_project_endpoint: str = Field(..., description="Foundry project endpoint URL")
    foundry_model_deployment_name: str = Field(default="gpt-4o")
    azure_client_id: str = Field(default="")

    # Azure AI Search
    azure_search_endpoint: str = Field(default="")
    azure_search_api_key: str = Field(default="")
    azure_search_index_name: str = Field(default="learning-resources")

    # App
    app_env: Literal["development", "staging", "production"] = Field(default="development")
    app_port: int = Field(default=8000)
    log_level: str = Field(default="INFO")
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # Telemetry
    applicationinsights_connection_string: str = Field(default="")

    # Agent tuning
    agent_max_retries: int = Field(default=3)
    agent_timeout_seconds: int = Field(default=60)
    max_concurrent_agents: int = Field(default=5)

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def telemetry_enabled(self) -> bool:
        return bool(self.applicationinsights_connection_string)


@lru_cache
def get_settings() -> Settings:
    """Cached singleton — call get_settings() anywhere in the app."""
    return Settings()  # type: ignore[call-arg]
