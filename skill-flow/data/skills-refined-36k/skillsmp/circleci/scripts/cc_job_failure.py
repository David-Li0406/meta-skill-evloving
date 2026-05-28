#!/usr/bin/env python3
"""Fetch failing CircleCI job step output (API v1.1 for output_url support)."""

import json
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


def load_token() -> str:
    """Load CircleCI token from env vars or ~/.circleci/cli.yml."""
    token = os.environ.get("CIRCLECI_CLI_TOKEN") or os.environ.get("CIRCLE_TOKEN")
    if token:
        return token

    config_path = Path.home() / ".circleci" / "cli.yml"
    if not config_path.exists():
        raise RuntimeError("CircleCI CLI config not found at ~/.circleci/cli.yml")

    for line in config_path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        match = re.match(r"^token\s*:\s*(.+)$", line)
        if match:
            token = match.group(1).strip()
            if len(token) >= 2 and token[0] in "\"'" and token[-1] == token[0]:
                token = token[1:-1]
            if token:
                return token

    raise RuntimeError("CircleCI token not found in ~/.circleci/cli.yml")


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: cc_job_failure.py <gh/org/repo> <job-number>")
        return 2

    slug = sys.argv[1].strip()
    job_number = sys.argv[2].strip()
    token = load_token()

    url = f"https://circleci.com/api/v1.1/project/github/{slug}/{job_number}"
    req = Request(url)
    req.add_header("Circle-Token", token)
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    print(f"status {data.get('status')}")
    output_url = None
    step_name = None
    for step in data.get("steps", []):
        for action in step.get("actions", []):
            if action.get("status") == "failed":
                output_url = action.get("output_url")
                step_name = step.get("name")
                break
        if output_url:
            break

    if not output_url:
        print("No failed step output url found.")
        return 0

    with urlopen(output_url) as resp:
        output_data = json.loads(resp.read().decode("utf-8"))

    print(f"failed-step {step_name}")
    for item in output_data:
        message = item.get("message", "").strip()
        if message:
            print(message)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
