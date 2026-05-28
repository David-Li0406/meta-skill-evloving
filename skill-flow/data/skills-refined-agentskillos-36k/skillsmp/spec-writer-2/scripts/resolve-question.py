#!/usr/bin/env python3
"""
Remove resolved question from OPEN_QUESTIONS.md.

Usage:
    resolve-question.py --question Q23
    resolve-question.py --question Q23 --note "Resolved by D15"
"""

import sys
import argparse
import re
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.file_operations import SafeFileOperations


def resolve_question(discovery_dir: Path, question_id: str, note: str = None):
    """
    Remove question from OPEN_QUESTIONS.md.

    Args:
        discovery_dir: Path to discovery/ directory
        question_id: Question ID to resolve (e.g., Q23)
        note: Optional resolution note
    """
    # Load OPEN_QUESTIONS.md
    questions_file = discovery_dir / 'OPEN_QUESTIONS.md'
    if not questions_file.exists():
        raise FileNotFoundError(f"File not found: {questions_file}")

    content = SafeFileOperations.read_file(questions_file)
    lines = content.split('\n')

    # Find and remove question entry
    question_pattern = re.compile(rf'^\- \*\*{re.escape(question_id)}\*\*:')
    found = False
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is the question to remove
        if question_pattern.match(line):
            found = True
            # Skip this line and any continuation lines (lines starting with spaces)
            i += 1
            while i < len(lines) and lines[i].startswith('  '):
                i += 1
            # Skip trailing blank line if present
            if i < len(lines) and not lines[i].strip():
                i += 1
            continue

        new_lines.append(line)
        i += 1

    if not found:
        raise ValueError(f"Question {question_id} not found in OPEN_QUESTIONS.md")

    # Write updated content
    updated_content = '\n'.join(new_lines)

    # Add resolution note if provided (as comment at end)
    if note:
        updated_content += f"\n\n<!-- Resolved: {question_id} - {note} -->"

    SafeFileOperations.write_file(questions_file, updated_content)

    print(f"✓ Resolved {question_id}")
    if note:
        print(f"  Note: {note}")


def main():
    parser = argparse.ArgumentParser(
        description='Remove resolved question from OPEN_QUESTIONS.md'
    )
    parser.add_argument(
        '--question',
        required=True,
        help='Question ID to resolve (e.g., Q23)'
    )
    parser.add_argument(
        '--note',
        help='Optional resolution note (e.g., "Resolved by D15")'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Validate question ID format
        if not re.match(r'^Q\d+$', args.question):
            print(f"ERROR: Invalid question ID format: {args.question}", file=sys.stderr)
            print("Expected format: Q#", file=sys.stderr)
            return 1

        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Resolve question
        resolve_question(discovery_dir, args.question, args.note)

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
