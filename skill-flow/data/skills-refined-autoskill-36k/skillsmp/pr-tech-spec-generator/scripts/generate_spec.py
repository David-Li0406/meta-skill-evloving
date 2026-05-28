#!/usr/bin/env python3
"""
Generate technical specification from GitHub PR.
Usage: python generate_spec.py <pr-url> [--repo-path <path>]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Execute shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    if check and result.returncode != 0:
        print(f"Error executing: {cmd}", file=sys.stderr)
        print(f"stderr: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def check_ref_exists(repo_path, ref):
    """Check if a git reference (branch, tag, commit) exists."""
    result = subprocess.run(
        f"git rev-parse --verify --quiet {ref}",
        shell=True,
        capture_output=True,
        cwd=repo_path
    )
    return result.returncode == 0


def resolve_branch_ref(repo_path, branch_name):
    """Resolve branch reference, trying remote, local, and commit hash.
    
    Returns the best available reference for the branch:
    1. origin/{branch} if remote branch exists
    2. {branch} if local branch exists
    3. {branch} as commit hash if it's a valid commit
    4. None if nothing exists
    """
    # Try remote branch first
    remote_ref = f"origin/{branch_name}"
    if check_ref_exists(repo_path, remote_ref):
        return remote_ref
    
    # Try local branch
    if check_ref_exists(repo_path, branch_name):
        return branch_name
    
    # Try as commit hash
    if check_ref_exists(repo_path, branch_name):
        return branch_name
    
    return None


def parse_pr_url(pr_url):
    """Extract owner, repo, and PR number from GitHub PR URL."""
    pattern = r'github\.com/([^/]+)/([^/]+)/pull/(\d+)'
    match = re.search(pattern, pr_url)
    if not match:
        raise ValueError(f"Invalid PR URL format: {pr_url}")
    return match.group(1), match.group(2), match.group(3)


def fetch_pr_info(owner, repo, pr_number):
    """Fetch PR information using gh CLI."""
    cmd = f'gh pr view {pr_number} --repo {owner}/{repo} --json number,title,body,baseRefName,headRefName,createdAt,additions,deletions,changedFiles,commits'
    output = run_command(cmd)
    return json.loads(output)


def get_git_diff(repo_path, base_branch, head_branch):
    """Get git diff between branches."""
    # Fetch latest changes (ignore errors if remote doesn't exist)
    run_command("git fetch --all", cwd=repo_path, check=False)
    
    # Resolve branch references
    base_ref = resolve_branch_ref(repo_path, base_branch)
    head_ref = resolve_branch_ref(repo_path, head_branch)
    
    if not base_ref:
        print(f"Warning: Base branch '{base_branch}' not found. Trying to fetch...", file=sys.stderr)
        run_command(f"git fetch origin {base_branch}:{base_branch}", cwd=repo_path, check=False)
        base_ref = resolve_branch_ref(repo_path, base_branch)
        if not base_ref:
            raise ValueError(f"Base branch '{base_branch}' not found in repository")
    
    if not head_ref:
        print(f"Warning: Head branch '{head_branch}' not found. Trying to fetch...", file=sys.stderr)
        run_command(f"git fetch origin {head_branch}:{head_branch}", cwd=repo_path, check=False)
        head_ref = resolve_branch_ref(repo_path, head_branch)
        if not head_ref:
            raise ValueError(f"Head branch '{head_branch}' not found in repository")
    
    print(f"Using refs: {base_ref}...{head_ref}")
    
    # Get diff statistics
    diff_stat = run_command(
        f"git diff --stat {base_ref}...{head_ref}",
        cwd=repo_path
    )
    
    # Get detailed diff
    diff_detail = run_command(
        f"git diff {base_ref}...{head_ref}",
        cwd=repo_path
    )
    
    # Get changed files list
    changed_files = run_command(
        f"git diff --name-status {base_ref}...{head_ref}",
        cwd=repo_path
    ).split('\n')
    
    return {
        'stat': diff_stat,
        'detail': diff_detail,
        'files': changed_files
    }


def get_commit_history(repo_path, base_branch, head_branch):
    """Get commit history between branches."""
    # Resolve branch references
    base_ref = resolve_branch_ref(repo_path, base_branch)
    head_ref = resolve_branch_ref(repo_path, head_branch)
    
    if not base_ref or not head_ref:
        print(f"Warning: Cannot get commit history. Base: {base_ref}, Head: {head_ref}", file=sys.stderr)
        return []
    
    commits = run_command(
        f"git log {base_ref}..{head_ref} --pretty=format:'%H|%an|%ad|%s' --date=short",
        cwd=repo_path,
        check=False
    ).split('\n')
    
    result = []
    for commit in commits:
        if commit:
            parts = commit.split('|')
            if len(parts) == 4:
                result.append({
                    'hash': parts[0][:7],
                    'author': parts[1],
                    'date': parts[2],
                    'message': parts[3]
                })
    return result


def build_directory_tree(changed_files):
    """Build directory tree structure from changed files."""
    tree = {}
    
    for file_line in changed_files:
        if not file_line:
            continue
        
        parts = file_line.split('\t')
        if len(parts) < 2:
            continue
        
        status = parts[0]
        filepath = parts[1]
        
        # Build tree structure
        path_parts = filepath.split('/')
        current = tree
        
        for i, part in enumerate(path_parts):
            if i == len(path_parts) - 1:  # File
                if 'files' not in current:
                    current['files'] = []
                
                status_label = {
                    'A': '(Added)',
                    'M': '(Modified)',
                    'D': '(Deleted)',
                    'R': '(Renamed)'
                }.get(status, '')
                
                current['files'].append(f"{part} {status_label}".strip())
            else:  # Directory
                if 'dirs' not in current:
                    current['dirs'] = {}
                if part not in current['dirs']:
                    current['dirs'][part] = {}
                current = current['dirs'][part]
    
    return tree


def format_tree(tree, prefix='', is_last=True):
    """Format directory tree as text."""
    lines = []
    
    if 'dirs' in tree:
        dirs = sorted(tree['dirs'].items())
        for i, (name, subtree) in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and ('files' not in tree or not tree['files'])
            connector = '└── ' if is_last_dir else '├── '
            lines.append(f"{prefix}{connector}{name}/")
            
            new_prefix = prefix + ('    ' if is_last_dir else '│   ')
            lines.extend(format_tree(subtree, new_prefix, is_last_dir))
    
    if 'files' in tree:
        files = sorted(tree['files'])
        for i, file in enumerate(files):
            is_last_file = (i == len(files) - 1)
            connector = '└── ' if is_last_file else '├── '
            lines.append(f"{prefix}{connector}{file}")
    
    return lines


def detect_db_changes(diff_detail):
    """Detect database schema changes from diff."""
    patterns = [
        r'CREATE TABLE',
        r'ALTER TABLE',
        r'DROP TABLE',
        r'CREATE INDEX',
        r'DROP INDEX',
        r'migration',
        r'schema\.prisma',
        r'\.sql$'
    ]
    
    changes = []
    for line in diff_detail.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    changes.append(line[1:].strip())
                    break
    
    return changes


def detect_api_changes(diff_detail, changed_files):
    """Detect API endpoint changes from diff."""
    # Common API route patterns
    route_patterns = [
        r'@(Get|Post|Put|Delete|Patch)\([\'"]([^\'"]+)',  # NestJS, Spring
        r'@app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)',  # Flask, FastAPI
        r'router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)',  # Express
        r'(GET|POST|PUT|DELETE|PATCH)\s+[\'"]([^\'"]+)[\'"]'  # Generic
    ]
    
    api_files = [
        f for f in changed_files
        if 'route' in f.lower() or 'controller' in f.lower() or 'api' in f.lower()
    ]
    
    changes = []
    for line in diff_detail.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            for pattern in route_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    changes.append(line[1:].strip())
                    break
    
    return changes, api_files


def detect_test_changes(changed_files):
    """Detect test file changes."""
    test_patterns = [
        r'\.test\.',
        r'\.spec\.',
        r'__tests__',
        r'/tests?/',
        r'/test/'
    ]
    
    test_files = []
    for file_line in changed_files:
        if not file_line:
            continue
        parts = file_line.split('\t')
        if len(parts) < 2:
            continue
        
        filepath = parts[1]
        for pattern in test_patterns:
            if re.search(pattern, filepath, re.IGNORECASE):
                test_files.append(file_line)
                break
    
    return test_files


def detect_dependency_changes(diff_detail):
    """Detect dependency changes from package files."""
    dependency_files = [
        'package.json',
        'requirements.txt',
        'Gemfile',
        'pom.xml',
        'build.gradle',
        'go.mod',
        'Cargo.toml'
    ]
    
    changes = []
    in_dependency_file = False
    current_file = None
    
    for line in diff_detail.split('\n'):
        if line.startswith('+++'):
            filename = line.split('/')[-1]
            if filename in dependency_files:
                in_dependency_file = True
                current_file = filename
            else:
                in_dependency_file = False
                current_file = None
        
        if in_dependency_file and (line.startswith('+') or line.startswith('-')):
            if not line.startswith('+++') and not line.startswith('---'):
                changes.append(f"[{current_file}] {line}")
    
    return changes


def generate_spec_document(pr_info, diff_info, commits, repo_path, owner, repo, pr_number):
    """Generate technical specification document."""
    
    tree = build_directory_tree(diff_info['files'])
    tree_lines = format_tree(tree)
    
    db_changes = detect_db_changes(diff_info['detail'])
    api_changes, api_files = detect_api_changes(diff_info['detail'], diff_info['files'])
    test_changes = detect_test_changes(diff_info['files'])
    dependency_changes = detect_dependency_changes(diff_info['detail'])
    
    # Generate document
    doc = f"""# Technical Specification: {pr_info['title']}

