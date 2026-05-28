#!/usr/bin/env python3
"""
Think About Collected Information Tool

Prompts the AI agent to reflect on whether sufficient information has been collected
to solve the current task.
"""

import sys


def main():
    """
    Display a reflection prompt about collected information completeness.
    This tool should ALWAYS be called after completing a non-trivial sequence of
    searching steps like find_symbol, find_references, search_pattern, read_file, etc.
    """
    message = """
Have you collected all the information you need for solving the current task?

Consider:
- Is the information sufficient and relevant?
- Can missing information be acquired using available tools (especially symbol discovery tools)?
- Do you need to ask the user for more information?

Think through step by step:
1. What information have you collected so far?
2. What information is still missing?
3. How could the missing information be acquired?

Provide a summary of your assessment.
"""
    print(message.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
