# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""jscpd wrapper for copy-paste detection.

Usage:
    uv run --script run_jscpd.py -- <path> [--output {json,text}]

Detects duplicate code blocks using jscpd via npx.
Requires Node.js (available via mise).
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_jscpd(target: Path, output_format: str = "text") -> int:
    """Run jscpd via npx for duplicate detection."""
    # Check npx availability
    if not shutil.which("npx"):
        print(
            "Error: npx not found. Install Node.js via mise: mise install node",
            file=sys.stderr,
        )
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        cmd = [
            "npx",
            "jscpd",
            "--reporters",
            "json",
            "--output",
            str(output_dir),
            str(target),
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            report_path = output_dir / "jscpd-report.json"

            if report_path.exists():
                data = json.loads(report_path.read_text())

                if output_format == "json":
                    output = {
                        "tool": "jscpd",
                        "total_findings": len(data.get("duplicates", [])),
                        "statistics": data.get("statistics", {}),
                        "findings": data.get("duplicates", []),
                    }
                    print(json.dumps(output, indent=2))
                else:
                    # Text format
                    duplicates = data.get("duplicates", [])
                    if duplicates:
                        print(f"Found {len(duplicates)} duplicate(s):\n")
                        for i, dup in enumerate(duplicates, 1):
                            first = dup.get("firstFile", {})
                            second = dup.get("secondFile", {})
                            lines = dup.get("lines", 0)
                            print(f"{i}. {first.get('name', '')}:{first.get('startLoc', {}).get('line', 0)}-{first.get('endLoc', {}).get('line', 0)}")
                            print(f"   Clone of: {second.get('name', '')}:{second.get('startLoc', {}).get('line', 0)}-{second.get('endLoc', {}).get('line', 0)}")
                            print(f"   Lines: {lines}\n")
                    else:
                        print("No duplicates found.")

                    # Summary
                    stats = data.get("statistics", {})
                    total = stats.get("total", {})
                    print("\nSummary:")
                    print(f"  Files analyzed: {total.get('sources', 0)}")
                    print(f"  Lines analyzed: {total.get('lines', 0)}")
                    print(f"  Duplicates: {total.get('clones', 0)}")
                    print(f"  Duplicate lines: {total.get('duplicatedLines', 0)}")
                    percentage = total.get("percentage", 0)
                    print(f"  Duplication: {percentage:.2f}%")

                return 0
            else:
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
                print("No jscpd report generated.", file=sys.stderr)
                return 1

        except subprocess.TimeoutExpired:
            print("Error: jscpd timed out after 5 minutes", file=sys.stderr)
            return 1
        except json.JSONDecodeError as e:
            print(f"Error parsing jscpd output: {e}", file=sys.stderr)
            return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run jscpd copy-paste detection")
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

    return run_jscpd(args.path, args.output)


if __name__ == "__main__":
    sys.exit(main())
