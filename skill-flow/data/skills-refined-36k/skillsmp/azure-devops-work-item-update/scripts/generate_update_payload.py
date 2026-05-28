#!/usr/bin/env python3
"""
Generate Azure DevOps work item update payload.

Usage:
    python generate_update_payload.py \
      --work-item-id 1234 \
      --commit-sha abc123 \
      --commit-url "https://github.com/org/repo/commit/abc123" \
      --summary "Implemented feature X" \
      --target-state "Ready for Testing"
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional


def generate_commit_link_update(commit_url: str, comment: str = "Implementation commit") -> Dict:
    """Generate update to add commit link."""
    return {
        "op": "add",
        "path": "/relations/-",
        "value": {
            "rel": "Hyperlink",
            "url": commit_url,
            "attributes": {
                "comment": comment
            }
        }
    }


def generate_history_comment(summary: str, commit_sha: Optional[str] = None,
                             files_changed: Optional[List[str]] = None) -> str:
    """Generate HTML formatted history comment."""
    lines = [
        "<p><b>Implementation Complete</b></p>",
        f"<p>{summary}</p>"
    ]

    if files_changed:
        files_str = ", ".join(files_changed[:5])  # Limit to first 5 files
        if len(files_changed) > 5:
            files_str += f" (+{len(files_changed) - 5} more)"
        lines.append(f"<p><b>Files changed:</b> {files_str}</p>")

    if commit_sha:
        lines.append(f"<p><b>Git commit:</b> {commit_sha[:8]}</p>")

    lines.append(f"<p><i>Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i></p>")

    return "".join(lines)


def generate_history_update(summary: str, commit_sha: Optional[str] = None,
                           files_changed: Optional[List[str]] = None) -> Dict:
    """Generate update to add history comment."""
    comment = generate_history_comment(summary, commit_sha, files_changed)

    return {
        "op": "add",
        "path": "/fields/System.History",
        "value": comment
    }


def generate_state_update(target_state: str) -> Dict:
    """Generate update to change work item state."""
    return {
        "op": "add",
        "path": "/fields/System.State",
        "value": target_state
    }


def generate_update_payload(
    work_item_id: int,
    project: str,
    commit_url: Optional[str] = None,
    summary: Optional[str] = None,
    commit_sha: Optional[str] = None,
    files_changed: Optional[List[str]] = None,
    target_state: Optional[str] = None,
    additional_updates: Optional[List[Dict]] = None
) -> Dict:
    """Generate complete update payload for Azure DevOps MCP."""
    updates = []

    # Add commit link
    if commit_url:
        updates.append(generate_commit_link_update(commit_url))

    # Add history comment
    if summary:
        updates.append(generate_history_update(summary, commit_sha, files_changed))

    # Add state change
    if target_state:
        updates.append(generate_state_update(target_state))

    # Add any additional updates
    if additional_updates:
        updates.extend(additional_updates)

    return {
        "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
        "parameters": {
            "project": project,
            "updates": [
                {
                    "id": work_item_id,
                    "updates": updates
                }
            ]
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate Azure DevOps work item update payload"
    )

    # Required
    parser.add_argument("--work-item-id", type=int, required=True,
                       help="Work item ID to update")
    parser.add_argument("--project", type=str, required=True,
                       help="Azure DevOps project name")

    # Optional - commit information
    parser.add_argument("--commit-sha", type=str,
                       help="Git commit SHA (short or full)")
    parser.add_argument("--commit-url", type=str,
                       help="Full URL to commit (GitHub/Azure Repos)")

    # Optional - implementation details
    parser.add_argument("--summary", type=str,
                       help="Implementation summary")
    parser.add_argument("--files-changed", type=str,
                       help="Comma-separated list of changed files")

    # Optional - state update
    parser.add_argument("--target-state", type=str,
                       help="Target state (e.g., 'Ready for Testing', 'Resolved')")

    # Optional - work item type context
    parser.add_argument("--work-item-type", type=str,
                       choices=["Task", "User Story", "Bug", "Feature", "Epic"],
                       help="Work item type (used for state validation)")

    # Output
    parser.add_argument("--pretty", action="store_true",
                       help="Pretty print JSON output")
    parser.add_argument("--output", type=str,
                       help="Output file path")

    args = parser.parse_args()

    # Validate inputs
    if not args.commit_url and not args.summary and not args.target_state:
        print("Error: Must specify at least one update (commit-url, summary, or target-state)",
              file=sys.stderr)
        sys.exit(1)

    # Parse files changed
    files_changed = None
    if args.files_changed:
        files_changed = [f.strip() for f in args.files_changed.split(',')]

    # Validate state transition (basic validation)
    if args.target_state and args.work_item_type:
        valid_states = {
            "Task": ["New", "Active", "Ready for Testing", "Closed", "Removed"],
            "User Story": ["New", "Active", "Resolved", "Closed", "Removed"],
            "Bug": ["New", "Active", "Resolved", "Closed"],
            "Feature": ["New", "Active", "Resolved", "Closed", "Removed"],
            "Epic": ["New", "Active", "Resolved", "Closed", "Removed"]
        }

        if args.target_state not in valid_states.get(args.work_item_type, []):
            print(f"Warning: '{args.target_state}' may not be valid for {args.work_item_type}",
                  file=sys.stderr)

    # Generate payload
    payload = generate_update_payload(
        work_item_id=args.work_item_id,
        project=args.project,
        commit_url=args.commit_url,
        summary=args.summary,
        commit_sha=args.commit_sha,
        files_changed=files_changed,
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