## 1. Overview

- **PR Number**: #{pr_number}
- **PR URL**: https://github.com/{owner}/{repo}/pull/{pr_number}
- **Created At**: {pr_info['createdAt']}
- **Base Branch**: {pr_info['baseRefName']}
- **Compare Branch**: {pr_info['headRefName']}

### Description

{pr_info.get('body', 'No description provided')}

## 2. Change Summary

- **Changed Files**: {pr_info['changedFiles']}
- **Additions**: +{pr_info['additions']}
- **Deletions**: -{pr_info['deletions']}
- **Commits**: {len(commits)}

## 3. Folder Structure

```
{'\\n'.join(tree_lines)}
```

## 4. Commit History

| Hash | Date | Message |
|------|------|---------|
"""
    
    for commit in commits:
        doc += f"| {commit['hash']} | {commit['date']} | {commit['message']} |\n"
    
    doc += f"""
## 5. DB Schema Changes

"""
    
    if db_changes:
        doc += "The following DB schema-related changes were detected:\n\n"
        for change in db_changes[:20]:  # Limit to first 20
            doc += f"- `{change}`\n"
        if len(db_changes) > 20:
            doc += f"\n... and {len(db_changes) - 20} more changes\n"
    else:
        doc += "No DB schema changes detected.\n"
    
    doc += f"""
