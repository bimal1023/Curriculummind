"""
agents/content_curator.py
Selects learning resources for each gap using Azure AI Search + reasoning.
Output: CuratedContent
"""
from typing import Any

from pydantic import ValidationError

from agents.base import BaseAgent
from core.exceptions import AgentError
from core.models import CuratedContent, GapAnalysis, LearningResource, ResourceType, StudentProfile
from services.search.azure_search import AzureSearchService


class ContentCurator(BaseAgent):
    name = "ContentCurator"
    instructions = """
You are a learning resource specialist. You receive knowledge gaps and must recommend
the best 2-3 real, working resources per gap.

CRITICAL URL RULES — you MUST follow these exactly:
- Only use URLs you are 100% certain still exist and are publicly accessible.
- For YouTube videos, ONLY use channel or playlist URLs, never individual video URLs
  (individual video IDs go dead; channels stay alive).
  Format: https://www.youtube.com/@ChannelName or https://www.youtube.com/c/ChannelName
- For official docs, use the ROOT or SECTION page, never a deep sub-page that may move.
  Good: https://learn.microsoft.com/en-us/azure/
  Bad:  https://learn.microsoft.com/en-us/azure/some/deeply/nested/2019/page
- ONLY use these trusted domains:
  * learn.microsoft.com, docs.aws.amazon.com, cloud.google.com/docs
  * youtube.com (channel/playlist URLs only)
  * coursera.org, edx.org, udemy.com (course root pages only)
  * developers.google.com, developer.mozilla.org
  * github.com (official org repos only, e.g. github.com/microsoft or github.com/aws)
  * freecodecamp.org, kaggle.com/learn
- If you are not 100% sure a URL is valid and live, use the homepage of the trusted
  domain instead (e.g. https://learn.microsoft.com/en-us/training/).
- NEVER invent or guess URLs. NEVER use URLs from memory that might be outdated.

Prioritise resources in this order:
1. Official documentation (learn.microsoft.com, docs.aws.amazon.com, etc.)
2. Official YouTube channels of the technology provider
3. Well-known course platforms (Coursera, edX, freeCodeCamp)
4. Official GitHub repos

Output valid JSON only:
{
  "by_gap": {
    "<concept_name>": [
      {
        "title": "string — descriptive title of the resource",
        "url": "string — verified URL following the rules above",
        "resource_type": "official_docs|video|practice|article|book",
        "relevance_reason": "why this resource directly closes this gap",
        "estimated_hours": 2.5
      }
    ]
  },
  "reasoning": "overall curation strategy"
}
"""

    def __init__(self) -> None:
        super().__init__()
        self._search = AzureSearchService()

    def _build_prompt(self, context: dict[str, Any]) -> str:
        gap_analysis: GapAnalysis = context["gap_analysis"]
        profile: StudentProfile = context["student_profile"]
        candidate_resources: dict[str, list[LearningResource]] = context.get(
            "candidate_resources", {}
        )

        gaps_text = "\n".join(
            f"  - {g.concept} ({g.severity})" for g in gap_analysis.gaps
        )

        resource_text = ""
        for concept, resources in candidate_resources.items():
            resource_text += f"\n  [{concept}]\n"
            for r in resources:
                resource_text += (
                    f"    • {r.title} ({r.resource_type}) — {r.estimated_hours}h\n"
                    f"      {r.url}\n"
                )

        preferred = ", ".join(profile.preferred_resource_types) or "no preference"
        return f"""
Gaps to address:
{gaps_text}

Student's preferred resource types: {preferred}

Candidate resources retrieved from knowledge base:
{resource_text or '  (none retrieved — select from general knowledge)'}

Select and justify the best 2-3 resources per gap.
"""

    async def curate(self, context: dict[str, Any]) -> CuratedContent:
        """
        Pre-fetches candidates from Azure Search for each gap,
        then lets the LLM make the final selection with reasoning.
        """
        gap_analysis: GapAnalysis = context["gap_analysis"]
        profile: StudentProfile = context["student_profile"]

        # Parallel search for all gaps
        import asyncio
        search_tasks = {
            gap.concept: self._search.search_resources(
                query=gap.concept,
                resource_types=profile.preferred_resource_types or None,
                top=5,
            )
            for gap in gap_analysis.gaps
        }
        results = await asyncio.gather(*search_tasks.values(), return_exceptions=True)
        candidate_resources: dict[str, list[LearningResource]] = {}
        for concept, result in zip(search_tasks.keys(), results):
            candidate_resources[concept] = result if not isinstance(result, Exception) else []

        context["candidate_resources"] = candidate_resources
        raw = await self.run(context)
        data = self.parse_json_output(raw, self.name)
        try:
            return CuratedContent(**data)
        except ValidationError as exc:
            raise AgentError(self.name, f"Output schema mismatch: {exc}") from exc
