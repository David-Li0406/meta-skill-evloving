#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage:
  pr_feedback.sh [-R OWNER/REPO] PR_NUMBER

Outputs a single JSON object containing:
- pr: core PR metadata + reviews + PR (issue) comments
- reviewComments: inline review comments (REST: list review comments)
- reviewThreads: review threads (GraphQL: includes resolved/outdated state)

Notes:
- Requires: gh, jq
- Defaults repo from current directory if -R is omitted
- GraphQL reviewThreads fetch is limited to first 100 threads/comments (no pagination)
EOF
}

repo=""
while getopts ":R:h" opt; do
  case "$opt" in
    R) repo="$OPTARG" ;;
    h) usage; exit 0 ;;
    \?) usage; exit 2 ;;
  esac
done
shift $((OPTIND-1))

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is required" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required" >&2
  exit 1
fi

pr_number="$1"

if [[ -z "$repo" ]]; then
  repo="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
fi
if [[ -z "$repo" ]]; then
  echo "Unable to determine repo. Pass -R OWNER/REPO or run inside a repo checkout." >&2
  exit 1
fi

owner="${repo%/*}"
name="${repo#*/}"

tmp_dir="$(mktemp -d)"
cleanup() { rm -rf "$tmp_dir"; }
trap cleanup EXIT

pr_file="$tmp_dir/pr.json"
review_comments_file="$tmp_dir/review_comments.json"
review_threads_file="$tmp_dir/review_threads.json"

gh pr view -R "$repo" "$pr_number" \
  --json number,title,url,state,author,createdAt,updatedAt,baseRefName,headRefName,mergeable,mergeStateStatus,reviewDecision,comments,reviews \
  >"$pr_file"

gh api --paginate -H "Accept: application/vnd.github+json" \
  "/repos/$owner/$name/pulls/$pr_number/comments?per_page=100" \
  >"$review_comments_file"

read -r -d '' query <<'GRAPHQL' || true
query($owner:String!, $name:String!, $number:Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      id
      number
      url
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          startLine
          diffSide
          startDiffSide
          viewerCanReply
          viewerCanResolve
          comments(first: 100) {
            nodes {
              id
              databaseId
              url
              createdAt
              author { login }
              body
            }
          }
        }
      }
    }
  }
}
GRAPHQL

gh api graphql -f query="$query" -F owner="$owner" -F name="$name" -F number="$pr_number" >"$review_threads_file"

jq -n \
  --arg repo "$repo" \
  --arg prNumber "$pr_number" \
  --slurpfile pr "$pr_file" \
  --slurpfile reviewComments "$review_comments_file" \
  --slurpfile reviewThreads "$review_threads_file" \
  '{
    repo: $repo,
    prNumber: ($prNumber | tonumber),
    pr: $pr[0],
    reviewComments: $reviewComments[0],
    reviewThreads: $reviewThreads[0].data.repository.pullRequest.reviewThreads.nodes
  }'

