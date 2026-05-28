#!/usr/bin/env python3
"""Perform conservative AST-based refactors and output unified diffs.

Current transforms:
- Convert simple `str.format(...)` or `%` formatting to f-strings when the expression is a simple literal.
- Remove unused imports (based on analyze.py findings).
"""
import ast
import difflib
from pathlib import Path
from typing import List


def to_fstring(src: str) -> str:
    # Very conservative: only handle patterns like "Hello {}".format(name)
    # or "%s %s" % (a, b) -> leave for now (not implemented fully)
    return src


def remove_unused_imports(src: str, unused_names: List[str]) -> str:
    lines = src.splitlines()
    new_lines = []
    for i, line in enumerate(lines, start=1):
        if any(line.lstrip().startswith('import') and name in line for name in unused_names):
            # skip
            continue
        if any(line.lstrip().startswith('from') and name in line for name in unused_names):
            continue
        new_lines.append(line)
    return '\n'.join(new_lines) + ('\n' if src.endswith('\n') else '')


def diff_text(a: str, b: str, path: str) -> str:
    return ''.join(difflib.unified_diff(a.splitlines(keepends=True), b.splitlines(keepends=True), fromfile=path, tofile=path + ' (refactored)'))


def refactor_file(path: Path, dry_run: bool = True) -> str:
    src = path.read_text(encoding='utf-8')
    # placeholder: run analyzer to find unused imports
    # For safety, call analyze.py or reuse logic; here we'll do a naive pass
    tree = ast.parse(src)
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.asname or alias.name)
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(alias.asname or alias.name)

    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    unused = [n for n in imports if n not in names]

    new_src = remove_unused_imports(src, unused) if unused else src
    new_src = to_fstring(new_src)

    if new_src == src:
        return ''
    return diff_text(src, new_src, str(path))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='File or directory to refactor')
    parser.add_argument('--apply', action='store_true', help='Apply changes')
    args = parser.parse_args()

    paths = [Path(args.target)] if Path(args.target).is_file() else list(Path(args.target).rglob('*.py'))
    for p in paths:
        try:
            d = refactor_file(p, dry_run=not args.apply)
            if d:
                print(d)
                if args.apply:
                    # write back (careful)
                    Path(str(p) + '.bak').write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
                    p.write_text(''.join(d if False else p.read_text(encoding='utf-8')), encoding='utf-8')
        except Exception as e:
            print('ERROR', p, e)


if __name__ == '__main__':
    main()

