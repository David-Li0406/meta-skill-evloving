#!/usr/bin/env python3
"""
Add revision entry to REVISIONS.md.

Usage:
    add-revision.py --story-number 1 \\
                    --change-type "Added scenario" \\
                    --trigger "Story 3 revealed edge case" \\
                    --before "Original scenarios" \\
                    --after "Updated scenarios" \\
                    --decision D52
"""

import sys
import argparse
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.id_manager import IDManager
from lib.file_operations import SafeFileOperations
from lib.templates import TemplateManager
from lib.id_helpers import normalize_and_notify
from lib.validators import validate_story_exists, validate_decision_exists


def add_revision(discovery_dir: Path, story_num: int, change_type: str,
                trigger: str, before: str, after: str,
                decision: str = None, confirmed: str = None):
    """
    Add revision entry to REVISIONS.md.

    Args:
        discovery_dir: Path to discovery/ directory
        story_num: Story number being revised
        change_type: Type of change
        trigger: What triggered the revision
        before: Content before change
        after: Content after change
        decision: Decision reference (optional)
        confirmed: User confirmation status (optional)
    """
    # Get next revision ID
    id_manager = IDManager(discovery_dir)
    revision_id = id_manager.get_next_id('revision')
    id_num = revision_id.split('-')[1]  # Extract number from REV-###

    # Load and render template
    template_mgr = TemplateManager()

    rendered = template_mgr.render_template(
        'revision-entry.md',
        ID=id_num,
        STORY_NUM=str(story_num),
        CHANGE_TYPE=change_type,
        TRIGGER=trigger,
        BEFORE=before,
        AFTER=after,
        DECISION=decision or '[Not specified]',
        CONFIRMED=confirmed or 'Pending',
        CONFIRM_DATE='[Date pending]' if not confirmed else '[Date]'
    )

    # Append to REVISIONS.md
    revisions_file = discovery_dir / 'archive' / 'REVISIONS.md'
    if not revisions_file.exists():
        raise FileNotFoundError(f"File not found: {revisions_file}")

    content = SafeFileOperations.read_file(revisions_file)

    # Append revision entry
    updated_content = content.rstrip() + '\n\n' + rendered

    # Write updated content
    SafeFileOperations.write_file(revisions_file, updated_content)

    print(f"✓ Logged {revision_id}: Story {story_num} - {change_type}")
    if decision:
        print(f"  Decision: {decision}")


def main():
    parser = argparse.ArgumentParser(
        description='Add revision entry to REVISIONS.md'
    )
    parser.add_argument(
        '--story-number',
        type=int,
        required=True,
        help='Story number being revised'
    )
    parser.add_argument(
        '--change-type',
        required=True,
        help='Type of change (e.g., "Added scenario", "Modified requirement")'
    )
    parser.add_argument(
        '--trigger',
        required=True,
        help='What triggered this revision'
    )
    parser.add_argument(
        '--before',
        required=True,
        help='Content before the change'
    )
    parser.add_argument(
        '--after',
        required=True,
        help='Content after the change'
    )
    parser.add_argument(
        '--decision',
        help='Decision reference (e.g., D52)'
    )
    parser.add_argument(
        '--confirmed',
        help='User confirmation status (Yes/No/Pending)'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Normalize decision ID if provided (accept flexible formats like D1, D02, d2)
        decision_id = args.decision
        if decision_id:
            normalized_id = normalize_and_notify(decision_id, 'decision')
            if not normalized_id:
                print(f"ERROR: Invalid decision ID format: {decision_id}", file=sys.stderr)
                print("Expected format: D# (e.g., D1, D23, D456)", file=sys.stderr)
                print("Flexible formats accepted: D1, D02, d2, etc.", file=sys.stderr)
                return 1
            decision_id = normalized_id

        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        # Validate cross-references (warnings only - don't block)
        id_manager = IDManager(discovery_dir)

        # Validate story exists
        exists, suggestions = validate_story_exists(args.story_number, discovery_dir)
        if not exists:
            print(f"⚠️  WARNING: Story {args.story_number} not found in STATE.md", file=sys.stderr)
            if suggestions:
                print(f"    Did you mean one of: {', '.join(map(str, suggestions))}?", file=sys.stderr)

        # Validate decision if provided
        if decision_id:
            exists, suggestions = validate_decision_exists(decision_id, discovery_dir, id_manager)
            if not exists:
                print(f"⚠️  WARNING: Decision {decision_id} not found in DECISIONS.md", file=sys.stderr)
                if suggestions:
                    print(f"    Did you mean one of: {', '.join(suggestions)}?", file=sys.stderr)

        # Add revision
        add_revision(
            discovery_dir, args.story_number, args.change_type,
            args.trigger, args.before, args.after,
            decision_id, args.confirmed
        )

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
