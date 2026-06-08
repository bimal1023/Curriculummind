"""
core/models.py
Domain models (pure Pydantic). No I/O here — these are passed between agents and layers.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator


# ── Enums ─────────────────────────────────────────────────────────────────────

class GapSeverity(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ResourceType(StrEnum):
    OFFICIAL_DOCS = "official_docs"
    VIDEO = "video"
    PRACTICE = "practice"
    ARTICLE = "article"
    BOOK = "book"


class VerificationStatus(StrEnum):
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"


# ── Input models ──────────────────────────────────────────────────────────────

class AssessmentResult(BaseModel):
    topic: str
    score: float = Field(ge=0.0, le=100.0)
    total_questions: int = Field(ge=1)

    @field_validator("score")
    @classmethod
    def round_score(cls, v: float) -> float:
        return round(v, 2)


class StudentProfile(BaseModel):
    student_id: str
    name: str
    goal: str = Field(min_length=10, description="What the student wants to achieve")
    target_deadline_weeks: int = Field(ge=1, le=52)
    hours_per_week: float = Field(ge=1.0, le=40.0)
    assessment_results: list[AssessmentResult] = Field(min_length=1)
    prior_courses: list[str] = Field(default_factory=list)
    preferred_resource_types: list[ResourceType] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ── Intermediate agent outputs ────────────────────────────────────────────────

class KnowledgeGap(BaseModel):
    concept: str
    severity: GapSeverity
    evidence: str
    prerequisite_for: list[str] = Field(default_factory=list)


class GapAnalysis(BaseModel):
    gaps: list[KnowledgeGap]
    reasoning: str


class Milestone(BaseModel):
    week: int
    title: str
    objectives: list[str]
    closes_gaps: list[str]
    reasoning: str


class MilestonePlan(BaseModel):
    milestones: list[Milestone]
    reasoning: str


class LearningResource(BaseModel):
    title: str
    url: str
    resource_type: ResourceType
    relevance_reason: str
    estimated_hours: float = Field(ge=0.1)


class CuratedContent(BaseModel):
    by_gap: dict[str, list[LearningResource]]
    reasoning: str


class PacedPlan(BaseModel):
    milestones: list[Milestone]
    adjustments_made: list[str]
    reasoning: str


class VerificationResult(BaseModel):
    status: VerificationStatus
    issues: list[str] = Field(default_factory=list)
    reasoning: str


# ── Reasoning trace ───────────────────────────────────────────────────────────

class AgentThought(BaseModel):
    """One agent's step in the pipeline — what it did and why.

    Surfaced in the API response so clients can show the multi-step reasoning
    behind a plan, not just the final output.
    """
    step: int
    agent: str
    role: str               # one-line description of the agent's job
    summary: str            # what it concluded this run (e.g. "Found 3 gaps")
    reasoning: str          # the agent's own narrative
    parallel: bool = False  # True if it ran concurrently with the previous step


# ── Final output ──────────────────────────────────────────────────────────────

class StudyPlan(BaseModel):
    student_id: str
    goal: str
    gap_analysis: GapAnalysis
    milestone_plan: PacedPlan
    resources: CuratedContent
    verification: VerificationResult
    reasoning_trace: list[AgentThought] = Field(default_factory=list)
    generation_metadata: dict[str, Any] = Field(default_factory=dict)
