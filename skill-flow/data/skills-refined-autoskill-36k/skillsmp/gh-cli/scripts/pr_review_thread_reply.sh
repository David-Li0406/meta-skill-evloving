#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage:
  pr_review_thread_reply.sh THREAD_ID --body "TEXT"
  pr_review_thread_reply.sh THREAD_ID --body-file path/to/body.txt

Replies to a PR review thread (GraphQL).

THREAD_ID is the GraphQL node id for a PullRequestReviewThread (e.g. PRRT_...),
which you can fetch via:
  ./skills/gh-cli/scripts/pr_feedback.sh -R OWNER/REPO PR_NUMBER | jq -r '.reviewThreads[] | select(.isResolved == false) | .id'
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

thread_id="$1"
shift

body=""
body_file=""

while [[ $# -gt 0 ]]; do
  case "$1" in
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
    *)
      break
      ;;
  esac
done

if [[ -z "$body" && -n "$body_file" ]]; then
  body="$(cat "$body_file")"
fi
if [[ -z "$body" ]]; then
  echo "Missing --body or --body-file" >&2
  exit 2
fi

read -r -d '' mutation <<'GRAPHQL' || true
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
    comment { id databaseId url }
  }
}
GRAPHQL

gh api graphql -f query="$mutation" -F threadId="$thread_id" -F body="$body" -q '.data.addPullRequestReviewThreadReply.comment'

