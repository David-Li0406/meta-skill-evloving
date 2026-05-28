#!/usr/bin/env python3
"""Diagnose ~/.claude.json size by section."""

import json
import os

def estimate_tokens(text: str) -> int:
    """Rough estimate: 1 token ≈ 4 chars."""
    return len(text) // 4

def main():
    path = os.path.expanduser('~/.claude.json')

    if not os.path.exists(path):
        print("ERROR: ~/.claude.json not found")
        return

    file_size = os.path.getsize(path)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("=" * 60)
    print("CLAUDE.JSON DIAGNOSTIC")
    print("=" * 60)
    print(f"\nFile: {path}")
    print(f"Total size: {file_size:,} bytes ({file_size // 1024} KB)")
    print(f"Estimated tokens: ~{estimate_tokens(open(path).read()):,}")
    print(f"Token limit: 25,000")
    print()

    # Analyze sections
    sections = []
    for key, value in data.items():
        size = len(json.dumps(value))
        tokens = estimate_tokens(json.dumps(value))
        sections.append((key, size, tokens))

    # Sort by size descending
    sections.sort(key=lambda x: x[1], reverse=True)

    print(f"{'Section':<35} {'Size':>10} {'Tokens':>10} {'%':>6}")
    print("-" * 65)

    total_chars = sum(s[1] for s in sections)

    for key, size, tokens in sections:
        pct = (size / total_chars) * 100 if total_chars > 0 else 0
        size_str = f"{size:,}"
        tokens_str = f"~{tokens:,}"

        # Highlight large sections
        if pct > 20:
            marker = " <<<"
        elif pct > 10:
            marker = " <"
        else:
            marker = ""

        print(f"{key:<35} {size_str:>10} {tokens_str:>10} {pct:>5.1f}%{marker}")

    print("-" * 65)
    print(f"{'TOTAL':<35} {total_chars:>10,} {estimate_tokens(json.dumps(data)):>10,}")
    print()

    # Recommendations
    print("RECOMMENDATIONS:")
    print("-" * 40)

    cleanable = 0
    for key, size, tokens in sections:
        if key == 'cachedChangelog' and size > 1000:
            print(f"  - Clear '{key}' (safe, auto-regenerates)")
            cleanable += size
        elif key == 'projects' and size > 30000:
            print(f"  - Trim old entries in '{key}'")
            cleanable += size // 2
        elif key.startswith('cached') and size > 500:
            print(f"  - Clear '{key}' (cache, safe)")
            cleanable += size

    if cleanable > 0:
        print(f"\n  Potential savings: ~{cleanable:,} chars ({cleanable // 1024} KB)")
    else:
        print("  File looks clean!")

if __name__ == '__main__':
    main()
