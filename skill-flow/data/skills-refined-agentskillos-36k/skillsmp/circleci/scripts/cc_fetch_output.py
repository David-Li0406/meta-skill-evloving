#!/usr/bin/env python3
"""Fetch CircleCI step output from a presigned output_url."""

import json
import sys
from urllib.request import urlopen


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: cc_fetch_output.py <output-url>")
        return 2

    output_url = sys.argv[1].strip()
    with urlopen(output_url) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    for item in data:
        message = item.get("message", "").strip()
        if message:
            print(message)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
