"""Orchestrator building a LangGraph style workflow."""
from __future__ import annotations

import os
from typing import Any, Dict
from .spec_parser import load_config

from .coder import CoderAgent
from .verifier import VerifierAgent
from .tester import TesterAgent


def create_orchestrator(llm: Any = None) -> Dict[str, Any]:
    """Create agents and return orchestrator configuration."""
    coder = CoderAgent(llm=llm)
    verifier = VerifierAgent(llm=llm)
    tester = TesterAgent(llm=llm)

    graph = {
        "coder": coder,
        "verifier": verifier,
        "tester": tester,
    }
    return graph


def run_workflow(config_path: str, llm: Any = None) -> str:
    """Run the development workflow end-to-end."""
    cfg = load_config(config_path)
    openapi = cfg["openapi"]
    asyncio_spec = cfg["asyncio"]
    features = cfg.get("features", {})
    output_dir = cfg.get("output", "build")

    agents = create_orchestrator(llm=llm)
    project = agents["coder"].generate_code(openapi, asyncio_spec, output_dir, features)
    verification = agents["verifier"].verify(project)
    tests = agents["tester"].test(project)
    summary = f"Verification:\n{verification}\nTest Results:\n{tests}"
    return summary
