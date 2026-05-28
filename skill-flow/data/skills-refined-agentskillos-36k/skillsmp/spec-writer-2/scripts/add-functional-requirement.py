#!/usr/bin/env python3
"""
Add functional requirement to SPEC.md Requirements table.

Usage:
    add-functional-requirement.py --requirement "System MUST support X" \\
                                   --stories "Story 1, Story 2" \\
                                   --confidence "✅ Confirmed"

    # Pipe-separated: FR-ID|requirement|stories|confidence (ID optional for new)
    echo "System MUST cache for 15 min|Story 2|✅ Confirmed" | add-functional-requirement.py --from-stdin
    echo "FR-005|Updated requirement|Story 2|🔄 Draft" | add-functional-requirement.py --from-stdin  # Update existing
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


def add_functional_requirement(discovery_dir: Path, requirement: str, stories: str,
                              confidence: str = "🔄 Draft", fr_id: str = None):
    """
    Add or update functional requirement in SPEC.md.

    Args:
        discovery_dir: Path to discovery/ directory
        requirement: Requirement text
        stories: Stories this applies to
        confidence: Confidence level
        fr_id: Existing FR ID to update (optional)
    """
    spec_file = discovery_dir / 'SPEC.md'
    if not spec_file.exists():
        raise FileNotFoundError(f"SPEC.md not found")

    content = SafeFileOperations.read_file(spec_file)

    # If no ID provided, generate next ID
    if not fr_id:
        id_manager = IDManager(discovery_dir)
        fr_id = id_manager.get_next_id('functional_requirement')
        is_update = False
    else:
        is_update = True

    # Build row data
    row_data = {
        'ID': fr_id,
        'Requirement': requirement,
        'Stories': stories,
        'Confidence': confidence
    }

    # Update or append to table
    try:
        if is_update:
            # Update existing row
            updated_content = SpecParser.update_table_row(
                content,
                '### Functional Requirements',
                'ID',
                fr_id,
                row_data
            )
            action = "Updated"
        else:
            # Append new row
            updated_content = SpecParser.append_table_row(
                content,
                '### Functional Requirements',
                row_data
            )
            action = "Added"
    except ValueError as e:
        # Table might use ## instead of ###
        try:
            if is_update:
                updated_content = SpecParser.update_table_row(
                    content,
                    '## Requirements',
                    'ID',
                    fr_id,
                    row_data
                )
                action = "Updated"
            else:
                updated_content = SpecParser.append_table_row(
                    content,
                    '## Requirements',
                    row_data
                )
                action = "Added"
        except ValueError:
            raise ValueError("Could not find Functional Requirements table in SPEC.md")

    # Write updated content
    SafeFileOperations.write_file(spec_file, updated_content)

    print(f"✓ {action} {fr_id}: {requirement[:60]}{'...' if len(requirement) > 60 else ''}")
    print(f"  Stories: {stories}")
    print(f"  Confidence: {confidence}")


def main():
    parser = argparse.ArgumentParser(
        description='Add/update functional requirement in SPEC.md'
    )
    parser.add_argument(
        '--id',
        help='FR ID to update (if updating existing requirement)'
    )
    parser.add_argument(
        '--requirement',
        help='Requirement text (e.g., "System MUST support X")'
    )
    parser.add_argument(
        '--stories',
        help='Stories this applies to (comma-separated)'
    )
    parser.add_argument(
        '--confidence',
        default='🔄 Draft',
        help='Confidence level (default: 🔄 Draft)'
    )
    parser.add_argument(
        '--from-stdin',
        action='store_true',
        help='Read pipe-separated input (requirement|stories|confidence) or (FR-ID|requirement|stories|confidence)'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Parse input
        if args.from_stdin:
            line = sys.stdin.read().strip()
            parts = line.split('|')

            if len(parts) < 2:
                print("ERROR: Pipe-separated input requires at least: requirement|stories", file=sys.stderr)
                return 1

            # Check if first part is an FR ID
            if re.match(r'^FR-\d{3}$', parts[0]):
                # Update mode: FR-ID|requirement|stories|confidence
                fr_id = parts[0]
                requirement = parts[1]
                stories = parts[2] if len(parts) > 2 else ""
                confidence = parts[3] if len(parts) > 3 else "🔄 Draft"
            else:
                # Add mode: requirement|stories|confidence
                fr_id = None
                requirement = parts[0]
                stories = parts[1]
                confidence = parts[2] if len(parts) > 2 else "🔄 Draft"
        else:
            # Read from args
            if not args.requirement or not args.stories:
                print("ERROR: --requirement and --stories are required", file=sys.stderr)
                return 1

            fr_id = args.id
            requirement = args.requirement
            stories = args.stories
            confidence = args.confidence

        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Add functional requirement
        add_functional_requirement(discovery_dir, requirement, stories, confidence, fr_id)

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
