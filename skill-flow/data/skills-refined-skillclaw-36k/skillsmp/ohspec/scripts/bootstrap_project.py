#!/usr/bin/env python3
"""
Bootstrap OHSpec project-local tooling.

Why:
  - Keep repo-local, stable paths for scripts/templates:
      .ohspec/scripts/*.py
      .ohspec/templates/*
  - Avoid depending on where the skill is installed (~/.codex vs ~/.claude).
  - Use a tool-agnostic directory (`.ohspec`) so different models/runners share the same artifacts.

What it does:
  - Creates .ohspec/{scripts,templates}
  - Optionally also creates legacy .claude/ohspec/{scripts,templates} (for backward compatibility)
  - Copies selected files from this skill repo into the target project

Usage:
  python3 scripts/bootstrap_project.py --project-root /path/to/repo
  python3 scripts/bootstrap_project.py   # defaults to git root or cwd
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SCRIPT_FILES = [
    "export_digest.py",
    "precheck_rfc.py",
]

TEMPLATE_FILES = [
    "rfc.md",
    "rfc-minimal.md",
    "findings.json",
    "progress.json",
]


def detect_project_root() -> Path:
    # Best-effort repo root without invoking git (works better on Windows / non-git environments).
    cur = Path.cwd().resolve()
    for p in [cur, *cur.parents]:
        if (p / ".git").exists():
            return p
    return cur


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Bootstrap .ohspec scripts/templates into a project")
    ap.add_argument("--project-root", default=None, help="target project root (default: git root or cwd)")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument(
        "--also-legacy-claude",
        action="store_true",
        help="also write legacy paths under .claude/ohspec/ (backward compatibility)",
    )
    args = ap.parse_args(argv)

    skill_root = Path(__file__).resolve().parents[1]
    project_root = Path(args.project_root).resolve() if args.project_root else detect_project_root()

    def copy_into(dst_base: Path) -> tuple[list[str], list[str]]:
        dst_scripts = dst_base / "scripts"
        dst_templates = dst_base / "templates"

        dst_scripts.mkdir(parents=True, exist_ok=True)
        dst_templates.mkdir(parents=True, exist_ok=True)

        copied: list[str] = []
        skipped: list[str] = []

        for name in SCRIPT_FILES:
            src = skill_root / "scripts" / name
            dst = dst_scripts / name
            if dst.exists() and not args.force:
                skipped.append(str(dst))
                continue
            shutil.copy2(src, dst)
            copied.append(str(dst))

        for name in TEMPLATE_FILES:
            src = skill_root / "templates" / name
            dst = dst_templates / name
            if dst.exists() and not args.force:
                skipped.append(str(dst))
                continue
            shutil.copy2(src, dst)
            copied.append(str(dst))

        return copied, skipped

    copied = []
    skipped = []

    # Preferred: tool-agnostic OHSpec home
    c1, s1 = copy_into(project_root / ".ohspec")
    copied.extend(c1)
    skipped.extend(s1)

    # Legacy: keep old layout working if requested or already present.
    legacy_base = project_root / ".claude" / "ohspec"
    if args.also_legacy_claude or legacy_base.exists():
        c2, s2 = copy_into(legacy_base)
        copied.extend(c2)
        skipped.extend(s2)

    print(f"project_root: {project_root}")
    for p in copied:
        print(f"copied: {p}")
    for p in skipped:
        print(f"skipped: {p}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
