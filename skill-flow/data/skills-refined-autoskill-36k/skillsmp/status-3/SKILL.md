---
name: status
description: Show project progress overview - recent commits, active workflows, open PRs, and issues by milestone. Use when user asks about progress, status, what's next, or recent work.
allowed-tools: Bash
---

# Status Skill

## Purpose

Provides a unified view of project progress by combining:

- Recent git commits
- Active checkpoint workflows
- Open pull requests with review status
- Open issues grouped by milestone

## When to Use

- User asks "what's the status?"
- User asks "show progress"
- User asks "what have we done recently?"
- User asks "what's next?"
- User asks "what PRs are open?"
- User asks "what are we working on?"

## Command

```bash
bun run checkpoint status
```

### Options

| Flag            | Description                                   |
| --------------- | --------------------------------------------- |
| `--commits <n>` | Number of recent commits to show (default: 5) |
| `--issues <n>`  | Number of open issues to show (default: 10)   |
| `--json`        | Output as JSON for machine processing         |

### Examples

```bash
# Default view
bun run checkpoint status

# More detail
bun run checkpoint status --commits 10 --issues 20

# Machine-readable
bun run checkpoint status --json
```

## Output

The command displays:

1. **Recent Commits** - Latest commits with SHA and message
2. **Active Workflows** - Issue workflows tracked by checkpoint system
3. **Open PRs** - Pull requests with review status (PENDING, APPROVED, CHANGES_REQUESTED)
4. **Open Issues** - Grouped by milestone, sorted alphabetically

## Instructions

1. Run `bun run checkpoint status` using the Bash tool
2. **Format the output as markdown** and display it to the user
3. Add a brief summary at the end highlighting:
   - What was recently done
   - What's currently in progress
   - Suggested next steps

**Important:** The Bash output is not visible to the user. You MUST format and print the results in your response.

## Integration

This skill uses `bun run checkpoint status` which queries:

- Git log for commits
- Checkpoint SQLite DB for workflows
- GitHub CLI for issues and PRs

See [agent-architecture.md](../../docs/agent-architecture.md) for how this fits into the workflow system.
