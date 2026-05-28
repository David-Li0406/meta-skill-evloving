#!/usr/bin/env python3
"""
Retry Ollama Call with Exponential Backoff

Usage:
    python3 retry_call.py <script_to_run> [args...]

    Wraps the execution of another script or command with retry logic.

Dependencies:
    None (uses subprocess)
"""

import sys
import subprocess
import time
import random

MAX_RETRIES = 5
BASE_DELAY = 1  # seconds


def run_with_retry(command):
    retries = 0
    while retries <= MAX_RETRIES:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            if retries == MAX_RETRIES:
                print(
                    f"Error: Command failed after {MAX_RETRIES} retries.",
                    file=sys.stderr,
                )
                print(f"Stderr: {e.stderr}", file=sys.stderr)
                return e.returncode

            # Calculate backoff with jitter
            delay = min(BASE_DELAY * (2**retries), 30)
            jitter = random.uniform(0, 0.1 * delay)
            wait_time = delay + jitter

            print(
                f"Command failed (attempt {retries+1}/{MAX_RETRIES+1}). Retrying in {wait_time:.2f}s...",
                file=sys.stderr,
            )
            time.sleep(wait_time)
            retries += 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 retry_call.py <command> [args...]", file=sys.stderr)
        sys.exit(1)

    # The command is the rest of the arguments
    command = sys.argv[1:]

    sys.exit(run_with_retry(command))


if __name__ == "__main__":
    main()
