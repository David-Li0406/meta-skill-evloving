#!/usr/bin/env python3
"""
Auto-select next issue based on priority and filters
Usage: python3 select_issue.py [--priority PRIORITY] [--epic EPIC] [--status STATUS]
"""

import json
import subprocess
import sys
import argparse

PRIORITY_ORDER = ["critical", "high", "medium", "low"]

def select_next_issue(
    priority: str = "critical",
    epic_filter: str = None,
    status: str = "backlog",
    owner: str = None,
    repo: str = None
) -> dict | None:
    """
    Auto-select next issue based on priority and filters

    Priority order: critical > high > medium > low
    Within same priority: oldest first (by creation date)

    Returns: Issue data or None if no matching issue found
    """
    # Build label filters
    labels = [f"priority:{priority}", f"status:{status}"]
    if epic_filter:
        labels.append(f"epic:{epic_filter}")

    # Build gh CLI query
    cmd = ["gh", "issue", "list", "--state", "open"]

    # Add repo context if provided
    if owner and repo:
        cmd.extend(["--repo", f"{owner}/{repo}"])

    # Add label filters
    for label in labels:
        cmd.extend(["--label", label])

    # Request JSON output with relevant fields
    cmd.extend([
        "--json", "number,title,createdAt,labels,assignees",
        "--jq", "sort_by(.createdAt)"  # Sort by creation date (oldest first)
    ])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error querying issues: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing issue list: {e}", file=sys.stderr)
        return None

    # Return first issue if any found
    if issues:
        return issues[0]
    else:
        return None

def select_with_fallback(
    epic_filter: str = None,
    status: str = "backlog",
    owner: str = None,
    repo: str = None
) -> dict | None:
    """
    Try to select issue with priority fallback

    Tries in order: critical → high → medium → low
    """
    for priority in PRIORITY_ORDER:
        issue = select_next_issue(
            priority=priority,
            epic_filter=epic_filter,
            status=status,
            owner=owner,
            repo=repo
        )
        if issue:
            return issue

    return None

def main():
    parser = argparse.ArgumentParser(
        description="Auto-select next GitHub issue based on priority and filters"
    )
    parser.add_argument(
        "--priority",
        choices=PRIORITY_ORDER,
        help="Priority level (default: tries all in order)"
    )
    parser.add_argument(
        "--epic",
        help="Filter by epic (e.g., 'booking-payment')"
    )
    parser.add_argument(
        "--status",
        default="backlog",
        help="Issue status (default: backlog)"
    )
    parser.add_argument(
        "--owner",
        help="Repository owner (optional)"
    )
    parser.add_argument(
        "--repo",
        help="Repository name (optional)"
    )

    args = parser.parse_args()

    # Select issue
    if args.priority:
        # Try specific priority
        issue = select_next_issue(
            priority=args.priority,
            epic_filter=args.epic,
            status=args.status,
            owner=args.owner,
            repo=args.repo
        )
    else:
        # Try with priority fallback
        issue = select_with_fallback(
            epic_filter=args.epic,
            status=args.status,
            owner=args.owner,
            repo=args.repo
        )

    if issue:
        # Extract priority from labels for display
        priority_label = next(
            (l["name"] for l in issue["labels"] if l["name"].startswith("priority:")),
            None
        )
        priority = priority_label.replace("priority:", "") if priority_label else "unknown"

        # Print selection info to stderr
        print(f"✅ Selected issue #{issue['number']}: {issue['title']}", file=sys.stderr)
        print(f"   Priority: {priority}", file=sys.stderr)
        print(f"   Created: {issue['createdAt']}", file=sys.stderr)

        if issue["assignees"]:
            assignees = ", ".join(a["login"] for a in issue["assignees"])
            print(f"   ⚠️  Assigned to: {assignees}", file=sys.stderr)

        print(file=sys.stderr)

        # Output issue number to stdout
        print(issue["number"])
        sys.exit(0)
    else:
        filters = []
        if args.priority:
            filters.append(f"priority:{args.priority}")
        if args.epic:
            filters.append(f"epic:{args.epic}")
        filters.append(f"status:{args.status}")

        print(f"❌ No issues found matching: {', '.join(filters)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
