#!/bin/bash
# verify-test-pr.sh - Verifies resolve-review test results
# Usage: ./verify-test-pr.sh --pr=<number>
# Output: JSON with passed status and assertion results

set -e

# Parse arguments
PR_NUMBER=""
for arg in "$@"; do
  case $arg in
    --pr=*) PR_NUMBER="${arg#*=}" ;;
  esac
done

if [ -z "$PR_NUMBER" ]; then
  echo "Usage: ./verify-test-pr.sh --pr=<number>" >&2
  exit 1
fi

OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
PASSED=true
ASSERTIONS="[]"

add_assertion() {
  local name="$1"
  local expected="$2"
  local actual="$3"
  local pass="$4"
  ASSERTIONS=$(echo "$ASSERTIONS" | jq --arg n "$name" --arg e "$expected" --arg a "$actual" --argjson p "$pass" \
    '. + [{"name": $n, "expected": $e, "actual": $a, "passed": $p}]')
  if [ "$pass" = "false" ]; then
    PASSED=false
  fi
}

echo "Fetching PR state..." >&2

# Get PR data
PR_DATA=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) { nodes { body } }
        }
      }
      comments(first: 100) {
        nodes {
          id
          body
          isMinimized
          author { login }
        }
      }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER")

# Check thread 1 (null check) - should be resolved
T1_RESOLVED=$(echo "$PR_DATA" | jq -r '.data.repository.pullRequest.reviewThreads.nodes[] | select(.comments.nodes[0].body | contains("null check before")) | .isResolved' | head -1)
if [ -z "$T1_RESOLVED" ]; then
  add_assertion "Thread 1 resolved" "true" "not found" false
elif [ "$T1_RESOLVED" = "true" ]; then
  add_assertion "Thread 1 resolved" "true" "true" true
else
  add_assertion "Thread 1 resolved" "true" "$T1_RESOLVED" false
fi

# Check thread 2 (also null) - should be resolved
T2_RESOLVED=$(echo "$PR_DATA" | jq -r '.data.repository.pullRequest.reviewThreads.nodes[] | select(.comments.nodes[0].body | contains("Also needs null")) | .isResolved' | head -1)
if [ -z "$T2_RESOLVED" ]; then
  add_assertion "Thread 2 resolved" "true" "not found" false
elif [ "$T2_RESOLVED" = "true" ]; then
  add_assertion "Thread 2 resolved" "true" "true" true
else
  add_assertion "Thread 2 resolved" "true" "$T2_RESOLVED" false
fi

# Check thread 3 (complex) - should NOT be resolved (deferred)
T3_RESOLVED=$(echo "$PR_DATA" | jq -r '.data.repository.pullRequest.reviewThreads.nodes[] | select(.comments.nodes[0].body | contains("refactoring")) | .isResolved' | head -1)
if [ -z "$T3_RESOLVED" ]; then
  add_assertion "Thread 3 open (deferred)" "false" "not found" false
elif [ "$T3_RESOLVED" = "false" ]; then
  add_assertion "Thread 3 open (deferred)" "false" "false" true
else
  add_assertion "Thread 3 open (deferred)" "false" "$T3_RESOLVED" false
fi

# Check comment 4 (loading state) - should be minimized
C4_MINIMIZED=$(echo "$PR_DATA" | jq -r '.data.repository.pullRequest.comments.nodes[] | select(.body | contains("loading state")) | .isMinimized' | head -1)
if [ -z "$C4_MINIMIZED" ]; then
  add_assertion "Comment 4 minimized" "true" "not found" false
elif [ "$C4_MINIMIZED" = "true" ]; then
  add_assertion "Comment 4 minimized" "true" "true" true
else
  add_assertion "Comment 4 minimized" "true" "$C4_MINIMIZED" false
fi

# Check comment 5 (multi-point) - should be minimized
C5_MINIMIZED=$(echo "$PR_DATA" | jq -r '.data.repository.pullRequest.comments.nodes[] | select(.body | contains("few things about")) | .isMinimized' | head -1)
if [ -z "$C5_MINIMIZED" ]; then
  add_assertion "Comment 5 minimized" "true" "not found" false
elif [ "$C5_MINIMIZED" = "true" ]; then
  add_assertion "Comment 5 minimized" "true" "true" true
else
  add_assertion "Comment 5 minimized" "true" "$C5_MINIMIZED" false
fi

# Check for summary comment (from current user, contains "Feedback Summary")
CURRENT_USER=$(gh api user -q '.login')
SUMMARY_EXISTS=$(echo "$PR_DATA" | jq -r --arg user "$CURRENT_USER" '.data.repository.pullRequest.comments.nodes[] | select(.author.login == $user and (.body | contains("Feedback Summary"))) | .id' | head -1)
if [ -z "$SUMMARY_EXISTS" ]; then
  add_assertion "Summary comment posted" "exists" "not found" false
else
  add_assertion "Summary comment posted" "exists" "exists" true
fi

# Check commit count (should be 4: threads 1+2 grouped, comment 4, comment 5 parts)
COMMIT_COUNT=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
[ "$COMMIT_COUNT" -ge 4 ] && add_assertion "Commits created" ">=4" "$COMMIT_COUNT" true || add_assertion "Commits created" ">=4" "$COMMIT_COUNT" false

# Output JSON
cat << ENDJSON
{
  "passed": $PASSED,
  "pr_number": $PR_NUMBER,
  "assertions": $ASSERTIONS
}
ENDJSON
