---
name: gh-address-comments
description: Use this skill to address review comments on the open GitHub PR for the current branch using the gh CLI, ensuring authentication is verified first.
---

# PR Comment Handler

This guide helps you find the open PR for the current branch and address its comments using the gh CLI. All `gh` commands should be run with elevated network access.

## Prerequisites
Ensure `gh` is authenticated (e.g., run `gh auth login` once), then check authentication status with `gh auth status` using escalated permissions (including workflow/repo scopes). If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## Steps

### 1) Inspect comments needing attention
- Run `scripts/fetch_comments.py` to print out all comments and review threads on the PR.

### 2) Ask the user for clarification
- Number all review threads and comments, providing a short summary of what is required to apply fixes.
- Ask the user which numbered comments should be addressed.

### 3) If user chooses comments
- Apply fixes for the selected comments.

## Notes
- If `gh` encounters authentication or rate issues during execution, prompt the user to re-authenticate with `gh auth login`, then retry.