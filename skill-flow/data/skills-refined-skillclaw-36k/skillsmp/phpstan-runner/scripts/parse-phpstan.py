#!/usr/bin/env python3
"""
PHPStan Log Parser

Parses PHPStan table format output to provide a clear summary of errors.

Usage:
    python3 .claude/skills/phpstan-runner/scripts/parse-phpstan.py [path/to/phpstan.log]

    If no path provided, defaults to: var/qa/phpstan_logs/ (most recent)

Examples:
    # Parse most recent log
    python3 .claude/skills/phpstan-runner/scripts/parse-phpstan.py

    # Parse specific log file
    python3 .claude/skills/phpstan-runner/scripts/parse-phpstan.py var/qa/phpstan_logs/phpstan.20251103-120621.log

Output:
    - Summary of total errors and affected files
    - Top files by error count
    - Common error patterns
    - File:line references
"""

import sys
import re
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


def parse_phpstan_table(log_path: str) -> Dict:
    """Parse PHPStan table format output."""
    with open(log_path, 'r') as f:
        content = f.read()

    # Extract error lines
    errors = []
    current_file = None

    for line in content.split('\n'):
        # Skip separator lines
        if line.strip().startswith('------'):
            continue

        # File header line (starts with space, not indented much)
        if line.startswith(' ') and not line.startswith('  ') and line.strip():
            # This is a file path
            current_file = line.strip()
            continue

        # Error line: "  123    Error message..."
        if line.startswith('  ') and line.strip():
            match = re.match(r'\s+(\d+)\s+(.+)', line)
            if match and current_file:
                line_num = int(match.group(1))
                message = match.group(2).strip()

                # Remove emoji identifiers if present
                message = re.sub(r'🪪\s+\S+', '', message).strip()

                errors.append({
                    'file': current_file,
                    'line': line_num,
                    'message': message
                })

    # Group by file and pattern
    by_file = defaultdict(list)
    for error in errors:
        by_file[error['file']].append(error)

    return {
        'total': len(errors),
        'by_file': dict(by_file),
        'patterns': group_by_pattern(errors)
    }


def group_by_pattern(errors: List[Dict]) -> Dict:
    """Group errors by pattern (first 100 chars of message)."""
    patterns = defaultdict(list)
    for error in errors:
        # Use first 100 chars as pattern key
        pattern = error['message'][:100]
        patterns[pattern].append(error)

    # Sort by frequency (most common first)
    return dict(sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True))


def find_most_recent_log(log_dir: Path) -> Path:
    """Find the most recent PHPStan log file."""
    # Look for timestamped logs first
    log_files = sorted(log_dir.glob('phpstan.*.log'), reverse=True)

    if log_files:
        return log_files[0]

    # Fall back to non-timestamped log
    default_log = log_dir / 'phpstan.log'
    if default_log.exists():
        return default_log

    raise FileNotFoundError(f"No PHPStan logs found in {log_dir}")


def main():
    """Main entry point."""
    log_dir = Path('var/qa/phpstan_logs')

    # Check if log directory exists
    if not log_dir.exists():
        print(f"Error: PHPStan log directory not found: {log_dir}", file=sys.stderr)
        print(f"\nNo PHPStan runs found. Run analysis first with: ./bin/qa -t stan", file=sys.stderr)
        sys.exit(1)

    # Determine log file path
    if len(sys.argv) > 1:
        log_path = Path(sys.argv[1])
        if not log_path.exists():
            print(f"Error: Log file not found: {log_path}", file=sys.stderr)
            sys.exit(1)
        print(f"Parsing specified log: {log_path.name}")
    else:
        try:
            log_path = find_most_recent_log(log_dir)
            print(f"Parsing most recent log: {log_path.name}")
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            print(f"\nRun PHPStan first with: ./bin/qa -t stan", file=sys.stderr)
            sys.exit(1)

    print()

    try:
        results = parse_phpstan_table(str(log_path))

        # Print summary
        print("PHPSTAN ANALYSIS")
        print("=" * 80)
        print(f"Total Errors: {results['total']}")
        print(f"Files with Errors: {len(results['by_file'])}")
        print()

        if results['total'] == 0:
            print("✓ No errors found! Code passes PHPStan analysis.")
            sys.exit(0)

        # Top 5 files by error count
        print("TOP FILES BY ERROR COUNT")
        print("-" * 80)
        sorted_files = sorted(results['by_file'].items(), key=lambda x: len(x[1]), reverse=True)
        for file, errors in sorted_files[:5]:
            print(f"{file}: {len(errors)} errors")
        print()

        # Top error patterns
        print("COMMON ERROR PATTERNS")
        print("-" * 80)
        for pattern, occurrences in list(results['patterns'].items())[:5]:
            print(f"\n{pattern}...")
            print(f"  Occurrences: {len(occurrences)}")
            print(f"  Example: {occurrences[0]['file']}:{occurrences[0]['line']}")

        print()
        print("-" * 80)
        print(f"\nTotal: {results['total']} errors across {len(results['by_file'])} files")
        print(f"Fix the most common patterns first for maximum impact.")

        sys.exit(1 if results['total'] > 0 else 0)

    except Exception as e:
        print(f"Error parsing log file: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
