#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


REQUIRED_RELATIVE_PATHS = [
    "SKILL.md",
    "references/quickstart.md",
    "references/INDEX.md",
    "references/Operational_Contract.md",
    "references/Scribe_Usage.md",
    "references/Scribe_Usage.upstream.md",
    "references/manage_docs.md",
    "references/read_file.md",
    "references/projects.md",
    "references/querying.md",
    "references/files.md",
    "references/docs_management.md",
    "references/maintenance.md",
    "references/modes.md",
    "references/logging.md",
    "references/doc_naming.md",
    "references/sentinel_cases.md",
    "references/troubleshooting.md",
    "references/sections/INDEX.md",
]


def _skill_root_from_here() -> Path:
    # .../.codex/skills/scribe-mcp-usage/scripts/validate_skill.py
    return Path(__file__).resolve().parents[1]


def _repo_root_from_here() -> Path:
    # .../.codex/skills/scribe-mcp-usage/scripts/validate_skill.py
    return Path(__file__).resolve().parents[4]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate scribe-mcp-usage skill layout.")
    parser.add_argument("--skill-root", default=None, help="Override skill root (defaults to auto-detect).")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="If provided (or auto-detected), verify references/Scribe_Usage.md matches docs/Scribe_Usage.md.",
    )
    args = parser.parse_args()

    root = Path(args.skill_root).expanduser().resolve() if args.skill_root else _skill_root_from_here()
    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else _repo_root_from_here()
    problems: list[str] = []

    for rel in REQUIRED_RELATIVE_PATHS:
        path = root / rel
        if not path.exists():
            problems.append(f"missing: {rel}")

    if (root / "SKILL.md").exists():
        lines = (root / "SKILL.md").read_text(encoding="utf-8").splitlines()
        if len(lines) > 500:
            problems.append(f"SKILL.md too long: {len(lines)} lines (target < 500)")

        if not any("references/" in line for line in lines):
            problems.append("SKILL.md missing navigation to references/")

    repo_usage = repo_root / "docs" / "Scribe_Usage.md"
    skill_usage_upstream = root / "references" / "Scribe_Usage.upstream.md"
    if repo_usage.exists() and skill_usage_upstream.exists():
        repo_hash = hashlib.sha256(repo_usage.read_bytes()).hexdigest()
        skill_hash = hashlib.sha256(skill_usage_upstream.read_bytes()).hexdigest()
        if repo_hash != skill_hash:
            problems.append(
                "references/Scribe_Usage.upstream.md does not match docs/Scribe_Usage.md (run scripts/sync_from_repo.py)"
            )

    if problems:
        print("FAIL")
        for item in problems:
            print(f"- {item}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
