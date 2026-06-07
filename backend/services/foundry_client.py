"""
services/foundry_client.py
Initialises and caches the FoundryChatClient.
All agents import get_foundry_client() — never instantiate directly.
"""
from functools import lru_cache

from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

from core.config import get_settings
from core.exceptions import FoundryClientError
from core.logging import get_logger

logger = get_logger(__name__)


@lru_cache
def get_foundry_client() -> FoundryChatClient:
    """
    Returns a cached FoundryChatClient.
    Uses ManagedIdentityCredential in production, DefaultAzureCredential in dev.
    """
    settings = get_settings()
    try:
        if settings.is_production:
            credential = ManagedIdentityCredential(
                client_id=settings.azure_client_id or None
            )
        else:
            credential = DefaultAzureCredential()

        client = FoundryChatClient(
            credential=credential,
            project_endpoint=settings.foundry_project_endpoint,
            model=settings.foundry_model_deployment_name,
        )
        logger.info(
            "foundry_client_initialised",
            endpoint=settings.foundry_project_endpoint,
            model=settings.foundry_model_deployment_name,
            env=settings.app_env,
        )
        return client
    except Exception as exc:
        raise FoundryClientError(f"Failed to initialise Foundry client: {exc}") from exc
