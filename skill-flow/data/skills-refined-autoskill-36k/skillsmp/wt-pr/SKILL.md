---
name: wt-pr
description: Create a GitHub PR from a worktree. Use when asked to create a PR, pull request, or submit changes from a worktree.
argument-hint: "<name> [draft]"
allowed-tools: mcp__worktree-maestro__create_pr
---

Use the `create_pr` MCP tool to create a GitHub pull request.

Parse `$ARGUMENTS` to extract:
- `name` (required) - Worktree name, ticket ID, or partial match
- `draft` (optional) - Set to true if "draft", "true", "yes", "1", or "-d" is present

## Examples

- `/wt-pr PROJ-123` → create PR for worktree matching PROJ-123
- `/wt-pr auth draft` → create draft PR for worktree matching "auth"

## Actions

The tool will:
1. Commit any uncommitted changes
2. Push the branch to origin
3. Create the PR via GitHub CLI

## Report

Report the PR URL when complete.

**Note:** Requires GitHub CLI (gh) to be installed and authenticated.
