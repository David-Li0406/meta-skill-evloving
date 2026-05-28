#!/usr/bin/env python3
"""Terraform lab guard checks for m0sh1.cc infra repo."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Issue:
    severity: str
    message: str
    path: str | None = None


def read_text(path: Path) -> str:
    try:
        return path.read_text()
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def main() -> int:
    parser = argparse.ArgumentParser(description="Terraform lab guard")
    parser.add_argument("--repo", required=True, help="Path to infra repo")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    terraform_dir = repo / "terraform"
    envs_dir = terraform_dir / "envs"
    lab_dir = envs_dir / "lab"

    if not terraform_dir.exists():
        print(f"terraform/ not found in {repo}", file=sys.stderr)
        return 2

    issues: List[Issue] = []

    # Environment overlays
    if envs_dir.exists():
        for child in envs_dir.iterdir():
            if child.is_dir() and child.name != "lab":
                issues.append(Issue("error", f"Unexpected terraform env: {child.name}", str(child)))
    else:
        issues.append(Issue("error", "terraform/envs directory missing", str(envs_dir)))

    # Required files
    for filename in ["providers.tf", "versions.tf", "defaults.auto.tfvars", "secrets.auto.tfvars"]:
        if not (lab_dir / filename).exists():
            issues.append(Issue("error", f"Missing {filename} in terraform/envs/lab", str(lab_dir / filename)))

    # Provider/backend blocks outside envs/lab
    for tf in terraform_dir.rglob("*.tf"):
        if lab_dir in tf.parents:
            continue
        text = read_text(tf)
        if re.search(r"(?m)^\s*provider\s+\"", text):
            issues.append(Issue("error", "provider block outside envs/lab", str(tf)))
        if re.search(r"(?m)^\s*backend\s+\"", text):
            issues.append(Issue("error", "backend block outside envs/lab", str(tf)))

    # Module sources in envs/lab
    for tf in lab_dir.rglob("*.tf"):
        if tf.name in {"versions.tf", "providers.tf"}:
            continue
        text = read_text(tf)
        for match in re.finditer(r"(?m)^\s*source\s*=\s*\"([^\"]+)\"", text):
            source = match.group(1)
            if not (
                source.startswith("./modules/")
                or source.startswith("../modules/")
                or source.startswith("../../modules/")
            ):
                issues.append(Issue("warning", f"Module source not under terraform/modules: {source}", str(tf)))

    if args.json:
        payload = {
            "repo": str(repo),
            "issues": [issue.__dict__ for issue in issues],
        }
        print(json.dumps(payload, indent=2))
    else:
        if not issues:
            print("✅ Terraform lab checks passed")
        else:
            print("Terraform lab issues:")
            for issue in issues:
                loc = f" ({issue.path})" if issue.path else ""
                print(f"- [{issue.severity}] {issue.message}{loc}")

        print("\nStandard workflow:")
        print("export $(cat terraform/op.env | xargs)")
        print("terraform -chdir=terraform fmt -recursive")
        print("terraform -chdir=terraform/envs/lab init -backend=false")
        print("terraform -chdir=terraform/envs/lab validate")
        print("terraform -chdir=terraform/envs/lab plan -var-file=defaults.auto.tfvars -var-file=secrets.auto.tfvars")

    if any(i.severity == "error" for i in issues):
        return 1
    if args.strict and issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
