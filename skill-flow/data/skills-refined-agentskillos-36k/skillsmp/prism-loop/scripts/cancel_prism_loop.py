#!/usr/bin/env python3
"""
Cancel PRISM Workflow Loop - removes state file to stop the workflow.
"""

import sys
import re
from pathlib import Path

STATE_FILE = Path(".claude/prism-loop.local.md")


def get_current_step() -> tuple[str, int]:
    """Extract current step from state file."""
    step = "unknown"
    index = 0
    try:
        content = STATE_FILE.read_text(encoding='utf-8')
        match = re.search(r"^current_step:\s*(\S+)", content, re.MULTILINE)
        if match:
            step = match.group(1)
        match = re.search(r"^current_step_index:\s*(\d+)", content, re.MULTILINE)
        if match:
            index = int(match.group(1))
    except (IOError, ValueError):
        pass
    return step, index


def main():
    if not STATE_FILE.exists():
        print("No active PRISM workflow loop found.")
        print("(No state file at .claude/prism-loop.local.md)")
        return

    step, index = get_current_step()

    # Delete the state file
    STATE_FILE.unlink()

    print("PRISM Workflow Loop CANCELLED")
    print(f"Stopped at step {index + 1}: {step}")


if __name__ == "__main__":
    main()
