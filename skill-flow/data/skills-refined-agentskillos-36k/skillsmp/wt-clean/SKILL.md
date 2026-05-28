---
name: wt-clean
description: Remove a worktree and clean up resources. Use when asked to clean, remove, or delete a worktree.
argument-hint: "<name> [force]"
allowed-tools: mcp__worktree-maestro__cleanup_worktree
---

Use the `cleanup_worktree` MCP tool to remove a worktree.

Parse `$ARGUMENTS` to extract:
- `name` (required) - Worktree name, ticket ID, or partial match
- `force` (optional) - Set to true if "force", "true", "yes", "1", or "-f" is present

## Examples

- `/wt-clean PROJ-123` → clean up worktree matching PROJ-123
- `/wt-clean auth` → clean up worktree matching "auth"
- `/wt-clean PROJ-123 force` → force clean even with uncommitted changes

## Actions

The tool will:
- Close associated iTerm tab
- Release port assignment
- Remove worktree directory
- Delete the branch

## Report

Report all actions taken and any warnings (e.g., uncommitted changes discarded).
