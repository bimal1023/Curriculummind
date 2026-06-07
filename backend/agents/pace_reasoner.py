"""
agents/pace_reasoner.py
Adjusts the milestone plan to match the student's actual available time.
Output: PacedPlan
"""
from typing import Any

from pydantic import ValidationError

from agents.base import BaseAgent
from core.exceptions import AgentError
from core.models import MilestonePlan, PacedPlan, StudentProfile


class PaceReasoner(BaseAgent):
    name = "PaceReasoner"
    instructions = """
You are a learning pace advisor. You receive a draft milestone plan and a student's
time constraints. Adjust the plan so it is realistic and achievable.

Adjustments you may make:
- Split overloaded weeks into two
- Merge sparse weeks
- Reorder milestones that are time-independent
- Flag milestones at risk of being skipped

Output ONLY valid JSON with this exact structure — no extra keys, no markdown:
{
  "milestones": [
    {
      "week": 1,
      "title": "string",
      "objectives": ["string", "string"],
      "closes_gaps": ["gap name"],
      "reasoning": "why this week covers these objectives"
    }
  ],
  "adjustments_made": ["description of each adjustment made"],
  "reasoning": "overall pacing strategy explanation"
}
"""

    def _build_prompt(self, context: dict[str, Any]) -> str:
        profile: StudentProfile = context["student_profile"]
        plan: MilestonePlan = context["milestone_plan"]

        milestones_text = "\n".join(
            f"  Week {m.week}: {m.title}\n"
            f"    Objectives: {', '.join(m.objectives)}\n"
            f"    Closes: {', '.join(m.closes_gaps)}"
            for m in plan.milestones
        )
        return f"""
Student: {profile.name}
Available: {profile.hours_per_week} hours/week over {profile.target_deadline_weeks} weeks

Draft milestone plan:
{milestones_text}

Adjust for realistic pacing. Show reasoning for each change.
"""

    async def adjust(self, context: dict[str, Any]) -> PacedPlan:
        raw = await self.run(context)
        data = self.parse_json_output(raw, self.name)
        try:
            return PacedPlan(**data)
        except ValidationError as exc:
            raise AgentError(self.name, f"Output schema mismatch: {exc}") from exc
