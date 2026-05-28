---
name: github-pr-comments
description: Fetches GitHub PR review comments, categorizes them, and guides resolution. Use when addressing PR review feedback.
---

# GitHub PR Comments Manager

Fetches review comments from a PR, categorizes by resolution status, and guides systematic fixes.

**Alternative:** If MCP tools fail, use `scripts/` pipeline (requires `gh` CLI auth).

## Workflow

### Step 1: Identify PR

1. Get current branch: `git branch --show-current`
2. Get repository info: `git remote -v` (extract owner/repo from origin URL)
3. Find matching PR using GitHub MCP tool:
   ```typescript
   // MCP Tool Call
   CallMcpTool({
     server: "user-github",
     toolName: "list_pull_requests",
     arguments: {
       owner: "<org-name>",
       repo: "<repo-name>",
       state: "open"
     }
   })
   ```
4. Match the current branch to a PR's `head.ref` field
5. If multiple PRs match, ask user for the PR number

### Step 2: Fetch Review Comments

Use the GitHub MCP tool `pull_request_read` with method `get_review_comments` to get all review threads:

```typescript
// MCP Tool Call
CallMcpTool({
  server: "user-github",
  toolName: "pull_request_read",
  arguments: {
    owner: "<org-name>",
    repo: "<repo-name>",
    pullNumber: <pr-number>,
    method: "get_review_comments",
    perPage: 100
  }
})
```

The response includes `reviewThreads` with fields:
- `IsResolved`: boolean - whether the thread is resolved
- `IsOutdated`: boolean - whether the code has changed since the comment
- `Comments.Nodes[].Body`: the comment text
- `Comments.Nodes[].Author.Login`: the reviewer's username

### Step 3: Categorize Comments

Process the response and categorize each thread:

**Unresolved (Needs Action):**
- `IsResolved === false` AND `IsOutdated === false`
- These require immediate attention

**Unresolved but Outdated:**
- `IsResolved === false` AND `IsOutdated === true`
- Code may have changed; verify if still relevant

**Resolved:**
- `IsResolved === true`
- No action needed

### Step 4: Present Summary

Use template: [review-comments-summary.md](assets/templates/review-comments-summary.md)

### Step 5: Address Unresolved Comments

For each unresolved comment:

1. **Read the affected file** at the specified line
2. **Assess priority** and apply fixes per [equipqr-resolution-playbook.md](references/equipqr-resolution-playbook.md)
3. **Verify fix:** `npm run type-check && npm run lint`

### Step 6: Commit and Push

After all fixes are applied:

1. **Commit changes:**
   ```bash
   git add .
   git commit -m "fix: address review comments for PR #<number>"
   ```

2. **Push to branch:**
   ```bash
   git push
   ```

### Step 7: Comment on PR

After pushing, post a summary using template [fixed-review-comments-comment.md](assets/templates/fixed-review-comments-comment.md):

```typescript
CallMcpTool({
  server: "user-github",
  toolName: "add_issue_comment",
  arguments: {
    owner: "<org-name>",
    repo: "<repo-name>",
    issue_number: <pr-number>,
    body: "<rendered template>"
  }
})
```

## Quick Reference

| IsResolved | IsOutdated | Status | Action |
|------------|------------|--------|--------|
| `false` | `false` | **Needs Action** | Must address |
| `false` | `true` | Outdated | Verify if still relevant |
| `true` | `false` | Resolved | No action needed |
| `true` | `true` | Resolved + Outdated | No action needed |
