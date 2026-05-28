#!/usr/bin/env python3
"""
Bulk GitHub issue creation from JSON data
Usage: python3 create_issues.py issues.json
"""

import json
import subprocess
import time
import sys

def create_issue(title, body, labels):
    """Create a GitHub issue using gh CLI"""
    label_args = []
    for label in labels:
        label_args.extend(["-l", label])

    cmd = ["gh", "issue", "create", "--title", title, "--body", body] + label_args

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issue_url = result.stdout.strip()
        print(f"✅ Created: {title}")
        print(f"   URL: {issue_url}")
        return issue_url
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create: {title}")
        print(f"   Error: {e.stderr}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 create_issues.py issues.json")
        sys.exit(1)

    # Load issues from JSON
    with open(sys.argv[1], "r") as f:
        epic_groups = json.load(f)

    total_issues = sum(len(group["issues"]) for group in epic_groups)
    created = 0
    failed = 0

    print(f"📝 Creating {total_issues} issues across {len(epic_groups)} epics...")
    print()

    for group in epic_groups:
        epic = group["epic"]
        status = group["status"]
        priority = group["priority"]

        print(f"\n{'='*60}")
        print(f"Epic: {epic}")
        print(f"Status: {status}, Priority: {priority}")
        print(f"Issues: {len(group['issues'])}")
        print(f"{'='*60}\n")

        for issue in group["issues"]:
            labels = [epic, status, priority, "type:feature"]
            url = create_issue(issue["title"], issue["body"], labels)

            if url:
                created += 1
            else:
                failed += 1

            # Rate limiting: don't overwhelm GitHub API
            time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"📊 Summary:")
    print(f"   Total: {total_issues}")
    print(f"   Created: {created}")
    print(f"   Failed: {failed}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
