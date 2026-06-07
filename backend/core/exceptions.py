"""
core/exceptions.py
Application-specific exception hierarchy.
Raising typed exceptions lets FastAPI exception handlers return correct HTTP codes.
"""


class CurriculumMindError(Exception):
    """Base exception for all application errors."""


# ── Agent-layer errors ────────────────────────────────────────────────────────

class AgentError(CurriculumMindError):
    """An agent failed to produce a valid response."""
    def __init__(self, agent_name: str, message: str) -> None:
        self.agent_name = agent_name
        super().__init__(f"[{agent_name}] {message}")


class AgentTimeoutError(AgentError):
    """An agent exceeded its configured timeout."""


class AgentRetryExhaustedError(AgentError):
    """An agent exhausted all retry attempts."""


class VerificationFailedError(CurriculumMindError):
    """The Verifier agent found issues the orchestrator could not resolve."""
    def __init__(self, issues: list[str]) -> None:
        self.issues = issues
        super().__init__(f"Verification failed with {len(issues)} issue(s): {issues}")


# ── Input / schema errors ─────────────────────────────────────────────────────

class InvalidStudentProfileError(CurriculumMindError):
    """Student profile failed domain validation."""


# ── External service errors ───────────────────────────────────────────────────

class SearchServiceError(CurriculumMindError):
    """Azure AI Search call failed."""


class FoundryClientError(CurriculumMindError):
    """Could not initialise or connect to Microsoft Foundry."""
