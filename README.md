# Multi-Agent API Development Framework

This repository implements a multi-agent architecture for generating
microservice APIs from OpenAPI and AsyncIO specifications. The agents follow a
LangGraph inspired workflow and demonstrate the Demeter principle of
responsibility. Generated services support REST endpoints with optional
observability via OpenTelemetry and Prometheus.

## Architecture

- **CoderAgent** – Generates API code from input specifications.
- **VerifierAgent** – Reviews generated code for quality and correctness.
- **TesterAgent** – Executes code in a sandbox and reports test results.
- **Orchestrator** – Connects the agents in a workflow similar to LangGraph
  graphs and manages short/long term memory.

Short‑term memory is stored in memory while long‑term memory persists to disk.
The `config.yaml` file specifies which features to enable when generating a new
service.

## Running the Workflow

The workflow is started from a configuration file containing the input specs and
feature flags. Execute:

```bash
python -c "from agents.orchestrator import run_workflow; print(run_workflow('config.yaml'))"
```

## Tests

Run the tests using `pytest`:

```bash
pytest -q
```
