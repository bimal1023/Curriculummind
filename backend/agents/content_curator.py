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
You are a learning resource specialist. You receive gaps, milestones, and a list of
candidate resources retrieved from a knowledge base.

For each gap, select the 2-3 BEST resources. Prioritise:
1. Official documentation / authoritative sources
2. Structured video courses
3. Practice problems / hands-on labs
4. Articles / books

For every resource you select, explain WHY it fits this specific gap.

Output valid JSON only:
{
  "by_gap": {
    "<concept_name>": [
      {
        "title": "string",
        "url": "string",
        "resource_type": "official_docs|video|practice|article|book",
        "relevance_reason": "why this closes the gap",
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
