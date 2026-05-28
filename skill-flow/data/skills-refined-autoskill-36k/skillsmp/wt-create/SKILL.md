---
name: wt-create
description: Create a new git worktree with iTerm integration. Use when asked to create, add, or start a new worktree.
argument-hint: "[ticket] <name> [mode] [repo]"
allowed-tools: mcp__worktree-maestro__create_worktree
---

Use the `create_worktree` MCP tool to create a new worktree.

Parse `$ARGUMENTS` to extract:
- `ticket` (optional) - Ticket ID like PROJ-123, detected by pattern matching
- `name` (required) - Short descriptive name like "user-auth" or "fix-login"
- `mode` (optional) - iTerm mode: `tab`, `split-h`/`h`, or `split-v`/`v`
- `repo` (optional) - Path to source repository

Mode mapping:
- `tab` or empty → `itermMode: "tab"`
- `split-h` or `h` → `itermMode: "split-horizontal"`
- `split-v` or `v` → `itermMode: "split-vertical"`

## Examples

- `/wt-create PROJ-123 user-auth` → creates with ticket
- `/wt-create auth-fix` → creates without ticket
- `/wt-create PROJ-123 user-auth split-v` → creates with vertical split
- `/wt-create PROJ-123 auth-fix tab ~/projects/myapp` → creates from specific repo

## Report

After calling the MCP tool, report:
- Worktree path
- Branch name
- Source repository
- Whether dependencies were installed
- iTerm status
