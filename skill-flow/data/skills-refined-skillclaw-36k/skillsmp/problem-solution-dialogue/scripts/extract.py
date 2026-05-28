#!/usr/bin/env python3
"""
Skill-local extraction/validation helper.

This repository doesn't rely on any external tooling for skill packaging, so this
script intentionally stays lightweight:
1) Ensures required companion files exist.
2) Validates that SKILL.md file references are relative and not deeply nested.

Run from the skill root:
  python3 scripts/extract.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


SKILL_MD = Path("SKILL.md")
REQUIRED_FILES = [
    Path("context-clarifier.md"),
    Path("references/REFERENCE.md"),
    Path("references/red-flags.md"),
]


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def warn(msg: str) -> None:
    print(f"WARN: {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(msg)


def iter_markdown_links(md: str) -> list[str]:
    # Matches standard markdown links: [text](path)
    return [m.group(1).strip() for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", md)]


def validate_relative_one_level(paths: list[str]) -> None:
    for p in paths:
        # Ignore web URLs and anchors.
        if "://" in p or p.startswith("#"):
            continue
        # Ignore mailto links.
        if p.startswith("mailto:"):
            continue

        # Must be relative (no leading slash, no drive letter).
        if p.startswith("/") or re.match(r"^[A-Za-z]:\\\\", p):
            die(f"non-relative link in SKILL.md: {p}")

        # Keep references one level deep from SKILL.md.
        # Allowed: "foo.md" or "dir/foo.md"
        parts = [x for x in p.split("/") if x and x != "."]
        if len(parts) > 2:
            die(f"link too deep (keep one level deep): {p}")


def main() -> None:
    if not SKILL_MD.exists():
        die("SKILL.md not found (run from the skill root)")

    missing = [str(p) for p in REQUIRED_FILES if not p.exists()]
    if missing:
        die(f"missing required files: {', '.join(missing)}")

    md = SKILL_MD.read_text(encoding="utf-8")
    links = iter_markdown_links(md)
    validate_relative_one_level(links)

    # Soft check: avoid calling the local doc "context-clarifier" a sub-skill.
    for line in md.splitlines():
        if "context-clarifier" in line and "必需子技能" in line:
            warn("SKILL.md calls context-clarifier a sub-skill; prefer '必需参考'.")
            break

    info("OK: required files present; SKILL.md links are relative and one-level deep.")


if __name__ == "__main__":
    main()
