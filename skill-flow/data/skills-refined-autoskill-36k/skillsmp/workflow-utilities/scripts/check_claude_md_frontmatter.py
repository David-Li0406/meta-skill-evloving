#!/usr/bin/env python3
"""Pre-commit hook: Check CLAUDE.md files have YAML frontmatter."""

import sys
from pathlib import Path


def main() -> int:
    """Check all CLAUDE.md files for YAML frontmatter."""
    errors = []
    for f in Path(".").rglob("CLAUDE.md"):
        # Skip .agents/ (synced from .claude/)
        if ".agents/" in str(f):
            continue
        content = f.read_text()
        # Root CLAUDE.md and skill CLAUDE.md should have frontmatter
        if not content.startswith("---"):
            errors.append(str(f))

    if errors:
        print("CLAUDE.md files missing YAML frontmatter:")
        for e in errors:
            print(f"  - {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
