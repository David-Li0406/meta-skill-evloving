#!/usr/bin/env python3
"""
Fetch GitHub issue details with structured parsing
Usage: python3 fetch_issue.py ISSUE_NUMBER [OWNER] [REPO]
"""

import json
import subprocess
import sys
import re

def parse_acceptance_criteria(body: str) -> list[str]:
    """Extract acceptance criteria from issue body"""
    if not body:
        return []

    lines = body.split("\n")
    criteria = []
    in_criteria_section = False

    for line in lines:
        # Check for "Acceptance Criteria" header
        if re.search(r'acceptance criteria', line, re.IGNORECASE):
            in_criteria_section = True
            continue

        # Parse checkbox items
        if in_criteria_section:
            # Match "- [ ]" or "- [x]" checkbox format
            match = re.match(r'^\s*-\s*\[([ xX])\]\s*(.+)$', line)
            if match:
                criteria.append({
                    "checked": match.group(1).lower() == 'x',
                    "text": match.group(2).strip()
                })
            elif line.strip() == "":
                # Empty line might signal end of section
                continue
            elif line.startswith("#"):
                # New section started, exit criteria parsing
                break

    return criteria

def extract_label(labels: list, prefix: str) -> str | None:
    """Extract label with given prefix"""
    for label in labels:
        name = label.get("name", "")
        if name.startswith(prefix):
            return name[len(prefix):]
    return None

def fetch_issue(issue_number: int, owner: str = None, repo: str = None) -> dict:
    """
    Fetch issue details from GitHub

    Returns structured issue data including:
    - number, title, body
    - acceptance_criteria (parsed from body)
    - epic, priority, status (from labels)
    - assignees, state, url
    """
    cmd = [
        "gh", "issue", "view", str(issue_number),
        "--json", "number,title,body,labels,assignees,milestone,state,url"
    ]

    # Add repo context if provided
    if owner and repo:
        cmd.extend(["--repo", f"{owner}/{repo}"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issue = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching issue #{issue_number}", file=sys.stderr)
        print(f"   {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing issue data: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract structured data
    structured = {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue.get("body", ""),
        "acceptance_criteria": parse_acceptance_criteria(issue.get("body", "")),
        "epic": extract_label(issue.get("labels", []), prefix="epic:"),
        "priority": extract_label(issue.get("labels", []), prefix="priority:"),
        "status": extract_label(issue.get("labels", []), prefix="status:"),
        "type": extract_label(issue.get("labels", []), prefix="type:"),
        "assignees": [a["login"] for a in issue.get("assignees", [])],
        "milestone": issue.get("milestone", {}).get("title") if issue.get("milestone") else None,
        "state": issue["state"],
        "url": issue["url"]
    }

    return structured

def validate_issue(issue: dict) -> tuple[bool, list[str]]:
    """
    Validate issue is suitable for implementation

    Returns: (is_valid, warnings)
    """
    warnings = []

    # Check if closed
    if issue["state"] == "CLOSED":
        warnings.append(f"⚠️  Issue is closed")

    # Check if already assigned
    if issue["assignees"]:
        assignees = ", ".join(issue["assignees"])
        warnings.append(f"⚠️  Already assigned to: {assignees}")

    # Check for acceptance criteria
    if not issue["acceptance_criteria"]:
        warnings.append("⚠️  No acceptance criteria found in issue body")

    # Check for labels
    if not issue["epic"]:
        warnings.append("⚠️  No epic label found")

    if not issue["priority"]:
        warnings.append("⚠️  No priority label found")

    # Issue is valid if it's open (warnings are just warnings)
    is_valid = issue["state"] == "OPEN"

    return is_valid, warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_issue.py ISSUE_NUMBER [OWNER] [REPO]")
        sys.exit(1)

    issue_number = int(sys.argv[1])
    owner = sys.argv[2] if len(sys.argv) > 2 else None
    repo = sys.argv[3] if len(sys.argv) > 3 else None

    # Fetch issue
    issue = fetch_issue(issue_number, owner, repo)

    # Validate
    is_valid, warnings = validate_issue(issue)

    # Print warnings
    if warnings:
        print("\n".join(warnings), file=sys.stderr)
        print(file=sys.stderr)

    # Output structured JSON to stdout
    print(json.dumps(issue, indent=2))

    # Exit with error if invalid
    if not is_valid:
        sys.exit(1)

if __name__ == "__main__":
    main()
