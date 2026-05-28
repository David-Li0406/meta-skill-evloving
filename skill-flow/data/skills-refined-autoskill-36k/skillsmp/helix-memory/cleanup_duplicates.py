#!/usr/bin/env python3
"""
Cleanup Duplicate Memories

Finds and removes duplicate memories, keeping only the most recent one.
Optionally links duplicates with "supersedes" relationship before deletion.
"""

import sys
from pathlib import Path
from collections import defaultdict

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "hooks"))

from common import (
    check_helix_running,
    get_all_memories,
    link_related_memories,
    delete_memory
)

def find_duplicates(memories):
    """
    Group memories by similar content (first 100 chars).

    Returns:
        Dict mapping content_key to list of duplicate memories
    """
    groups = defaultdict(list)

    for memory in memories:
        content = memory.get("content", "")
        content_key = content[:100].lower().strip()
        groups[content_key].append(memory)

    # Only return groups with duplicates
    return {k: v for k, v in groups.items() if len(v) > 1}

def cleanup_duplicates(dry_run=True):
    """
    Remove duplicate memories, keeping the most recent.

    Args:
        dry_run: If True, only show what would be deleted
    """
    if not check_helix_running():
        print("ERROR: HelixDB is not running. Start it with: helix push dev", file=sys.stderr)
        return 1

    memories = get_all_memories()

    if not memories:
        print("No memories found.")
        return 0

    duplicates = find_duplicates(memories)

    if not duplicates:
        print("No duplicates found.")
        return 0

    print(f"\nFound {len(duplicates)} groups of duplicates:\n")

    total_to_delete = 0

    for content_key, group in duplicates.items():
        print(f"Duplicate group ({len(group)} copies):")
        print(f"  Content preview: {content_key[:80]}...")
        print(f"  IDs: {[m.get('id') for m in group]}")

        # Keep the last one (most recent by ID)
        group_sorted = sorted(group, key=lambda m: m.get('id', ''))
        to_keep = group_sorted[-1]
        to_delete = group_sorted[:-1]

        print(f"  KEEP: {to_keep.get('id')}")
        print(f"  DELETE: {[m.get('id') for m in to_delete]}")
        print()

        total_to_delete += len(to_delete)

    if dry_run:
        print(f"DRY RUN: Would delete {total_to_delete} duplicate memories.")
        print("Run with --execute to actually delete them.")
    else:
        print(f"\nDeleting {total_to_delete} duplicate memories...")
        deleted = 0
        failed = 0

        for content_key, group in duplicates.items():
            # Keep the last one (most recent by ID)
            group_sorted = sorted(group, key=lambda m: m.get('id', ''))
            to_keep = group_sorted[-1]
            to_delete = group_sorted[:-1]

            # For preferences, link before deleting
            if to_keep.get('category') == 'preference':
                for old_memory in to_delete:
                    old_id = old_memory.get('id')
                    if old_id:
                        # Link new to old with "supersedes" before deletion
                        link_related_memories(
                            from_id=to_keep.get('id'),
                            to_id=old_id,
                            relationship="supersedes",
                            strength=10
                        )

            # Delete duplicates
            for memory in to_delete:
                memory_id = memory.get('id')
                if memory_id:
                    if delete_memory(memory_id):
                        deleted += 1
                        print(f"  ✓ Deleted {memory_id}")
                    else:
                        failed += 1
                        print(f"  ✗ Failed to delete {memory_id}")

        print(f"\nDone! Deleted {deleted} memories, {failed} failed.")

    return 0

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Clean up duplicate memories")
    parser.add_argument("--execute", action="store_true", help="Actually delete duplicates (default is dry-run)")

    args = parser.parse_args()

    sys.exit(cleanup_duplicates(dry_run=not args.execute))

if __name__ == "__main__":
    main()
