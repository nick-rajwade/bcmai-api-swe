"""Implementation of the coder agent."""
from __future__ import annotations

from typing import Any, Dict

from .base import Agent
from .api_generator import generate_fastapi_app

CODER_PROMPT = (
    "You are the Coder agent. Generate high quality API code using the given "
    "OpenAPI and AsyncIO specifications. Adhere to best practices and write "
    "production ready code."
)


class CoderAgent(Agent):
    def __init__(self, llm: Any = None) -> None:
        super().__init__(name="coder", system_prompt=CODER_PROMPT, llm=llm)

    def generate_code(self, openapi_path: str, asyncio_path: str, output_dir: str, features: Dict[str, Any]) -> str:
        """Generate code and return path to generated project."""
        # Use language model to plan generation (stubbed)
        self.run(f"Generate API for {openapi_path} and {asyncio_path}")
        return generate_fastapi_app(openapi_path, asyncio_path, output_dir, features)
