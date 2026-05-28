---
name: gh-cli
description: "GitHub CLI patterns for PR reviews, comments, and API operations. Use when working with gh api commands, especially for review threads and comments."
---

# GitHub CLI Patterns

Common `gh` CLI patterns for PR operations, especially review comments and thread resolution.

## When to Use

- Replying to PR review comments
- Resolving review threads
- Querying PR review data
- Any `gh api` or `gh api graphql` operation

---

## PR Review Comments

### Reply to a Review Comment (REST API)

**Correct endpoint:** `/repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies`

```bash
# Reply to a specific review comment
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments/COMMENT_ID/replies \
  -X POST \
  -f body="Your reply message here"
```

**Example:**
```bash
gh api repos/erikpr1994/myrepo/pulls/123/comments/2705458190/replies \
  -X POST \
  -f body="Fixed in commit abc123"
```

### Common Mistake - Wrong Endpoint

```bash
# WRONG - This creates a NEW comment, not a reply
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments \
  -X POST \
  -f body="..." \
  -f in_reply_to=COMMENT_ID  # This field doesn't work here!

# CORRECT - Use the /replies sub-endpoint
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments/COMMENT_ID/replies \
  -X POST \
  -f body="..."
```

### List All PR Comments

```bash
# Get all review comments on a PR
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments \
  --jq '.[] | {id: .id, user: .user.login, body: .body[:80], path: .path}'
```

---

## Review Threads (GraphQL)

### Get All Review Threads

```bash
# List all review threads with resolution status
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              body
              author { login }
            }
          }
        }
      }
    }
  }
}'
```

### Get Only Unresolved Threads

```bash
# Count unresolved threads
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
        }
      }
    }
  }
}' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length'
```

### Resolve a Review Thread

```bash
# Resolve a thread by its ID
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID"}) {
    thread {
      isResolved
    }
  }
}'
```

**Example with actual thread ID:**
```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "PRRT_kwDONAi3wc6XYZABC"}) {
    thread {
      isResolved
    }
  }
}'
```

---

## GraphQL Variable Escaping

### The Problem

GraphQL uses `$` for variables, but bash also interprets `$`. This causes issues:

```bash
# BROKEN - bash interprets $owner as a shell variable
gh api graphql -f query='query($owner: String!) { ... }'
# Error: Expected VAR_SIGN, actual: UNKNOWN_CHAR ("")
```

### Solution 1: Hardcode Values (Simplest)

```bash
# Works - no variables to escape
gh api graphql -f query='
query {
  repository(owner: "erikpr1994", name: "myrepo") {
    pullRequest(number: 123) {
      title
    }
  }
}'
```

### Solution 2: Use -F for GraphQL Variables

```bash
# Works - use -F (uppercase) for typed parameters
gh api graphql \
  -F owner="erikpr1994" \
  -F repo="myrepo" \
  -F pr=123 \
  -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      title
    }
  }
}'
```

**Note:** `-F` (uppercase) passes typed values. `-f` (lowercase) passes strings.

### Solution 3: Escape the Dollar Signs

```bash
# Works - escape $ with backslash
gh api graphql -f query='
query(\$owner: String!, \$repo: String!, \$pr: Int!) {
  repository(owner: \$owner, name: \$repo) {
    pullRequest(number: \$pr) {
      title
    }
  }
}' -F owner="erikpr1994" -F repo="myrepo" -F pr=123
```

### Recommendation

**Use hardcoded values** when possible (Solution 1). It's simpler and avoids escaping issues. Only use variables when you need dynamic values.

---

## Complete Workflow: Process PR Review Threads

### Step 1: Get Unresolved Threads

```bash
# Get thread IDs and first comment
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              id
              body
              author { login }
            }
          }
        }
      }
    }
  }
}' | jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)'
```

### Step 2: Reply to Each Comment

```bash
# For each unresolved thread, reply to its comment
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments/COMMENT_ID/replies \
  -X POST \
  -f body="Fixed in commit abc123"
```

### Step 3: Resolve Each Thread

```bash
# Resolve the thread
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID_HERE"}) {
    thread { isResolved }
  }
}'
```

### Step 4: Verify All Resolved

```bash
# Should return 0
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100) {
        nodes { isResolved }
      }
    }
  }
}' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length'
```

---

## Other Useful Patterns

### Get PR Details

```bash
gh pr view PR_NUMBER --json number,title,state,reviewDecision,statusCheckRollup
```

### List PR Checks

```bash
gh pr checks PR_NUMBER
gh pr checks PR_NUMBER --watch  # Wait for completion
```

### Request Reviewers

```bash
gh pr edit PR_NUMBER --add-reviewer username1,username2
```

### Create PR

```bash
gh pr create --title "feat: my feature" --body "Description here"
```

### Merge PR

```bash
gh pr merge PR_NUMBER --squash --delete-branch
```

---

## Quick Reference

| Operation | Command |
|-----------|---------|
| Reply to comment | `gh api repos/O/R/pulls/N/comments/ID/replies -X POST -f body="..."` |
| Resolve thread | `gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "ID"}) { thread { isResolved } } }'` |
| List threads | `gh api graphql -f query='query { repository(...) { pullRequest(...) { reviewThreads(...) } } }'` |
| Count unresolved | `... \| jq '[... \| select(.isResolved == false)] \| length'` |
| PR checks | `gh pr checks N --watch` |
| Request review | `gh pr edit N --add-reviewer user` |

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Expected VAR_SIGN, actual: UNKNOWN_CHAR` | Bash ate the `$` in GraphQL | Use hardcoded values or escape `\$` |
| `"in_reply_to" is not a permitted key` | Wrong endpoint for replies | Use `/comments/{id}/replies` endpoint |
| `No subschema in "oneOf" matched` | Missing required fields | Check API docs for required params |
| `InputObject doesn't accept argument` | Wrong GraphQL mutation | Verify mutation field names |

---

## Integration

**Used by:**
- submit-pr (Phase 6 - review feedback)
- pr-feedback-tracker
- coderabbit

**Related:**
- git-expert
- pr-workflow
