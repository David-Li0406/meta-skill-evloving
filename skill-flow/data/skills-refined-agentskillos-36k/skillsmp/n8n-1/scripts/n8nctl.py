#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.27",
# ]
# ///
"""
n8nctl - Minimal REST CLI for n8n workflow authoring.

Usage:
  n8nctl.py list [--limit N] [--active true|false]
  n8nctl.py get <workflow-id>
  n8nctl.py create <workflow.json>
  n8nctl.py update <workflow-id> <workflow.json>
  n8nctl.py export <workflow-id> <out.json>
  n8nctl.py activate <workflow-id>
  n8nctl.py deactivate <workflow-id>
  n8nctl.py mcp-enable <workflow-id>
  n8nctl.py validate <workflow.json>

Environment:
  N8N_BASE_URL   Base URL like http://localhost:5678
  N8N_API_KEY    API key for X-N8N-API-KEY header
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


@dataclass(frozen=True)
class Config:
    base_url: str
    api_key: str


class N8nError(Exception):
    """Base error for n8nctl."""


def _fail(msg: str) -> None:
    print(f"n8nctl: {msg}", file=sys.stderr)
    raise SystemExit(2)


def _require_env(name: str, value: str | None) -> str:
    if value is None or value.strip() == "":
        _fail(f"missing required env var: {name}")
    return value


def load_config(args: argparse.Namespace) -> Config:
    base_url = args.base_url or os.getenv("N8N_BASE_URL")
    api_key = args.api_key or os.getenv("N8N_API_KEY")
    return Config(
        base_url=_require_env("N8N_BASE_URL", base_url).rstrip("/"),
        api_key=_require_env("N8N_API_KEY", api_key),
    )


def _headers(cfg: Config) -> dict[str, str]:
    return {"X-N8N-API-KEY": cfg.api_key}


def _request(
    cfg: Config,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{cfg.base_url}{path}"
    headers = _headers(cfg)
    if body is not None:
        headers["Content-Type"] = "application/json"
    with httpx.Client(timeout=30.0) as client:
        resp = client.request(method, url, params=params, json=body, headers=headers)
    if resp.is_error:
        _fail(f"HTTP {resp.status_code} {resp.reason_phrase}: {resp.text}")
    return resp.json()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        _fail(f"failed to read {path}: {exc}")
    except json.JSONDecodeError as exc:
        _fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        _fail(f"expected JSON object in {path}")
    return data


def _require_workflow_fields(data: dict[str, Any], path: Path) -> dict[str, Any]:
    missing = [key for key in ("name", "nodes", "connections", "settings") if key not in data]
    if missing:
        _fail(f"workflow JSON missing keys {missing} in {path}")
    return data


def _workflow_payload(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": data.get("name"),
        "nodes": data.get("nodes"),
        "connections": data.get("connections"),
        "settings": data.get("settings"),
    }


def _validate_workflow_data(data: dict[str, Any], path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    for key in ("name", "nodes", "connections", "settings"):
        if key not in data:
            errors.append(f"missing key: {key}")
    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings}

    nodes = data.get("nodes")
    connections = data.get("connections")
    settings = data.get("settings")
    if not isinstance(nodes, list):
        errors.append("nodes must be a list")
        return {"valid": False, "errors": errors, "warnings": warnings}
    if not isinstance(connections, dict):
        errors.append("connections must be an object")
    if not isinstance(settings, dict):
        errors.append("settings must be an object")

    names: list[str] = []
    for idx, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"nodes[{idx}] must be an object")
            continue
        name = node.get("name")
        node_type = node.get("type")
        if not isinstance(name, str) or name.strip() == "":
            errors.append(f"nodes[{idx}].name must be a non-empty string")
        else:
            if name in names:
                errors.append(f"duplicate node name: {name}")
            names.append(name)
        if not isinstance(node_type, str) or node_type.strip() == "":
            errors.append(f"nodes[{idx}].type must be a non-empty string")

    name_set = set(names)
    if isinstance(connections, dict):
        for src_name, src_conn in connections.items():
            if src_name not in name_set:
                warnings.append(f"connection source not in nodes: {src_name}")
            if not isinstance(src_conn, dict):
                warnings.append(f"connection for {src_name} is not an object")
                continue
            main = src_conn.get("main")
            if not isinstance(main, list):
                warnings.append(f"connection {src_name}.main is not a list")
                continue
            for branch in main:
                if not isinstance(branch, list):
                    warnings.append(f"connection {src_name}.main branch is not a list")
                    continue
                for edge in branch:
                    if not isinstance(edge, dict):
                        warnings.append(f"connection {src_name} edge is not an object")
                        continue
                    target = edge.get("node")
                    if isinstance(target, str) and target not in name_set:
                        errors.append(f"connection from {src_name} to missing node: {target}")

    if isinstance(settings, dict):
        if "availableInMCP" in settings and not isinstance(settings["availableInMCP"], bool):
            warnings.append("settings.availableInMCP should be boolean")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "path": str(path)}


def cmd_list(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.active is not None:
        params["active"] = args.active
    return _request(cfg, "GET", "/api/v1/workflows", params=params)


def cmd_get(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    return _request(cfg, "GET", f"/api/v1/workflows/{args.workflow_id}")


def cmd_create(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    payload = _workflow_payload(_require_workflow_fields(_load_json(args.path), args.path))
    return _request(cfg, "POST", "/api/v1/workflows", body=payload)


def cmd_update(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    payload = _workflow_payload(_require_workflow_fields(_load_json(args.path), args.path))
    return _request(cfg, "PUT", f"/api/v1/workflows/{args.workflow_id}", body=payload)


def cmd_export(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    data = _request(cfg, "GET", f"/api/v1/workflows/{args.workflow_id}")
    args.out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"saved": str(args.out)}


def cmd_activate(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    return _request(cfg, "POST", f"/api/v1/workflows/{args.workflow_id}/activate")


def cmd_deactivate(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    return _request(cfg, "POST", f"/api/v1/workflows/{args.workflow_id}/deactivate")


def cmd_mcp_enable(cfg: Config, args: argparse.Namespace) -> dict[str, Any]:
    wf = _request(cfg, "GET", f"/api/v1/workflows/{args.workflow_id}")
    settings = dict(wf.get("settings") or {})
    settings["availableInMCP"] = True
    payload = _workflow_payload(
        {
            "name": wf.get("name"),
            "nodes": wf.get("nodes"),
            "connections": wf.get("connections"),
            "settings": settings,
        }
    )
    return _request(cfg, "PUT", f"/api/v1/workflows/{args.workflow_id}", body=payload)


def cmd_validate(_: Config | None, args: argparse.Namespace) -> dict[str, Any]:
    data = _load_json(args.path)
    return _validate_workflow_data(data, args.path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="n8nctl - minimal REST CLI")
    parser.add_argument("--base-url", help="override N8N_BASE_URL")
    parser.add_argument("--api-key", help="override N8N_API_KEY")

    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="list workflows")
    list_p.add_argument("--limit", type=int)
    list_p.add_argument("--active", choices=["true", "false"])

    get_p = sub.add_parser("get", help="get workflow by id")
    get_p.add_argument("workflow_id")

    create_p = sub.add_parser("create", help="create workflow from JSON")
    create_p.add_argument("path", type=Path)

    update_p = sub.add_parser("update", help="update workflow from JSON")
    update_p.add_argument("workflow_id")
    update_p.add_argument("path", type=Path)

    export_p = sub.add_parser("export", help="export workflow JSON")
    export_p.add_argument("workflow_id")
    export_p.add_argument("out", type=Path)

    activate_p = sub.add_parser("activate", help="activate workflow")
    activate_p.add_argument("workflow_id")

    deactivate_p = sub.add_parser("deactivate", help="deactivate workflow")
    deactivate_p.add_argument("workflow_id")

    mcp_p = sub.add_parser("mcp-enable", help="enable MCP access for workflow")
    mcp_p.add_argument("workflow_id")

    validate_p = sub.add_parser("validate", help="validate workflow JSON")
    validate_p.add_argument("path", type=Path)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    handlers = {
        "list": cmd_list,
        "get": cmd_get,
        "create": cmd_create,
        "update": cmd_update,
        "export": cmd_export,
        "activate": cmd_activate,
        "deactivate": cmd_deactivate,
        "mcp-enable": cmd_mcp_enable,
        "validate": cmd_validate,
    }

    handler = handlers[args.command]
    cfg: Config | None = None
    if args.command != "validate":
        cfg = load_config(args)
    result = handler(cfg, args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
