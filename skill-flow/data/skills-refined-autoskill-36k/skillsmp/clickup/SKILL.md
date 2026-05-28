---
name: clickup
description: ClickUp project management CLI. Full CRUD for tasks and time entries. Search, filter, view time reports. Use `/clickup` for task management and time tracking.
---

# ClickUp CLI Skill

Manage ClickUp tasks and time entries from the command line. Full CRUD for tasks, subtasks, and time tracking.

## When to Use

Use `/clickup` when:
- Managing tasks (search, create, update, delete)
- Tracking time (add entries, view reports, fix dates)
- Viewing weekly time reports
- Finding task or member IDs

## Quick Start

```bash
cd /Users/will/Projects/tcg-rbs/.claude/skills/click-up-skill

# Setup (first time only)
cp .env.example .env
# Add: CLICKUP_API_TOKEN, CLICKUP_WORKSPACE_ID, CLICKUP_USER_ID

# Run commands
npm run dev -- <command>
```

## Essential Commands

### Tasks
```bash
# Search tasks
npm run dev -- tasks search "billing" --assignee me --table

# Get task details
npm run dev -- tasks get TCG-4752 --full

# Update task
npm run dev -- tasks update TCG-4752 --status "complete"
```

### Time Tracking
```bash
# Today's time
npm run dev -- time list

# Weekly report
npm run dev -- time report

# Add time entry
npm run dev -- time add TCG-4752 --duration "2h 30m" --date "2026-01-20"

# Move entry to different date
npm run dev -- time move <entry_id> --to "2026-01-21"

# Update entry
npm run dev -- time update <entry_id> --duration "3h"

# Delete entry
npm run dev -- time delete <entry_id> --force
```

### Utilities
```bash
# Find your user ID
npm run dev -- members find "will@blackairplane"

# List workspaces
npm run dev -- workspaces list

# Show config
npm run dev -- config show
```

## Output Formats

All commands support:
- Default: Human-readable
- `--table`: Tabular format
- `--json`: JSON output

## Configuration

Required in `.env`:
```
CLICKUP_API_TOKEN=pk_your_token_here
CLICKUP_WORKSPACE_ID=your_workspace_id
CLICKUP_USER_ID=your_user_id
CLICKUP_TEAM_ID=your_team_id
```

Get your API token: ClickUp Settings → Apps → API Token

## Reference Documentation

- [Full Command Reference](./docs/REFERENCE.md) - All commands and options
- [Time Tracking Guide](./docs/TIME-TRACKING.md) - Workflows and reports
- [Troubleshooting](./docs/TROUBLESHOOTING.md) - Common issues

## Development

```bash
npm install     # Install deps
npm run build   # Compile TypeScript
npm run dev     # Run without building
npm test        # Run tests
```
