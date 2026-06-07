"""
api/routers/plans.py
/api/v1/plans endpoints.
"""
from functools import lru_cache

from fastapi import APIRouter, Depends

from api.schemas.plans import ErrorResponse, GeneratePlanRequest, StudyPlanResponse
from core.models import StudentProfile
from orchestrator.pipeline import CurriculumPipeline

router = APIRouter()


@lru_cache
def get_pipeline() -> CurriculumPipeline:
    """Singleton pipeline — agents are initialised once at startup."""
    return CurriculumPipeline()


@router.post(
    "/generate",
    response_model=StudyPlanResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation or verification failure"},
        503: {"model": ErrorResponse, "description": "Agent service unavailable"},
    },
    summary="Generate a personalised study plan",
    description="""
Runs the full 5-agent CurriculumMind pipeline:
1. DiagnosticAnalyzer — identifies knowledge gaps
2. GoalPlanner — builds milestone sequence
3. ContentCurator + PaceReasoner — run in parallel
4. Verifier — quality gate with one correction pass
""",
)
async def generate_plan(
    request: GeneratePlanRequest,
    pipeline: CurriculumPipeline = Depends(get_pipeline),
) -> StudyPlanResponse:
    profile = StudentProfile(**request.model_dump())
    plan = await pipeline.generate(profile)
    return StudyPlanResponse.model_validate(plan.model_dump())
