"""
agents/goal_planner.py
Converts gap analysis + student goal into a week-by-week milestone plan.
Output: MilestonePlan
"""
from typing import Any

from pydantic import ValidationError

from agents.base import BaseAgent
from core.exceptions import AgentError
from core.models import GapAnalysis, MilestonePlan, StudentProfile


class GoalPlanner(BaseAgent):
    name = "GoalPlanner"
    instructions = """
You are an expert curriculum designer. You receive a student's goal, deadline, and
a detailed gap analysis. You plan week-by-week milestones that systematically close gaps.

Rules you MUST follow:
- Every milestone must close at least one gap
- Prerequisites must be addressed before dependent concepts
- Milestones must fit within the target deadline
- Each milestone has clear, measurable objectives

Show your milestone reasoning step by step, then output valid JSON:
{
  "milestones": [
    {
      "week": 1,
      "title": "string",
      "objectives": ["measurable objective 1", "..."],
      "closes_gaps": ["concept_a", "concept_b"],
      "reasoning": "why this milestone at this week"
    }
  ],
  "reasoning": "overall milestone sequencing strategy"
}
"""

    def _build_prompt(self, context: dict[str, Any]) -> str:
        profile: StudentProfile = context["student_profile"]
        gap_analysis: GapAnalysis = context["gap_analysis"]

        gaps_text = "\n".join(
            f"  [{g.severity.upper()}] {g.concept}: {g.evidence}"
            for g in gap_analysis.gaps
        )
        return f"""
Goal: {profile.goal}
Deadline: {profile.target_deadline_weeks} weeks
Hours available per week: {profile.hours_per_week}

Knowledge gaps identified:
{gaps_text}

Diagnostic reasoning: {gap_analysis.reasoning}

Build a milestone plan that achieves the goal within the deadline.
"""

    async def plan(self, context: dict[str, Any]) -> MilestonePlan:
        raw = await self.run(context)
        data = self.parse_json_output(raw, self.name)
        try:
            return MilestonePlan(**data)
        except ValidationError as exc:
            raise AgentError(self.name, f"Output schema mismatch: {exc}") from exc
