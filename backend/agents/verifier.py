"""
agents/verifier.py
Final quality gate. Checks prerequisite ordering, gap coverage, and plan coherence.
Output: VerificationResult
"""
from typing import Any

from pydantic import ValidationError

from agents.base import BaseAgent
from core.exceptions import AgentError
from core.models import GapAnalysis, PacedPlan, VerificationResult


class Verifier(BaseAgent):
    name = "Verifier"
    instructions = """
You are a pragmatic curriculum quality auditor. You receive a complete study plan
and decide whether it is good enough for a student to start following.

Return "needs_revision" ONLY for SERIOUS, blocking problems:
- A high-severity gap that no milestone addresses at all
- A hard prerequisite taught AFTER the concept that depends on it
- A milestone that depends on a strictly later milestone (circular)

Do NOT request revision for minor or subjective concerns. The following are
ACCEPTABLE and must NOT trigger needs_revision:
- A topic reinforced across multiple weeks (spaced repetition is good)
- A slightly ambitious but plausible weekly workload
- A gap covered "partially" as long as it is meaningfully addressed
- Ordering preferences that are reasonable either way

Default to "approved" when the plan is coherent and covers the gaps. Only use
"needs_revision" when a student would genuinely be blocked or misled. You may
still list non-blocking observations in "issues" while marking "approved".

Output valid JSON only:
{
  "status": "approved|needs_revision",
  "issues": ["only SERIOUS blocking issues, with evidence"],
  "reasoning": "your audit narrative — explain why approved or not"
}
"""

    def _build_prompt(self, context: dict[str, Any]) -> str:
        gap_analysis: GapAnalysis = context["gap_analysis"]
        paced_plan: PacedPlan = context["paced_plan"]
        hours_per_week: float = context["hours_per_week"]
        deadline_weeks: int = context["deadline_weeks"]

        total_weeks = max(m.week for m in paced_plan.milestones)
        gaps_list = ", ".join(f"{g.concept}({g.severity})" for g in gap_analysis.gaps)
        milestones_text = "\n".join(
            f"  Week {m.week}: {m.title} — closes: {', '.join(m.closes_gaps)}"
            for m in paced_plan.milestones
        )

        return f"""
Gaps identified: {gaps_list}
Student deadline: {deadline_weeks} weeks | {hours_per_week}h/week
Plan spans: {total_weeks} weeks

Milestones:
{milestones_text}

Adjustments made by PaceReasoner:
{chr(10).join(f'  - {a}' for a in paced_plan.adjustments_made)}

Audit the plan. Be strict. Output JSON.
"""

    async def verify(self, context: dict[str, Any]) -> VerificationResult:
        raw = await self.run(context)
        data = self.parse_json_output(raw, self.name)
        try:
            return VerificationResult(**data)
        except ValidationError as exc:
            raise AgentError(self.name, f"Output schema mismatch: {exc}") from exc
