#!/usr/bin/env python3
"""
GitOps guard checks for m0sh1.cc infra repo.
"""

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
    severity: str  # "error" | "warning"
    message: str
    path: str | None = None


SKIP_DIRS = {".git", ".venv", ".terraform", "node_modules", ".cache"}


def should_skip(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    parts = path.parts
    if "docs" in parts and "archive" in parts:
        return True
    for idx, part in enumerate(parts[:-1]):
        if part == "cluster" and parts[idx + 1] == "bootstrap":
            return True
    return False


def iter_yaml_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.yml"):
        if should_skip(path):
            continue
        yield path
    for path in root.rglob("*.yaml"):
        if should_skip(path):
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text()
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def is_application(text: str) -> bool:
    return re.search(r"(?m)^kind:\s*Application(Set)?\b", text) is not None


def has_label_value(text: str, label: str, value: str) -> bool:
    pattern = rf"(?m)^\s*{re.escape(label)}:\s*{re.escape(value)}\b"
    return re.search(pattern, text) is not None


def is_argocd_application_path(path: Path) -> bool:
    parts = path.parts
    if "apps" not in parts:
        return False
    try:
        idx = parts.index("apps")
    except ValueError:
        return False
    return parts[idx : idx + 3] in (("apps", "argocd", "applications"), ("apps", "argocd", "disabled"))


def main() -> int:
    parser = argparse.ArgumentParser(description="GitOps guard checks for m0sh1.cc infra repo")
    parser.add_argument("--repo", required=True, help="Path to infra repo")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    args = parser.parse_args()

    base = Path.cwd().resolve()
    repo_arg = Path(args.repo)
    if repo_arg.is_absolute():
        print(f"Repo path must be relative, got absolute path: {repo_arg}", file=sys.stderr)
        return 2
    repo_candidate = (base / repo_arg).resolve()
    try:
        repo_candidate.relative_to(base)
    except ValueError:
        print(f"Repo path must be within {base}, got: {repo_candidate}", file=sys.stderr)
        return 2
    repo = repo_candidate

    if not repo.exists():
        print(f"Repo path does not exist: {repo}", file=sys.stderr)
        return 2

    issues: List[Issue] = []

    # App layout check
    apps_dir = repo / "apps"
    if apps_dir.exists():
        allowed = {"cluster", "user", "argocd"}
        for child in apps_dir.iterdir():
            if child.is_dir() and child.name not in allowed:
                issues.append(Issue("error", f"Unexpected apps/ child directory: {child.name}", str(child)))

    # Environment overlays
    env_root = repo / "cluster" / "environments"
    if env_root.exists():
        for child in env_root.iterdir():
            if child.is_dir() and child.name != "lab":
                issues.append(Issue("error", f"Unexpected environment overlay: {child.name}", str(child)))

    for path in iter_yaml_files(repo):
        text = read_text(path)

        # Skip empty files
        if not text.strip():
            continue

        # Skip sealedsecret manifests for Secret check
        has_sealed = re.search(r"(?m)^kind:\s*SealedSecret\b", text) is not None

        # Secret vs SealedSecret
        if re.search(r"(?m)^kind:\s*Secret\b", text) and not has_sealed:
            issues.append(Issue("error", "Plain Secret found; use SealedSecrets", str(path)))

        # Skip-reconcile annotation
        if "argocd.argoproj.io/skip-reconcile" in text:
            issues.append(Issue("warning", "skip-reconcile annotation present (recovery-only)", str(path)))

        # ArgoCD Application checks
        if is_application(text):
            if not is_argocd_application_path(path):
                issues.append(Issue("error", "ArgoCD Application manifest outside apps/argocd/{applications,disabled}", str(path)))

            if not has_label_value(text, "app.kubernetes.io/part-of", "apps-root"):
                issues.append(
                    Issue("error", "ArgoCD Application missing app.kubernetes.io/part-of: apps-root label", str(path))
                )

            if re.search(r"(?m)^\s*chart:\s*\S+", text):
                issues.append(Issue("error", "ArgoCD Application uses chart: (direct Helm repo); use wrapper chart path", str(path)))

    # Report
    if args.json:
        payload = {
            "repo": str(repo),
            "issues": [issue.__dict__ for issue in issues],
        }
        print(json.dumps(payload, indent=2))
    else:
        if not issues:
            print("✅ No GitOps issues detected")
        else:
            print("GitOps issues:")
            for issue in issues:
                loc = f" ({issue.path})" if issue.path else ""
                print(f"- [{issue.severity}] {issue.message}{loc}")

    if any(i.severity == "error" for i in issues):
        return 1
    if args.strict and issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
