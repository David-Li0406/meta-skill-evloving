#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage:
  pr_review_comment_reply.sh [-R OWNER/REPO] PR_NUMBER COMMENT_ID --body "TEXT"
  pr_review_comment_reply.sh [-R OWNER/REPO] PR_NUMBER COMMENT_ID --body-file path/to/body.txt

Replies to an existing inline PR review comment (REST).

Uses:
  POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies
EOF
}

repo=""
body=""
body_file=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -R)
      repo="$2"
      shift 2
      ;;
    --body)
      body="$2"
      shift 2
      ;;
    --body-file)
      body_file="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -lt 2 ]]; then
  usage
  exit 2
fi

pr_number="$1"
comment_id="$2"
shift 2

if [[ -z "$body" && -n "$body_file" ]]; then
  body="$(cat "$body_file")"
fi
if [[ -z "$body" ]]; then
  echo "Missing --body or --body-file" >&2
  exit 2
fi

if [[ -z "$repo" ]]; then
  repo="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
fi
if [[ -z "$repo" ]]; then
  echo "Unable to determine repo. Pass -R OWNER/REPO or run inside a repo checkout." >&2
  exit 1
fi

owner="${repo%/*}"
name="${repo#*/}"

gh api -X POST -H "Accept: application/vnd.github+json" \
  "/repos/$owner/$name/pulls/$pr_number/comments/$comment_id/replies" \
  -f body="$body"

