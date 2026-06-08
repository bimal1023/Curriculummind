"""
api/schemas/plans.py
HTTP-layer request and response schemas.
Kept separate from core/models.py so API contract can evolve independently.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from core.models import (
    AgentThought,
    AssessmentResult,
    CuratedContent,
    GapAnalysis,
    PacedPlan,
    ResourceType,
    VerificationResult,
)


class GeneratePlanRequest(BaseModel):
    student_id: str = Field(examples=["student_abc123"])
    name: str = Field(examples=["Bimal Thapa"])
    goal: str = Field(
        min_length=10,
        examples=["Pass the AZ-900 Microsoft Azure Fundamentals exam in 6 weeks"],
    )
    target_deadline_weeks: int = Field(ge=1, le=52, examples=[6])
    hours_per_week: float = Field(ge=1.0, le=40.0, examples=[10.0])
    assessment_results: list[AssessmentResult]
    prior_courses: list[str] = Field(default_factory=list)
    preferred_resource_types: list[ResourceType] = Field(default_factory=list)


class StudyPlanResponse(BaseModel):
    student_id: str
    goal: str
    gap_analysis: GapAnalysis
    milestone_plan: PacedPlan
    resources: CuratedContent
    verification: VerificationResult
    reasoning_trace: list[AgentThought] = []
    generation_metadata: dict[str, Any]

    model_config = {"from_attributes": True}


class ErrorResponse(BaseModel):
    error: str
    issues: list[str] | None = None
    detail: str | None = None
