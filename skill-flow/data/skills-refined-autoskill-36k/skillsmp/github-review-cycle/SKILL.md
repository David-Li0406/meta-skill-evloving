---
name: github-review-cycle
description: manage pull request code reviews, approvals, comments, and feedback cycles
metadata:
  category: github
---

# GitHub Review Cycle

## What is it?

This skill manages the **collaboration & review phase** of software development. It handles commenting, approving, requesting changes, and leveraging AI reviews.

## Success Criteria

- Review comments are specific and actionable.
- Batching is used (`add_comment_to_pending_review`) for multiple comments in a single PR.
- Final review event (`APPROVE`, `REQUEST_CHANGES`, `COMMENT`) matches the overall feedback.
- AI reviews are triggered only when appropriate and add value.

## Why use it?

- **Structured code review**: Manage the complete review lifecycle from commenting to approval
- **Batched feedback**: Group multiple comments into a single review submission
- **Clear communication**: Distinguish between general discussion and code-specific feedback
- **AI assistance**: Leverage Copilot for automated code review insights
- **Review etiquette**: Avoid spam by consolidating feedback appropriately

## When to use this skill

- "Review this PR."
- "Add a comment on line 50."
- "Request a review from @octocat."
- "Ask Copilot to review this PR."

## What this skill can do

- **Comment**: Add general issue comments or specific file-level review comments.
- **Review**: Submit formal reviews (APPROVE, REQUEST_CHANGES, COMMENT).
- **Pending Reviews**: Manage batched review comments (`add_comment_to_pending_review`).
- **AI Review**: Trigger Copilot code reviews.

## What this skill will NOT do

- Merge PRs (use `github-pr-flow`).
- Change code.

## How to use this skill

1. **General Feedback**: Use `add_issue_comment`.
2. **Code-Specific Feedback**: Use `add_comment_to_pending_review` (start/add to batch) -> `pull_request_review_write` (submit batch).
3. **Automated Feedback**: Use `request_copilot_review`.

## Tool usage rules

- **Distinguish Comments**:
  - `add_issue_comment`: General PR discussion (timeline).
  - `pull_request_review_write`: Code review (diff context).
- **Bot Etiquette**: Do not spam. Group comments into a single review where possible.

## Examples

See [references/examples.md](references/examples.md) for compliant review examples.

## Limitations

- Cannot view "pending" comments from other users.
- Review requests depend on user permissions.
