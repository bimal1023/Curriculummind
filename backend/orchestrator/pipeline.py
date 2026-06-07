"""
orchestrator/pipeline.py
CurriculumMind orchestration pipeline.

Execution order:
  1. DiagnosticAnalyzer            (sequential — everything depends on this)
  2. GoalPlanner                   (sequential — needs gap analysis)
  3. ContentCurator + PaceReasoner (PARALLEL — independent of each other)
  4. Verifier                      (sequential — needs all outputs)

If Verifier returns needs_revision, the orchestrator makes one correction pass.
If issues remain, it returns the best-effort plan with the verification status
attached rather than discarding the work.
"""
from __future__ import annotations

import asyncio
import time
from typing import Any

from agents.content_curator import ContentCurator
from agents.diagnostic_analyzer import DiagnosticAnalyzer
from agents.goal_planner import GoalPlanner
from agents.pace_reasoner import PaceReasoner
from agents.verifier import Verifier
from core.logging import get_logger
from core.models import StudentProfile, StudyPlan, VerificationStatus

logger = get_logger(__name__)


class CurriculumPipeline:
    """
    Stateless orchestrator. Create one instance per app startup and reuse.
    Each call to generate() is fully independent.
    """

    def __init__(self) -> None:
        self._diagnostic = DiagnosticAnalyzer()
        self._planner = GoalPlanner()
        self._curator = ContentCurator()
        self._pacer = PaceReasoner()
        self._verifier = Verifier()

    async def generate(self, profile: StudentProfile) -> StudyPlan:
        """
        Full pipeline execution. Returns a StudyPlan. After one correction
        pass, any remaining verification issues are attached to the plan's
        verification field rather than raised.
        """
        start = time.monotonic()
        logger.info("pipeline_started", student_id=profile.student_id, goal=profile.goal)

        # ── Stage 1: Diagnose ─────────────────────────────────────────────────
        gap_analysis = await self._diagnostic.analyze({"student_profile": profile})
        logger.info("diagnostic_done", gap_count=len(gap_analysis.gaps))

        # ── Stage 2: Plan milestones ──────────────────────────────────────────
        milestone_plan = await self._planner.plan({
            "student_profile": profile,
            "gap_analysis": gap_analysis,
        })
        logger.info("planning_done", milestone_count=len(milestone_plan.milestones))

        # ── Stage 3: Curate + Pace in parallel ───────────────────────────────
        curated_content, paced_plan = await asyncio.gather(
            self._curator.curate({
                "student_profile": profile,
                "gap_analysis": gap_analysis,
                "milestone_plan": milestone_plan,
            }),
            self._pacer.adjust({
                "student_profile": profile,
                "milestone_plan": milestone_plan,
            }),
        )
        logger.info(
            "curation_and_pacing_done",
            resource_groups=len(curated_content.by_gap),
            adjustments=len(paced_plan.adjustments_made),
        )

        # ── Stage 4: Verify ───────────────────────────────────────────────────
        verification_ctx: dict[str, Any] = {
            "gap_analysis": gap_analysis,
            "paced_plan": paced_plan,
            "curated_content": curated_content,
            "hours_per_week": profile.hours_per_week,
            "deadline_weeks": profile.target_deadline_weeks,
        }
        verification = await self._verifier.verify(verification_ctx)

        if verification.status == VerificationStatus.NEEDS_REVISION:
            logger.warning(
                "verification_failed_attempting_fix",
                issues=verification.issues,
            )
            # One correction pass: re-run planner with issues appended, then
            # re-pace so the Verifier receives a PacedPlan (it reads
            # adjustments_made, which only PaceReasoner produces).
            corrected_milestones = await self._planner.plan({
                "student_profile": profile,
                "gap_analysis": gap_analysis,
                "verifier_feedback": verification.issues,
            })
            corrected_plan = await self._pacer.adjust({
                "student_profile": profile,
                "milestone_plan": corrected_milestones,
            })
            verification_ctx["paced_plan"] = corrected_plan
            verification = await self._verifier.verify(verification_ctx)

            # Always keep the corrected (best-effort) plan. If the Verifier
            # still flags minor issues, we return the plan with its
            # needs_revision status attached rather than discarding all the
            # work — the client surfaces the issues to the student.
            paced_plan = corrected_plan
            if verification.status == VerificationStatus.NEEDS_REVISION:
                logger.warning(
                    "verification_still_flagged_returning_best_effort",
                    issues=verification.issues,
                )

        elapsed = round(time.monotonic() - start, 2)
        logger.info("pipeline_completed", student_id=profile.student_id, elapsed_s=elapsed)

        return StudyPlan(
            student_id=profile.student_id,
            goal=profile.goal,
            gap_analysis=gap_analysis,
            milestone_plan=paced_plan,
            resources=curated_content,
            verification=verification,
            generation_metadata={
                "elapsed_seconds": elapsed,
                "agent_count": 5,
                "framework": "Microsoft Agent Framework 1.0",
            },
        )
