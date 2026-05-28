# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Gitleaks wrapper for secret detection.

Usage:
    uv run --script run_gitleaks.py -- <path> [--output {json,text}]

Examples:
    uv run --script run_gitleaks.py -- src/
    uv run --script run_gitleaks.py -- . --output json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_gitleaks(target: Path, output_format: str = "text") -> int:
    """Run gitleaks on target directory.

    Args:
        target: Directory to scan
        output_format: Output format (json or text)

    Returns:
        Exit code (0 = no secrets, 1 = secrets found or error)
    """
    # Use modern 'dir' command for directory scanning (v8.19.0+)
    cmd = [
        "gitleaks",
        "dir",
        str(target),
        "--report-format",
        "json",
        "--report-path",
        "/dev/stdout",
        "--verbose",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        # Exit code 0 = clean, 1 = secrets found, 2+ = error
        if result.returncode == 0:
            if output_format == "json":
                output = {
                    "tool": "gitleaks",
                    "rule": "secret-detection",
                    "total_findings": 0,
                    "findings": [],
                }
                print(json.dumps(output, indent=2))
            else:
                print("No secrets detected")
            return 0

        elif result.returncode == 1:
            # Secrets found - parse JSON output
            findings = []
            if result.stdout.strip():
                try:
                    findings = json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass

            if output_format == "json":
                output = {
                    "tool": "gitleaks",
                    "rule": "secret-detection",
                    "total_findings": len(findings),
                    "findings": findings,
                }
                print(json.dumps(output, indent=2))
            else:
                # Text format - compiler-style output
                for f in findings:
                    file_path = f.get("File", "unknown")
                    line = f.get("StartLine", 0)
                    rule_id = f.get("RuleID", "secret")
                    match_text = f.get("Match", "")[:50]  # Truncate for safety
                    print(f"{file_path}:{line}: {rule_id} - {match_text}... [gitleaks]")
                print(f"\nTotal: {len(findings)} secret(s) detected")
            return 1

        else:
            # Tool error
            print(
                f"gitleaks error (exit {result.returncode}): {result.stderr}",
                file=sys.stderr,
            )
            return result.returncode

    except FileNotFoundError:
        print(
            "Error: gitleaks not found. Install with: mise use --global gitleaks",
            file=sys.stderr,
        )
        return 1
    except subprocess.TimeoutExpired:
        print("Error: gitleaks timed out after 120 seconds", file=sys.stderr)
        return 1


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Run gitleaks for secret detection")
    parser.add_argument("path", type=Path, help="Directory to scan")
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        return 1

    return run_gitleaks(args.path, args.output)


if __name__ == "__main__":
    sys.exit(main())
