#!/usr/bin/env python3
"""
Log Agent Run

Usage:
    python3 log_run.py <agent_name> <message> [--log_dir <dir>]

Dependencies:
    None
"""

import sys
import argparse
import os
import datetime
import json


def log_agent_run(agent_name, message, log_dir=".tmp/logs"):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {"timestamp": timestamp, "agent": agent_name, "message": message}

    # Ensure log directory exists
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating log directory: {e}", file=sys.stderr)
        return

    log_file = os.path.join(log_dir, f"{agent_name}.log")

    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"Logged to {log_file}")
    except Exception as e:
        print(f"Error writing log: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Log agent activity")
    parser.add_argument("agent_name", help="Name of the agent")
    parser.add_argument("message", help="Message or data to log")
    parser.add_argument("--log_dir", default=".tmp/logs", help="Directory for logs")

    args = parser.parse_args()

    log_agent_run(args.agent_name, args.message, args.log_dir)


if __name__ == "__main__":
    main()
