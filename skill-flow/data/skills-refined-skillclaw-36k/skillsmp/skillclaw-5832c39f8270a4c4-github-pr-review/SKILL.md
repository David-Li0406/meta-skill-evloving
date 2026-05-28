---
name: github-pr-review
description: Use this skill when you need to manage GitHub pull request reviews, including adding comments and implementing suggested changes based on review feedback.
---

# Skill body

## Critical Rules

- NEVER submit reviews. The user will manually submit pending reviews.
- All comments must be added to a pending review, never posted directly.

## Extension Setup

If any `gh pr-review` command fails with "unknown command" or similar, install the extension:

```sh
gh extension install agynio/gh-pr-review
```

Then retry the failed command.

## Pending Review Workflow

### Check for Existing Pending Review

Before starting a new review, check if one already exists:

```sh
gh pr-review review view --reviewer "$(gh api user --jq .login)" --states PENDING -R owner/repo 42
```

If a pending review exists, reuse its `PRR_...` ID.

### Start a Pending Review

Only if no pending review exists. Returns a `PRR_...` ID for subsequent operations.

```sh
gh pr-review review --start -R owner/repo 42
```

Output: `{"id": "PRR_kwDOAAABbcdEFG12", "state": "PENDING"}`

Pin to specific commit with `--commit <sha>`.

### Add Comment (Single Line)

Requires `--review-id` with the `PRR_...` identifier (not numeric).

```sh
gh pr-review review --add-comment \
  --review-id PRR_kwDOAAABbcdEFG12 \
  --path internal/service.go \
  --line 42 \
  --body "nit: prefer helper" \
  -R owner/repo 42
```

### Add Comment (Multi-Line)

Spans lines 10-15:

```sh
gh pr-review review --add-comment \
  --review-id PRR_kwDOAAABbcdEFG12 \
  --path internal/service.go \
  --start-line 10 \
  --line 15 \
  --body "This entire block should be extracted into a helper function" \
  -R owner/repo 42
```

Optional flags:

- `--side RIGHT|LEFT`: RIGHT for additions/context, LEFT for deletions.
- `--start-side RIGHT|LEFT`: side for start of multi-line range.

### Reply to Existing Thread (Within Pending Review)

Use `thread_id` from `review view`. Always include `--review-id` to attach reply to pending review.

```sh
gh pr-review comments reply \
  --thread-id PRRT_kwDOAAABbFg12345 \
  --review-id PRR_kwDOAAABbcdEFG12 \
  --body "Acknowledged" \
  -R owner/repo 42
```

## Reading Reviews and Threads

### Get Review Snapshot

```sh
gh pr-review review view -R owner/repo 42
```

Filters:

- `--reviewer <login>`: single reviewer
- `--states PENDING,APPROVED,CHANGES_REQUESTED,COMMENTED,DISMISSED`: comma-separated
- `--unresolved`: only unresolved threads
- `--not_outdated`: exclude outdated threads
- `--tail <n>`: limit replies per thread

## Implementation of Review Comments

### Input Format

Users provide URLs in the following format:

```
https://github.com/{org}/{repo}/pull/{pr}/files#r{comment_id}
```

### Processing Flow

1. **Fetch Comments (Parallel Execution)**: Extract information from each URL and fetch comments using `gh api repos/{org}/{repo}/pulls/comments/{comment_id}`.
2. **Impact Analysis**: Identify the affected files with minimal file reads.
3. **Implementation Plan**: Present a plan for implementation based on the comments received.
4. **Implementation**: After user approval, manage tasks and make changes to the code.
5. **Completion Report**: Display changes made and affected files.

## Error Handling

- Handle `gh api` 404 errors gracefully and continue processing other URLs.
- Confirm unclear comments with the user.
- Report missing files and continue.

## Output Style

- Use concise language.
- Reference files in `file:line` format.
- Avoid unnecessary expressions; clearly report processing status.