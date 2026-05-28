#!/usr/bin/env python3
"""
Memory Consolidation

Finds and merges similar memories to reduce redundancy.
Keeps the highest-importance version and merges content.

Example:
- Memory A: "User prefers Playwright" (importance 8)
- Memory B: "Use Playwright over Puppeteer" (importance 7)
- Consolidated: Single memory with best content, importance 8
"""

import sys
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

sys.path.insert(0, str(Path(__file__).parent / "hooks"))

from common import (
    check_helix_running,
    get_all_memories,
    delete_memory,
    store_memory,
    store_memory_embedding,
    generate_simple_embedding
)


def similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def extract_key_phrases(content: str) -> set:
    """Extract key phrases/words from content."""
    # Simple word extraction
    words = set(content.lower().split())
    # Remove common words
    stop = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
            'and', 'or', 'but', 'not', 'this', 'that', 'it', 'i', 'you'}
    return words - stop


def find_consolidation_groups(memories: list, threshold: float = 0.6) -> list:
    """
    Find groups of memories that can be consolidated.

    Args:
        memories: List of memory dicts
        threshold: Similarity threshold (0-1)

    Returns:
        List of groups, each group is a list of similar memories
    """
    # Group by category first
    by_category = defaultdict(list)
    for m in memories:
        by_category[m.get('category', 'unknown')].append(m)

    all_groups = []

    for category, cat_memories in by_category.items():
        # Skip if only one memory in category
        if len(cat_memories) < 2:
            continue

        # Find similar pairs within category
        used = set()

        for i, m1 in enumerate(cat_memories):
            if m1['id'] in used:
                continue

            group = [m1]
            used.add(m1['id'])

            c1 = m1.get('content', '')
            phrases1 = extract_key_phrases(c1)

            for j, m2 in enumerate(cat_memories[i+1:], i+1):
                if m2['id'] in used:
                    continue

                c2 = m2.get('content', '')
                phrases2 = extract_key_phrases(c2)

                # Check phrase overlap
                if phrases1 and phrases2:
                    overlap = len(phrases1 & phrases2) / min(len(phrases1), len(phrases2))
                else:
                    overlap = 0

                # Check string similarity
                sim = similarity(c1[:200], c2[:200])

                # Consider similar if either metric is high
                if overlap > threshold or sim > threshold:
                    group.append(m2)
                    used.add(m2['id'])

            if len(group) > 1:
                all_groups.append(group)

    return all_groups


def merge_memories(group: list) -> dict:
    """
    Merge a group of similar memories into one.

    Keeps:
    - Highest importance
    - Best (longest meaningful) content
    - Combined tags
    """
    # Sort by importance (desc), then content length (desc)
    sorted_group = sorted(
        group,
        key=lambda m: (m.get('importance', 0), len(m.get('content', ''))),
        reverse=True
    )

    best = sorted_group[0]

    # Combine unique tags
    all_tags = set()
    for m in group:
        tags = m.get('tags', '').split(',')
        all_tags.update(t.strip() for t in tags if t.strip())

    return {
        'content': best.get('content', ''),
        'category': best.get('category', 'unknown'),
        'importance': best.get('importance', 5),
        'tags': ','.join(sorted(all_tags))
    }


def consolidate(dry_run: bool = True):
    """
    Run memory consolidation.

    Args:
        dry_run: If True, show what would happen without making changes
    """
    if not check_helix_running():
        print("ERROR: HelixDB not running")
        return

    memories = get_all_memories()
    print(f"\n{'='*60}")
    print("MEMORY CONSOLIDATION")
    print(f"{'='*60}\n")
    print(f"Total memories: {len(memories)}")

    groups = find_consolidation_groups(memories)

    if not groups:
        print("No consolidation candidates found.")
        return

    print(f"Found {len(groups)} groups to consolidate:\n")

    total_to_remove = 0

    for i, group in enumerate(groups, 1):
        print(f"Group {i} ({len(group)} memories):")
        for m in group:
            content = m.get('content', '')[:60].replace('\n', ' ')
            imp = m.get('importance', 0)
            print(f"  [{imp}] {m['id'][:8]}... {content}...")

        merged = merge_memories(group)
        print(f"  -> Merged: [{merged['importance']}] {merged['content'][:60]}...")
        print()

        total_to_remove += len(group) - 1  # Keep one, remove rest

    print(f"Would consolidate {sum(len(g) for g in groups)} memories into {len(groups)}")
    print(f"Net reduction: {total_to_remove} memories\n")

    if dry_run:
        print("DRY RUN - use --execute to apply")
    else:
        print("Executing consolidation...")
        created = 0
        deleted = 0

        for group in groups:
            merged = merge_memories(group)

            # Create new consolidated memory
            new_id = store_memory(
                content=merged['content'],
                category=merged['category'],
                importance=merged['importance'],
                tags=merged['tags']
            )

            if new_id:
                created += 1
                # Add embedding
                embedding = generate_simple_embedding(merged['content'])
                store_memory_embedding(new_id, embedding, merged['content'])

                # Delete old memories
                for m in group:
                    if delete_memory(m['id']):
                        deleted += 1

        print(f"Created {created} consolidated memories")
        print(f"Deleted {deleted} old memories")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Consolidate similar memories")
    parser.add_argument("--execute", action="store_true",
                       help="Actually consolidate (default is dry-run)")
    parser.add_argument("--threshold", type=float, default=0.6,
                       help="Similarity threshold 0-1 (default 0.6)")

    args = parser.parse_args()

    consolidate(dry_run=not args.execute)


if __name__ == "__main__":
    main()
