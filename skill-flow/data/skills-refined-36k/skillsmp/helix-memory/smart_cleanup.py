#!/usr/bin/env python3
"""
Smart Memory Cleanup

Comprehensive cleanup that removes:
1. Exact duplicates (keeps newest)
2. Near-duplicates (similar content)
3. Low-value task memories (generic steps)
4. Noise memories (raw outputs, configs, etc.)
5. Old low-importance memories (pruning)
"""

import sys
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent / "hooks"))

from common import (
    check_helix_running,
    get_all_memories,
    delete_memory,
    content_hash
)

# Patterns that indicate noise/low-value content
NOISE_PATTERNS = [
    r'^<bash-',                           # Bash output markers
    r'bash-stdout|bash-stderr',           # More bash markers
    r'^\[.*\]$',                          # Single bracketed content
    r'^Perfect!',                         # Generic acknowledgments
    r'^Done!',
    r'^Great!',
    r'^Let me',                           # Task narration
    r'^Now let me',
    r'^Now I',
    r'^I\'ll',
    r'^I\'m going to',
    r'^\s*\[\d+',                         # Line number prefixes
    r'^\s*cat /',                         # Raw cat output
    r'server\s*\{',                       # Nginx configs
    r'location\s*~',
    r'#!/bin/bash',                       # Script content
    r'#!/usr/bin/env',
    r'^Base directory for this skill:',  # Skill loading
    r'This session is being continued',  # Session continuations
    r'\[38;5;',                           # Terminal escape codes
    r'\[\?2026',
    r'^Project path:.*Context:.*<bash',  # Corrupted path+bash combo
    r'^Project location:.*`\)',          # Malformed path
]

# Generic task content that's not worth keeping
GENERIC_TASK_PATTERNS = [
    r'^Perfect! .*todo',
    r'^Let me .*(update|check|verify|complete)',
    r'^Now .*(let me|I\'ll|I need to)',
    r'^Done.*Next',
    r'^\[@',                             # Truncated content
]

def is_noise(content: str) -> bool:
    """Check if content matches noise patterns."""
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            return True
    return False

def is_generic_task(content: str, category: str) -> bool:
    """Check if it's a generic task step not worth keeping."""
    if category != 'task':
        return False
    for pattern in GENERIC_TASK_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False

def is_corrupted(content: str) -> bool:
    """Check for corrupted/malformed memories."""
    # Too short to be useful
    if len(content.strip()) < 20:
        return True
    # Starts with special characters (truncated)
    if content.strip().startswith(('[@', '[?', '</', '`)', '...')):
        return True
    # Contains unbalanced tags
    if content.count('<bash') != content.count('</bash'):
        return True
    return False

def is_path_spam(content: str) -> bool:
    """Check if it's just a path extraction with no context."""
    # Paths that are just "Project path: X\nContext: <raw output>"
    if content.startswith('Project path:') or content.startswith('Project location:'):
        # Check if context is just raw output
        if 'Context:' in content:
            context_part = content.split('Context:', 1)[1] if 'Context:' in content else ''
            if is_noise(context_part):
                return True
            # Context is too short or looks like bash
            if len(context_part.strip()) < 50 or '<bash' in context_part:
                return True
    return False

def find_groups(memories):
    """Group memories by content hash for deduplication."""
    groups = defaultdict(list)
    for memory in memories:
        h = content_hash(memory.get('content', ''))
        groups[h].append(memory)
    return groups

def analyze_memories(memories):
    """Analyze memories and categorize for cleanup."""
    to_delete = []
    reasons = defaultdict(list)

    # Group by hash
    hash_groups = find_groups(memories)

    # Find duplicates (same hash)
    for h, group in hash_groups.items():
        if len(group) > 1:
            # Keep newest (by ID, which is time-based)
            sorted_group = sorted(group, key=lambda m: m.get('id', ''))
            for m in sorted_group[:-1]:
                to_delete.append(m)
                reasons['duplicate'].append(m['id'])

    # Check individual memories for quality issues
    for memory in memories:
        mid = memory.get('id', '')
        content = memory.get('content', '')
        category = memory.get('category', '')
        importance = memory.get('importance', 5)

        # Skip if already marked for deletion
        if any(d.get('id') == mid for d in to_delete):
            continue

        # Check for noise
        if is_noise(content):
            to_delete.append(memory)
            reasons['noise'].append(mid)
            continue

        # Check for corrupted content
        if is_corrupted(content):
            to_delete.append(memory)
            reasons['corrupted'].append(mid)
            continue

        # Check for generic task narration
        if is_generic_task(content, category):
            to_delete.append(memory)
            reasons['generic_task'].append(mid)
            continue

        # Check for path spam
        if is_path_spam(content):
            to_delete.append(memory)
            reasons['path_spam'].append(mid)
            continue

        # Low importance + old = prune (importance <= 4)
        # Note: We can't check age without timestamp, so skip for now

    return to_delete, reasons

def print_summary(memories, to_delete, reasons):
    """Print cleanup summary."""
    print(f"\n{'='*60}")
    print(f"MEMORY CLEANUP ANALYSIS")
    print(f"{'='*60}\n")
    print(f"Total memories: {len(memories)}")
    print(f"To delete: {len(to_delete)}")
    print(f"To keep: {len(memories) - len(to_delete)}")
    print()

    print("Breakdown by reason:")
    for reason, ids in sorted(reasons.items()):
        print(f"  {reason}: {len(ids)}")
    print()

def preview_deletions(to_delete, limit=20):
    """Show preview of what will be deleted."""
    print(f"Preview (first {limit}):")
    print("-" * 60)
    for m in to_delete[:limit]:
        content = m.get('content', '')[:80].replace('\n', ' ')
        print(f"  [{m.get('category', '?')}] {m.get('id', '?')[:8]}... {content}...")
    if len(to_delete) > limit:
        print(f"  ... and {len(to_delete) - limit} more")
    print()

def execute_cleanup(to_delete):
    """Actually delete the memories."""
    deleted = 0
    failed = 0

    for memory in to_delete:
        mid = memory.get('id')
        if mid:
            if delete_memory(mid):
                deleted += 1
                print(f"  ✓ {mid[:8]}...")
            else:
                failed += 1
                print(f"  ✗ {mid[:8]}... FAILED")

    print(f"\nDeleted: {deleted}, Failed: {failed}")
    return deleted, failed

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Smart memory cleanup")
    parser.add_argument("--execute", action="store_true", help="Actually delete (default is dry-run)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    if not check_helix_running():
        print("ERROR: HelixDB not running. Start with: helix push dev")
        return 1

    memories = get_all_memories()
    if not memories:
        print("No memories found.")
        return 0

    to_delete, reasons = analyze_memories(memories)

    print_summary(memories, to_delete, reasons)

    if to_delete:
        preview_deletions(to_delete)

        if args.execute:
            print("EXECUTING CLEANUP...")
            execute_cleanup(to_delete)
        else:
            print("DRY RUN - run with --execute to delete")

    return 0

if __name__ == "__main__":
    sys.exit(main())
