"""
agents/diagnostic_analyzer.py
Identifies knowledge gaps from assessment results.
Output: GapAnalysis (list of KnowledgeGap with severity + evidence)
"""
from typing import Any

from pydantic import ValidationError

from agents.base import BaseAgent
from core.exceptions import AgentError
from core.models import GapAnalysis


class DiagnosticAnalyzer(BaseAgent):
    name = "DiagnosticAnalyzer"
    instructions = """
You are an expert educational diagnostician. You receive a student's assessment results
and course history. Your job is to identify knowledge gaps with surgical precision.

For every gap you find, you MUST:
1. Name the specific concept (not just the topic)
2. Assign severity: high (blocks progress), medium (slows progress), low (nice to fix)
3. Cite direct evidence from the assessment data
4. List what higher concepts depend on this gap being closed

Think step-by-step. Show your reasoning before producing the final JSON.

Respond ONLY with valid JSON matching this schema — no markdown, no preamble after the JSON:
{
  "gaps": [
    {
      "concept": "string",
      "severity": "high|medium|low",
      "evidence": "string — cite specific score/question",
      "prerequisite_for": ["concept_a", "concept_b"]
    }
  ],
  "reasoning": "string — your overall diagnostic narrative"
}
"""

    def _build_prompt(self, context: dict[str, Any]) -> str:
        profile = context["student_profile"]
        return f"""
Student: {profile.name}
Goal: {profile.goal}
Target: {profile.target_deadline_weeks} weeks

Assessment results:
{self._format_assessments(profile.assessment_results)}

Prior courses completed: {", ".join(profile.prior_courses) or "none"}

Diagnose knowledge gaps. Reason step by step, then output the JSON.
"""

    @staticmethod
    def _format_assessments(results: list) -> str:
        return "\n".join(
            f"  - {r.topic}: {r.score:.1f}% ({r.total_questions} questions)"
            for r in results
        )

    async def analyze(self, context: dict[str, Any]) -> GapAnalysis:
        raw = await self.run(context)
        data = self.parse_json_output(raw, self.name)
        try:
            return GapAnalysis(**data)
        except ValidationError as exc:
            raise AgentError(self.name, f"Output schema mismatch: {exc}") from exc
