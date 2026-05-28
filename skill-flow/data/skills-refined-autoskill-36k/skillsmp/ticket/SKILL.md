---
name: ticket
description: "[start <ticket>] [cleanup <ticket>] - Manages git worktrees for Jira tickets. Creates worktrees with auto branch naming, or cleans up completed worktrees."
allowed-tools:
  - mcp__atlassian__getJiraIssue
  - mcp__atlassian__getTransitionsForJiraIssue
  - mcp__atlassian__transitionJiraIssue
  - Bash
  - Read
---

# Ticket

Manages git worktrees for Jira ticket development.

## Subcommands

| Command | Description |
|---------|-------------|
| `/ticket start <ticket>` | Create worktree for a Jira ticket |
| `/ticket cleanup [ticket]` | Remove worktree (or list all if no ticket specified) |

## Configuration

- **Main repo**: `~/Vuori/cascade`
- **Worktrees**: `~/Vuori/cascade-worktrees`
- **Jira cloud**: `vuoriclothing.atlassian.net`

## Start Workflow

See [start.md](start.md) for detailed instructions.

**Quick overview:**
1. Parse ticket ID from URL or direct input
2. Fetch ticket details via Atlassian MCP
3. Generate branch name: `feat/TDE-XXXX-short-description`
4. Check for existing branch/worktree
5. Create worktree from origin/main
6. Copy .env and run npm install
7. Move ticket to "In Development" status if not already
8. Provide summary with next steps

## Cleanup Workflow

See [cleanup.md](cleanup.md) for detailed instructions.

**Quick overview:**
1. List worktrees if no ticket specified
2. Find matching worktree
3. Check for uncommitted changes (warn if found)
4. Check if branch is merged
5. Remove worktree
6. Optionally delete local branch
7. Provide summary with remaining worktrees

## Branch Naming Rules

Convert ticket summary to kebab-case:
- Lowercase, 3-5 words max
- Remove filler words (the, a, an, for, to)
- Examples:
  - "Optimize Lytics Tag Loading" → `feat/TDE-1234-optimize-lytics-loading`
  - "Fix Cart Mobile Layout Bug" → `feat/TDE-1234-fix-cart-mobile-layout`
