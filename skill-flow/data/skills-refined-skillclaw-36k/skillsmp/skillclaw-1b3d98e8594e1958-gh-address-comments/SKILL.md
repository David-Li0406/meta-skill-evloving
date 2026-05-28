---
name: gh-address-comments
description: Use this skill to address review comments on the open GitHub PR for the current branch using the gh CLI, ensuring you are authenticated first.
---

# PR Comment Handler

This guide helps you find the open PR for the current branch and address its comments using the `gh` CLI. Ensure all `gh` commands are run with elevated network access.

## Prerequisites
1. Ensure `gh` is authenticated (e.g., run `gh auth login` once).
2. Verify authentication status with `gh auth status`, including workflow/repo scopes for successful command execution. If sandboxing blocks this, rerun with `sandbox_permissions=require_escalated`.

## Steps

### 1) Inspect comments needing attention
- Run `scripts/fetch_comments.py` to print all comments and review threads on the PR.

### 2) Ask the user for clarification
- Number all review threads and comments, providing a short summary of what is required to apply fixes.
- Ask the user which numbered comments should be addressed.

### 3) If user chooses comments
- Apply fixes for the selected comments.

## Notes
- If `gh` encounters authentication or rate issues during execution, prompt the user to re-authenticate with `gh auth login`, then retry.