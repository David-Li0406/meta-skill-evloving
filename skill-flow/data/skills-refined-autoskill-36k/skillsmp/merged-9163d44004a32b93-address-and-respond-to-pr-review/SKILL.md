---
name: address-and-respond-to-pr-review
description: Use this skill when you need to fetch, analyze, and address review comments on pull requests, including responding to reviewers and fixing issues raised in code reviews.
---

# Address and Respond to PR Review

This skill allows you to handle unresolved PR review comments, address feedback, and respond to reviewers.

## Process

### 1. Determine PR Number

If not provided, detect from the current branch:

```bash
gh pr view --json number -q .number
```

### 2. Fetch Review Comments

Get PR details and fetch review comments:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments
```

### 3. Fetch Unresolved Comments and Review Thread IDs

Fetch unresolved threads via GraphQL:

```bash
gh api graphql -f query='
query {
  repository(owner: "{owner}", name: "{repo}") {
    pullRequest(number: {pr}) {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes {
              body
              path
              line
            }
          }
        }
      }
    }
  }
}'
```

### 4. Present Unresolved Comments

Summarize each unresolved comment showing:

- File path and line number
- The core issue (ignore HTML badges, buttons, metadata)
- Severity if mentioned (High/Medium/Low)

### 5. Verify Before Fixing

Read the relevant code and verify each issue is valid before fixing.

### 6. Launch PR Comment Reviewer Agents

For each unresolved comment, launch a `pr-comment-reviewer` agent in parallel. Use the following prompt structure:

```
Review this PR comment and evaluate whether the suggested change should be implemented:

**File**: {path}
**Line**: {line}
**Comment**:
{body}

Provide a critical but reasonable evaluation of:
1. Whether this change is necessary
2. The proposed solution (if any) vs alternatives
3. Your recommendation
```

### 7. Generate Report

Consolidate agent responses into a summary:

```markdown
# PR Review Comment Analysis for PR #{number}

Found {N} unresolved comments.

## Summary

- **Should Fix**: {count} comments
- **Optional**: {count} comments
- **Skip**: {count} comments

---

## Comment 1: {Short description}

**File**: {path}:{line}
**Verdict**: {Should Fix / Optional / Skip}

{Agent's reasoning and recommendation}

---

## Overall Recommendation

{Synthesized recommendation across all comments}
```

### 8. Fix and Respond

For each valid issue:

1. Fix the code.
2. Reply to the thread with the Claude signature:

```bash
# Write response with signature
printf '%s\n' \
  'Fixed! [explanation of what was changed]' \
  '' \
  '🤖 _Response by [Claude Code](https://claude.com/claude-code)_' \
  > /tmp/claude/pr-comment.md

# Post the comment
gh api graphql -f query='
mutation($body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: "{thread_id}"
    body: $body
  }) {
    comment { id }
  }
}' -f body="$(cat /tmp/claude/pr-comment.md)"
```

3. Resolve the thread:

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: { threadId: "{thread_id}" }) {
    thread { isResolved }
  }
}'
```

4. Clean up:

```bash
rm /tmp/claude/pr-comment.md
```

### 9. Commit and Push

Commit all fixes with a message referencing the review feedback, then push.

## Guidelines

- Only analyze unresolved comments (`isResolved == false`).
- Launch agents in parallel for speed.
- Be critical but reasonable about recommendations.
- Consolidate duplicate comments.
- Use clear verdicts: Should Fix, Optional, or Skip.

## Examples

**User says:** "Check the PR comments"  
**Action:** Fetch comments for the current branch's PR, present issues, ask which to fix.

**User says:** "Address the review feedback on PR 42"  
**Action:** Fetch comments for PR #42, fix valid issues, respond and resolve threads.

**User says:** "Respond to the reviewers"  
**Action:** Reply to review threads explaining fixes, resolve addressed comments.