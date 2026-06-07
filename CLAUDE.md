# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

CurriculumMind is an AI-powered adaptive learning path generator built on **Microsoft Agent Framework 1.0** and **Azure AI Foundry**. It accepts a `StudentProfile` (assessment scores + goal + time constraints) and returns a verified week-by-week `StudyPlan` via a 5-agent async pipeline.

## Layout

The repo is split into two apps:

```
curriculummind/
├── backend/     # FastAPI + 5-agent pipeline (Python 3.11+)
└── frontend/    # Next.js 14 + Tailwind UI (Pinterest-themed)
```

All backend commands run from `backend/`; all frontend commands from `frontend/`.

## Commands

**Backend** (run from `backend/`):
```bash
# Install (Python 3.11+ required; uses conda env "curriculummind")
pip install -e ".[dev]"

# Run the API
python main.py                    # starts uvicorn on APP_PORT (default 8000)

# Lint / type check
ruff check .
ruff format .
mypy .

# Tests (no Azure credentials needed — all mocked)
pytest tests/ -v --cov=. --cov-report=term-missing

# Single test
pytest tests/unit/test_diagnostic_analyzer.py::test_analyze_returns_gap_analysis -v
```

**Frontend** (run from `frontend/`):
```bash
npm install
npm run dev                       # http://localhost:3000 → calls backend on :8000
npm run build                     # production build
```

## Environment

`backend/`: copy `.env.example` to `.env`. The only required variable is `FOUNDRY_PROJECT_ENDPOINT`. All others have defaults or are optional.

`frontend/`: optional `.env` with `NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8000`). The backend's CORS already allows `http://localhost:3000`.

| Variable | Purpose |
|---|---|
| `FOUNDRY_PROJECT_ENDPOINT` | Azure AI Foundry project URL (required) |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Model deployment name (default: `gpt-4o`) |
| `AZURE_SEARCH_ENDPOINT` / `AZURE_SEARCH_API_KEY` | Needed for ContentCurator's resource retrieval |
| `APP_ENV` | `development` disables Swagger auth and uses `DefaultAzureCredential` |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Optional — enables distributed tracing |

## Architecture

### Pipeline execution order

```
StudentProfile
  → DiagnosticAnalyzer          # stage 1: finds KnowledgeGaps
  → GoalPlanner                 # stage 2: builds Milestones from gaps
  → ContentCurator  ─┐          # stage 3: parallel (asyncio.gather)
  → PaceReasoner    ─┘          # stage 3: parallel
  → Verifier                    # stage 4: quality gate, one correction pass
  → StudyPlan
```

`orchestrator/pipeline.py` is the only file that wires agents together. If `Verifier` returns `needs_revision`, `GoalPlanner` runs once more with verifier feedback appended; if it still fails, `VerificationFailedError` is raised.

### Domain model flow

All inter-agent data uses typed Pydantic v2 models from `core/models.py`:  
`StudentProfile → GapAnalysis → MilestonePlan → (CuratedContent + PacedPlan) → VerificationResult → StudyPlan`

### BaseAgent pattern

Every agent in `agents/` inherits `BaseAgent` (`agents/base.py`):
- Implements `_build_prompt(context)` to produce the user-turn string
- Exposes a typed public method (e.g., `analyze()`, `plan()`) that calls `run()` then `parse_json_output()` then Pydantic validation
- `parse_json_output` has three-pass extraction: raw JSON → fenced code block → outermost `{…}` brace match
- `_run_with_retry` wraps the agent call with `tenacity` exponential backoff (`AGENT_MAX_RETRIES` attempts)

### Key files

All backend paths below are relative to `backend/`.

| File | Role |
|---|---|
| `orchestrator/pipeline.py` | Pipeline sequencing, parallel gather, correction pass |
| `agents/base.py` | Retry logic, JSON extraction, structured logging |
| `core/models.py` | All domain models — the schema contract between agents |
| `core/exceptions.py` | Typed exception hierarchy (maps to HTTP codes in `api/app.py`) |
| `core/config.py` | `get_settings()` — cached Pydantic settings singleton |
| `services/foundry_client.py` | `get_foundry_client()` — `@lru_cache` singleton, Managed vs Default credential |
| `services/search/azure_search.py` | Azure AI Search wrapper used by ContentCurator |
| `api/app.py` | FastAPI factory with exception handlers per exception type |
| `api/routers/plans.py` | `POST /api/v1/plans/generate` — the only non-health endpoint |

Frontend (relative to `frontend/`): `app/page.jsx` holds the `setup → loading → results` state machine; `lib/api.js` is the single fetch helper; reusable UI lives in `components/`.

### HTTP error mapping

| Exception | HTTP code |
|---|---|
| `InvalidStudentProfileError` | 422 |
| `VerificationFailedError` | 422 (with `issues` list) |
| `AgentError` | 503 |
| `CurriculumMindError` (base) | 500 |

## Testing conventions

All tests mock at two points: `agents.base.get_foundry_client` and `agents.base.Agent`. No Azure credentials are needed. Integration tests in `tests/integration/test_pipeline.py` additionally mock `AzureSearchService.search_resources`. New agent tests follow the pattern in `tests/unit/test_diagnostic_analyzer.py`.
