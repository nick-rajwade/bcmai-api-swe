"""Minimal parsers for YAML-like spec files."""
from __future__ import annotations

from typing import Dict, List


def parse_openapi_paths(path: str) -> Dict[str, List[str]]:
    """Return mapping of path -> methods."""
    result: Dict[str, List[str]] = {}
    current_path: str | None = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if stripped.startswith('/') and stripped.endswith(':'):
                current_path = stripped[:-1]
                result[current_path] = []
            elif current_path and stripped.endswith(':'):
                method = stripped[:-1]
                result[current_path].append(method)
    return result


def parse_asyncio_operations(path: str) -> Dict[str, str]:
    ops: Dict[str, str] = {}
    current_op = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if not stripped.startswith(' '):
                if stripped.endswith(':'):
                    current_op = stripped[:-1]
            elif current_op and 'topic:' in stripped:
                topic = stripped.split(':', 1)[1].strip()
                ops[current_op] = topic
    return ops


def load_config(path: str) -> Dict[str, object]:
    """Very small YAML-like config parser."""
    cfg: Dict[str, object] = {}
    current_map: Dict[str, object] | None = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if value == "":
                    current_map = {}
                    cfg[key] = current_map
                else:
                    if value.lower() == "true":
                        val: object = True
                    elif value.lower() == "false":
                        val = False
                    else:
                        val = value
                    if line.startswith("  ") and current_map is not None:
                        current_map[key] = val
                    else:
                        cfg[key] = val
                        current_map = None
            else:
                continue
    return cfg
