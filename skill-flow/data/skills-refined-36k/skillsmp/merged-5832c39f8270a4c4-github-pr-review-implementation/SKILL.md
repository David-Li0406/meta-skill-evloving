---
name: github-pr-review-implementation
description: Use this skill for managing GitHub PR reviews, including comment analysis and implementation of suggested changes.
---

## GitHub PR Review and Implementation Workflow

This skill encompasses the operations for reviewing GitHub pull requests (PRs) and implementing comments from the review process.

### Critical Rules

- NEVER submit reviews. The user will manually submit pending reviews.
- All comments must be added to a pending review, never posted directly.

### Extension Setup

If any `gh pr-review` command fails with "unknown command" or similar, install the extension:

```sh
gh extension install agynio/gh-pr-review
```

Then retry the failed command.

### Pending Review Workflow

#### Check for Existing Pending Review

Before starting a new review, check if one already exists:

```sh
gh pr-review review view --reviewer "$(gh api user --jq .login)" --states PENDING -R <owner>/<repo> <pr_number>
```

If a pending review exists, reuse its `PRR_...` ID.

#### Start a Pending Review

Only if no pending review exists. Returns a `PRR_...` ID for subsequent operations.

```sh
gh pr-review review --start -R <owner>/<repo> <pr_number>
```

Output: `{"id": "PRR_...", "state": "PENDING"}`

Pin to specific commit with `--commit <sha>`.

### Adding Comments to Reviews

#### Add Comment (Single Line)

Requires `--review-id` with the `PRR_...` identifier (not numeric).

```sh
gh pr-review review --add-comment \
  --review-id PRR_... \
  --path <file_path> \
  --line <line_number> \
  --body "<comment_body>" \
  -R <owner>/<repo> <pr_number>
```

#### Add Comment (Multi-Line)

Spans lines `<start_line>-<end_line>`:

```sh
gh pr-review review --add-comment \
  --review-id PRR_... \
  --path <file_path> \
  --start-line <start_line> \
  --line <end_line> \
  --body "<comment_body>" \
  -R <owner>/<repo> <pr_number>
```

Optional flags:
- `--side RIGHT|LEFT`: RIGHT for additions/context, LEFT for deletions.

#### Reply to Existing Thread

Use `thread_id` from `review view`. Always include `--review-id` to attach reply to pending review.

```sh
gh pr-review comments reply \
  --thread-id PRRT_... \
  --review-id PRR_... \
  --body "<reply_body>" \
  -R <owner>/<repo> <pr_number>
```

### Reading Reviews and Threads

#### Get Review Snapshot

```sh
gh pr-review review view -R <owner>/<repo> <pr_number>
```

Filters:
- `--reviewer <login>`: single reviewer
- `--states PENDING,APPROVED,CHANGES_REQUESTED,COMMENTED,DISMISSED`: comma-separated
- `--unresolved`: only unresolved threads

#### List Threads

```sh
gh pr-review threads list -R <owner>/<repo> <pr_number>
gh pr-review threads list --unresolved --mine -R <owner>/<repo> <pr_number>
```

#### Resolve/Unresolve Thread

```sh
gh pr-review threads resolve --thread-id PRRT_... -R <owner>/<repo> <pr_number>
gh pr-review threads unresolve --thread-id PRRT_... -R <owner>/<repo> <pr_number>
```

### Implementation of Review Comments

#### Input Format

Users provide URLs in the following format:

```
https://github.com/{org}/{repo}/pull/{pr}/files#r{comment_id}
```

#### Processing Flow

1. **Fetch Comments (Parallel Execution)**: Extract information from each URL and fetch comments using `gh api repos/{org}/{repo}/pulls/comments/{comment_id}`.
2. **Impact Analysis**: Identify the affected areas with minimal file reads.
3. **Implementation Plan**: Present a plan for implementation based on the comments.
4. **Implementation**: After user approval, create a task list and make changes.
5. **Completion Report**: Display changes made and affected files.

### Error Handling

- Handle `gh api` 404 errors by reporting and continuing with other URLs.
- Confirm unclear comments with the user.
- Report missing files and continue processing.

### Output Style

- Use concise language.
- Reference files in `file:line` format.
- Avoid unnecessary expressions; clearly report processing status.

## ID Formats

- `PRR_...`: Review ID (from `review --start` or `review view`, used in `--review-id`).
- `PRRT_...`: Thread ID (from `review view` or `threads list`, used in `--thread-id`).

## Output Notes

- All commands emit JSON only.
- Optional fields omitted (not null).
- Empty arrays return `[]`.
- Errors exit non-zero with `{"status": "...", "errors": [...]}`.