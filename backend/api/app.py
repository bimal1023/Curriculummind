"""
api/app.py
FastAPI application factory.
Call create_app() to get the configured application instance.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.middleware.logging import RequestLoggingMiddleware
from api.routers import health, plans
from core.config import get_settings
from core.exceptions import (
    AgentError,
    CurriculumMindError,
    InvalidStudentProfileError,
    VerificationFailedError,
)
from core.logging import configure_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown logic."""
    configure_logging()
    # Warm up the Foundry client at startup so first request isn't slow
    from services.foundry_client import get_foundry_client
    get_foundry_client()
    logger.info("app_started")
    yield
    logger.info("app_shutdown")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="CurriculumMind API",
        description="AI-powered adaptive learning path generator — Microsoft Foundry",
        version="0.1.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── Middleware ─────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    # ── Routers ────────────────────────────────────────────────────────────────
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])

    # ── Exception handlers ────────────────────────────────────────────────────
    @app.exception_handler(InvalidStudentProfileError)
    async def handle_invalid_profile(_: Request, exc: InvalidStudentProfileError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"error": str(exc)})

    @app.exception_handler(VerificationFailedError)
    async def handle_verification_failed(
        _: Request, exc: VerificationFailedError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": "Plan verification failed", "issues": exc.issues},
        )

    @app.exception_handler(AgentError)
    async def handle_agent_error(_: Request, exc: AgentError) -> JSONResponse:
        logger.error("agent_error", agent=exc.agent_name, error=str(exc))
        return JSONResponse(
            status_code=503,
            content={"error": f"Agent {exc.agent_name} failed", "detail": str(exc)},
        )

    @app.exception_handler(CurriculumMindError)
    async def handle_app_error(_: Request, exc: CurriculumMindError) -> JSONResponse:
        logger.error("app_error", error=str(exc))
        return JSONResponse(status_code=500, content={"error": str(exc)})

    return app
