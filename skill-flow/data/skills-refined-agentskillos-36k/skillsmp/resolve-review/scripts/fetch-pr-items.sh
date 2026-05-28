#!/bin/bash
set -euo pipefail

# fetch-pr-items.sh - Fetch PR review threads and comments, output as Item JSON
#
# Usage: fetch-pr-items.sh [--pr=N] [--author=NAME] [--self]
#
# Options:
#   --pr=N        PR number (default: current branch's PR)
#   --author=NAME Filter by author (case-insensitive contains)
#   --self        Include own comments (default: exclude)
#
# Output: JSON array of Items to stdout

# Parse arguments
PR_NUMBER=""
AUTHOR_FILTER=""
INCLUDE_SELF=false

for arg in "$@"; do
  case $arg in
    --pr=*) PR_NUMBER="${arg#*=}" ;;
    --author=*) AUTHOR_FILTER="${arg#*=}" ;;
    --self) INCLUDE_SELF=true ;;
    *) echo "Unknown argument: $arg" >&2; exit 1 ;;
  esac
done

# Get repo info
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

# Get PR number if not provided
if [[ -z "$PR_NUMBER" ]]; then
  PR_NUMBER=$(gh pr view --json number -q .number 2>/dev/null || true)
  if [[ -z "$PR_NUMBER" ]]; then
    echo "Error: No open PR for current branch. Use --pr=N to specify." >&2
    exit 1
  fi
fi

# Fetch data via GraphQL
RESPONSE=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  viewer { login }
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      id
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          comments(first: 10) {
            nodes {
              id
              author { login }
              body
              path
              line
              originalLine
              diffHunk
              url
              createdAt
            }
          }
        }
      }
      comments(first: 100) {
        nodes {
          id
          author { login }
          body
          url
          createdAt
          isMinimized
        }
      }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER")

# Check if PR exists
if echo "$RESPONSE" | jq -e '.data.repository.pullRequest == null' > /dev/null; then
  echo "Error: PR #$PR_NUMBER not found." >&2
  exit 1
fi

# Extract current user
CURRENT_USER=$(echo "$RESPONSE" | jq -r '.data.viewer.login')

# Build jq filter for threads
THREAD_FILTER='.isResolved == false'
if [[ "$INCLUDE_SELF" != "true" ]]; then
  THREAD_FILTER="$THREAD_FILTER and .comments.nodes[0].author.login != \"$CURRENT_USER\""
fi
if [[ -n "$AUTHOR_FILTER" ]]; then
  THREAD_FILTER="$THREAD_FILTER and (.comments.nodes[0].author.login | ascii_downcase | contains(\"${AUTHOR_FILTER,,}\"))"
fi

# Build jq filter for comments
COMMENT_FILTER='.isMinimized == false'
if [[ "$INCLUDE_SELF" != "true" ]]; then
  COMMENT_FILTER="$COMMENT_FILTER and .author.login != \"$CURRENT_USER\""
fi
if [[ -n "$AUTHOR_FILTER" ]]; then
  COMMENT_FILTER="$COMMENT_FILTER and (.author.login | ascii_downcase | contains(\"${AUTHOR_FILTER,,}\"))"
fi

# Transform to Items JSON
echo "$RESPONSE" | jq --arg prId "$(echo "$RESPONSE" | jq -r '.data.repository.pullRequest.id')" \
  --arg threadFilter "$THREAD_FILTER" \
  --arg commentFilter "$COMMENT_FILTER" '
def gist: (.[0:40] | gsub("\n"; " ") | gsub("\\s+"; " ") | if length > 37 then .[0:37] + "..." else . end);

.data.repository.pullRequest as $pr |

# Process threads
[
  $pr.reviewThreads.nodes[]
  | select('"$THREAD_FILTER"')
  | {
      type: "threads",
      feedback: [
        .comments.nodes[0] | {
          url: .url,
          author: .author.login,
          created: .createdAt,
          body: .body,
          gist: (.body | gist),
          outdated: false,
          file: .path,
          line: (.line // .originalLine),
          diffHunk: .diffHunk,
          replies: (if (.comments.nodes | length) > 1 then
            [.comments.nodes[1:][] | {author: .author.login, body: .body, created: .createdAt}]
          else [] end)
        }
      ],
      _threadId: .id,
      _commentId: .comments.nodes[0].id,
      _outdated: .isOutdated
    }
] +

# Process PR comments
[
  $pr.comments.nodes[]
  | select('"$COMMENT_FILTER"')
  | {
      type: "comment-part",
      feedback: [{
        url: .url,
        author: .author.login,
        created: .createdAt,
        body: .body,
        gist: (.body | gist),
        outdated: false,
        partIndex: 1,
        partTotal: 1,
        parentBody: .body
      }],
      _commentId: .id
    }
]

# Add item IDs and sort
| sort_by(.feedback[0].created)
| to_entries
| map(.value + {id: (.key + 1), _prNodeId: $prId})
'
