#!/usr/bin/env python3
"""Apply unified diff patches to files safely.

This is a small helper that takes a unified diff and applies it, creating a .bak of the original.
"""
import sys
from pathlib import Path
import difflib


def apply_patch_from_diff(diff_text: str):
    # Naive: parse diff in chunks per file
    lines = diff_text.splitlines(keepends=True)
    # Find fromfile and tofile headers
    i = 0
    while i < len(lines):
        if lines[i].startswith('--- '):
            fromfile = lines[i].split(' ', 1)[1].strip()
            tofile = lines[i+1].split(' ', 1)[1].strip() if i+1 < len(lines) else fromfile
            # gather hunk
            j = i+2
            hunks = []
            while j < len(lines) and not lines[j].startswith('--- '):
                hunks.append(lines[j])
                j += 1
            # write the tofile contents by applying the hunk using difflib
            path = Path(fromfile)
            if not path.exists():
                print('SKIP missing', fromfile)
            else:
                orig = path.read_text(encoding='utf-8').splitlines(keepends=True)
                patched = list(difflib.restore(hunks, 2))
                bak = path.with_suffix(path.suffix + '.bak')
                bak.write_text(''.join(orig), encoding='utf-8')
                path.write_text(''.join(patched), encoding='utf-8')
            i = j
        else:
            i += 1


def main():
    data = sys.stdin.read()
    if not data:
        print('Expecting unified diff on stdin')
        return
    apply_patch_from_diff(data)


if __name__ == '__main__':
    main()

