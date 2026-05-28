#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an MCP LSP config for this repo (Pyright LSP).")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Path to the repo root.")
    parser.add_argument("--out", type=Path, default=Path(".codex/lsp.json"), help="Output path for lsp.json.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    out_path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "servers": {
            "python": {
                "command": "pyright-langserver",
                "args": ["--stdio"],
                "extensions": [".py"],
                "projects": [
                    {
                        "name": "OpenEvent-AI",
                        "description": "OpenEvent AI backend",
                        "path": str(repo_root),
                        "patterns": {
                            "exclude": [
                                "**/.git/**",
                                "**/.venv/**",
                                "**/venv/**",
                                "**/node_modules/**",
                                "**/tmp-*/**",
                                "**/tmp/**",
                                "**/.playwright-mcp/**",
                            ]
                        },
                    }
                ],
                "configuration": {
                    "settings": {
                        "python": {
                            "analysis": {
                                "autoSearchPaths": True,
                                "diagnosticMode": "workspace",
                            }
                        }
                    }
                },
            }
        }
    }

    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

