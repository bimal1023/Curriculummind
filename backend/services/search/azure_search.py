"""
services/search/azure_search.py
Thin wrapper around Azure AI Search for resource retrieval.
ContentCurator agent calls this instead of calling the SDK directly.

If search is unconfigured or fails, this degrades gracefully by returning an
empty list — the ContentCurator then curates from the model's own knowledge.
"""
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents.aio import SearchClient

from core.config import get_settings
from core.logging import get_logger
from core.models import LearningResource, ResourceType

logger = get_logger(__name__)


class AzureSearchService:
    def __init__(self) -> None:
        settings = get_settings()
        self._endpoint = settings.azure_search_endpoint
        self._index_name = settings.azure_search_index_name
        self._api_key = settings.azure_search_api_key
        # No endpoint configured → search is effectively disabled.
        self._enabled = bool(self._endpoint)

    def _new_client(self) -> SearchClient:
        # A fresh client per call: the async context manager closes the client
        # on exit, so a long-lived shared client breaks on the 2nd parallel use.
        credential = (
            AzureKeyCredential(self._api_key)
            if self._api_key
            else DefaultAzureCredential()
        )
        return SearchClient(
            endpoint=self._endpoint,
            index_name=self._index_name,
            credential=credential,
        )

    async def search_resources(
        self,
        query: str,
        resource_types: list[ResourceType] | None = None,
        top: int = 5,
    ) -> list[LearningResource]:
        """
        Keyword + semantic search for learning resources. Returns an empty list
        on any failure so the caller can fall back to model-generated resources.
        """
        if not self._enabled:
            return []

        filter_expr = None
        if resource_types:
            types_str = " or ".join(
                f"resource_type eq '{rt}'" for rt in resource_types
            )
            filter_expr = f"({types_str})"

        try:
            async with self._new_client() as client:
                results = await client.search(
                    search_text=query,
                    filter=filter_expr,
                    top=top,
                    select=["title", "url", "resource_type",
                            "estimated_hours", "description"],
                )

                resources: list[LearningResource] = []
                async for result in results:
                    resources.append(
                        LearningResource(
                            title=result["title"],
                            url=result["url"],
                            resource_type=ResourceType(result["resource_type"]),
                            relevance_reason=result.get("description", ""),
                            estimated_hours=float(result.get("estimated_hours", 1.0)),
                        )
                    )

            logger.info("search_completed", query=query, result_count=len(resources))
            return resources

        except Exception as exc:
            # Non-fatal: curator falls back to model knowledge. Logged at
            # warning (not error) so it doesn't look like a pipeline failure.
            logger.warning(
                "search_unavailable_using_fallback",
                query=query,
                reason=str(exc).split("\n")[0][:160],
            )
            return []
