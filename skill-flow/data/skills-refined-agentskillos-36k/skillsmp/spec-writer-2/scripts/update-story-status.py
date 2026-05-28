#!/usr/bin/env python3
"""
Update story status in STATE.md Story Status Overview table.

Usage:
    update-story-status.py --story-number 3 --status in_progress
    update-story-status.py --story-number 5 --status queued
"""

import sys
import argparse
import re
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.file_operations import SafeFileOperations


# Status emoji mapping
STATUS_MAPPING = {
    'queued': '⏳ Queued',
    'in_progress': '🔄 In Progress',
    'in_spec': '✅ In SPEC',
    'new': '🆕 New'
}


def update_story_status(discovery_dir: Path, story_number: int, new_status: str):
    """
    Update story status in STATE.md.

    Args:
        discovery_dir: Path to discovery/ directory
        story_number: Story number to update
        new_status: New status (queued, in_progress, in_spec, new)
    """
    # Load STATE.md
    state_file = discovery_dir / 'STATE.md'
    if not state_file.exists():
        raise FileNotFoundError(f"File not found: {state_file}")

    content = SafeFileOperations.read_file(state_file)
    lines = content.split('\n')

    # Find Story Status Overview table
    table_start = None
    table_header_index = None
    story_row_index = None

    for i, line in enumerate(lines):
        if '## Story Status Overview' in line:
            table_start = i
        elif table_start and line.strip().startswith('| # |'):
            table_header_index = i
        elif table_header_index and line.strip().startswith(f'| {story_number} |'):
            story_row_index = i
            break

    if story_row_index is None:
        raise ValueError(f"Story {story_number} not found in Story Status Overview table")

    # Parse current row
    row = lines[story_row_index]
    cells = [c.strip() for c in row.split('|')[1:-1]]

    # Check if setting to in_progress
    if new_status == 'in_progress':
        # Verify no other story is in_progress
        for i, line in enumerate(lines):
            if i == story_row_index:
                continue
            if table_header_index and i > table_header_index and line.strip().startswith('|'):
                if '🔄 In Progress' in line:
                    # Found another in_progress story
                    other_story_match = re.match(r'^\| (\d+) \|', line.strip())
                    if other_story_match:
                        other_story_num = other_story_match.group(1)
                        raise ValueError(
                            f"Story {other_story_num} is already 'In Progress'. "
                            f"Only one story can be in progress at a time. "
                            f"Set story {other_story_num} to 'queued' first."
                        )

    # Update status column (index 3)
    if len(cells) >= 4:
        cells[3] = STATUS_MAPPING[new_status]

    # Rebuild row
    updated_row = '| ' + ' | '.join(cells) + ' |'
    lines[story_row_index] = updated_row

    # Write updated content
    updated_content = '\n'.join(lines)
    SafeFileOperations.write_file(state_file, updated_content)

    print(f"✓ Updated Story {story_number} status to: {STATUS_MAPPING[new_status]}")


def main():
    parser = argparse.ArgumentParser(
        description='Update story status in STATE.md'
    )
    parser.add_argument(
        '--story-number',
        type=int,
        required=True,
        help='Story number to update'
    )
    parser.add_argument(
        '--status',
        required=True,
        choices=['queued', 'in_progress', 'in_spec', 'new'],
        help='New status for the story'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Update story status
        update_story_status(discovery_dir, args.story_number, args.status)

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
