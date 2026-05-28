---
name: address-review-comments
description: Addresses PR review comments systematically. Use when fixing review feedback, responding to code review threads, or processing PR comments.
---

# Address Review Comments

## Workflow

- [ ] Identify target PR and ensure correct branch
- [ ] Fetch review comments
- [ ] Clarify ambiguous feedback with user
- [ ] Fix each comment (one commit per fix)
- [ ] Confirm changes with user
- [ ] Push changes
- [ ] Reply to review threads with commit references

## Step 1: Identify Target PR

### If given a PR URL (e.g., `https://github.com/owner/repo/pull/123`)

Extract owner, repo, and PR number from the URL.

Check current repo matches:
```bash
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

Check out the PR branch:
```bash
gh pr checkout 123        # normal checkout
gh pr checkout 123 --force  # if local changes conflict
```

### If no URL provided

Find PR for current branch:
```bash
gh pr view --json number,title,url,headRefName
```

If no PR exists for current branch, ask the user which PR to address.

## Step 2: Fetch Comments

### Get review comments (code review threads)

Use the `github-mcp-server-pull_request_read` tool:
```
method: "get_review_comments"
owner: "<repo_owner>"
repo: "<repo_name>"
pullNumber: <pr_number>
```

Response includes `reviewThreads` with:
- `IsResolved`: filter for `false` to get unresolved comments
- `IsOutdated`: whether the code location has changed
- `Comments.Nodes[]`: array with `Body`, `Path`, `Line`, `Author`

### Get general PR comments (conversation tab)

Use the `github-mcp-server-pull_request_read` tool:
```
method: "get_comments"
owner: "<repo_owner>"
repo: "<repo_name>"
pullNumber: <pr_number>
```

## Step 3: Review and Clarify

Present unresolved comments to the user. For each comment, summarize:
- File and line number
- Reviewer's feedback
- Your proposed fix

Ask clarifying questions if:
- The feedback is ambiguous
- Multiple valid solutions exist
- The fix might affect other code

## Step 4: Fix Each Comment

For each review comment:

1. Make the code change
2. Validate the change (run build/tests as appropriate)
3. Create a focused commit:
```bash
git add <file>
git commit -m "Address review: <brief description>"
```

**Important**: One commit per review comment for easy tracking.

## Step 5: Confirm and Push

Show the user a summary of commits:
```bash
git log --oneline origin/HEAD..HEAD
```

Ask user to confirm:
- Changes look correct
- Ready to push

Push when confirmed:
```bash
git push
```

## Step 6: Reply to Review Threads

Offer to reply to each review thread with a "Fixed in" message.

Use `gh` CLI to add replies:
```bash
# Get the short SHA of the fixing commit
SHORT_SHA=$(git rev-parse --short <commit>)

# Reply to a review thread
gh api graphql -f query='
  mutation($threadId: ID!, $body: String!) {
    addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
      comment { id }
    }
  }
' -f threadId="<thread_id>" -f body="Fixed in $SHORT_SHA"
```

The thread ID is available in the `get_review_comments` response as `ID` on each review thread.

GitHub automatically links short SHAs to the commit.

## Quick Reference

| Task | Tool/Command |
|------|--------------|
| Get review comments | `github-mcp-server-pull_request_read` with `method: "get_review_comments"` |
| Get PR comments | `github-mcp-server-pull_request_read` with `method: "get_comments"` |
| Checkout PR | `gh pr checkout <number>` |
| Current PR info | `gh pr view --json number,title,url` |
| Reply to thread | `gh api graphql` mutation (see above) |
