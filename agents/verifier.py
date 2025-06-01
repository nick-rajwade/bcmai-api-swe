"""Implementation of the verifier agent."""
from __future__ import annotations

from typing import Any
import os
import subprocess

from .base import Agent

VERIFIER_PROMPT = (
    "You are the Verifier agent. Check the generated API code for quality, "
    "correctness and adherence to requirements. Provide detailed feedback."
)


class VerifierAgent(Agent):
    def __init__(self, llm: Any = None) -> None:
        super().__init__(name="verifier", system_prompt=VERIFIER_PROMPT, llm=llm)

    def verify(self, project_path: str) -> str:
        """Verify generated project by compiling it."""
        files = []
        for root, _, filenames in os.walk(project_path):
            for fname in filenames:
                if fname.endswith(".py"):
                    files.append(os.path.join(root, fname))
        errors = []
        for file in files:
            proc = subprocess.run(["python", "-m", "py_compile", file], capture_output=True)
            if proc.returncode != 0:
                errors.append(proc.stderr.decode())
        msg = "\n".join(errors) if errors else "All files compile"
        # Record result in memory via LLM stub
        self.run(f"Verification result: {msg}")
        return msg
