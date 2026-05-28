#!/usr/bin/env python3
"""Analyze Python files for simple refactor opportunities.

Produces a JSON report of candidates.
"""
import ast
import json
from pathlib import Path
from typing import List, Dict


def find_py_files(path: Path) -> List[Path]:
    return [p for p in path.rglob('*.py') if not any(part.startswith('.') for part in p.parts)]


def analyze_file(path: Path) -> Dict:
    src = path.read_text(encoding='utf-8')
    tree = ast.parse(src)
    findings = []

    # long functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # rough line count
            if getattr(node, 'end_lineno', None) and node.end_lineno - node.lineno > 80:
                findings.append({'type': 'long_function', 'name': node.name, 'lineno': node.lineno, 'length': node.end_lineno - node.lineno})

    # unused imports (naive: imported names not referenced)
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name.split('.')[0], node.lineno))
        if isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append((alias.asname or alias.name, node.lineno))

    # collect names
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    for name, lineno in imports:
        if name not in names:
            findings.append({'type': 'unused_import', 'name': name, 'lineno': lineno})

    return {'path': str(path), 'findings': findings}


def analyze_dir(target: str) -> Dict:
    path = Path(target)
    files = find_py_files(path)
    report = {'target': str(path), 'files_analyzed': len(files), 'results': []}
    for f in files:
        try:
            report['results'].append(analyze_file(f))
        except Exception as e:
            report['results'].append({'path': str(f), 'error': str(e)})
    return report


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Target file or directory to analyze')
    parser.add_argument('--json', help='Output JSON path', default=None)
    args = parser.parse_args()

    report = analyze_dir(args.target)
    out = json.dumps(report, indent=2)
    if args.json:
        Path(args.json).write_text(out, encoding='utf-8')
        print('Wrote', args.json)
    else:
        print(out)


if __name__ == '__main__':
    main()