## 6. API Definition

"""
    
    if api_changes:
        doc += "The following API-related changes were detected:\n\n"
        for change in api_changes[:20]:  # Limit to first 20
            doc += f"- `{change}`\n"
        if len(api_changes) > 20:
            doc += f"\n... and {len(api_changes) - 20} more changes\n"
        
        if api_files:
            doc += "\n### Modified API Files\n\n"
            for file in api_files[:10]:
                doc += f"- {file}\n"
    else:
        doc += "No API definition changes detected.\n"
    
    doc += f"""
## 7. Major Changes

### Changed Files Statistics

```
{diff_info['stat']}
```

### Key Changes

"""
    
    # Extract key changes (added/removed functions, classes, etc.)
    for line in diff_info['detail'].split('\n')[:100]:  # First 100 lines
        if line.startswith('+++') or line.startswith('---'):
            doc += f"\n#### {line[4:]}\n\n"
        elif line.startswith('+') and (
            'function ' in line or 'class ' in line or 
            'def ' in line or 'const ' in line or 'export' in line
        ):
            doc += f"- Added: `{line[1:].strip()}`\n"
        elif line.startswith('-') and (
            'function ' in line or 'class ' in line or 
            'def ' in line or 'const ' in line or 'export' in line
        ):
            doc += f"- Removed: `{line[1:].strip()}`\n"
    
    doc += f"""
