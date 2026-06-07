# CurriculumMind 🎓

> AI-powered adaptive learning path generator — Microsoft Agents League Hackathon (Reasoning Agents track)

CurriculumMind is a production-grade multi-agent system built on **Microsoft Agent Framework 1.0** and **Azure AI Foundry**. It takes a student's goal and assessment results and produces a personalised, verified week-by-week study plan — with explicit reasoning at every step.

---

## Agent architecture

```
StudentProfile
     │
     ▼
┌─────────────────────┐
│  DiagnosticAnalyzer │  → identifies knowledge gaps with severity + evidence
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│    GoalPlanner      │  → builds week-by-week milestones that close each gap
└─────────────────────┘
     │
     ├──────────────────────────┐  (parallel)
     ▼                          ▼
┌──────────────┐    ┌─────────────────┐
│ContentCurator│    │  PaceReasoner   │
│(Azure Search)│    │ (time-adjusted) │
└──────────────┘    └─────────────────┘
     │                          │
     └──────────────────────────┘
                   │
                   ▼
          ┌─────────────┐
          │   Verifier  │  → quality gate (1 correction pass if needed)
          └─────────────┘
                   │
                   ▼
           StudyPlan output
```

**ContentCurator and PaceReasoner run in parallel** — `asyncio.gather()` halves that stage's latency.

---

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/your-username/curriculummind
cd curriculummind
pip install -e ".[dev]"

# 2. Configure environment
cp .env.example .env
# Edit .env with your Foundry endpoint and Azure Search credentials

# 3. Run the API
python main.py

# 4. Generate a plan
curl -X POST http://localhost:8000/api/v1/plans/generate \
  -H "Content-Type: application/json" \
  -d @data/sample_profiles/az900_student.json
```

---

## Project structure

```
curriculummind/
├── agents/                    # One file per agent
│   ├── base.py                # Abstract base: retry, timeout, JSON parsing
│   ├── diagnostic_analyzer.py
│   ├── goal_planner.py
│   ├── content_curator.py     # Uses Azure AI Search
│   ├── pace_reasoner.py
│   └── verifier.py
├── orchestrator/
│   └── pipeline.py            # Async pipeline with parallel stage 3
├── api/
│   ├── app.py                 # FastAPI factory + exception handlers
│   ├── routers/               # health, plans
│   ├── schemas/               # HTTP-layer request/response models
│   └── middleware/            # Request logging
├── core/
│   ├── config.py              # Pydantic settings (env / .env)
│   ├── models.py              # Domain models (StudentProfile → StudyPlan)
│   ├── exceptions.py          # Typed exception hierarchy
│   └── logging.py             # structlog JSON/console
├── services/
│   ├── foundry_client.py      # Cached FoundryChatClient factory
│   └── search/azure_search.py # Azure AI Search wrapper
├── tests/
│   ├── unit/                  # Agent-level tests (fully mocked)
│   └── integration/           # Pipeline-level tests (fully mocked)
├── infrastructure/docker/     # Dockerfile + docker-compose
├── data/sample_profiles/      # Test inputs for judges
└── main.py                    # Uvicorn entry point
```

---

## Why every design decision exists

| Decision | Reason |
|---|---|
| `asyncio.gather` in stage 3 | ContentCurator and PaceReasoner are independent — parallel saves ~50% of their combined latency |
| Typed exception hierarchy | FastAPI handlers return correct HTTP codes per error type |
| `BaseAgent.parse_json_output` | LLMs sometimes wrap JSON in fences or prose — three-pass extraction handles this robustly |
| One correction pass in Verifier | Avoids infinite loops while still being resilient to first-pass imperfections |
| `@lru_cache` on Foundry client | Expensive auth handshake happens once at startup, not per request |
| Pydantic domain models | Schema is validated at every agent boundary — type errors surface immediately |

---

## Running tests

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

All tests are fully mocked — no Azure credentials required to run the test suite.

---

## Tech stack

- **Microsoft Agent Framework 1.0** — agent harness, skills, middleware
- **Azure AI Foundry** — hosted model deployment (GPT-4o)
- **Azure AI Search** — semantic resource retrieval for ContentCurator
- **FastAPI + Pydantic v2** — typed HTTP layer
- **structlog** — structured JSON logging
- **tenacity** — exponential backoff retry
- **Docker** — production container with non-root user

---

## Demo

[5-minute demo video link]
