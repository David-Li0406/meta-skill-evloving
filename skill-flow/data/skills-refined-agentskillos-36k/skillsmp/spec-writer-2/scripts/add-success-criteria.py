#!/usr/bin/env python3
"""
Add success criteria to SPEC.md Success Criteria table.

Usage:
    add-success-criteria.py --criterion "Integration bugs decrease" \\
                            --measurement "60% reduction measured over 2 months" \\
                            --stories "Story 1, Story 3"

    # Pipe-separated: criterion|measurement|stories (or SC-ID|... for update)
    echo "Bugs decrease|60% reduction|Story 1, Story 3" | add-success-criteria.py --from-stdin
"""

import sys
import argparse
import re
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.id_manager import IDManager
from lib.file_operations import SafeFileOperations
from lib.spec_parser import SpecParser


def add_success_criteria(discovery_dir: Path, criterion: str, measurement: str,
                        stories: str, sc_id: str = None):
    """Add or update success criteria in SPEC.md."""
    spec_file = discovery_dir / 'SPEC.md'
    if not spec_file.exists():
        raise FileNotFoundError(f"SPEC.md not found")

    content = SafeFileOperations.read_file(spec_file)

    # If no ID provided, generate next ID
    if not sc_id:
        id_manager = IDManager(discovery_dir)
        sc_id = id_manager.get_next_id('success_criteria')
        is_update = False
    else:
        is_update = True

    # Build row data
    row_data = {
        'ID': sc_id,
        'Criterion': criterion,
        'Measurement': measurement,
        'Stories': stories
    }

    # Update or append to table
    if is_update:
        updated_content = SpecParser.update_table_row(
            content,
            '## Success Criteria',
            'ID',
            sc_id,
            row_data
        )
        action = "Updated"
    else:
        updated_content = SpecParser.append_table_row(
            content,
            '## Success Criteria',
            row_data
        )
        action = "Added"

    # Write updated content
    SafeFileOperations.write_file(spec_file, updated_content)

    print(f"✓ {action} {sc_id}: {criterion[:60]}{'...' if len(criterion) > 60 else ''}")
    print(f"  Stories: {stories}")


def main():
    parser = argparse.ArgumentParser(
        description='Add/update success criteria in SPEC.md'
    )
    parser.add_argument('--id', help='SC ID to update')
    parser.add_argument('--criterion', help='Success criterion')
    parser.add_argument('--measurement', help='How to measure this criterion')
    parser.add_argument('--stories', help='Stories this applies to (comma-separated)')
    parser.add_argument('--from-stdin', action='store_true',
                       help='Read pipe-separated input')
    parser.add_argument('--discovery-path', help='Path to discovery/ directory')

    args = parser.parse_args()

    try:
        if args.from_stdin:
            line = sys.stdin.read().strip()
            parts = line.split('|')

            if len(parts) < 3:
                print("ERROR: Pipe-separated input requires: criterion|measurement|stories", file=sys.stderr)
                return 1

            # Check if first part is SC ID
            if re.match(r'^SC-\d{3}$', parts[0]):
                sc_id, criterion, measurement, stories = parts[0], parts[1], parts[2], parts[3] if len(parts) > 3 else ""
            else:
                sc_id, criterion, measurement, stories = None, parts[0], parts[1], parts[2]
        else:
            if not args.criterion or not args.measurement or not args.stories:
                print("ERROR: --criterion, --measurement, and --stories are required", file=sys.stderr)
                return 1
            sc_id, criterion, measurement, stories = args.id, args.criterion, args.measurement, args.stories

        discovery_dir = find_discovery_dir(args.discovery_path)
        add_success_criteria(discovery_dir, criterion, measurement, stories, sc_id)
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
