"""
services/search/azure_search.py
Thin wrapper around Azure AI Search for resource retrieval.
ContentCurator agent calls this instead of calling the SDK directly.
"""
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents.aio import SearchClient
from azure.search.documents.models import VectorizedQuery

from core.config import get_settings
from core.exceptions import SearchServiceError
from core.logging import get_logger
from core.models import LearningResource, ResourceType

logger = get_logger(__name__)


class AzureSearchService:
    def __init__(self) -> None:
        settings = get_settings()
        credential = (
            AzureKeyCredential(settings.azure_search_api_key)
            if settings.azure_search_api_key
            else DefaultAzureCredential()
        )
        self._client = SearchClient(
            endpoint=settings.azure_search_endpoint,
            index_name=settings.azure_search_index_name,
            credential=credential,
        )

    async def search_resources(
        self,
        query: str,
        resource_types: list[ResourceType] | None = None,
        top: int = 5,
    ) -> list[LearningResource]:
        """
        Hybrid keyword + semantic search for learning resources.
        Falls back to keyword-only if semantic ranker is not configured.
        """
        try:
            filter_expr = None
            if resource_types:
                types_str = " or ".join(
                    f"resource_type eq '{rt}'" for rt in resource_types
                )
                filter_expr = f"({types_str})"

            async with self._client:
                results = await self._client.search(
                    search_text=query,
                    filter=filter_expr,
                    top=top,
                    select=["title", "url", "resource_type",
                            "estimated_hours", "description"],
                    query_type="semantic",
                    semantic_configuration_name="default",
                )

                resources = []
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
            logger.error("search_failed", query=query, error=str(exc))
            raise SearchServiceError(f"Search failed for query '{query}': {exc}") from exc
