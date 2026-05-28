#!/usr/bin/env python3
"""
Garbage Review - Memory Cleanup Tool

Reviews existing memories and identifies:
1. Garbage (code snippets, raw outputs, meaningless content)
2. Duplicates
3. Low-value entries

Generates a report and optionally rewrites garbage as high-level summaries.

Usage:
    python3 garbage_review.py [--fix] [--delete-garbage]
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent / "hooks"))

from common import (
    check_helix_running,
    get_all_memories,
    delete_memory,
    store_memory,
    llm_generate,
    extract_json_array
)


def is_garbage(content: str) -> tuple[bool, str]:
    """
    Check if memory content is garbage.
    Returns (is_garbage, reason).
    """
    if not content:
        return True, "empty"

    # Too short
    if len(content) < 30:
        return True, "too_short"

    # Code patterns - must be at line start or after newline to avoid false positives
    code_line_patterns = [
        'def ', 'class ', 'const ', 'let ', 'var ',
        '<?php', '<?=', '#!/',
        '{ return', '=> {', ') {', '});',
        'console.log(', 'print("', 'echo $',
    ]
    for pattern in code_line_patterns:
        # Check if pattern appears at start of line
        if f"\n{pattern}" in content or content.startswith(pattern):
            return True, f"code_pattern:{pattern.strip()}"

    # HTML/template patterns
    html_patterns = ['<div', '<span', '<script', '</div>', '<?=']
    html_count = sum(1 for p in html_patterns if p in content)
    if html_count >= 2:
        return True, "html_template"

    # Import statements (only if multiple)
    import_count = content.count('\nimport ') + content.count('\nfrom ')
    if import_count >= 2:
        return True, "multiple_imports"

    # Function definitions
    if content.count('function ') >= 2 or content.count('def ') >= 2:
        return True, "multiple_functions"

    # Raw output patterns - be specific to avoid markdown
    output_patterns = [
        'Exit code:', 'stdout:', 'stderr:',
        '[FAIL]', '[ERROR]',
        'Traceback (most recent',
        'npm WARN', 'npm ERR!',
        '>>> ', '... ',  # Python REPL
    ]
    for pattern in output_patterns:
        if pattern in content:
            return True, f"raw_output:{pattern}"

    # Heavy separator patterns (likely copy-pasted output)
    if content.count('===') >= 3 or content.count('---') >= 5:
        return True, "heavy_separators"

    # JSON/config patterns
    if content.strip().startswith('{') or content.strip().startswith('['):
        return True, "json_blob"

    # Path-heavy content
    path_count = content.count('/Users/') + content.count('/home/')
    if path_count > 2:
        return True, "path_heavy"

    # Low alphabetic ratio (likely data/code)
    alpha_count = sum(1 for c in content if c.isalpha())
    if len(content) > 50 and alpha_count / len(content) < 0.4:
        return True, "low_alpha_ratio"

    return False, ""


def find_duplicates(memories: list) -> dict:
    """Find duplicate or near-duplicate memories."""
    duplicates = defaultdict(list)

    for i, m1 in enumerate(memories):
        c1 = m1.get("content", "").lower()[:100]
        for m2 in memories[i+1:]:
            c2 = m2.get("content", "").lower()[:100]
            # Simple similarity: first 100 chars match
            if c1 == c2 or (len(c1) > 50 and c1[:50] == c2[:50]):
                key = c1[:50]
                if m1["id"] not in [x["id"] for x in duplicates[key]]:
                    duplicates[key].append(m1)
                if m2["id"] not in [x["id"] for x in duplicates[key]]:
                    duplicates[key].append(m2)

    return dict(duplicates)


def summarize_garbage(garbage_memories: list) -> list:
    """Try to extract value from garbage memories using LLM (Ollama or Haiku)."""
    if not garbage_memories:
        return []

    # Group garbage by category/tags
    content_sample = "\n".join([
        f"- {m.get('content', '')[:200]}"
        for m in garbage_memories[:20]
    ])

    prompt = f'''These memories were flagged as low-quality (code snippets, raw outputs).
Extract any high-level insights or summaries that might be valuable.

Garbage memories:
{content_sample}

For each valuable insight found, return:
[{{"content": "High-level summary in English", "category": "fact|solution|insight", "importance": 5-7, "tags": "recovered"}}]

If nothing valuable, return: []'''

    output, provider = llm_generate(prompt, timeout=60)
    if output:
        print(f"   Using LLM: {provider}")
        return extract_json_array(output)
    return []


def main():
    parser = argparse.ArgumentParser(description="Review and clean garbage memories")
    parser.add_argument("--fix", action="store_true", help="Try to recover value from garbage")
    parser.add_argument("--delete-garbage", action="store_true", help="Delete identified garbage")
    parser.add_argument("--delete-duplicates", action="store_true", help="Delete duplicate memories")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without doing it")

    args = parser.parse_args()

    if not check_helix_running():
        print("ERROR: HelixDB not running", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("🗑️  GARBAGE REVIEW - Memory Cleanup Tool")
    print("=" * 60)

    # Get all memories
    memories = get_all_memories()
    print(f"\nTotal memories: {len(memories)}")

    # Identify garbage
    garbage = []
    clean = []
    garbage_reasons = defaultdict(int)

    for m in memories:
        is_garb, reason = is_garbage(m.get("content", ""))
        if is_garb:
            garbage.append(m)
            garbage_reasons[reason] += 1
        else:
            clean.append(m)

    print(f"Clean: {len(clean)}")
    print(f"Garbage: {len(garbage)}")

    if garbage_reasons:
        print("\nGarbage breakdown:")
        for reason, count in sorted(garbage_reasons.items(), key=lambda x: -x[1]):
            print(f"  {reason}: {count}")

    # Find duplicates
    duplicates = find_duplicates(memories)
    dup_count = sum(len(v) for v in duplicates.values())
    print(f"\nDuplicates found: {len(duplicates)} groups ({dup_count} total)")

    # Show sample garbage
    if garbage:
        print("\n--- Sample Garbage (first 5) ---")
        for m in garbage[:5]:
            content = m.get("content", "")[:80].replace("\n", " ")
            print(f"  [{m.get('id', '?')[:8]}] {content}...")

    # Show sample duplicates
    if duplicates:
        print("\n--- Sample Duplicates (first 3 groups) ---")
        for key, mems in list(duplicates.items())[:3]:
            print(f"  Group: {key[:40]}...")
            for m in mems[:2]:
                print(f"    - {m.get('id', '?')[:8]}")

    # Actions
    if args.fix and garbage:
        print("\n🔧 Attempting to recover value from garbage...")
        recovered = summarize_garbage(garbage)
        if recovered:
            print(f"   Recovered {len(recovered)} insights")
            for r in recovered:
                print(f"   - {r.get('content', '')[:60]}...")
                if not args.dry_run:
                    store_memory(r["content"], r["category"], r["importance"], r.get("tags", ""), "recovered")
        else:
            print("   No value recovered")

    if args.delete_garbage and garbage:
        print(f"\n🗑️  Deleting {len(garbage)} garbage memories...")
        deleted = 0
        for m in garbage:
            if args.dry_run:
                print(f"   [DRY RUN] Would delete: {m.get('id', '?')[:8]}")
            else:
                if delete_memory(m.get("id")):
                    deleted += 1
        if not args.dry_run:
            print(f"   Deleted: {deleted}")

    if args.delete_duplicates and duplicates:
        print(f"\n🗑️  Deleting duplicates (keeping one per group)...")
        deleted = 0
        for key, mems in duplicates.items():
            # Keep first, delete rest
            for m in mems[1:]:
                if args.dry_run:
                    print(f"   [DRY RUN] Would delete duplicate: {m.get('id', '?')[:8]}")
                else:
                    if delete_memory(m.get("id")):
                        deleted += 1
        if not args.dry_run:
            print(f"   Deleted: {deleted}")

    # Summary
    print("\n" + "=" * 60)
    if args.dry_run:
        print("DRY RUN - no changes made")
    print(f"Review complete. Run with --delete-garbage or --delete-duplicates to clean up.")
    print("=" * 60)


if __name__ == "__main__":
    main()
