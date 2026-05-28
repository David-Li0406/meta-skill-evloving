#!/usr/bin/env python3
"""
Generate a sanitized, repo-local audit snapshot for governance reviews.

- Uses only Python stdlib.
- Avoids printing file contents or potential secrets.
- Focuses on inventory and workflow safety signals.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
}


def _run(cmd: List[str], cwd: Path) -> Optional[str]:
    try:
        out = subprocess.check_output(cmd, cwd=str(cwd), stderr=subprocess.STDOUT, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return out.strip()


def _walk_files(repo: Path, target_name: str) -> List[str]:
    matches: List[str] = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        if target_name in files:
            matches.append(str(Path(root, target_name).relative_to(repo)))
    return sorted(matches)


def _check_presence(repo: Path, candidates: List[str]) -> Dict[str, bool]:
    out: Dict[str, bool] = {}
    for rel in candidates:
        out[rel] = (repo / rel).exists()
    return out


def _workflow_signals(text: str) -> Dict[str, Any]:
    uses = re.findall(r"(?m)^\\s*uses:\\s*([^\\s#]+)", text)
    uses = [u.strip() for u in uses if u.strip()]
    unpinned: List[str] = []
    pinned: List[str] = []
    for u in uses:
        if u.startswith("./") or u.startswith("../"):
            pinned.append(u)
            continue
        if "@" not in u:
            unpinned.append(u)
            continue
        _, ref = u.rsplit("@", 1)
        if re.fullmatch(r"[0-9a-fA-F]{40}", ref):
            pinned.append(u)
        else:
            unpinned.append(u)

    return {
        "has_permissions": bool(re.search(r"(?m)^\\s*permissions\\s*:", text)),
        "has_write_all": bool(re.search(r"(?m)^\\s*permissions\\s*:\\s*write-all\\s*$", text)),
        "has_pull_request_target": "pull_request_target" in text,
        "has_curl_pipe_shell": bool(re.search(r"curl[^\\n]*\\|\\s*(bash|sh)\\b", text)),
        "has_wget_pipe_shell": bool(re.search(r"wget[^\\n]*\\|\\s*(bash|sh)\\b", text)),
        "uses_count": len(uses),
        "uses_unpinned_count": len(unpinned),
        "uses_unpinned_sample": sorted(set(unpinned))[:25],
        "uses_pinned_count": len(pinned),
    }


def build_snapshot(repo: Path) -> Dict[str, Any]:
    repo = repo.resolve()

    snapshot: Dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo),
        "git": {},
        "instruction_files": {},
        "workflows": {"path": None, "files": []},
        "project_files": {},
        "github": {},
    }

    # Git context (best-effort)
    if (repo / ".git").exists():
        snapshot["git"] = {
            "branch": _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo),
            "commit": _run(["git", "rev-parse", "HEAD"], cwd=repo),
            "status_porcelain": _run(["git", "status", "--porcelain"], cwd=repo),
        }

    # Instruction files
    snapshot["instruction_files"] = {
        "AGENTS.md": _walk_files(repo, "AGENTS.md"),
        "CONTRIBUTING.md": _walk_files(repo, "CONTRIBUTING.md"),
        "SECURITY.md": _walk_files(repo, "SECURITY.md"),
    }

    # Common project files (root or conventional locations)
    snapshot["project_files"] = _check_presence(
        repo,
        [
            "README.md",
            "LICENSE",
            "pyproject.toml",
            "requirements.txt",
            "requirements-dev.txt",
            ".editorconfig",
            ".pre-commit-config.yaml",
            "Dockerfile",
            "docker-compose.yml",
            "Makefile",
            ".github/dependabot.yml",
            ".github/CODEOWNERS",
            "CODEOWNERS",
        ],
    )

    # GitHub directory quick checks
    snapshot["github"] = _check_presence(
        repo,
        [
            ".github/workflows",
            ".github/workflows/deploy.yml",
            ".github/workflows/run_tests.yml",
        ],
    )

    workflows_dir = repo / ".github" / "workflows"
    if workflows_dir.exists() and workflows_dir.is_dir():
        workflow_files = sorted(
            [p for p in workflows_dir.glob("*.yml")] + [p for p in workflows_dir.glob("*.yaml")]
        )
        snapshot["workflows"]["path"] = str(workflows_dir.relative_to(repo))
        for wf in workflow_files:
            try:
                text = wf.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            snapshot["workflows"]["files"].append(
                {
                    "path": str(wf.relative_to(repo)),
                    "signals": _workflow_signals(text),
                }
            )

    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a repo audit snapshot (sanitized).")
    parser.add_argument("--repo", default=".", help="Path to repo root (default: .)")
    parser.add_argument("--out", default=None, help="Write JSON output to this path (default: stdout)")
    args = parser.parse_args()

    snapshot = build_snapshot(Path(args.repo))
    encoded = json.dumps(snapshot, indent=2, sort_keys=True)

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(encoded + "\n", encoding="utf-8")
        print(f"Wrote audit snapshot: {out_path}")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
