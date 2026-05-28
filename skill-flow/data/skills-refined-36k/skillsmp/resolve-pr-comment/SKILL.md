---
name: resolve-pr-comment
description: Resolve a PR review comment thread using the GitHub CLI. ONLY use this as part of the pr-review-comments skill workflow after addressing a comment. Takes a comment ID (PRRC_...) and resolves its parent thread.
---

# Resolve PR Review Comment

Helper skill to resolve PR review comment threads via the gh CLI. **Only use this during the `pr-review-comments` workflow** after you've addressed a comment.

## Prerequisites

- `gh` CLI installed and authenticated
- Currently on a branch with an open PR
- Comment ID from the review feedback file (format: `PRRC_...`)

## Usage

After addressing a PR review comment, resolve its thread:

### Step 1: Get Repository and PR Info

```bash
# Get repo info from git remote
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# Get PR number for current branch
PR_NUMBER=$(gh pr view --json number -q .number)
```

### Step 2: Find Thread ID from Comment ID

The comment files use comment IDs (`PRRC_...`), but we need the thread ID (`PRRT_...`) to resolve. Query the PR to find it:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              id
            }
          }
        }
      }
    }
  }
}' -f owner="OWNER" -f repo="REPO" -F pr=PR_NUMBER
```

Find the thread where `comments.nodes[0].id` matches your comment ID (e.g., `PRRC_kwDOOjkBEM6gPPfE`). The parent `id` is the thread ID (e.g., `PRRT_kwDOOjkBEM5pQksb`).

### Step 3: Resolve the Thread

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "PRRT_..."}) {
    thread {
      isResolved
    }
  }
}'
```

## One-Liner Pattern

For a known comment ID, you can combine these steps. Example for `nebariai/nebari-mvp` PR #3264:

```bash
# Query threads and find the one containing your comment ID
gh api graphql -f query='
query {
  repository(owner: "nebariai", name: "nebari-mvp") {
    pullRequest(number: 3264) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              id
            }
          }
        }
      }
    }
  }
}'
```

Then resolve with the thread ID you found:

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "PRRT_xxxxx"}) {
    thread {
      isResolved
    }
  }
}'
```

## Important Notes

- **Thread vs Comment**: Comments (`PRRC_`) are nested inside threads (`PRRT_`). You resolve threads, not individual comments.
- **Only use after fixing**: Don't resolve comments you haven't actually addressed.
- **Part of pr-review-comments workflow**: This is a helper skill, not standalone. Use it after completing a batch in the pr-review-comments workflow.