## 8. Tests

"""
    
    if test_changes:
        doc += f"**Modified Test Files**: {len(test_changes)}\n\n"
        for test in test_changes[:10]:
            doc += f"- {test}\n"
        if len(test_changes) > 10:
            doc += f"\n... and {len(test_changes) - 10} more files\n"
    else:
        doc += "No test file changes detected.\n"
    
    doc += f"""
## 9. Dependencies

"""
    
    if dependency_changes:
        doc += "The following dependency changes were detected:\n\n```diff\n"
        for change in dependency_changes[:30]:
            doc += f"{change}\n"
        if len(dependency_changes) > 30:
            doc += f"... and {len(dependency_changes) - 30} more changes\n"
        doc += "```\n"
    else:
        doc += "No dependency changes detected.\n"
    
    doc += f"""
## 10. Generation Info

- **Generated At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Repository Path**: {repo_path}
"""
    
    return doc


def main():
    parser = argparse.ArgumentParser(
        description='Generate technical specification from GitHub PR'
    )
    parser.add_argument('pr_url', help='GitHub PR URL')
    parser.add_argument(
        '--repo-path',
        help='Local repository path (defaults to current directory)',
        default=None
    )
    parser.add_argument(
        '--output-dir',
        help='Output directory for specification',
        default=None
    )
    
    args = parser.parse_args()
    
    # Parse PR URL
    owner, repo, pr_number = parse_pr_url(args.pr_url)
    print(f"Processing PR #{pr_number} from {owner}/{repo}")
    
    # Determine repo path
    if args.repo_path:
        repo_path = Path(args.repo_path).resolve()
    else:
        # Try to find git root from current directory
        try:
            repo_path = Path(run_command("git rev-parse --show-toplevel")).resolve()
        except:
            print("Error: Could not determine repository path. Please specify --repo-path", file=sys.stderr)
            sys.exit(1)
    
    print(f"Using repository at: {repo_path}")
    
    # Fetch PR information
    print("Fetching PR information...")
    pr_info = fetch_pr_info(owner, repo, pr_number)
    
    # Get git diff and commits
    print("Analyzing git diff...")
    diff_info = get_git_diff(repo_path, pr_info['baseRefName'], pr_info['headRefName'])
    
    print("Fetching commit history...")
    commits = get_commit_history(repo_path, pr_info['baseRefName'], pr_info['headRefName'])
    
    # Generate specification document
    print("Generating specification document...")
    spec_doc = generate_spec_document(
        pr_info, diff_info, commits, repo_path, owner, repo, pr_number
    )
    
    # Determine output path
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        # Default to skill's outputs directory
        script_dir = Path(__file__).parent
        output_dir = script_dir.parent / 'outputs'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"tech-spec-pr{pr_number}-{timestamp}.md"
    output_path = output_dir / filename
    
    # Write specification
    output_path.write_text(spec_doc, encoding='utf-8')
    print(f"\n✓ Technical specification generated: {output_path}")


if __name__ == '__main__':
    main()
