---
name: reply-pr-comment
description: Use when user wants to reply to a specific PR comment thread
---

# Reply to PR Comment

## Overview

Reply to specific Pull Request comments using GitHub CLI.

**Announce at start:** "I'm using the reply-pr-comment skill to respond to PR feedback."

## When to Use

- User wants to reply to a specific comment thread
- Need to respond to review feedback
- Want to clarify implementation decisions
- Need to acknowledge feedback

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- PR number or current PR context
- Comment ID from the comment you want to reply to

## The Process

### Step 1: Get Repository Name

**Command:**
```bash
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

**Example output:** `gmliao/swift-state-tree`

**Note:** Use actual repo name instead of `:owner/:repo` placeholder.

### Step 2: Get PR Number

**Command:**
```bash
gh pr view --json number --jq '.number'
```

**Example output:** `24`

### Step 3: Find Comment ID

**Option A: View Line Comments**
```bash
gh api repos/gmliao/swift-state-tree/pulls/24/comments --jq '.[] | {id: .id, path: .path, line: .line, body: (.body | split("\n")[0:2] | join("\n"))}'
```

**Option B: View Review Comments**
```bash
gh pr view 24 --json reviews --jq '.reviews[].comments[] | {id: .id, author: .author.login, body: (.body | split("\n")[0:2] | join("\n"))}'
```

**Output format:**
```json
{
  "id": 2700778279,
  "path": "Sources/SwiftStateTree/Sync/SyncEngine.swift",
  "line": 123,
  "body": "This could be optimized..."
}
```

### Step 4: Reply to Comment

**Command:**
```bash
gh api --method POST repos/gmliao/swift-state-tree/pulls/24/comments/2700778279/replies -f body="Your reply text"
```

**Example:**
```bash
gh api --method POST repos/gmliao/swift-state-tree/pulls/24/comments/2700778279/replies -f body="Thanks for the review! I've updated the implementation to address your concerns."
```

## Complete Example

```bash
# Get repo name
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# Get PR number
PR_NUMBER=$(gh pr view --json number --jq '.number')

# Find comment ID (example: looking for comments on SyncEngine.swift)
COMMENT_ID=$(gh api repos/$REPO/pulls/$PR_NUMBER/comments --jq '.[] | select(.path == "Sources/SwiftStateTree/Sync/SyncEngine.swift") | .id' | head -1)

# Reply to comment
gh api --method POST repos/$REPO/pulls/$PR_NUMBER/comments/$COMMENT_ID/replies -f body="Thanks for the feedback! I've addressed this in the latest commit."
```

## Reply Best Practices

- **Be respectful**: Acknowledge feedback positively
- **Be specific**: Reference the exact concern or suggestion
- **Be actionable**: Explain what you've done or will do
- **Be concise**: Keep replies focused and clear

## Common Reply Templates

### Acknowledging Feedback
```
Thanks for the review! I've updated the implementation to address your concerns.
```

### Explaining Decision
```
I understand your concern. I chose this approach because [reason]. Let me know if you'd prefer a different solution.
```

### Requesting Clarification
```
Thanks for the feedback! Could you clarify what you mean by [specific point]? I want to make sure I address it correctly.
```

### Indicating Fix
```
Good catch! I've fixed this in commit [hash]. The implementation now [what changed].
```

## Integration with Other Skills

- Use `SwiftStateTree/view-pr-comments` to find comments to reply to
- Use `Superpowers/receiving-code-review` for systematic review response workflow
