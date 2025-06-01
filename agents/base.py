"""Base classes for multi-agent system."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


class SimpleMemory:
    """In-memory store for short-term data."""
    def __init__(self) -> None:
        self._store: Dict[str, List[Dict[str, str]]] = {}

    def append(self, key: str, user: str, assistant: str) -> None:
        self._store.setdefault(key, []).append({"user": user, "assistant": assistant})

    def get(self, key: str) -> List[Dict[str, str]]:
        return self._store.get(key, [])


class FileMemory:
    """Simple disk-based long-term memory."""

    def __init__(self, path: str) -> None:
        self.path = path
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._store = json.load(f)
        except FileNotFoundError:
            self._store = {}

    def append(self, key: str, user: str, assistant: str) -> None:
        self._store.setdefault(key, []).append({"user": user, "assistant": assistant})
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._store, f, indent=2)

    def get(self, key: str) -> List[Dict[str, str]]:
        return self._store.get(key, [])


@dataclass
class Agent:
    """Base agent using a callable for LLM interaction."""

    name: str
    system_prompt: str
    llm: Any
    short_memory: SimpleMemory = field(default_factory=SimpleMemory)
    long_memory: FileMemory | None = None

    def _record(self, user: str, assistant: str) -> None:
        self.short_memory.append(self.name, user, assistant)
        if self.long_memory:
            self.long_memory.append(self.name, user, assistant)

    def run(self, user_input: str) -> str:
        """Run the agent with the provided user input."""
        history = self.short_memory.get(self.name)
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        for turn in history[-5:]:
            messages.append({"role": "user", "content": turn["user"]})
            messages.append({"role": "assistant", "content": turn["assistant"]})
        messages.append({"role": "user", "content": user_input})

        if self.llm is None:
            # Fallback behaviour if no model is available
            assistant = f"Echo: {user_input}"
        else:
            assistant = self.llm(messages)
        self._record(user_input, assistant)
        return assistant
