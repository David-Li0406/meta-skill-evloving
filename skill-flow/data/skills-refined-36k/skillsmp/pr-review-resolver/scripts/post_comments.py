#!/usr/bin/env python3
"""
PR Review Progress를 읽고 GitHub PR에 결과 코멘트를 작성한다.

Usage:
    python3 post_comments.py [--dry-run]

Options:
    --dry-run    실제 코멘트를 작성하지 않고 출력만 함
"""

import subprocess
import sys
from pathlib import Path

import yaml


def load_progress(path: Path = Path(".pr-review-progress.yaml")) -> dict | None:
    if not path.exists():
        print(f"Error: {path} not found")
        return None
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse {path}: {e}")
        return None
    if not isinstance(data, dict):
        print(f"Error: {path} must be a mapping")
        return None
    return data


def get_pr_number() -> int | None:
    """현재 브랜치의 PR 번호를 가져온다."""
    result = subprocess.run(
        ["gh", "pr", "view", "--json", "number", "-q", ".number"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Error: Could not get PR number")
        return None
    try:
        return int(result.stdout.strip())
    except ValueError:
        print("Error: Invalid PR number output")
        return None


def post_comment(pr_number: int, comment_id: int, body: str, dry_run: bool = False):
    """PR 리뷰 코멘트에 답글을 작성한다."""
    if dry_run:
        print(f"[DRY-RUN] Would post to comment #{comment_id}:")
        print(f"  {body}")
        return

    # gh api를 사용하여 코멘트 작성
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/:owner/:repo/pulls/{pr_number}/comments/{comment_id}/replies",
            "-X",
            "POST",
            "-f",
            f"body={body}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Warning: Failed to post comment #{comment_id}: {result.stderr}")
    else:
        print(f"Posted reply to comment #{comment_id}")


def format_resolved_message(comment: dict) -> str:
    """resolved 코멘트에 대한 메시지를 생성한다."""
    commit_sha = comment.get("commit_sha") or "unknown"
    return f"다음 커밋에서 수정하였습니다. \n\n`{str(commit_sha)[:7]}`"


def format_skipped_message(comment: dict) -> str:
    """skipped 코멘트에 대한 메시지를 생성한다."""
    reason = comment.get("skip_reason") or "No reason provided"
    return f"다음 이유로 스킵하였습니다. \n\n{reason}"


def main():
    dry_run = "--dry-run" in sys.argv

    progress = load_progress()
    if not progress:
        sys.exit(1)

    pr_number = progress.get("pr_number") or get_pr_number()
    if not pr_number:
        sys.exit(1)

    comments = progress.get("comments", [])
    if not comments:
        print("No comments to process")
        sys.exit(0)

    resolved_count = 0
    skipped_count = 0

    for comment in comments:
        status = comment.get("status")
        github_comment_id = comment.get("github_comment_id")

        if not github_comment_id:
            print(f"Warning: Comment #{comment.get('id')} has no github_comment_id")
            continue

        if status == "resolved":
            body = format_resolved_message(comment)
            post_comment(pr_number, github_comment_id, body, dry_run)
            resolved_count += 1
        elif status == "skipped":
            body = format_skipped_message(comment)
            post_comment(pr_number, github_comment_id, body, dry_run)
            skipped_count += 1

    print(f"\nSummary: {resolved_count} resolved, {skipped_count} skipped")


if __name__ == "__main__":
    main()
