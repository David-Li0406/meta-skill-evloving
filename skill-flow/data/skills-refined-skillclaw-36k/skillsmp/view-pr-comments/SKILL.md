---
name: view-pr-comments
description: Use when user says "看 PR comment" or "查看 PR" - view PR details, comments, and reviews
---

# View PR Comments

## Overview

View Pull Request comments, reviews, and details using GitHub CLI.

**Announce at start:** "I'm using the view-pr-comments skill to view PR information."

## When to Use

- User says "看 PR comment" or "查看 PR"
- Need to check PR review feedback
- Want to see conversation thread
- Need to understand PR status

## The Process

### Option 1: View PR Details with Comments

**Command:**
```bash
gh pr view --comments
```

**What it shows:**
- PR information (title, status, author, etc.)
- Review comments from reviewers
- Conversation thread

### Option 2: View PR Comments (留言區)

**Command:**
```bash
gh api repos/:owner/:repo/pulls/$(gh pr view --json number --jq '.number')/comments --jq '.[] | {id: .id, author: .user.login, body: .body, createdAt: .created_at}'
```

**What it shows:**
- All comments in the conversation thread
- Comment ID, author, body, creation time
- Useful for finding specific comments to reply to

**Note:** Replace `:owner/:repo` with actual repo name (e.g., `gmliao/swift-state-tree`)

### Option 3: View PR Reviews (Review Comments)

**Command:**
```bash
gh pr view --json reviews --jq '.reviews[] | select(.state == "COMMENTED") | {body: .body, author: .author.login}'
```

**What it shows:**
- Review comments from reviewers
- Only shows reviews with "COMMENTED" state
- Author and comment body

### Option 4: View All Comments and Reviews Together

**Command:**
```bash
gh pr view --json comments,reviews --jq '{comments: .comments, reviews: .reviews}'
```

**What it shows:**
- Complete view of all comments and reviews
- Structured JSON output
- Useful for comprehensive review

### Option 5: Open PR in Browser

**Command:**
```bash
gh pr view --web
```

**What it does:**
- Opens PR in default web browser
- Full GitHub UI with all comments and reviews
- Best for detailed review

## Getting PR Number

If you need the PR number:
```bash
gh pr view --json number --jq '.number'
```

## Getting Repo Name

If you need the repo name:
```bash
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

Example output: `gmliao/swift-state-tree`

## Common Use Cases

### View Latest PR Comments
```bash
gh pr view --comments | head -50
```

### Find Comments by Specific Author
```bash
gh pr view --json comments --jq '.comments[] | select(.author.login == "username") | {body: .body, createdAt: .created_at}'
```

### View Line Comments
```bash
gh api repos/gmliao/swift-state-tree/pulls/$(gh pr view --json number --jq '.number')/comments --jq '.[] | {id: .id, path: .path, line: .line, body: (.body | split("\n")[0:2] | join("\n"))}'
```

## Integration with Other Skills

After viewing comments:
- Use `SwiftStateTree/reply-pr-comment` to reply to specific comments
- Use `Superpowers/receiving-code-review` to respond to feedback systematically
