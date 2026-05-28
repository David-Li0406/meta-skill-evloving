#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage:
  pr_review_thread_resolve.sh THREAD_ID

Marks a PR review thread as resolved (GraphQL).

THREAD_ID is the GraphQL node id for a PullRequestReviewThread (e.g. PRRT_...).
EOF
}

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

thread_id="$1"

read -r -d '' mutation <<'GRAPHQL' || true
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved }
  }
}
GRAPHQL

gh api graphql -f query="$mutation" -F threadId="$thread_id" -q '.data.resolveReviewThread.thread'

