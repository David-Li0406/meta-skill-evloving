#!/usr/bin/env python3
"""
Feed Jules Feedback Script
Checks open PRs from Jules, analyzes CI results and reviews, and feeds feedback back to Jules.
"""
import os
import sys
import argparse
import requests
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# Import JulesClient from the same directory
try:
    # If run as a script in the directory
    from repo_client import JulesClient
except ImportError:
    # If run from root via python .claude/skills/jules-api/feed_feedback.py
    # We need to make sure the directory is in path or we use relative import if it was a module
    sys.path.append(str(Path(__file__).parent))
    try:
        from repo_client import JulesClient
    except ImportError:
        print("Error: Could not import JulesClient.", file=sys.stderr)

def get_repo_info():
    """Get owner and repo from environment or git config."""
    repo_full = os.environ.get("GITHUB_REPOSITORY")
    if repo_full:
        owner, repo = repo_full.split("/")
        return owner, repo

    # Fallback to local git
    try:
        url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True).strip()
        # Parse GitHub remotes like:
        # - https://github.com/owner/repo.git
        # - git@github.com:owner/repo.git
        parsed_url = url
        # Handle SSH-style URLs without a scheme, e.g. git@github.com:owner/repo.git
        if "://" not in parsed_url and "@" in parsed_url and ":" in parsed_url:
            user_host, path_part = parsed_url.split("@", 1)[-1].split(":", 1)
            parsed_url = f"ssh://{user_host}/{path_part}"
        parsed = urlparse(parsed_url)
        if parsed.hostname == "github.com":
            path = parsed.path.lstrip("/")
            if path.endswith(".git"):
                path = path[:-4]
            parts = path.split("/")
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                return owner, repo
    except Exception:
        pass
    return None, None

def run_gh_command(args):
    """Run a gh CLI command and return JSON."""
    # Use basic fields for list
    safe_fields = ["number", "title", "author", "headRefName", "url", "statusCheckRollup"]

    # Check if 'view' or 'list'
    is_view = "view" in args
    if is_view:
        safe_fields.extend(["commits", "reviews", "latestReviews", "body"])

    cmd = ["gh"] + args + ["--json", ",".join(safe_fields)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e.stderr}", file=sys.stderr)
        return []

