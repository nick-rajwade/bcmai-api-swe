"""Implementation of the tester agent."""
from __future__ import annotations

from typing import Any
import subprocess

from .base import Agent

TESTER_PROMPT = (
    "You are the Tester agent. Execute the code in a sandbox, run tests and "
    "report results."
)


class TesterAgent(Agent):
    def __init__(self, llm: Any = None) -> None:
        super().__init__(name="tester", system_prompt=TESTER_PROMPT, llm=llm)

    def test(self, project_path: str) -> str:
        """Run pytest inside the generated project."""
        proc = subprocess.run(["pytest", "-q", project_path], capture_output=True)
        result = proc.stdout.decode() + proc.stderr.decode()
        self.run(f"Test results: {result}")
        return result
