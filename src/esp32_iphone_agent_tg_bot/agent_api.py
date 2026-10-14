"""Client for interacting with the ESP32 iPhone Agent API."""

import os
from typing import Any
from typing import AsyncIterator

import httpx

AGENT_API_URL = os.getenv("AGENT_API_URL", "http://localhost:8000")


class AgentAPIError(Exception):
    """Raised when the Agent API returns an error."""


class AgentClient:
    """Asynchronous client for the ESP32 iPhone Agent."""

    def __init__(self, base_url: str = AGENT_API_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=300.0)

    async def send_task(self, instruction: str) -> AsyncIterator[dict[str, Any]]:
        """Send a task instruction and stream execution steps.

        Args:
            instruction: Natural language instruction for the agent.

        Yields:
            Dictionaries containing step information, including screenshots and status.

        Raises:
            AgentAPIError: If the API request fails.
        """
        try:
            async with self._client.stream("POST", "/api/v1/tasks", json={"instruction": instruction}) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        import json

                        data = line[6:].strip()
                        if data == "[DONE]":
                            break
                        try:
                            yield json.loads(data)
                        except json.JSONDecodeError:
                            continue
        except httpx.HTTPStatusError as e:
            raise AgentAPIError(f"API request failed: {e}") from e
        except httpx.RequestError as e:
            raise AgentAPIError(f"Network error: {e}") from e

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()
