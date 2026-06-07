"""
tests/unit/test_diagnostic_analyzer.py
Unit tests for DiagnosticAnalyzer — mocks the Foundry agent so no Azure credentials needed.
"""
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from agents.diagnostic_analyzer import DiagnosticAnalyzer
from core.models import AssessmentResult, StudentProfile


@pytest.fixture
def sample_profile() -> StudentProfile:
    return StudentProfile(
        student_id="test_001",
        name="Test Student",
        goal="Pass AZ-900 exam in 6 weeks with a strong understanding of cloud fundamentals",
        target_deadline_weeks=6,
        hours_per_week=10.0,
        assessment_results=[
            AssessmentResult(topic="Cloud concepts", score=45.0, total_questions=20),
            AssessmentResult(topic="Azure networking", score=30.0, total_questions=25),
        ],
        prior_courses=[],
    )


MOCK_AGENT_RESPONSE = json.dumps({
    "gaps": [
        {
            "concept": "Virtual Networks",
            "severity": "high",
            "evidence": "Azure networking score: 30% (7/25 correct)",
            "prerequisite_for": ["Load Balancers", "VPN Gateway"],
        },
        {
            "concept": "Cloud service models",
            "severity": "medium",
            "evidence": "Cloud concepts score: 45% (9/20 correct)",
            "prerequisite_for": ["Azure IaaS", "Azure PaaS"],
        },
    ],
    "reasoning": "Student has foundational gaps in networking that must be addressed first.",
})


@pytest.mark.asyncio
async def test_analyze_returns_gap_analysis(sample_profile):
    with (
        patch("agents.base.get_foundry_client"),
        patch("agents.base.Agent") as mock_agent_cls,
    ):
        mock_instance = AsyncMock()
        mock_instance.run.return_value = SimpleNamespace(text=MOCK_AGENT_RESPONSE)
        mock_agent_cls.return_value = mock_instance

        analyzer = DiagnosticAnalyzer()
        result = await analyzer.analyze({"student_profile": sample_profile})

    assert len(result.gaps) == 2
    assert result.gaps[0].concept == "Virtual Networks"
    assert result.gaps[0].severity.value == "high"


@pytest.mark.asyncio
async def test_analyze_parses_json_from_fenced_output(sample_profile):
    fenced = f"Here is my analysis:\n```json\n{MOCK_AGENT_RESPONSE}\n```"
    with (
        patch("agents.base.get_foundry_client"),
        patch("agents.base.Agent") as mock_agent_cls,
    ):
        mock_instance = AsyncMock()
        mock_instance.run.return_value = SimpleNamespace(text=fenced)
        mock_agent_cls.return_value = mock_instance

        analyzer = DiagnosticAnalyzer()
        result = await analyzer.analyze({"student_profile": sample_profile})

    assert len(result.gaps) == 2
