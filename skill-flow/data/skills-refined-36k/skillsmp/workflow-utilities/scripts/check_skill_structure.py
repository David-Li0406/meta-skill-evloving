#!/usr/bin/env python3
"""Pre-commit hook: Verify skill directory structure."""

import sys
from pathlib import Path


def main() -> int:
    """Check all skills have required files."""
    required_files = ["CLAUDE.md", "README.md", "SKILL.md"]
    skills_dir = Path(".claude/skills")

    if not skills_dir.exists():
        return 0

    errors = []
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith(".") or skill_dir.name == "__pycache__":
            continue
        for required in required_files:
            if not (skill_dir / required).exists():
                errors.append(f"{skill_dir.name}: missing {required}")

    if errors:
        print("Skill directory structure violations:")
        for e in errors:
            print(f"  - {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
