#!/usr/bin/env python3
"""
Dead Code Detector for Architecture Review

Detects potential dead code including:
- Orphaned files (not imported anywhere)
- Unused exports
- TODO/FIXME/HACK comments
- Large commented code blocks
- Empty directories
"""

import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

# Directories to skip
SKIP_DIRS: Set[str] = {
    'node_modules', '.git', 'build', 'dist', '.next', 'venv',
    '__pycache__', 'coverage', '.turbo', '.vercel', '.expo',
    'android', 'ios', '.architecture-review'
}

# Files that are entry points by convention (not dead even if not imported)
ENTRY_POINT_PATTERNS = [
    r'^index\.[jt]sx?$',
    r'^main\.[jt]sx?$',
    r'^app\.[jt]sx?$',
    r'^server\.[jt]sx?$',
    r'^page\.[jt]sx?$',
    r'^layout\.[jt]sx?$',
    r'^route\.[jt]sx?$',
    r'^middleware\.[jt]sx?$',
    r'^_app\.[jt]sx?$',
    r'^_document\.[jt]sx?$',
    r'\.config\.[jt]sx?$',
    r'\.test\.[jt]sx?$',
    r'\.spec\.[jt]sx?$',
    r'\.stories\.[jt]sx?$',
    r'\.d\.ts$',
]

# Comment patterns
TODO_PATTERNS = [
    (r'\bTODO\b', 'TODO'),
    (r'\bFIXME\b', 'FIXME'),
    (r'\bHACK\b', 'HACK'),
    (r'\bXXX\b', 'XXX'),
    (r'\bBUG\b', 'BUG'),
    (r'\bWARNING\b', 'WARNING'),
    (r'\bDEPRECATED\b', 'DEPRECATED'),
]

MAX_FILE_SIZE_BYTES = 512 * 1024
MAX_FILES_TO_PROCESS = 500

# Minimum lines of consecutive comments to flag as potential dead code
MIN_COMMENTED_BLOCK_SIZE = 10


def read_file_safe(file_path: Path) -> Optional[str]:
    """Read file with size limit."""
    try:
        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
            return None
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


def get_file_mtime(file_path: Path) -> Optional[str]:
    """Get file modification time as ISO string."""
    try:
        mtime = file_path.stat().st_mtime
        return datetime.fromtimestamp(mtime).isoformat()
    except Exception:
        return None


def is_entry_point_by_convention(filename: str, rel_path: str) -> bool:
    """Check if file is an entry point by naming convention."""
    # Check filename patterns
    for pattern in ENTRY_POINT_PATTERNS:
        if re.search(pattern, filename, re.IGNORECASE):
            return True

    # Check path patterns
    entry_dirs = ['pages/', 'app/', 'api/', 'routes/', 'handlers/', 'scripts/']
    for dir_pattern in entry_dirs:
        if dir_pattern in rel_path:
            return True

    return False


def find_commented_code_blocks(content: str) -> List[Dict[str, Any]]:
    """Find large blocks of commented code."""
    blocks = []
    lines = content.split('\n')

    in_block_comment = False
    comment_start = 0
    consecutive_comments = 0
    comment_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track block comments
        if '/*' in stripped and '*/' not in stripped:
            in_block_comment = True
            if consecutive_comments == 0:
                comment_start = i + 1
            consecutive_comments += 1
            comment_lines.append(line)
            continue
        elif '*/' in stripped:
            in_block_comment = False
            consecutive_comments += 1
            comment_lines.append(line)
            continue
        elif in_block_comment:
            consecutive_comments += 1
            comment_lines.append(line)
            continue

        # Track single-line comments
        if stripped.startswith('//') or stripped.startswith('#'):
            if consecutive_comments == 0:
                comment_start = i + 1
            consecutive_comments += 1
            comment_lines.append(line)
        else:
            # End of comment block
            if consecutive_comments >= MIN_COMMENTED_BLOCK_SIZE:
                # Check if it looks like code (has typical code patterns)
                comment_text = '\n'.join(comment_lines)
                if looks_like_code(comment_text):
                    blocks.append({
                        'line': comment_start,
                        'lines_count': consecutive_comments,
                        'preview': comment_text[:200] + '...' if len(comment_text) > 200 else comment_text
                    })
            consecutive_comments = 0
            comment_lines = []

    # Check final block
    if consecutive_comments >= MIN_COMMENTED_BLOCK_SIZE:
        comment_text = '\n'.join(comment_lines)
        if looks_like_code(comment_text):
            blocks.append({
                'line': comment_start,
                'lines_count': consecutive_comments,
                'preview': comment_text[:200] + '...' if len(comment_text) > 200 else comment_text
            })

    return blocks


def looks_like_code(text: str) -> bool:
    """Check if commented text looks like code rather than documentation."""
    code_patterns = [
        r'(?:const|let|var|function|class|import|export|return|if|else|for|while)\s',
        r'[a-zA-Z_]\w*\s*\(',  # Function calls
        r'=>',  # Arrow functions
        r'[{}\[\]];',  # Brackets and semicolons
        r'=\s*[\'"`]',  # Assignments
    ]

    matches = sum(1 for p in code_patterns if re.search(p, text))
    return matches >= 2


