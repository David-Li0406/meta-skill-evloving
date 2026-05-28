#!/usr/bin/env python3
"""Find deferred work markers: TODO, FIXME, HACK, XXX, BUG, NOTE, OPTIMIZE."""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

MARKERS = {
    "FIXME": {"severity": "high", "description": "Known bug or critical issue"},
    "BUG": {"severity": "high", "description": "Known bug"},
    "HACK": {"severity": "high", "description": "Workaround that should be fixed"},
    "XXX": {"severity": "high", "description": "Dangerous or problematic code"},
    "TODO": {"severity": "medium", "description": "Planned work"},
    "OPTIMIZE": {"severity": "medium", "description": "Performance improvement needed"},
    "NOTE": {"severity": "low", "description": "Important context"},
    "REVIEW": {"severity": "low", "description": "Needs review"},
}

# Only match markers at start of comment (after #)
MARKER_PATTERN = re.compile(
    r'#\s*(' + '|'.join(MARKERS.keys()) + r')[\s:\-]*(.*)$',
    re.IGNORECASE
)

# Match markers at start of line in docstrings (with optional leading whitespace)
DOCSTRING_MARKER_PATTERN = re.compile(
    r'^\s*(' + '|'.join(MARKERS.keys()) + r')[\s:\-]+(.*)$',
    re.IGNORECASE | re.MULTILINE
)

class Finding(NamedTuple):
    file: str
    line: int
    marker: str
    message: str
    severity: str
    context: str

def scan_file(filepath: Path) -> list[Finding]:
    """Scan a single file for deferred work markers."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        lines = content.splitlines()
    except Exception:
        return findings

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip lines that are clearly inside string literals (dict values, etc.)
        # We only want actual comments: lines starting with # or inline # comments
        if '#' not in line:
            continue

        # Find the comment portion (everything after # that's not in a string)
        # Simple heuristic: if the line has quotes before #, check if # is inside string
        hash_pos = line.find('#')
        pre_hash = line[:hash_pos]

        # Count quotes before # - if odd number, # is likely inside a string
        single_quotes = pre_hash.count("'") - pre_hash.count("\\'")
        double_quotes = pre_hash.count('"') - pre_hash.count('\\"')
        if single_quotes % 2 == 1 or double_quotes % 2 == 1:
            continue  # Hash is inside a string literal

        # Check inline comments
        match = MARKER_PATTERN.search(line)
        if match:
            marker = match.group(1).upper()
            message = match.group(2).strip() or "(no description)"
            findings.append(Finding(
                file=str(filepath),
                line=i,
                marker=marker,
                message=message,
                severity=MARKERS[marker]["severity"],
                context=line.strip()[:100]
            ))

    return findings

def scan_directory(path: Path, exclude_dirs: set[str]) -> list[Finding]:
    """Recursively scan directory for Python files."""
    findings = []
    exclude_dirs = exclude_dirs | {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.tox', 'build', 'dist', '.eggs'}

    for item in path.rglob('*.py'):
        if any(excluded in item.parts for excluded in exclude_dirs):
            continue
        findings.extend(scan_file(item))

    return findings

def format_text(findings: list[Finding]) -> str:
    """Format findings as human-readable text."""
    if not findings:
        return "✅ No deferred work markers found."

    output = []
    by_severity = defaultdict(list)
    for f in findings:
        by_severity[f.severity].append(f)

    severity_icons = {"high": "🔴", "medium": "🟡", "low": "🔵"}

    for severity in ["high", "medium", "low"]:
        items = by_severity[severity]
        if not items:
            continue

        output.append(f"\n{severity_icons[severity]} {severity.upper()} ({len(items)} items)")
        output.append("-" * 50)

        for f in sorted(items, key=lambda x: (x.file, x.line)):
            output.append(f"  {f.file}:{f.line}")
            output.append(f"    [{f.marker}] {f.message}")

    # Summary by marker type
    output.append("\n📊 Summary")
    output.append("-" * 50)
    by_marker = defaultdict(int)
    for f in findings:
        by_marker[f.marker] += 1
    for marker, count in sorted(by_marker.items(), key=lambda x: -x[1]):
        output.append(f"  {marker}: {count}")

    output.append(f"\n  Total: {len(findings)} deferred items")

    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Find deferred work markers in Python code")
    parser.add_argument("path", type=Path, help="File or directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--severity", choices=["high", "medium", "low"], help="Filter by minimum severity")
    parser.add_argument("--exclude", nargs="*", default=[], help="Directories to exclude")
    parser.add_argument("--marker", help="Filter by specific marker (e.g., TODO, FIXME)")
    args = parser.parse_args()

    path = args.path.resolve()
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if path.is_file():
        findings = scan_file(path)
    else:
        findings = scan_directory(path, set(args.exclude))

    # Apply filters
    if args.severity:
        severity_order = {"high": 0, "medium": 1, "low": 2}
        max_level = severity_order[args.severity]
        findings = [f for f in findings if severity_order[f.severity] <= max_level]

    if args.marker:
        findings = [f for f in findings if f.marker == args.marker.upper()]

    if args.format == "json":
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        print(format_text(findings))

    # Exit with error code if high-severity items found
    if any(f.severity == "high" for f in findings):
        sys.exit(1)

if __name__ == "__main__":
    main()
