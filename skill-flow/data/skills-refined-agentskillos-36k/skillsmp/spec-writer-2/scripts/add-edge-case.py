#!/usr/bin/env python3
"""
Add edge case to SPEC.md Edge Cases table.

Usage:
    add-edge-case.py --scenario "Feature has zero dependencies" \\
                     --handling "Show clear message" \\
                     --stories "Story 1"

    # Pipe-separated: scenario|handling|stories (or EC-ID|scenario|handling|stories for update)
    echo "Zero dependencies|Show message|Story 1" | add-edge-case.py --from-stdin
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


def add_edge_case(discovery_dir: Path, scenario: str, handling: str,
                 stories: str, ec_id: str = None):
    """Add or update edge case in SPEC.md."""
    spec_file = discovery_dir / 'SPEC.md'
    if not spec_file.exists():
        raise FileNotFoundError(f"SPEC.md not found")

    content = SafeFileOperations.read_file(spec_file)

    # If no ID provided, generate next ID
    if not ec_id:
        id_manager = IDManager(discovery_dir)
        ec_id = id_manager.get_next_id('edge_case')
        is_update = False
    else:
        is_update = True

    # Build row data
    row_data = {
        'ID': ec_id,
        'Scenario': scenario,
        'Handling': handling,
        'Stories Affected': stories
    }

    # Update or append to table
    if is_update:
        updated_content = SpecParser.update_table_row(
            content,
            '## Edge Cases',
            'ID',
            ec_id,
            row_data
        )
        action = "Updated"
    else:
        updated_content = SpecParser.append_table_row(
            content,
            '## Edge Cases',
            row_data
        )
        action = "Added"

    # Write updated content
    SafeFileOperations.write_file(spec_file, updated_content)

    print(f"✓ {action} {ec_id}: {scenario[:60]}{'...' if len(scenario) > 60 else ''}")
    print(f"  Stories: {stories}")


def main():
    parser = argparse.ArgumentParser(
        description='Add/update edge case in SPEC.md'
    )
    parser.add_argument('--id', help='EC ID to update')
    parser.add_argument('--scenario', help='Edge case scenario')
    parser.add_argument('--handling', help='How to handle this edge case')
    parser.add_argument('--stories', help='Stories affected (comma-separated)')
    parser.add_argument('--from-stdin', action='store_true',
                       help='Read pipe-separated input')
    parser.add_argument('--discovery-path', help='Path to discovery/ directory')

    args = parser.parse_args()

    try:
        if args.from_stdin:
            line = sys.stdin.read().strip()
            parts = line.split('|')

            if len(parts) < 3:
                print("ERROR: Pipe-separated input requires: scenario|handling|stories", file=sys.stderr)
                return 1

            # Check if first part is EC ID
            if re.match(r'^EC-\d{2}$', parts[0]):
                ec_id, scenario, handling, stories = parts[0], parts[1], parts[2], parts[3] if len(parts) > 3 else ""
            else:
                ec_id, scenario, handling, stories = None, parts[0], parts[1], parts[2]
        else:
            if not args.scenario or not args.handling or not args.stories:
                print("ERROR: --scenario, --handling, and --stories are required", file=sys.stderr)
                return 1
            ec_id, scenario, handling, stories = args.id, args.scenario, args.handling, args.stories

        discovery_dir = find_discovery_dir(args.discovery_path)
        add_edge_case(discovery_dir, scenario, handling, stories, ec_id)
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
