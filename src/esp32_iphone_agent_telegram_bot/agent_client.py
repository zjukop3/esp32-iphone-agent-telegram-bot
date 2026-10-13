"""HTTP client to interact with the esp32-iphone-agent API."""

import httpx
import logging

logger = logging.getLogger(__name__)

class AgentClient:
    """Client for the esp32-iphone-agent API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=60.0)

    async def run_task(self, task_description: str) -> dict:
        """
        Send a task to the agent and wait for completion.
        
        Args:
            task_description: Natural language description of the task.
            
        Returns:
            A dictionary containing the task result (status, screenshot_url, etc.)
        """
        payload = {"task": task_description}
        try:
            response = await self.client.post("/api/v1/run", json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            return {"status": "error", "error": f"API returned {e.response.status_code}"}
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            return {"status": "error", "error": "Failed to connect to agent API"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"status": "error", "error": str(e)}

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()