def get_pr_ci_status(pr_number):
    """Get detailed CI status for a PR."""
    # gh pr checks <number> --json bucket,name,state,link
    cmd = ["gh", "pr", "checks", str(pr_number), "--json", "name,state,link"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching checks for PR {pr_number}: {e.stderr}", file=sys.stderr)
        return []

def get_pr_comments(pr_number):
    """Get comments and reviews for a PR."""
    # gh pr view <number> --json comments,reviews
    cmd = ["gh", "pr", "view", str(pr_number), "--json", "comments,reviews"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching comments for PR {pr_number}: {e.stderr}", file=sys.stderr)
        return {}

def should_trigger_feedback(pr):
    """Determine if a PR needs feedback."""
    # 1. Check CI Status
    status = pr.get("statusCheckRollup") or {}
    state = status.get("state", "PENDING")

    ci_failed = state == "FAILURE"

    # 2. Check Reviews
    reviews = pr.get("latestReviews", [])
    changes_requested = any(r["state"] == "CHANGES_REQUESTED" for r in reviews)

    return ci_failed or changes_requested

def construct_prompt(pr, ci_checks, comments_data):
    """Construct the prompt for Jules."""
    pr_number = pr["number"]
    pr_title = pr["title"]
    branch = pr["headRefName"]

    # Analyze CI
    failed_checks = [c for c in ci_checks if c["state"] == "FAILURE"]
    ci_section = ""
    if failed_checks:
        ci_section = "## CI Failures\nThe following checks failed:\n"
        for check in failed_checks:
            ci_section += f"- **{check['name']}**: {check['link']}\n"
    else:
        ci_section = "## CI Status\nCI checks passed (or none failed yet).\n"

    # Analyze Reviews
    reviews = comments_data.get("reviews", [])
    comments = comments_data.get("comments", [])

    review_section = "## Review Feedback\n"

    # Get recent reviews (last 3)
    for review in reviews[-3:]:
        if review["state"] in ["CHANGES_REQUESTED", "COMMENTED"]:
             review_section += f"### Review by {review['author']['login']} ({review['state']})\n{review['body']}\n\n"

    # Get recent comments (last 5)
    for comment in comments[-5:]:
        review_section += f"**{comment['author']['login']}**: {comment['body'][:500]}...\n\n"

    prompt = f"""
# Task: Fix Pull Request #{pr_number}

Your Pull Request "{pr_title}" on branch `{branch}` has received feedback that needs attention.

{ci_section}

{review_section}

## Instructions
1. Analyze the feedback above.
2. Examine the code in the current branch (`{branch}`).
3. Fix the reported issues (CI failures or review comments).
4. Commit and push your changes.
"""
    return prompt

def extract_session_id(branch_name: str) -> str | None:
    """Extract session ID from branch name."""
    uuid_match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', branch_name)
    if uuid_match:
        return uuid_match.group(1)

    parts = branch_name.split('-')
    if len(parts) > 1:
        last_part = parts[-1]
        if len(last_part) > 10 and last_part.isalnum():
             return last_part

    return None

def extract_session_id_from_body(body: str) -> str | None:
    """Extract session ID from PR body/description."""
    if not body:
        return None
    match = re.search(r'/task/([a-zA-Z0-9-]+)', body)
    if not match:
        match = re.search(r'/sessions/([a-zA-Z0-9-]+)', body)
    return match.group(1) if match else None

def should_skip_feedback(pr_data, comments_data):
    """Check if we should skip feedback (loop prevention)."""
    if not comments_data.get("comments"):
        return False

    last_comment = None
    for c in reversed(comments_data["comments"]):
        if "# Task: Fix Pull Request" in c["body"] or "<!-- # Task: Fix Pull Request -->" in c["body"]:
            last_comment = c
            break

    if not last_comment:
        return False

    commits = pr_data.get("commits", [])
    if not commits:
         return True

    last_commit = commits[-1]
    commit_date_str = last_commit.get("committedDate")
    comment_date_str = last_comment.get("createdAt")

    if commit_date_str and comment_date_str:
        if comment_date_str > commit_date_str:
            return True

    return False

def main():
    parser = argparse.ArgumentParser(description="Feed Jules Feedback")
    parser.add_argument("--dry-run", action="store_true", help="Do not create sessions")
    parser.add_argument("--author", default="app/google-labs-jules", help="Filter PRs by author")
    args = parser.parse_args()

    owner, repo = get_repo_info()
    if not owner or not repo:
        print("Error: Could not determine repo owner/name", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning PRs for {owner}/{repo} by author {args.author}...")

    cmd = ["pr", "list", "--author", args.author, "--state", "open"]
    try:
        prs = run_gh_command(cmd)
    except FileNotFoundError:
        print("Error: 'gh' command not found. Ensure GitHub CLI is installed.", file=sys.stderr)
        sys.exit(1)

    if not prs:
        print("No open PRs found for this author.")
        return

    client = None
    if not args.dry_run:
        try:
            client = JulesClient()
        except Exception as e:
            print(f"Failed to initialize JulesClient: {e}", file=sys.stderr)
            sys.exit(1)

    for pr in prs:
        print(f"Checking PR #{pr['number']}: {pr['title']}")

        try:
             res = subprocess.run(["gh", "pr", "view", str(pr['number']), "--json", "number,title,headRefName,statusCheckRollup,latestReviews,author,body,commits"], capture_output=True, text=True, check=True)
             pr_data = json.loads(res.stdout)
        except Exception as e:
            print(f"Failed to view PR {pr['number']}: {e}")
            continue

        comments_data = get_pr_comments(pr['number'])

        if should_skip_feedback(pr_data, comments_data):
            print(f"-> PR #{pr['number']} has pending feedback and no new commits. Skipping.")
            continue

        if should_trigger_feedback(pr_data):
            print(f"-> PR #{pr['number']} needs feedback.")

            ci_checks = get_pr_ci_status(pr['number'])
            prompt = construct_prompt(pr_data, ci_checks, comments_data)
            branch_name = pr_data["headRefName"]

            session_id = extract_session_id_from_body(pr_data.get("body"))
            if not session_id:
                session_id = extract_session_id(branch_name)

            print(f"   Branch: {branch_name}")
            print(f"   Extracted Session ID: {session_id}")

            if not args.dry_run and client:
                try:
                    if session_id:
                        print(f"Sending message to existing session {session_id}...")
                        client.send_message(session_id, prompt)
                        print("Message sent.")
                    else:
                        print("No session ID found. Creating new session...")
                        resp = client.create_session(
                            prompt=prompt,
                            owner=owner,
                            repo=repo,
                            branch=branch_name,
                            title=f"Fix PR #{pr['number']}: {pr['title']}",
                            automation_mode="AUTO_CREATE_PR"
                        )
                        print(f"Session created: {resp.get('name')}")

                    print("Posting comment to PR to mark feedback loop...")
                    marker_body = f"🤖 Feedback sent to Jules session. \n<!-- # Task: Fix Pull Request -->"
                    subprocess.run(["gh", "pr", "comment", str(pr['number']), "--body", marker_body], check=True)

                except Exception as e:
                    print(f"Failed to communicate with Jules or update PR: {e}")
        else:
            print(f"-> PR #{pr['number']} CI is green or pending.")

if __name__ == "__main__":
    main()
