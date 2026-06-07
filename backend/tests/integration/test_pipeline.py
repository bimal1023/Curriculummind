"""
tests/integration/test_pipeline.py
Integration test for the full orchestration pipeline.
All agents are mocked — tests the pipeline sequencing and data flow.
"""
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from core.models import AssessmentResult, StudentProfile, VerificationStatus
from orchestrator.pipeline import CurriculumPipeline

PROFILE = StudentProfile(
    student_id="integration_test_001",
    name="Test Student",
    goal="Pass the AZ-900 exam in 6 weeks with deep understanding of cloud fundamentals",
    target_deadline_weeks=6,
    hours_per_week=10.0,
    assessment_results=[
        AssessmentResult(topic="Cloud concepts", score=50.0, total_questions=20),
    ],
)

GAP_OUTPUT = {"gaps": [{"concept": "Cloud models", "severity": "medium", "evidence": "50%", "prerequisite_for": []}], "reasoning": "foundational gap"}
MILESTONE_OUTPUT = {"milestones": [{"week": 1, "title": "Cloud foundations", "objectives": ["Understand IaaS, PaaS, SaaS"], "closes_gaps": ["Cloud models"], "reasoning": "core first"}], "reasoning": "linear plan"}
CONTENT_OUTPUT = {"by_gap": {"Cloud models": [{"title": "AZ-900 Docs", "url": "https://learn.microsoft.com", "resource_type": "official_docs", "relevance_reason": "authoritative", "estimated_hours": 3.0}]}, "reasoning": "official first"}
PACED_OUTPUT = {**MILESTONE_OUTPUT, "adjustments_made": ["no changes needed"]}
VERIFY_OUTPUT = {"status": "approved", "issues": [], "reasoning": "plan is sound"}


@pytest.mark.asyncio
async def test_pipeline_happy_path():
    with (
        patch("agents.base.get_foundry_client"),
        patch("agents.base.Agent") as mock_cls,
        patch("services.search.azure_search.AzureSearchService.search_resources", new_callable=AsyncMock, return_value=[]),
    ):
        # Stage 3 runs ContentCurator and PaceReasoner concurrently, so the
        # order their run() calls fire is non-deterministic. Dispatch the mock
        # by agent name instead of call order. Agent.run() returns an
        # AgentResponse whose .text holds the output.
        responses = {
            "DiagnosticAnalyzer": GAP_OUTPUT,
            "GoalPlanner": MILESTONE_OUTPUT,
            "ContentCurator": CONTENT_OUTPUT,
            "PaceReasoner": PACED_OUTPUT,
            "Verifier": VERIFY_OUTPUT,
        }

        def make_agent(*args, **kwargs):
            agent = AsyncMock()
            agent.run.return_value = SimpleNamespace(
                text=json.dumps(responses[kwargs["name"]])
            )
            return agent

        mock_cls.side_effect = make_agent

        pipeline = CurriculumPipeline()
        plan = await pipeline.generate(PROFILE)

    assert plan.student_id == "integration_test_001"
    assert plan.verification.status == VerificationStatus.APPROVED
    assert len(plan.gap_analysis.gaps) == 1
    assert len(plan.milestone_plan.milestones) == 1
