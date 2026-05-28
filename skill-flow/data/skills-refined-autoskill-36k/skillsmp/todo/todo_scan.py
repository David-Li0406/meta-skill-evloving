#!/usr/bin/env python3
"""
Todo Scanner - Scans codebase for TODO and CLAUDE comments.

Saves tokens by performing code scanning in Python instead of having Claude read all files.

Usage:
    python .claude/skills/todo/todo_scan.py [--json] [--untracked-only] [--no-github]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class TodoItem:
    """A TODO found in code."""
    file: str
    line: int
    marker: str  # TODO or CLAUDE
    issue_id: str | None  # #123 or TC1 or None
    content: str
    context_before: str
    context_after: str


@dataclass
class TodoFile:
    """A file with 'todo' in the name."""
    path: str
    has_new_entries: bool
    in_todo_folder: bool


@dataclass
class TodoFileEntry:
    """An entry in a todo file that references a GitHub Issue."""
    file: str
    line: int
    issue_num: str
    status: str  # open, in-progress, investigating, etc.
    description: str


def find_project_root() -> Path:
    """Find project root by looking for .git or .claude folder."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / '.git').exists() or (current / '.claude').exists():
            return current
        current = current.parent
    return Path.cwd()


def scan_code_todos(directories: list[str], project_root: Path) -> list[TodoItem]:
    """Scan directories for TODO: and CLAUDE: comments."""
    todos: list[TodoItem] = []

    # Pattern: # TODO [ID]: text  or  # CLAUDE: text
    pattern = re.compile(
        r'#\s*(TODO|CLAUDE)\s*(?:\[([^\]]+)\])?\s*:?\s*(.*)$',
        re.IGNORECASE
    )

    for directory in directories:
        dir_path = project_root / directory
        if not dir_path.exists():
            continue

        for file_path in dir_path.rglob('*.py'):
            if '__pycache__' in str(file_path) or '.venv' in str(file_path):
                continue

            try:
                lines = file_path.read_text(encoding='utf-8').splitlines()
            except (UnicodeDecodeError, PermissionError):
                continue

            for i, line in enumerate(lines):
                match = pattern.search(line)
                if match:
                    marker = match.group(1).upper()
                    issue_id = match.group(2)
                    content = match.group(3).strip()

                    context_before = '\n'.join(lines[max(0, i-2):i])
                    context_after = '\n'.join(lines[i+1:min(len(lines), i+3)])

                    rel_path = str(file_path.relative_to(project_root))

                    todos.append(TodoItem(
                        file=rel_path,
                        line=i + 1,
                        marker=marker,
                        issue_id=issue_id,
                        content=content,
                        context_before=context_before,
                        context_after=context_after
                    ))

    return todos


def find_todo_files(project_root: Path) -> list[TodoFile]:
    """Find all files with 'todo' in the filename."""
    todo_files: list[TodoFile] = []
    seen: set[str] = set()

    for pattern in ['**/*todo*', '**/*TODO*']:
        for file_path in project_root.glob(pattern):
            if file_path.is_dir():
                continue
            if '__pycache__' in str(file_path) or '.venv' in str(file_path):
                continue
            if '.git' in str(file_path):
                continue
            if '.claude' in str(file_path):
                continue

            rel_path = str(file_path.relative_to(project_root))
            if rel_path in seen:
                continue
            seen.add(rel_path)

            in_todo_folder = rel_path.startswith('todo/') or rel_path.startswith('todo\\')

            # Skip requirements/documentation/settings files for "new entries" detection
            is_docs_file = any(x in rel_path.lower() for x in ['requirements', 'readme', 'settings', 'skill.md'])

            has_new_entries = False
            if not is_docs_file:
                try:
                    content = file_path.read_text(encoding='utf-8').lower()
                    has_new_entries = 'new entries' in content or 'new entry' in content
                except (UnicodeDecodeError, PermissionError):
                    pass

            todo_files.append(TodoFile(
                path=rel_path,
                has_new_entries=has_new_entries,
                in_todo_folder=in_todo_folder
            ))

    return todo_files


