#!/usr/bin/env python3
"""Supply chain guard checks for m0sh1.cc repos."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class Issue:
    severity: str
    message: str
    path: str | None = None


SKIP_DIRS = {".git", ".venv", ".terraform", "node_modules", ".cache"}


def should_skip(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    parts = path.parts
    if "docs" in parts and "archive" in parts:
        return True
    return False


def iter_files(root: Path, patterns: Iterable[str]) -> Iterable[Path]:
    for pattern in patterns:
        for path in root.rglob(pattern):
            if should_skip(path):
                continue
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text()
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def is_pinned_action(ref: str) -> bool:
    if "@" not in ref:
        return False
    _, version = ref.rsplit("@", 1)
    return bool(re.fullmatch(r"[0-9a-f]{40}", version))


def from_line_image(line: str) -> str | None:
    line = line.strip()
    if not line.startswith("FROM "):
        return None
    # Handle optional --platform flag
    parts = line.split()
    if len(parts) >= 3 and parts[1].startswith("--platform="):
        return parts[2]
    if len(parts) >= 2:
        return parts[1]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Supply chain guard checks")
    parser.add_argument("--repo", required=True, help="Path to repo")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    args = parser.parse_args()

    # Normalize the repository path and ensure it is contained within the current
    # working directory to avoid traversing arbitrary locations on the filesystem.
    root = Path.cwd().resolve()
    repo = Path(args.repo).resolve()
    try:
        # This will raise ValueError if repo is not under root.
        relative_repo = repo.relative_to(root)
        # Reconstruct repo to be explicitly rooted under the validated base path.
        repo = root / relative_repo
    except ValueError:
        print(f"Repo path must be inside the current working directory: {repo}", file=sys.stderr)
        return 2

    if not repo.exists():
        print(f"Repo path does not exist: {repo}", file=sys.stderr)
        return 2
    if not repo.is_dir():
        print(f"Repo path is not a directory: {repo}", file=sys.stderr)
        return 2

    issues: List[Issue] = []

    # CI workflow pinning (.github and .gitea)
    workflow_dirs = [repo / ".github" / "workflows", repo / ".gitea" / "workflows"]
    for workflows_dir in workflow_dirs:
        if not workflows_dir.exists():
            continue
        for wf in workflows_dir.rglob("*.yml"):
            text = read_text(wf)
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("uses:"):
                    ref = line.split("uses:", 1)[1].strip()
                    if ref.startswith("./") or ref.startswith("docker://"):
                        continue
                    if not is_pinned_action(ref):
                        issues.append(Issue("warning", f"Action not pinned to SHA: {ref}", str(wf)))

    # Dockerfiles/Containerfiles
    for df in iter_files(repo, ["Dockerfile", "Containerfile", "*.Dockerfile"]):
        text = read_text(df)
        for line in text.splitlines():
            image = from_line_image(line)
            if not image:
                continue
            if image == "scratch":
                continue
            if "@sha256:" not in image:
                issues.append(Issue("warning", f"Base image not pinned by digest: {image}", str(df)))

    # Helm values: repository + tag pattern
    for values in iter_files(repo, ["values.yaml", "values.yml"]):
        text = read_text(values)
        repo_name = None
        repo_indent = None
        for line in text.splitlines():
            if "repository:" in line:
                repo_indent = len(line) - len(line.lstrip(" "))
                repo_name = line.split("repository:", 1)[1].strip().strip('"')
            if repo_name is not None and "tag:" in line:
                tag_indent = len(line) - len(line.lstrip(" "))
                if repo_indent is not None and tag_indent == repo_indent:
                    tag = line.split("tag:", 1)[1].strip().strip('"')
                    if "sha256" not in tag and "@" not in tag:
                        issues.append(Issue("warning", f"Image tag not pinned by digest: {repo_name}:{tag}", str(values)))
                    repo_name = None
                    repo_indent = None

        # image: repo:tag pattern
        for line in text.splitlines():
            if re.search(r"\bimage:\s*", line):
                image = line.split("image:", 1)[1].strip().strip('"')
                if image and "@sha256:" not in image and ":" in image:
                    issues.append(Issue("warning", f"Image not pinned by digest: {image}", str(values)))

    # history.md presence
    history = repo / "docs" / "history.md"
    if not history.exists():
        issues.append(Issue("warning", "docs/history.md missing (used to document tag usage/exceptions)", str(history)))

    if args.json:
        payload = {"repo": str(repo), "issues": [issue.__dict__ for issue in issues]}
        print(json.dumps(payload, indent=2))
    else:
        if not issues:
            print("✅ Supply chain checks passed")
        else:
            print("Supply chain findings:")
            for issue in issues:
                loc = f" ({issue.path})" if issue.path else ""
                print(f"- [{issue.severity}] {issue.message}{loc}")
            print("\nReminder: document temporary tag usage or exceptions in docs/history.md")

    if args.strict and issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
