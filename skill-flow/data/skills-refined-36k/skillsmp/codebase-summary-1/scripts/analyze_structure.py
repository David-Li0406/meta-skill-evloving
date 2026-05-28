#!/usr/bin/env python3
"""
Analyze codebase directory structure and generate a structured tree report.
Identifies key directories, file types, and project patterns.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# Common directories to skip
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv', 'env',
    '.idea', '.vscode', 'dist', 'build', 'target', '.next', '.nuxt',
    'coverage', '.pytest_cache', '.mypy_cache', '.tox', 'eggs',
    '*.egg-info', '.sass-cache', 'bower_components', 'vendor',
    '.bundle', '.cargo', 'Pods', '.gradle', '.mvn'
}

# Key project files that indicate project type
PROJECT_MARKERS = {
    'package.json': 'Node.js/JavaScript',
    'requirements.txt': 'Python',
    'setup.py': 'Python',
    'pyproject.toml': 'Python',
    'Cargo.toml': 'Rust',
    'go.mod': 'Go',
    'pom.xml': 'Java/Maven',
    'build.gradle': 'Java/Gradle',
    'Gemfile': 'Ruby',
    'composer.json': 'PHP',
    'pubspec.yaml': 'Dart/Flutter',
    'Package.swift': 'Swift',
    'CMakeLists.txt': 'C/C++',
    'Makefile': 'Make-based',
    'Dockerfile': 'Docker',
    'docker-compose.yml': 'Docker Compose',
    'docker-compose.yaml': 'Docker Compose',
}


def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    name = path.name
    if name.startswith('.') and name not in {'.github', '.gitlab'}:
        return True
    return name in SKIP_DIRS


def get_file_extension(path: Path) -> str:
    """Get file extension, handling special cases."""
    if path.suffix:
        return path.suffix.lower()
    return '(no extension)'


def analyze_directory(root_path: Path, max_depth: int = 4) -> dict:
    """
    Analyze directory structure.

    Returns dict with:
    - tree: nested directory structure
    - file_types: count by extension
    - project_types: detected project types
    - key_dirs: important directories found
    - stats: overall statistics
    """
    results = {
        'tree': {},
        'file_types': defaultdict(int),
        'project_types': set(),
        'key_dirs': [],
        'stats': {
            'total_files': 0,
            'total_dirs': 0,
            'max_depth_reached': 0
        }
    }

    def build_tree(path: Path, depth: int = 0) -> dict:
        if depth > max_depth:
            return {'...': 'max depth reached'}

        results['stats']['max_depth_reached'] = max(
            results['stats']['max_depth_reached'], depth
        )

        tree = {}
        try:
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return {'error': 'permission denied'}

        dirs = []
        files = []

        for entry in entries:
            if should_skip(entry):
                continue

            if entry.is_dir():
                dirs.append(entry)
                results['stats']['total_dirs'] += 1
            elif entry.is_file():
                files.append(entry)
                results['stats']['total_files'] += 1

                ext = get_file_extension(entry)
                results['file_types'][ext] += 1

                # Check for project markers
                if entry.name in PROJECT_MARKERS:
                    results['project_types'].add(PROJECT_MARKERS[entry.name])

        # Identify key directories
        dir_names = {d.name for d in dirs}
        key_indicators = {'src', 'lib', 'app', 'api', 'tests', 'test', 'docs', 'config'}
        if dir_names & key_indicators:
            results['key_dirs'].append(str(path.relative_to(root_path) or '.'))

        # Build tree for directories
        for d in dirs:
            tree[d.name + '/'] = build_tree(d, depth + 1)

        # Add files (summarized if too many)
        if len(files) > 20:
            by_ext = defaultdict(list)
            for f in files:
                by_ext[get_file_extension(f)].append(f.name)
            tree['_files'] = {ext: f'{len(names)} files' for ext, names in by_ext.items()}
        else:
            for f in files:
                tree[f.name] = None

        return tree

    results['tree'] = build_tree(root_path)
    results['project_types'] = list(results['project_types'])
    results['file_types'] = dict(sorted(
        results['file_types'].items(),
        key=lambda x: -x[1]
    )[:20])  # Top 20 extensions

    return results


def format_tree(tree: dict, prefix: str = '') -> str:
    """Format tree dict as text."""
    lines = []
    items = list(tree.items())

    for i, (name, subtree) in enumerate(items):
        is_last = i == len(items) - 1
        connector = '└── ' if is_last else '├── '

        if name == '_files':
            for ext, count in subtree.items():
                lines.append(f'{prefix}{connector}[{ext}: {count}]')
        elif subtree is None:
            lines.append(f'{prefix}{connector}{name}')
        elif isinstance(subtree, str):
            lines.append(f'{prefix}{connector}{name} ({subtree})')
        else:
            lines.append(f'{prefix}{connector}{name}')
            extension = '    ' if is_last else '│   '
            lines.append(format_tree(subtree, prefix + extension))

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze codebase directory structure'
    )
    parser.add_argument('path', nargs='?', default='.', help='Path to analyze')
    parser.add_argument('--depth', type=int, default=4, help='Max depth (default: 4)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--output', '-o', help='Output file path')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f'Error: Path does not exist: {root}', file=sys.stderr)
        sys.exit(1)

    results = analyze_directory(root, args.depth)

    if args.json:
        output = json.dumps(results, indent=2)
    else:
        output = f"""# Codebase Structure Analysis

## Project Types Detected
{', '.join(results['project_types']) or 'None identified'}

## Statistics
- Total files: {results['stats']['total_files']}
- Total directories: {results['stats']['total_dirs']}
- Analysis depth: {results['stats']['max_depth_reached']}

## Top File Types
{chr(10).join(f'- {ext}: {count}' for ext, count in list(results['file_types'].items())[:10])}

## Key Directories
{chr(10).join(f'- {d}' for d in results['key_dirs']) or 'None identified'}

## Directory Tree

```
{root.name}/
{format_tree(results['tree'])}
```
"""

    if args.output:
        Path(args.output).write_text(output)
        print(f'Output written to {args.output}')
    else:
        print(output)


if __name__ == '__main__':
    main()