def parse_todo_file_entries(todo_files: list[TodoFile], project_root: Path) -> list[TodoFileEntry]:
    """Parse todo files for entries that reference GitHub Issues."""
    entries: list[TodoFileEntry] = []

    # Pattern for markdown table rows with issue links: | [#123](url) | status | ... |
    # or just | #123 | status | ... |
    table_pattern = re.compile(
        r'\|\s*\[?#?(\d+)\]?(?:\([^)]+\))?\s*\|\s*(\w+(?:-\w+)?)\s*\|.*\|\s*(.+?)\s*\|',
        re.IGNORECASE
    )

    for todo_file in todo_files:
        file_path = project_root / todo_file.path
        if not file_path.exists():
            continue

        try:
            lines = file_path.read_text(encoding='utf-8').splitlines()
        except (UnicodeDecodeError, PermissionError):
            continue

        for i, line in enumerate(lines):
            match = table_pattern.search(line)
            if match:
                issue_num = match.group(1)
                status = match.group(2).lower()
                description = match.group(3).strip()

                entries.append(TodoFileEntry(
                    file=todo_file.path,
                    line=i + 1,
                    issue_num=issue_num,
                    status=status,
                    description=description
                ))

    return entries


def get_github_issues() -> list[dict]:
    """Get list of all open GitHub issues."""
    try:
        result = subprocess.run(
            ['gh', 'issue', 'list', '--state', 'open',
             '--limit', '100', '--json', 'number,title,state,labels'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return []


@dataclass
class SyncResult:
    """Result of sync check between code/files and GitHub."""
    # Code TODOs
    code_missing_in_github: list[tuple[TodoItem, str]]  # (todo, reason)
    code_missing_in_code: list[dict]  # GitHub issues with todo:code but no code ref
    code_stale: list[tuple[TodoItem, dict]]  # (todo, closed_issue)
    code_synced: int
    # File entries
    file_missing_in_github: list[tuple[TodoFileEntry, str]]  # (entry, reason)
    file_missing_in_file: list[dict]  # GitHub issues with todo:file but no file entry
    file_stale: list[tuple[TodoFileEntry, dict]]  # (entry, closed_issue)
    file_status_mismatch: list[tuple[TodoFileEntry, dict, str]]  # (entry, issue, expected)
    file_synced: int
    # Orphan issues (have 'todo' label but no source label)
    orphan_issues: list[dict]  # GitHub issues with todo but no todo:code or todo:file


def check_sync(
    code_todos: list[TodoItem],
    file_entries: list[TodoFileEntry],
    github_issues: list[dict]
) -> SyncResult:
    """Check for inconsistencies between code/files and GitHub Issues."""
    # Build lookup maps
    github_by_num: dict[str, dict] = {str(i['number']): i for i in github_issues}
    github_with_todo_label = {
        str(i['number']): i for i in github_issues
        if any(l.get('name') == 'todo' for l in i.get('labels', []))
    }
    github_with_code_label = {
        str(i['number']): i for i in github_issues
        if any(l.get('name') == 'todo:code' for l in i.get('labels', []))
    }
    github_with_file_label = {
        str(i['number']): i for i in github_issues
        if any(l.get('name') == 'todo:file' for l in i.get('labels', []))
    }

    # === Check code TODOs ===
    code_missing_in_github: list[tuple[TodoItem, str]] = []
    code_stale: list[tuple[TodoItem, dict]] = []
    code_synced = 0
    code_issue_refs: set[str] = set()

    for todo in code_todos:
        if not todo.issue_id:
            continue

        # Normalize issue ID (remove # prefix)
        issue_num = todo.issue_id.lstrip('#')

        # Skip non-numeric IDs (like TC1, TC2)
        if not issue_num.isdigit():
            continue

        code_issue_refs.add(issue_num)

        if issue_num not in github_by_num:
            code_missing_in_github.append((todo, "issue does not exist"))
        elif issue_num not in github_with_todo_label:
            code_missing_in_github.append((todo, "issue exists but missing 'todo' label"))
        else:
            issue = github_by_num[issue_num]
            if issue.get('state') == 'CLOSED':
                code_stale.append((todo, issue))
            else:
                code_synced += 1

    # Find GitHub issues with todo:code label but no code reference
    code_missing_in_code: list[dict] = []
    for issue_num, issue in github_with_code_label.items():
        if issue_num not in code_issue_refs and issue.get('state') != 'CLOSED':
            code_missing_in_code.append(issue)

    # === Check file entries ===
    file_missing_in_github: list[tuple[TodoFileEntry, str]] = []
    file_stale: list[tuple[TodoFileEntry, dict]] = []
    file_status_mismatch: list[tuple[TodoFileEntry, dict, str]] = []
    file_synced = 0
    file_issue_refs: set[str] = set()

    for entry in file_entries:
        issue_num = entry.issue_num
        file_issue_refs.add(issue_num)

        if issue_num not in github_by_num:
            file_missing_in_github.append((entry, "issue does not exist"))
        elif issue_num not in github_with_todo_label:
            file_missing_in_github.append((entry, "issue exists but missing 'todo' label"))
        else:
            issue = github_by_num[issue_num]
            gh_state = issue.get('state', '').upper()
            gh_labels = [l.get('name', '') for l in issue.get('labels', [])]
            gh_in_progress = 'in-progress' in gh_labels

            if gh_state == 'CLOSED':
                file_stale.append((entry, issue))
            else:
                # Check status mismatch
                file_status = entry.status.lower()
                if file_status == 'in-progress' and not gh_in_progress:
                    file_status_mismatch.append((entry, issue, "file says 'in-progress' but GitHub lacks label"))
                elif file_status in ('open', 'investigating') and gh_in_progress:
                    file_status_mismatch.append((entry, issue, f"file says '{file_status}' but GitHub has 'in-progress' label"))
                else:
                    file_synced += 1

    # Find GitHub issues with todo:file label but no file entry
    file_missing_in_file: list[dict] = []
    for issue_num, issue in github_with_file_label.items():
        if issue_num not in file_issue_refs and issue.get('state') != 'CLOSED':
            file_missing_in_file.append(issue)

    # Find orphan issues: have 'todo' label but no 'todo:code' or 'todo:file' label
    orphan_issues: list[dict] = []
    for issue_num, issue in github_with_todo_label.items():
        if issue.get('state') == 'CLOSED':
            continue
        has_code_label = issue_num in github_with_code_label
        has_file_label = issue_num in github_with_file_label
        if not has_code_label and not has_file_label:
            orphan_issues.append(issue)

    return SyncResult(
        code_missing_in_github=code_missing_in_github,
        code_missing_in_code=code_missing_in_code,
        code_stale=code_stale,
        code_synced=code_synced,
        file_missing_in_github=file_missing_in_github,
        file_missing_in_file=file_missing_in_file,
        file_stale=file_stale,
        file_status_mismatch=file_status_mismatch,
        file_synced=file_synced,
        orphan_issues=orphan_issues
    )


def print_sync_report(sync_result: SyncResult) -> None:
    """Print sync report."""
    print("=" * 60)
    print("SYNC REPORT")
    print("=" * 60)
    print()

    has_issues = False

    # === Code TODOs ===
    if sync_result.code_missing_in_github:
        has_issues = True
        print(f"Code: Missing in GitHub ({len(sync_result.code_missing_in_github)}):")
        for todo, reason in sync_result.code_missing_in_github:
            print(f"  {todo.file}:{todo.line} - [{todo.issue_id}] {reason}")
        print()

    if sync_result.code_missing_in_code:
        has_issues = True
        print(f"Code: Missing in Code ({len(sync_result.code_missing_in_code)}):")
        for issue in sync_result.code_missing_in_code:
            print(f"  #{issue['number']} \"{issue['title']}\" - has todo:code label but no code reference")
        print()

    if sync_result.code_stale:
        has_issues = True
        print(f"Code: Stale TODOs ({len(sync_result.code_stale)}):")
        for todo, issue in sync_result.code_stale:
            print(f"  {todo.file}:{todo.line} - [{todo.issue_id}] issue is CLOSED - remove this TODO")
        print()

    # === File entries ===
    if sync_result.file_missing_in_github:
        has_issues = True
        print(f"File: Missing in GitHub ({len(sync_result.file_missing_in_github)}):")
        for entry, reason in sync_result.file_missing_in_github:
            print(f"  {entry.file}:{entry.line} - [#{entry.issue_num}] {reason}")
        print()

    if sync_result.file_missing_in_file:
        has_issues = True
        print(f"File: Missing in File ({len(sync_result.file_missing_in_file)}):")
        for issue in sync_result.file_missing_in_file:
            print(f"  #{issue['number']} \"{issue['title']}\" - has todo:file label but no file entry")
        print()

    if sync_result.file_stale:
        has_issues = True
        print(f"File: Stale Entries ({len(sync_result.file_stale)}):")
        for entry, issue in sync_result.file_stale:
            print(f"  {entry.file}:{entry.line} - [#{entry.issue_num}] issue is CLOSED - remove this entry")
        print()

    if sync_result.file_status_mismatch:
        has_issues = True
        print(f"File: Status Mismatch ({len(sync_result.file_status_mismatch)}):")
        for entry, issue, expected in sync_result.file_status_mismatch:
            print(f"  {entry.file}:{entry.line} - [#{entry.issue_num}] {expected}")
        print()

    # === Orphan issues ===
    if sync_result.orphan_issues:
        has_issues = True
        print(f"Orphan Issues ({len(sync_result.orphan_issues)}):")
        print("  (have 'todo' label but missing 'todo:code' or 'todo:file' source label)")
        for issue in sync_result.orphan_issues:
            print(f"  #{issue['number']} \"{issue['title']}\"")
        print()

    # === Summary ===
    if not has_issues:
        print("No inconsistencies found!")
        print()

    print(f"Synced: {sync_result.code_synced} code TODOs, {sync_result.file_synced} file entries")
    print()


def print_report(
    code_todos: list[TodoItem],
    todo_files: list[TodoFile],
    github_issues: list[dict],
    untracked_only: bool = False
) -> None:
    """Print human-readable report."""
    print("=" * 60)
    print("TODO SCAN REPORT")
    print("=" * 60)
    print()

    with_id = [t for t in code_todos if t.issue_id]
    without_id = [t for t in code_todos if not t.issue_id]

    # Check which IDs are GitHub issue numbers (start with #)
    github_issue_nums = {str(i['number']) for i in github_issues}
    in_github = [t for t in with_id if t.issue_id and t.issue_id.lstrip('#') in github_issue_nums]
    not_in_github = [t for t in with_id if t not in in_github]

    if not untracked_only:
        print(f"Code TODOs: {len(code_todos)}")
        print(f"  - With ID, in GitHub:     {len(in_github)}")
        print(f"  - With ID, NOT in GitHub: {len(not_in_github)}")
        print(f"  - Without ID:             {len(without_id)}")
        print(f"Todo files: {len(todo_files)}")
        print(f"GitHub Issues (open): {len(github_issues)}")
        print()

    if without_id:
        print("-" * 60)
        print("CODE TODOs WITHOUT ID (need ID assignment)")
        print("-" * 60)
        for todo in without_id:
            print(f"\n  {todo.file}:{todo.line}")
            print(f"  {todo.marker}: {todo.content}")
        print()

    if not_in_github and not untracked_only:
        print("-" * 60)
        print("CODE TODOs WITH ID BUT NOT IN GITHUB (need migration)")
        print("-" * 60)
        for todo in not_in_github:
            print(f"  [{todo.issue_id}] {todo.file}:{todo.line} - {todo.content[:50]}")
        print()

    if in_github and not untracked_only:
        print("-" * 60)
        print("CODE TODOs IN GITHUB")
        print("-" * 60)
        for todo in in_github:
            print(f"  [{todo.issue_id}] {todo.file}:{todo.line} - {todo.content[:50]}")
        print()

    if todo_files and not untracked_only:
        print("-" * 60)
        print("TODO FILES")
        print("-" * 60)
        not_in_folder = [f for f in todo_files if not f.in_todo_folder]
        with_new = [f for f in todo_files if f.has_new_entries]

        if not_in_folder:
            print("\n  NOT in todo/ folder:")
            for f in not_in_folder:
                print(f"    - {f.path}")

        if with_new:
            print("\n  Have 'new entries' section:")
            for f in with_new:
                print(f"    - {f.path}")

        print(f"\n  All ({len(todo_files)}):")
        for f in todo_files:
            markers = []
            if not f.in_todo_folder:
                markers.append("NOT IN FOLDER")
            if f.has_new_entries:
                markers.append("HAS NEW")
            suffix = f" [{', '.join(markers)}]" if markers else ""
            print(f"    - {f.path}{suffix}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description='Scan codebase for TODOs')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--untracked-only', action='store_true', help='Only show untracked TODOs')
    parser.add_argument('--no-github', action='store_true', help='Skip GitHub API call')
    parser.add_argument('--sync', action='store_true', help='Check sync between code and GitHub')
    args = parser.parse_args()

    project_root = find_project_root()
    directories = ['src', 'tests', 'docs']

    code_todos = scan_code_todos(directories, project_root)
    todo_files = find_todo_files(project_root)
    github_issues = [] if args.no_github else get_github_issues()

    if args.sync:
        if args.no_github:
            print("Error: --sync requires GitHub access (cannot use --no-github)")
            return 1
        file_entries = parse_todo_file_entries(todo_files, project_root)
        sync_result = check_sync(code_todos, file_entries, github_issues)
        if args.json:
            output = {
                'code': {
                    'missing_in_github': [
                        {'file': t.file, 'line': t.line, 'issue_id': t.issue_id, 'reason': r}
                        for t, r in sync_result.code_missing_in_github
                    ],
                    'missing_in_code': [
                        {'number': i['number'], 'title': i['title']}
                        for i in sync_result.code_missing_in_code
                    ],
                    'stale': [
                        {'file': t.file, 'line': t.line, 'issue_id': t.issue_id}
                        for t, _ in sync_result.code_stale
                    ],
                    'synced': sync_result.code_synced
                },
                'file': {
                    'missing_in_github': [
                        {'file': e.file, 'line': e.line, 'issue_num': e.issue_num, 'reason': r}
                        for e, r in sync_result.file_missing_in_github
                    ],
                    'missing_in_file': [
                        {'number': i['number'], 'title': i['title']}
                        for i in sync_result.file_missing_in_file
                    ],
                    'stale': [
                        {'file': e.file, 'line': e.line, 'issue_num': e.issue_num}
                        for e, _ in sync_result.file_stale
                    ],
                    'status_mismatch': [
                        {'file': e.file, 'line': e.line, 'issue_num': e.issue_num, 'reason': r}
                        for e, _, r in sync_result.file_status_mismatch
                    ],
                    'synced': sync_result.file_synced
                },
                'orphan_issues': [
                    {'number': i['number'], 'title': i['title']}
                    for i in sync_result.orphan_issues
                ]
            }
            print(json.dumps(output, indent=2))
        else:
            print_sync_report(sync_result)
        return 0

    if args.json:
        output = {
            'code_todos': [asdict(t) for t in code_todos],
            'todo_files': [asdict(f) for f in todo_files],
            'github_issues': github_issues,
            'summary': {
                'total_code_todos': len(code_todos),
                'tracked': len([t for t in code_todos if t.issue_id]),
                'untracked': len([t for t in code_todos if not t.issue_id]),
                'todo_files': len(todo_files),
                'github_issues': len(github_issues)
            }
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(code_todos, todo_files, github_issues, args.untracked_only)

    return 0


if __name__ == '__main__':
    sys.exit(main())