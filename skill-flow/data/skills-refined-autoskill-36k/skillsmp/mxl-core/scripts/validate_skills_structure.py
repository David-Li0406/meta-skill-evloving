#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class SkillMeta:
    name: str
    description: str


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "skills").is_dir() and (candidate / "projects").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate repo root (missing skills/ and projects/)")


def _parse_frontmatter(text: str) -> Optional[SkillMeta]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("Missing closing '---' for YAML frontmatter")

    name = ""
    description = ""
    for raw in lines[1:end_idx]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "name":
            name = value
        elif key == "description":
            description = value

    if not name or not description:
        raise ValueError("Frontmatter must include non-empty 'name' and 'description'")
    return SkillMeta(name=name, description=description)


def main(argv: list[str]) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    skills_dir = repo_root / "skills"

    errors: list[str] = []
    for path in sorted(skills_dir.iterdir()):
        if not path.is_dir():
            continue
        if path.name in {"resources"}:
            continue
        skill_md = path / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            meta = _parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            if meta is None:
                errors.append(f"{skill_md}: missing YAML frontmatter")
                continue
            if not meta.description.lower().startswith("this skill should be used when"):
                errors.append(
                    f"{skill_md}: description should start with "
                    f"'This skill should be used when...'"
                )
        except Exception as exc:
            errors.append(f"{skill_md}: {exc}")

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
