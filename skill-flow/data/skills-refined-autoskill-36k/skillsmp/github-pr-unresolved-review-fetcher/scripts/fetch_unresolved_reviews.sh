#!/bin/bash
# Fetch unresolved PR review comments using GitHub GraphQL API
# Usage: ./fetch_unresolved_reviews.sh <owner> <repo> <pr_number>

set -e

OWNER="${1:?Usage: $0 <owner> <repo> <pr_number>}"
REPO="${2:?Usage: $0 <owner> <repo> <pr_number>}"
PR_NUMBER="${3:?Usage: $0 <owner> <repo> <pr_number>}"

RESULT=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
        pullRequest(number: $number) {
            reviewThreads(first: 100) {
                nodes {
                    isResolved
                    isOutdated
                    path
                    line
                    comments(first: 10) {
                        nodes {
                            author { login }
                            body
                        }
                    }
                }
            }
        }
    }
}' -f owner="$OWNER" -f repo="$REPO" -F number="$PR_NUMBER" 2>&1)

if [ $? -ne 0 ]; then
    echo "Error fetching PR reviews: $RESULT" >&2
    exit 1
fi

echo "$RESULT" | jq -r '
    .data.repository.pullRequest.reviewThreads.nodes
    | map(select(.isResolved == false and .isOutdated == false))
    | if length == 0 then
        "<no-unresolved-comments />"
      else
        .[] |
        "<review-comment>",
        "  <file>\(.path // "unknown")</file>",
        "  <line>\(.line // "unknown")</line>",
        "  <author>\(.comments.nodes[0].author.login // "unknown")</author>",
        "  <body>\(.comments.nodes[0].body // "")</body>",
        "</review-comment>",
        ""
      end
'
