#!/usr/bin/env python3
"""
File Tree Analyzer for Architecture Review

Generates annotated directory structure with metadata including:
- File types, sizes, and line counts
- File categorization (component, util, test, config, etc.)
- Flags for suspiciously large or empty files
"""

import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Set

# Directories to skip during analysis
SKIP_DIRS: Set[str] = {
    'node_modules', '.git', 'build', 'dist', '.next', 'venv',
    '__pycache__', 'coverage', '.turbo', '.vercel', '.expo',
    'android', 'ios', '.architecture-review'
}

# File extensions to analyze
CODE_EXTENSIONS: Set[str] = {
    '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
    '.json', '.md', '.yml', '.yaml', '.css', '.scss',
    '.html', '.graphql', '.gql', '.sql', '.prisma'
}

# Size limits
MAX_FILE_SIZE_BYTES = 512 * 1024  # 512KB
LARGE_FILE_THRESHOLD = 500  # lines
EMPTY_FILE_THRESHOLD = 5  # lines

# Category detection patterns
CATEGORY_PATTERNS: Dict[str, List[str]] = {
    'component': ['/components/', '/screens/', '/views/', '/pages/', '/app/'],
    'hook': ['/hooks/', 'use'],
    'util': ['/utils/', '/helpers/', '/lib/', '/common/'],
    'service': ['/services/', '/api/', '/clients/'],
    'store': ['/store/', '/redux/', '/zustand/', '/context/', '/providers/'],
    'test': ['.test.', '.spec.', '/__tests__/', '/test/', '/tests/'],
    'config': ['config', '.config.', 'rc.', 'settings'],
    'type': ['/types/', '.d.ts', '/interfaces/', '/models/'],
    'style': ['.css', '.scss', '.styled.', '.styles.'],
    'asset': ['/assets/', '/images/', '/icons/', '/fonts/'],
    'route': ['/routes/', '/router/', '/routing/'],
    'middleware': ['/middleware/', 'middleware.'],
}


def categorize_file(file_path: str, filename: str) -> str:
    """Determine the category of a file based on its path and name."""
    path_lower = file_path.lower()
    name_lower = filename.lower()

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if pattern in path_lower or pattern in name_lower:
                return category

    # Default categorization by extension
    ext = Path(filename).suffix.lower()
    if ext in {'.ts', '.tsx', '.js', '.jsx'}:
        return 'source'
    elif ext in {'.json'}:
        return 'data'
    elif ext in {'.md'}:
        return 'documentation'

    return 'other'


def count_lines(file_path: Path) -> int:
    """Count lines in a file safely."""
    try:
        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
            return -1  # File too large

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def analyze_directory(root_dir: str) -> Dict[str, Any]:
    """Analyze directory structure and generate metadata."""
    root_path = Path(root_dir).resolve()
    root_name = root_path.name

    result = {
        'root': root_name,
        'root_path': str(root_path),
        'total_files': 0,
        'total_lines': 0,
        'total_directories': 0,
        'tree': [],
        'by_extension': defaultdict(lambda: {'count': 0, 'lines': 0}),
        'by_category': defaultdict(list),
        'largest_files': [],
        'empty_files': [],
        'flagged_files': []
    }

    all_files_with_lines = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out skip directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]

        rel_dir = os.path.relpath(dirpath, root_path)
        if rel_dir == '.':
            rel_dir = ''

        # Add directory entry
        if rel_dir:
            result['tree'].append({
                'path': rel_dir,
                'type': 'directory',
                'category': None,
                'line_count': None
            })
            result['total_directories'] += 1

        for filename in filenames:
            # Skip hidden files and non-code files
            if filename.startswith('.'):
                continue

            ext = Path(filename).suffix.lower()
            if ext not in CODE_EXTENSIONS:
                continue

            file_path = Path(dirpath) / filename
            rel_path = os.path.relpath(file_path, root_path)

            # Count lines
            line_count = count_lines(file_path)

            # Categorize
            category = categorize_file(rel_path, filename)

            # Build tree entry
            tree_entry = {
                'path': rel_path,
                'type': 'file',
                'category': category,
                'line_count': line_count if line_count >= 0 else 'too_large',
                'extension': ext
            }
            result['tree'].append(tree_entry)

            # Update counters
            result['total_files'] += 1
            if line_count > 0:
                result['total_lines'] += line_count
                result['by_extension'][ext]['count'] += 1
                result['by_extension'][ext]['lines'] += line_count
                all_files_with_lines.append({'path': rel_path, 'lines': line_count, 'category': category})

            # Track by category
            result['by_category'][category].append(rel_path)

            # Flag files
            if line_count > LARGE_FILE_THRESHOLD:
                result['flagged_files'].append({
                    'path': rel_path,
                    'lines': line_count,
                    'reason': 'large_file',
                    'category': category
                })
            elif 0 < line_count <= EMPTY_FILE_THRESHOLD:
                result['empty_files'].append({
                    'path': rel_path,
                    'lines': line_count,
                    'reason': 'nearly_empty'
                })
            elif line_count == 0:
                result['empty_files'].append({
                    'path': rel_path,
                    'lines': 0,
                    'reason': 'empty'
                })

    # Sort and extract largest files
    all_files_with_lines.sort(key=lambda x: x['lines'], reverse=True)
    result['largest_files'] = all_files_with_lines[:20]

    # Convert defaultdicts to regular dicts for JSON serialization
    result['by_extension'] = dict(result['by_extension'])
    result['by_category'] = dict(result['by_category'])

    # Add summary stats
    result['summary'] = {
        'total_files': result['total_files'],
        'total_lines': result['total_lines'],
        'total_directories': result['total_directories'],
        'extensions_found': list(result['by_extension'].keys()),
        'categories_found': list(result['by_category'].keys()),
        'large_files_count': len([f for f in result['flagged_files'] if f['reason'] == 'large_file']),
        'empty_files_count': len(result['empty_files'])
    }

    return result


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

    if not os.path.isdir(root_dir):
        print(json.dumps({'error': f'Directory not found: {root_dir}'}, indent=2))
        sys.exit(1)

    result = analyze_directory(root_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
