#!/usr/bin/env python3
"""Automate AGENTS.md updates with meta-issue #55 + PR auto-merge."""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from typing import List, Optional


def run(
    cmd: List[str],
    check: bool = True,
    capture: bool = True,
    strip_output: bool = True,
) -> str:
    print("+ " + " ".join(cmd))
    result = subprocess.run(cmd, check=check, text=True, capture_output=capture)
    if capture:
        return result.stdout.strip() if strip_output else result.stdout
    return ""


def die(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def git_status_porcelain() -> List[str]:
    output = run(["git", "status", "--porcelain"], strip_output=False)
    return [line for line in output.splitlines() if line]


def ensure_only_agents_modified() -> None:
    changed = git_status_porcelain()
    if not changed:
        die("No local changes detected. Edit AGENTS.md first.")
    non_agents = []
    agents_modified = False
    for line in changed:
        path = line[3:]
        if path == "AGENTS.md":
            agents_modified = True
        else:
            non_agents.append(path)
    if not agents_modified:
        die("AGENTS.md is not modified. Edit it before running this script.")
    if non_agents:
        die("Working tree has other changes: " + ", ".join(sorted(set(non_agents))))


def current_branch() -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def ensure_repo_root() -> str:
    return run(["git", "rev-parse", "--show-toplevel"])


def check_file_exists(path: str) -> None:
    if not os.path.exists(path):
        die(f"Required file not found: {path}")


def gh_json(cmd: List[str]) -> dict:
    output = run(cmd)
    if not output:
        return {}
    return json.loads(output)


def pr_status(pr_number: int) -> dict:
    return gh_json(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--json",
            "autoMergeRequest,mergeStateStatus,reviewDecision,statusCheckRollup,url",
        ]
    )


def log_pr_status(pr_number: int, prefix: str) -> None:
    data = pr_status(pr_number)
    print(f"{prefix} mergeStateStatus={data.get('mergeStateStatus')}")
    print(f"{prefix} autoMergeRequest={data.get('autoMergeRequest')}")
    print(f"{prefix} reviewDecision={data.get('reviewDecision')}")


def wait_for_merge(pr_number: int, timeout_sec: int) -> dict:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        data = gh_json(
            [
                "gh",
                "pr",
                "view",
                str(pr_number),
                "--json",
                "state,mergeCommit,url,number",
            ]
        )
        if data.get("state") == "MERGED":
            return data
        time.sleep(10)
    die("Timed out waiting for PR to merge. Check auto-merge status.")
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Automate AGENTS.md update flow with meta-issue #55."
    )
    parser.add_argument(
        "--summary",
        required=True,
        help="Short summary of the AGENTS.md change (used in commit/PR/issue comment).",
    )
    parser.add_argument(
        "--short",
        help="Branch suffix, used as docs/agents-55-<short>. Default: YYYYMMDD.",
    )
    parser.add_argument("--base", default="main", help="Base branch for the PR.")
    parser.add_argument("--issue", default="55", help="Meta issue number.")
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Seconds to wait for auto-merge before timing out.",
    )
    args = parser.parse_args()

    repo_root = ensure_repo_root()
    os.chdir(repo_root)

    agents_path = os.path.join(repo_root, "AGENTS.md")
    check_file_exists(agents_path)
    ensure_only_agents_modified()

    base_branch = args.base
    original_branch = current_branch()
    short = args.short or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
    branch_name = f"docs/agents-{args.issue}-{short}"

    # Refresh base branch
    run(["git", "fetch", "origin", base_branch])

    # Move to base while keeping AGENTS.md changes
    try:
        run(["git", "switch", base_branch])
    except subprocess.CalledProcessError:
        die(
            "Failed to switch to base branch with local changes. Resolve conflicts and retry."
        )

    run(["git", "pull", "--ff-only", "origin", base_branch])

    # Create branch for AGENTS update
    run(["git", "switch", "-c", branch_name])

    # Commit changes
    run(["git", "add", "AGENTS.md"])
    commit_message = "docs(agents): update AGENTS.md"
    run(["git", "commit", "-m", commit_message])
    commit_id = run(["git", "rev-parse", "HEAD"])

    # Push branch
    run(["git", "push", "-u", "origin", branch_name])

    # Create PR
    pr_title = commit_message
    pr_body = f"{args.summary}\n\nRefs #{args.issue}"
    pr_url = run(
        [
            "gh",
            "pr",
            "create",
            "--title",
            pr_title,
            "--body",
            pr_body,
            "--base",
            base_branch,
            "--head",
            branch_name,
        ]
    )

    pr_number = gh_json(["gh", "pr", "view", branch_name, "--json", "number"]).get(
        "number"
    )
    if pr_number is None:
        die("Unable to fetch PR number. Check PR creation.")

    log_pr_status(pr_number, "Pre-merge:")
    retry_unknown = 3
    while retry_unknown > 0:
        merge_state = pr_status(pr_number).get("mergeStateStatus")
        if merge_state != "UNKNOWN":
            break
        retry_unknown -= 1
        time.sleep(5)

    log_pr_status(pr_number, "Post-wait:")
    try:
        run(["gh", "pr", "merge", "--auto", "--squash", str(pr_number)])
    except subprocess.CalledProcessError:
        print(
            "WARN: auto-merge failed. Falling back to direct squash merge.",
            file=sys.stderr,
        )
        run(["gh", "pr", "merge", "--squash", str(pr_number)])

    # Comment on meta issue with changelog entry
    date_str = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    changelog = f"Changelog: {date_str} - {args.summary} ({pr_url})"
    run(["gh", "issue", "comment", str(args.issue), "--body", changelog])

    # Wait for auto-merge to complete
    merged_data = wait_for_merge(pr_number, args.timeout)
    merge_commit = merged_data.get("mergeCommit", {}).get("oid")

    # Cleanup branch
    run(["git", "push", "origin", "--delete", branch_name])
    run(["git", "switch", original_branch])

    # Update original branch with latest AGENTS.md
    try:
        run(["git", "pull", "--ff-only"])
    except subprocess.CalledProcessError:
        print(
            "WARN: git pull failed (no upstream?). Run a pull manually if needed.",
            file=sys.stderr,
        )

    # Delete local branch (after leaving it)
    run(["git", "branch", "-D", branch_name])

    # Final recap
    print("\nRecap:")
    print(f"- AGENTS.md updated and committed: {commit_id}")
    print(f"- PR: {pr_url}")
    if merge_commit:
        print(f"- Merge commit: {merge_commit}")
    else:
        print("- Merge commit: not available")
    print(f"- Meta issue #{args.issue} updated with changelog entry")

    return 0


if __name__ == "__main__":
    sys.exit(main())
