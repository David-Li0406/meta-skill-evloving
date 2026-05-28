#!/usr/bin/env python3
"""
Think About Task Adherence Tool

Prompts the AI agent to verify alignment with the original task before making code changes.
"""

import sys


def main():
    """
    Display a reflection prompt about task adherence.
    This tool should ALWAYS be called before inserting, replacing, or deleting code.
    """
    message = """
Are you staying on track with the task at hand?

Before modifying code, verify:
- Are you deviating from the original task?
- Do you need additional information to proceed?
- Have you loaded all relevant memory files?
- Is your implementation aligned with project code style, conventions, and guidelines?

Important reminders:
- It is better to stop and ask the user for clarification than to perform large changes
  that might not align with user intentions
- If the conversation has become too long or is deviating, create a summary and suggest
  starting a new conversation
- Always check memory files for code style and conventions before editing

Reflect on your current approach and adjust if necessary before proceeding.
"""
    print(message.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
