# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Ruff PLR2004 wrapper for magic number detection.

Usage:
    uv run --script run_ruff_plr.py -- <path> [--output {json,text}]

Detects magic value comparisons in Python code.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_ruff_plr(target: Path, output_format: str = "text") -> int:
    """Run Ruff PLR2004 check."""
    ruff_format = "json" if output_format == "json" else "concise"
    cmd = [
        "ruff",
        "check",
        "--select",
        "PLR2004",
        "--output-format",
        ruff_format,
        str(target),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if output_format == "json" and result.stdout:
            # Wrap in standard schema
            data = json.loads(result.stdout)
            output = {
                "tool": "ruff",
                "rule": "PLR2004",
                "total_findings": len(data),
                "findings": data,
            }
            print(json.dumps(output, indent=2))
        else:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

        return result.returncode

    except FileNotFoundError:
        print("Error: ruff not found. Install with: uv tool install ruff", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error parsing ruff output: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Ruff PLR2004 magic number detection")
    parser.add_argument("path", type=Path, help="Path to check")
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format",
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        return 1

    return run_ruff_plr(args.path, args.output)


if __name__ == "__main__":
    sys.exit(main())
