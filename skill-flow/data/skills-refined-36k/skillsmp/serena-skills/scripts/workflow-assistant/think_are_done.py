#!/usr/bin/env python3
"""
Think About Whether You Are Done Tool

Prompts the AI agent to verify task completion before finalizing work.
"""

import sys


def main():
    """
    Display a reflection prompt about task completion.
    This tool should be called whenever you feel the task is complete.
    """
    message = """
Have you truly completed all steps required by the task?

Completion checklist:
- Have you performed all required implementation steps?
- Is it appropriate to run tests and linting? If so, have you done that?
- Should non-code files (documentation, config) be adjusted? Have you done that?
- Should new tests be written to cover the changes?
- Read memory files about what should be done when a task is completed

Note: 
- Exploration tasks don't necessarily require tests or linting
- Code modification tasks typically require verification steps
- Check project-specific completion requirements in memory files

Review your work against the original task requirements before declaring completion.
"""
    print(message.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
