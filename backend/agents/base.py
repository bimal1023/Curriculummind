"""
agents/base.py
Abstract base for all CurriculumMind agents.
Handles retry logic, timeout enforcement, structured logging, and JSON parsing.
Every concrete agent inherits from BaseAgent and implements `_build_prompt`.
"""
from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from agent_framework import Agent
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from core.config import get_settings
from core.exceptions import AgentError, AgentRetryExhaustedError
from core.logging import get_logger
from services.foundry_client import get_foundry_client

T = TypeVar("T")
logger = get_logger(__name__)
settings = get_settings()


class BaseAgent(ABC):
    """
    Wraps a Microsoft Agent Framework Agent with:
    - Exponential-backoff retry
    - Structured logging on every invocation
    - JSON extraction from freeform LLM output
    """

    name: str
    instructions: str

    def __init__(self) -> None:
        self._agent = Agent(
            client=get_foundry_client(),
            name=self.name,
            instructions=self.instructions,
        )

    @abstractmethod
    def _build_prompt(self, context: dict[str, Any]) -> str:
        """Construct the user-turn prompt from context data."""

    async def run(self, context: dict[str, Any]) -> str:
        """
        Entry point called by the orchestrator.
        Returns raw string output; JSON parsing is done by parse_json_output().
        """
        prompt = self._build_prompt(context)
        return await self._run_with_retry(prompt)

    @retry(
        retry=retry_if_exception_type(AgentError),
        stop=stop_after_attempt(settings.agent_max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def _run_with_retry(self, prompt: str) -> str:
        try:
            logger.info("agent_invoked", agent=self.name)
            response = await self._agent.run(prompt)
            result: str = response.text
            logger.info("agent_succeeded", agent=self.name, output_len=len(result))
            return result
        except Exception as exc:
            logger.warning("agent_failed", agent=self.name, error=str(exc))
            raise AgentError(self.name, str(exc)) from exc

    @staticmethod
    def parse_json_output(raw: str, agent_name: str) -> dict[str, Any]:
        """
        Extracts JSON from an LLM response that may include explanation text.
        Tries: raw parse → code fence extraction → lenient brace extraction.
        """
        # 1. Direct parse
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # 2. Extract from ```json ... ``` fence
        fence = re.search(r"```(?:json)?\s*([\s\S]+?)```", raw)
        if fence:
            try:
                return json.loads(fence.group(1))
            except json.JSONDecodeError:
                pass

        # 3. Find outermost { ... }
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(raw[start : end + 1])
            except json.JSONDecodeError:
                pass

        raise AgentError(agent_name, f"Could not extract valid JSON from output: {raw[:200]}")
