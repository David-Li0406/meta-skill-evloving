---
name: wt-config
description: View or update worktree-maestro configuration. Use when asked to show, view, or change worktree settings.
argument-hint: "[show | set <key> <value>]"
allowed-tools: mcp__worktree-maestro__get_config, mcp__worktree-maestro__set_config
---

Use the `get_config` or `set_config` MCP tools to manage configuration.

Parse `$ARGUMENTS`:
- Empty or "show" → use `get_config` and display all settings
- "set <key> <value>" → use `set_config` with the key-value pair

## Available Config Keys

| Key | Description | Default |
|-----|-------------|---------|
| `baseDirectory` | Where worktrees are created | ~/worktrees |
| `portRangeStart` | Start of port range | 3001 |
| `portRangeEnd` | End of port range | 3099 |
| `defaultBaseBranch` | Default base branch | main |
| `branchPrefix` | Branch name prefix | feature/ |

## Examples

- `/wt-config` → show all config
- `/wt-config show` → show all config
- `/wt-config set baseDirectory ~/projects/worktrees` → update base directory
- `/wt-config set branchPrefix feat/` → update branch prefix

## Report

For show: Display all settings in a readable table format.
For set: Confirm the change was applied.
