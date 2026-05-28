# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Semgrep wrapper for pattern-based hardcode detection.

Usage:
    uv run --script run_semgrep.py -- <path> [--output {json,text}]

Detects hardcoded URLs, ports, paths, credentials, and API limits.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_semgrep(target: Path, output_format: str = "text") -> int:
    """Run Semgrep with custom hardcode rules."""
    rules_path = Path(__file__).parent.parent / "assets" / "semgrep-hardcode-rules.yaml"

    if not rules_path.exists():
        print(f"Error: Semgrep rules not found: {rules_path}", file=sys.stderr)
        return 1

    cmd = [
        "semgrep",
        "--config",
        str(rules_path),
        str(target),
    ]

    if output_format == "json":
        cmd.append("--json")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if output_format == "json" and result.stdout:
            # Wrap in standard schema
            data = json.loads(result.stdout)
            output = {
                "tool": "semgrep",
                "rules_file": str(rules_path),
                "total_findings": len(data.get("results", [])),
                "findings": data.get("results", []),
                "errors": data.get("errors", []),
            }
            print(json.dumps(output, indent=2))
        else:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                # Filter out semgrep info messages
                for line in result.stderr.splitlines():
                    if not line.startswith("Scanning"):
                        print(line, file=sys.stderr)

        return 0 if result.returncode in (0, 1) else result.returncode

    except FileNotFoundError:
        print(
            "Error: semgrep not found. Install with: brew install semgrep",
            file=sys.stderr,
        )
        return 1
    except json.JSONDecodeError as e:
        print(f"Error parsing semgrep output: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Semgrep pattern-based hardcode detection"
    )
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

    return run_semgrep(args.path, args.output)


if __name__ == "__main__":
    sys.exit(main())
