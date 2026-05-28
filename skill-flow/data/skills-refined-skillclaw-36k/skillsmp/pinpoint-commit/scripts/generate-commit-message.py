#!/usr/bin/env python3
"""
Conventional Commit Message Generator

Analyzes changed files and generates a conventional commit message.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from collections import Counter


# Conventional commit types
COMMIT_TYPES = {
    'feat': 'New feature',
    'fix': 'Bug fix',
    'chore': 'Maintenance (deps, config, etc.)',
    'docs': 'Documentation',
    'refactor': 'Code refactoring',
    'test': 'Test changes',
    'perf': 'Performance improvement',
    'style': 'Code style changes (formatting)',
}


# Scope detection patterns
SCOPE_PATTERNS = {
    'src/app/(auth)/**/*': 'auth',
    'src/app/(app)/issues/**/*': 'issues',
    'src/app/(app)/machines/**/*': 'machines',
    'src/app/(app)/m/**/*': 'machines',
    'src/components/ui/*': 'ui',
    'src/lib/auth/*': 'auth',
    'src/server/db/*': 'db',
    'src/server/actions/*': 'actions',
    'supabase/migrations/*': 'migrations',
    'e2e/**/*': 'e2e',
    'src/test/**/*': 'tests',
}


def get_changed_files() -> List[str]:
    """Get list of changed files from git."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []


def get_diff_stats() -> Tuple[int, int]:
    """Get insertion/deletion counts from diff."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--shortstat'],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse: "3 files changed, 42 insertions(+), 10 deletions(-)"
        import re
        insertions = 0
        deletions = 0
        if 'insertion' in result.stdout:
            match = re.search(r'(\d+) insertion', result.stdout)
            if match:
                insertions = int(match.group(1))
        if 'deletion' in result.stdout:
            match = re.search(r'(\d+) deletion', result.stdout)
            if match:
                deletions = int(match.group(1))
        return insertions, deletions
    except subprocess.CalledProcessError:
        return 0, 0


def matches_pattern(filepath: str, pattern: str) -> bool:
    """Check if filepath matches a glob pattern."""
    from fnmatch import fnmatch
    return fnmatch(filepath, pattern)


def detect_scope(files: List[str]) -> Optional[str]:
    """Detect scope from changed files."""
    scope_votes = Counter()

    for filepath in files:
        for pattern, scope in SCOPE_PATTERNS.items():
            if matches_pattern(filepath, pattern):
                scope_votes[scope] += 1
                break

    # Return most common scope if any
    if scope_votes:
        return scope_votes.most_common(1)[0][0]
    return None


def detect_type(files: List[str]) -> str:
    """Detect commit type from changed files."""
    # Simple heuristics
    has_tests = any('test' in f or 'spec' in f for f in files)
    has_docs = any(f.endswith('.md') for f in files)
    has_migrations = any('migrations' in f for f in files)
    has_src = any(f.startswith('src/') for f in files)

    if has_docs and not has_src:
        return 'docs'
    elif has_tests and not has_src:
        return 'test'
    elif has_migrations:
        return 'chore'
    else:
        # Default to feat for src changes
        return 'feat'


def generate_description(files: List[str], scope: Optional[str]) -> str:
    """Generate commit description based on files changed."""
    # Group files by directory
    dirs = set()
    for f in files:
        parts = Path(f).parts
        if len(parts) > 2:
            dirs.add('/'.join(parts[:3]))

    if len(files) == 1:
        return f"Update {Path(files[0]).name}"
    elif scope:
        return f"Update {scope} functionality"
    else:
        return f"Update {len(files)} files"


def main():
    """Main entry point."""
    files = get_changed_files()

    if not files:
        print('{"error": "No files changed"}')
        return

    commit_type = detect_type(files)
    scope = detect_scope(files)
    description = generate_description(files, scope)
    insertions, deletions = get_diff_stats()

    # Build commit message
    if scope:
        title = f"{commit_type}({scope}): {description}"
    else:
        title = f"{commit_type}: {description}"

    # Generate body bullet points
    body_lines = []

    # Group files by type
    src_files = [f for f in files if f.startswith('src/')]
    test_files = [f for f in files if 'test' in f or 'spec' in f]
    doc_files = [f for f in files if f.endswith('.md')]
    config_files = [f for f in files if f in ['package.json', 'tsconfig.json', '.env.example']]

    if src_files:
        body_lines.append(f"- Update {len(src_files)} source file(s)")
    if test_files:
        body_lines.append(f"- Add/update {len(test_files)} test(s)")
    if doc_files:
        body_lines.append(f"- Update documentation")
    if config_files:
        body_lines.append(f"- Update configuration")

    # Output JSON
    import json
    output = {
        'title': title,
        'body': '\n'.join(body_lines),
        'type': commit_type,
        'scope': scope,
        'files': files,
        'stats': {
            'insertions': insertions,
            'deletions': deletions,
        }
    }

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
