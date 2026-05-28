#!/usr/bin/env python3
"""
Script: greet.py
Purpose: Generate personalized greeting messages

Usage:
    python greet.py --name "Alice"
    python greet.py --name "World" --style formal

Arguments:
    --name    Name to greet (required)
    --style   Greeting style: casual, formal, friendly (default: casual)

Exit Codes:
    0 - Success
    1 - Invalid arguments

Example Output:
    {"status": "success", "message": "Hello, Alice!"}
"""

import argparse
import json
import sys


def generate_greeting(name: str, style: str = "casual") -> str:
    """Generate a greeting based on style."""
    greetings = {
        "casual": f"Hello, {name}!",
        "formal": f"Good day, {name}. How may I assist you?",
        "friendly": f"Hey {name}! Great to see you! 👋",
    }
    return greetings.get(style, greetings["casual"])


def main():
    parser = argparse.ArgumentParser(
        description="Generate personalized greeting messages"
    )
    parser.add_argument("--name", required=True, help="Name to greet")
    parser.add_argument(
        "--style",
        choices=["casual", "formal", "friendly"],
        default="casual",
        help="Greeting style (default: casual)",
    )
    args = parser.parse_args()

    try:
        message = generate_greeting(args.name, args.style)
        result = {"status": "success", "message": message, "style": args.style}
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except Exception as e:
        error = {"status": "error", "code": 1, "message": str(e)}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