def extract_todo_comments(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract TODO, FIXME, HACK and similar comments."""
    todos = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        for pattern, tag in TODO_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                # Extract the comment content
                comment_match = re.search(r'(?://|/\*|\*|#)\s*(.*?' + pattern + r'.*?)(?:\*/)?$', line, re.IGNORECASE)
                comment = comment_match.group(1).strip() if comment_match else line.strip()

                todos.append({
                    'file': file_path,
                    'line': i + 1,
                    'tag': tag,
                    'content': comment[:200]
                })
                break  # Only count once per line

    return todos


def find_empty_directories(root_path: Path) -> List[str]:
    """Find directories that contain no code files."""
    empty_dirs = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]

        rel_dir = os.path.relpath(dirpath, root_path)

        # Check if directory has any code files (recursively would have been caught)
        has_code = any(
            f.endswith(('.ts', '.tsx', '.js', '.jsx'))
            for f in filenames
            if not f.startswith('.')
        )

        # If no code files and no subdirectories, it might be dead
        if not has_code and not dirnames and rel_dir != '.':
            empty_dirs.append(rel_dir)

    return empty_dirs


def build_import_graph(root_path: Path) -> Dict[str, Set[str]]:
    """Build a simple import graph to detect orphaned files."""
    imported_files: Set[str] = set()
    all_files: Set[str] = set()

    # Simple import pattern to extract module paths
    import_pattern = re.compile(
        r'(?:import|from|require)\s*\(?\s*[\'"]([^\'"]+)[\'"]'
    )

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]

        for filename in filenames:
            if not filename.endswith(('.ts', '.tsx', '.js', '.jsx')):
                continue

            file_path = Path(dirpath) / filename
            rel_path = str(file_path.relative_to(root_path))
            all_files.add(rel_path)

            content = read_file_safe(file_path)
            if not content:
                continue

            # Find all imports
            for match in import_pattern.finditer(content):
                import_path = match.group(1)

                # Skip external packages
                if not import_path.startswith('.') and not import_path.startswith('@/') and not import_path.startswith('~/'):
                    continue

                # Try to resolve the import
                if import_path.startswith('.'):
                    base_dir = file_path.parent
                    resolved = (base_dir / import_path).resolve()
                else:
                    # Alias - assume @/ or ~/ maps to src/
                    alias_path = import_path.replace('@/', 'src/').replace('~/', 'src/')
                    resolved = (root_path / alias_path).resolve()

                # Try different extensions
                for ext in ['', '.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx', '/index.js', '/index.jsx']:
                    test_path = Path(str(resolved) + ext)
                    if test_path.is_file():
                        try:
                            imported_files.add(str(test_path.relative_to(root_path)))
                        except ValueError:
                            pass
                        break

    return {'all': all_files, 'imported': imported_files}


def analyze_dead_code(root_dir: str) -> Dict[str, Any]:
    """Main analysis function."""
    root_path = Path(root_dir).resolve()

    if not root_path.is_dir():
        return {'error': f'Directory not found: {root_dir}'}

    result = {
        'root': root_path.name,
        'orphaned_files': [],
        'unused_exports': [],  # This requires dependency_mapper output
        'todo_fixme_comments': [],
        'todo_fixme_count': defaultdict(int),
        'commented_code_blocks': [],
        'empty_directories': [],
        'summary': {}
    }

    # Build import graph
    graph = build_import_graph(root_path)
    all_files = graph['all']
    imported_files = graph['imported']

    # Find orphaned files
    for file_path in all_files:
        filename = os.path.basename(file_path)

        # Skip if it's imported
        if file_path in imported_files:
            continue

        # Skip if it's an entry point by convention
        if is_entry_point_by_convention(filename, file_path):
            continue

        # This file is potentially orphaned
        full_path = root_path / file_path
        result['orphaned_files'].append({
            'path': file_path,
            'last_modified': get_file_mtime(full_path),
            'reason': 'no imports found'
        })

    # Scan for TODOs and commented code
    files_processed = 0
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]

        for filename in filenames:
            if not filename.endswith(('.ts', '.tsx', '.js', '.jsx')):
                continue

            if files_processed >= MAX_FILES_TO_PROCESS:
                break

            file_path = Path(dirpath) / filename
            rel_path = str(file_path.relative_to(root_path))

            content = read_file_safe(file_path)
            if not content:
                continue

            files_processed += 1

            # Extract TODOs
            todos = extract_todo_comments(content, rel_path)
            result['todo_fixme_comments'].extend(todos)
            for todo in todos:
                result['todo_fixme_count'][todo['tag']] += 1

            # Find commented code blocks
            blocks = find_commented_code_blocks(content)
            for block in blocks:
                result['commented_code_blocks'].append({
                    'file': rel_path,
                    **block
                })

        if files_processed >= MAX_FILES_TO_PROCESS:
            break

    # Find empty directories
    result['empty_directories'] = find_empty_directories(root_path)

    # Convert defaultdict
    result['todo_fixme_count'] = dict(result['todo_fixme_count'])

    # Build summary
    result['summary'] = {
        'orphaned_files_count': len(result['orphaned_files']),
        'total_todo_comments': len(result['todo_fixme_comments']),
        'todo_by_type': result['todo_fixme_count'],
        'commented_code_blocks_count': len(result['commented_code_blocks']),
        'empty_directories_count': len(result['empty_directories']),
        'files_analyzed': files_processed
    }

    # Limit output sizes
    result['orphaned_files'] = result['orphaned_files'][:50]
    result['todo_fixme_comments'] = result['todo_fixme_comments'][:100]
    result['commented_code_blocks'] = result['commented_code_blocks'][:50]

    return result


def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    result = analyze_dead_code(root_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
