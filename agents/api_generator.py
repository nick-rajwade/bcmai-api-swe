"""Generate FastAPI projects from specs."""
from __future__ import annotations

import os
from typing import Dict, Any

from .spec_parser import parse_openapi_paths


TEMPLATE_MAIN = """\
from fastapi import FastAPI, Depends

app = FastAPI()

{observability}

{routes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

ROUTE_TEMPLATE = """\n@app.{method}(\"{path}\")\nasync def {func_name}():\n    return {{"message": \"not implemented\"}}\n"""

OBSERVABILITY_TEMPLATE = """\ntry:\n    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor\n    FastAPIInstrumentor().instrument_app(app)\nexcept Exception:\n    pass\ntry:\n    from prometheus_fastapi_instrumentator import Instrumentator\n    Instrumentator().instrument(app).expose(app)\nexcept Exception:\n    pass\n"""

TEST_TEMPLATE = """\
from fastapi.testclient import TestClient
from generated_api.main import app

client = TestClient(app)

def test_root():
    response = client.get("{first_path}")
    assert response.status_code == 200
"""


def sanitize(name: str) -> str:
    return name.replace('/', '_').replace('{', '').replace('}', '').strip('_')


def generate_fastapi_app(openapi_path: str, asyncio_path: str, output_dir: str, features: Dict[str, Any]) -> str:
    """Generate a FastAPI project from OpenAPI and AsyncIO specs."""
    paths = parse_openapi_paths(openapi_path)
    os.makedirs(output_dir, exist_ok=True)
    routes_code = []
    first_path = None
    for path, methods in paths.items():
        if first_path is None:
            first_path = path
        for method in methods:
            func_name = sanitize(f"{method}_{path}")
            routes_code.append(ROUTE_TEMPLATE.format(method=method, path=path, func_name=func_name))
    routes = "\n".join(routes_code)
    observability = OBSERVABILITY_TEMPLATE if features.get("observability") else ""
    main_py = TEMPLATE_MAIN.format(observability=observability, routes=routes)
    gen_dir = os.path.join(output_dir, "generated_api")
    os.makedirs(gen_dir, exist_ok=True)
    with open(os.path.join(gen_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")
    with open(os.path.join(gen_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_py)
    tests_dir = os.path.join(gen_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, "test_app.py"), "w", encoding="utf-8") as f:
        f.write(TEST_TEMPLATE.format(first_path=first_path or "/"))
    return gen_dir
