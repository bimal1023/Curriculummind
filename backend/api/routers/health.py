"""
api/routers/health.py
Liveness and readiness probes for Azure Container Apps / AKS.
"""
import time

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
_start_time = time.time()


class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    version: str = "0.1.0"


@router.get("/live", response_model=HealthResponse, summary="Liveness probe")
async def liveness() -> HealthResponse:
    return HealthResponse(status="ok", uptime_seconds=round(time.time() - _start_time, 1))


@router.get("/ready", response_model=HealthResponse, summary="Readiness probe")
async def readiness() -> HealthResponse:
    # In production: add a lightweight Foundry connectivity check here
    return HealthResponse(status="ready", uptime_seconds=round(time.time() - _start_time, 1))
