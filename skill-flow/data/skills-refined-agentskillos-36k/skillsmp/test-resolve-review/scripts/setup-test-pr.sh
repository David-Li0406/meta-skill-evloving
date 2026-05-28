#!/bin/bash
# setup-test-pr.sh - Creates test fixtures for resolve-review integration testing
# Usage: ./setup-test-pr.sh
# Output: JSON with pr_number, branch, thread_ids, comment_ids

set -e

BRANCH="test/resolve-review-fixture-$(date +%s)"
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')

echo "Creating test branch..." >&2
git checkout -b "$BRANCH"

echo "Creating test file..." >&2
cat > test-fixture-file.ts << 'EOF'
// Fixture code for resolve-review testing

function processUser(user: unknown) {
  // Thread 1 target: "Add null check before accessing user.name"
  console.log(user.name);

  // Thread 2 target: "Also needs null check here" (groups with Thread 1)
  console.log(user.email);

  return user;
}

// Spacer to separate line numbers




function complexFunction(data: any) {
  // Thread 3 target: "This needs refactoring - significant rework"
  // Expected action: DEFER
  return data.map((x: any) => x.value).filter(Boolean);
}

function loadData() {
  // PR Comment 4 target: "Add loading state while fetching"
  return fetch('/api/data');
}

function handleError(err: Error) {
  // PR Comment 5 target (multi-point):
  // "Fix error handling. Also add types. And tests."
  console.log(err);
}
EOF

git add test-fixture-file.ts
git commit -m "test: add fixture file for resolve-review testing"
git push -u origin "$BRANCH"

echo "Creating PR..." >&2
PR_URL=$(gh pr create --title "Test: resolve-review fixtures" --body "Integration test PR - do not merge" --head "$BRANCH")
PR_NUMBER=$(echo "$PR_URL" | grep -oE '[0-9]+$')

echo "Fetching PR node ID..." >&2
PR_NODE_ID=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) { id }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER" -q '.data.repository.pullRequest.id')

echo "Adding review threads..." >&2

# Thread 1: null check on line 5
THREAD1=$(gh api graphql -f query='
mutation($prId: ID!, $path: String!, $line: Int!, $body: String!) {
  addPullRequestReviewThread(input: {
    pullRequestId: $prId,
    path: $path,
    line: $line,
    body: $body
  }) { thread { id } }
}' -f prId="$PR_NODE_ID" -f path="test-fixture-file.ts" -F line=5 \
   -f body="Add null check before accessing user.name" \
   -q '.data.addPullRequestReviewThread.thread.id')

# Thread 2: also null check on line 8
THREAD2=$(gh api graphql -f query='
mutation($prId: ID!, $path: String!, $line: Int!, $body: String!) {
  addPullRequestReviewThread(input: {
    pullRequestId: $prId,
    path: $path,
    line: $line,
    body: $body
  }) { thread { id } }
}' -f prId="$PR_NODE_ID" -f path="test-fixture-file.ts" -F line=8 \
   -f body="Also needs null check here - same issue as above" \
   -q '.data.addPullRequestReviewThread.thread.id')

# Thread 3: complex refactor on line 22
THREAD3=$(gh api graphql -f query='
mutation($prId: ID!, $path: String!, $line: Int!, $body: String!) {
  addPullRequestReviewThread(input: {
    pullRequestId: $prId,
    path: $path,
    line: $line,
    body: $body
  }) { thread { id } }
}' -f prId="$PR_NODE_ID" -f path="test-fixture-file.ts" -F line=22 \
   -f body="This needs refactoring to use proper types and error handling - significant rework required, probably out of scope for this PR" \
   -q '.data.addPullRequestReviewThread.thread.id')

echo "Adding PR comments..." >&2

# Comment 4: single-point
COMMENT4=$(gh api graphql -f query='
mutation($prId: ID!, $body: String!) {
  addComment(input: {subjectId: $prId, body: $body}) {
    commentEdge { node { id } }
  }
}' -f prId="$PR_NODE_ID" \
   -f body="Add loading state while fetching data in loadData function" \
   -q '.data.addComment.commentEdge.node.id')

# Comment 5: multi-point (3 parts)
COMMENT5=$(gh api graphql -f query='
mutation($prId: ID!, $body: String!) {
  addComment(input: {subjectId: $prId, body: $body}) {
    commentEdge { node { id } }
  }
}' -f prId="$PR_NODE_ID" \
   -f body="A few things about handleError:

1. Fix error handling - currently just logs, should throw or return
2. Also add proper types for the error parameter
3. And we need tests for this function" \
   -q '.data.addComment.commentEdge.node.id')

# Output JSON
cat << ENDJSON
{
  "pr_number": $PR_NUMBER,
  "branch": "$BRANCH",
  "pr_node_id": "$PR_NODE_ID",
  "threads": {
    "thread1_null_check": "$THREAD1",
    "thread2_also_null": "$THREAD2",
    "thread3_complex": "$THREAD3"
  },
  "comments": {
    "comment4_loading": "$COMMENT4",
    "comment5_multipoint": "$COMMENT5"
  }
}
ENDJSON
