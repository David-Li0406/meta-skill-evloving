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
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.id_manager import IDManager
from lib.file_operations import SafeFileOperations
from lib.spec_parser import SpecParser
from lib.id_helpers import normalize_and_notify
from lib.validators import validate_story_exists


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
        # Normalize ID (accept flexible formats like SC1, SC-001, sc-1)
        normalized_id = normalize_and_notify(sc_id, 'success_criteria')
        if not normalized_id:
            raise ValueError(f"Invalid success criteria ID format: {sc_id}\n"
                           f"Expected format: SC-### (e.g., SC-001, SC-025, SC-123)\n"
                           f"Flexible formats accepted: SC1, SC-001, sc-1, etc.")
        sc_id = normalized_id
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

            # Check if first part is SC ID (flexible formats accepted)
            normalized_id = normalize_and_notify(parts[0], 'success_criteria', quiet=True)
            if normalized_id:
                # Update mode: SC-ID|criterion|measurement|stories
                sc_id = parts[0]  # Will be normalized later in add_success_criteria
                criterion = parts[1]
                measurement = parts[2] if len(parts) > 2 else ""
                stories = parts[3] if len(parts) > 3 else ""
            else:
                # Add mode: criterion|measurement|stories
                sc_id = None
                criterion = parts[0]
                measurement = parts[1]
                stories = parts[2]
        else:
            if not args.criterion or not args.measurement or not args.stories:
                print("ERROR: --criterion, --measurement, and --stories are required", file=sys.stderr)
                return 1
            sc_id, criterion, measurement, stories = args.id, args.criterion, args.measurement, args.stories

        discovery_dir = find_discovery_dir(args.discovery_path)

        # Validate story references (warnings only - don't block)
        if stories:
            import re
            story_nums = re.findall(r'Story\s+(\d+)', stories, re.IGNORECASE)
            for story_num_str in story_nums:
                story_num = int(story_num_str)
                exists, suggestions = validate_story_exists(story_num, discovery_dir)
                if not exists:
                    print(f"⚠️  WARNING: Story {story_num} not found in STATE.md", file=sys.stderr)
                    if suggestions:
                        print(f"    Did you mean one of: {', '.join(map(str, suggestions))}?", file=sys.stderr)

        add_success_criteria(discovery_dir, criterion, measurement, stories, sc_id)
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
