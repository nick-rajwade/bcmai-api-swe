import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.orchestrator import run_workflow


def test_run_workflow(tmp_path):
    cfg_data = open("config.yaml").read()
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(cfg_data + f"\noutput: {tmp_path/'build'}\n")
    summary = run_workflow(str(cfg_path), llm=None)
    assert "Verification" in summary
    assert "Test Results" in summary
