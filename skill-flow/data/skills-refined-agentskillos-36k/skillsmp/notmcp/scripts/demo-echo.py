#!/usr/bin/env python3
"""
name: demo-echo
description: Echo back the input (useful for testing notmcp)
credentials:
input:
  message: string (optional, default "Hello from notmcp!")
output:
  echo: the input message echoed back
  timestamp: ISO timestamp when the tool ran
"""

import json
import sys
from datetime import datetime


def main():
    # Read input
    if sys.stdin.isatty():
        inp = {}
    else:
        try:
            inp = json.load(sys.stdin)
        except json.JSONDecodeError:
            inp = {}

    message = inp.get("message", "Hello from notmcp!")

    # Return result
    result = {
        "echo": message,
        "timestamp": datetime.now().isoformat(),
        "notmcp": "Tools are just code.",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
