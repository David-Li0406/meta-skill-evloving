---
name: wt
description: List all git worktrees with status. Use when asked to show, list, or view worktrees.
argument-hint: "[repo-path]"
allowed-tools: mcp__worktree-maestro__list_worktrees
---

Use the `list_worktrees` MCP tool with `verbose: true` and `allRepos: true` to show all worktrees.

If `$ARGUMENTS` contains a path, pass it as `repo` to filter worktrees from that specific repository.

Display the results in a clear table format showing:
- Repository (if multiple repos)
- Name
- Branch
- Status (clean/dirty)
- Changed files count
- Port (if assigned)
- iTerm tab status
