---
name: gh-pr-review
description: GitHub PR review operations (inline comments, pending reviews, thread resolution)
---

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

### Check for existing pending review

Before starting a new review, check if one already exists:

```sh
gh pr-review review view --reviewer "$(gh api user --jq .login)" --states PENDING -R owner/repo 42
```

If a pending review exists, reuse its `PRR_...` ID.

### Start a pending review

Only if no pending review exists. Returns a `PRR_...` ID for subsequent operations.

```sh
gh pr-review review --start -R owner/repo 42
```

Output: `{"id": "PRR_kwDOAAABbcdEFG12", "state": "PENDING"}`

Pin to specific commit with `--commit <sha>`.

### Add comment (single line)

Requires `--review-id` with the `PRR_...` identifier (not numeric).

```sh
gh pr-review review --add-comment \
  --review-id PRR_kwDOAAABbcdEFG12 \
  --path internal/service.go \
  --line 42 \
  --body "nit: prefer helper" \
  -R owner/repo 42
```

### Add comment (multi-line)

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

- `--side RIGHT|LEFT`: RIGHT for additions/context, LEFT for deletions - `--start-side RIGHT|LEFT`:
side for start of multi-line range

### Reply to existing thread (within pending review)

Use `thread_id` from `review view`. Always include `--review-id` to attach reply to pending review.

```sh
gh pr-review comments reply \
  --thread-id PRRT_kwDOAAABbFg12345 \
  --review-id PRR_kwDOAAABbcdEFG12 \
  --body "Acknowledged" \
  -R owner/repo 42
```

## Reading Reviews and Threads

### Get review snapshot

```sh
gh pr-review review view -R owner/repo 42
```

Filters:

- `--reviewer <login>`: single reviewer
- `--states PENDING,APPROVED,CHANGES_REQUESTED,COMMENTED,DISMISSED`: comma-separated
- `--unresolved`: only unresolved threads
- `--not_outdated`: exclude outdated threads
- `--tail <n>`: limit replies per thread
- `--include-comment-node-id`: include GraphQL comment IDs

### List threads

```sh
gh pr-review threads list -R owner/repo 42
gh pr-review threads list --unresolved --mine -R owner/repo 42
```

### Resolve/unresolve thread

```sh
gh pr-review threads resolve --thread-id PRRT_kwDOAAABbFg12345 -R owner/repo 42
gh pr-review threads unresolve --thread-id PRRT_kwDOAAABbFg12345 -R owner/repo 42
```

## ID Formats

- `PRR_...`: Review ID (from `review --start` or `review view`, used in `--review-id`)
- `PRRT_...`: Thread ID (from `review view` or `threads list`, used in `--thread-id`)

## Output Notes

- All commands emit JSON only
- Optional fields omitted (not null)
- Empty arrays return `[]`
- Errors exit non-zero with `{"status": "...", "errors": [...]}`
