#!/usr/bin/env python3
"""
Update multiple work items from a range of git commits.

Usage:
    python batch_update_from_commits.py \
      --git-range "HEAD~5..HEAD" \
      --project "ProjectName" \
      --repo-url "https://github.com/org/repo"
"""

import argparse
import json
import re
import subprocess
import sys
from typing import Dict, List, Optional


def get_commits_in_range(git_range: str) -> List[Dict]:
    """Get all commits in specified range."""
    try:
        # Get commit SHAs, messages, and dates
        result = subprocess.run(
            ['git', 'log', git_range, '--pretty=format:%H|%s|%ci|%an'],
            capture_output=True,
            text=True,
            check=True
        )

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|')
            if len(parts) == 4:
                commits.append({
                    "sha": parts[0],
                    "message": parts[1],
                    "date": parts[2],
                    "author": parts[3]
                })

        return commits
    except subprocess.CalledProcessError as e:
        print(f"Error getting commits: {e}", file=sys.stderr)
        return []


def get_files_changed(commit_sha: str) -> List[str]:
    """Get list of files changed in commit."""
    try:
        result = subprocess.run(
            ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_sha],
            capture_output=True,
            text=True,
            check=True
        )
        return [f for f in result.stdout.strip().split('\n') if f]
    except subprocess.CalledProcessError:
        return []


def extract_work_item_id(commit_message: str) -> Optional[int]:
    """Extract work item ID from commit message."""
    patterns = [
        r'\(#(\d+)\)',
        r'#(\d+)',
        r'\[#(\d+)\]',
    ]

    for pattern in patterns:
        match = re.search(pattern, commit_message)
        if match:
            return int(match.group(1))

    return None


def generate_summary_from_message(commit_message: str) -> str:
    """Generate summary from commit message, removing work item reference."""
    # Remove work item references
    cleaned = re.sub(r'\(#\d+\)', '', commit_message)
    cleaned = re.sub(r'#\d+:?\s*', '', cleaned)
    cleaned = re.sub(r'\[#\d+\]', '', cleaned)

    # Remove common prefixes (feat, fix, etc.)
    cleaned = re.sub(r'^(feat|fix|docs|style|refactor|test|chore)[\(:]\s*', '', cleaned)

    return cleaned.strip()


def group_commits_by_work_item(commits: List[Dict], repo_url: str) -> Dict[int, List[Dict]]:
    """Group commits by work item ID."""
    work_items = {}

    for commit in commits:
        work_item_id = extract_work_item_id(commit["message"])

        if work_item_id:
            if work_item_id not in work_items:
                work_items[work_item_id] = []

            commit_url = f"{repo_url}/commit/{commit['sha']}"
            files_changed = get_files_changed(commit["sha"])
            summary = generate_summary_from_message(commit["message"])

            work_items[work_item_id].append({
                "sha": commit["sha"],
                "url": commit_url,
                "message": commit["message"],
                "summary": summary,
                "files_changed": files_changed,
                "date": commit["date"],
                "author": commit["author"]
            })

    return work_items


def generate_batch_payload(
    work_items: Dict[int, List[Dict]],
    project: str,
    target_state: Optional[str] = None
) -> Dict:
    """Generate batch update payload for multiple work items."""
    updates = []

    for work_item_id, commits in work_items.items():
        work_item_updates = []

        # Add commit links
        for commit in commits:
            work_item_updates.append({
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "Hyperlink",
                    "url": commit["url"],
                    "attributes": {
                        "comment": f"Implementation commit: {commit['sha'][:8]}"
                    }
                }
            })

        # Generate combined summary
        if len(commits) == 1:
            summary_text = commits[0]["summary"]
            files_changed = commits[0]["files_changed"]
        else:
            summary_text = f"Multiple commits ({len(commits)}):\n"
            for i, commit in enumerate(commits, 1):
                summary_text += f"{i}. {commit['summary']}\n"

            # Combine all files
            all_files = []
            for commit in commits:
                all_files.extend(commit["files_changed"])
            files_changed = list(set(all_files))  # Remove duplicates

        # Format history comment
        history_lines = [
            "<p><b>Implementation Complete</b></p>",
            f"<p>{summary_text}</p>"
        ]

        if files_changed:
            files_str = ", ".join(files_changed[:10])
            if len(files_changed) > 10:
                files_str += f" (+{len(files_changed) - 10} more)"
            history_lines.append(f"<p><b>Files changed:</b> {files_str}</p>")

        history_lines.append(f"<p><b>Commits:</b> {len(commits)}</p>")

        work_item_updates.append({
            "op": "add",
            "path": "/fields/System.History",
            "value": "".join(history_lines)
        })

        # Add state change if specified
        if target_state:
            work_item_updates.append({
                "op": "add",
                "path": "/fields/System.State",
                "value": target_state
            })

        updates.append({
            "id": work_item_id,
            "updates": work_item_updates
        })

    return {
        "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
        "parameters": {
            "project": project,
            "updates": updates
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Update multiple work items from git commit range"
    )

    parser.add_argument("--git-range", type=str, required=True,
                       help="Git commit range (e.g., 'HEAD~5..HEAD', 'main..feature')")
    parser.add_argument("--project", type=str, required=True,
                       help="Azure DevOps project name")
    parser.add_argument("--repo-url", type=str, required=True,
                       help="Repository URL (e.g., 'https://github.com/org/repo')")
    parser.add_argument("--target-state", type=str,
                       help="Target state for all work items")
    parser.add_argument("--pretty", action="store_true",
                       help="Pretty print JSON output")
    parser.add_argument("--output", type=str,
                       help="Output file path")
    parser.add_argument("--summary", action="store_true",
                       help="Print summary of work items to be updated")

    args = parser.parse_args()

    # Get commits
    print(f"Fetching commits in range: {args.git_range}", file=sys.stderr)
    commits = get_commits_in_range(args.git_range)

    if not commits:
        print("No commits found in range", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(commits)} commit(s)", file=sys.stderr)

    # Group by work item
    work_items = group_commits_by_work_item(commits, args.repo_url)

    if not work_items:
        print("No work item references found in commit messages", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(work_items)} work item(s) to update", file=sys.stderr)

    # Print summary if requested
    if args.summary:
        print("\nWork Items to Update:", file=sys.stderr)
        for work_item_id, commits in work_items.items():
            print(f"  #{work_item_id}: {len(commits)} commit(s)", file=sys.stderr)
            for commit in commits:
                print(f"    - {commit['sha'][:8]}: {commit['summary']}", file=sys.stderr)
        print("", file=sys.stderr)

    # Generate payload
    payload = generate_batch_payload(
        work_items=work_items,
        project=args.project,
        target_state=args.target_state
    )

    # Output
    indent = 2 if args.pretty else None
    output = json.dumps(payload, indent=indent)

    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Payload written to {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
