#!/usr/bin/env python3
"""
Helper script for your skill.

This is an example utility script that your skill can execute.
Scripts can handle error conditions, validate inputs, and produce
verifiable outputs that Claude can use.

Usage:
    python scripts/helper-script.py <input>
"""

import sys


def process_input(input_value):
    """
    Process the input and return results.

    Args:
        input_value: The input to process

    Returns:
        The processed result
    """
    try:
        # Add your processing logic here
        result = f"Processed: {input_value}"
        return result
    except Exception as e:
        # Provide clear error messages instead of failing silently
        print(f"Error processing input: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python helper-script.py <input>", file=sys.stderr)
        sys.exit(1)

    input_value = sys.argv[1]
    result = process_input(input_value)
    print(result)
