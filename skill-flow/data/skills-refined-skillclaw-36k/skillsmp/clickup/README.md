# ClickUp CLI Skill

A command-line tool for managing ClickUp tasks and time entries, built as a Claude Code skill for the TCG team.

## Why This Exists

The ClickUp MCP integration provides read-only access to tasks and time entries, but lacks the ability to:
- Update or delete time entries (fixing wrong dates, removing duplicates)
- Full CRUD operations on tasks
- Generate weekly time reports

This CLI fills those gaps, giving developers complete control over their ClickUp workflow without leaving the terminal.

---

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Set up your environment
cp .env.example .env

# 3. Edit .env with your credentials:
#    - CLICKUP_API_TOKEN: Get from ClickUp Settings → Apps → API Token
#    - CLICKUP_WORKSPACE_ID: From your ClickUp URL (app.clickup.com/WORKSPACE_ID/home)
#    - CLICKUP_USER_ID: Your user ID (embedded in your API token after pk_)
#    - CLICKUP_TEAM_ID: Usually same as workspace ID

# 4. Verify setup
npm run dev -- config show

# 5. Try it out
npm run dev -- tasks search "my task"
npm run dev -- time list
```

---

## Common Commands

### Tasks
```bash
# Search tasks
npm run dev -- tasks search "billing" --assignee me --table

# Get task details with comments and subtasks
npm run dev -- tasks get TCG-4752 --full

# Update task status
npm run dev -- tasks update TCG-4752 --status "complete"

# Create a task
npm run dev -- tasks create "New feature" --list "Sprint 13" --priority high
```

### Time Tracking
```bash
# Today's time entries
npm run dev -- time list

# Weekly report
npm run dev -- time report

# Add time entry
npm run dev -- time add TCG-4752 --duration "2h 30m" --date "2026-01-20"

# Move entry to different date (fixes wrong date)
npm run dev -- time move <entry_id> --to "2026-01-21"

# Delete duplicate entry
npm run dev -- time delete <entry_id> --force
```

---

## Finding Your Credentials

### API Token
1. Go to ClickUp Settings → Apps → API Token
2. Generate or copy your personal token
3. Token format: `pk_USER_ID_RANDOM_STRING`

### Workspace ID
Look at your ClickUp URL: `app.clickup.com/WORKSPACE_ID/home`

### User ID
Your user ID is embedded in your API token. For `pk_4373512_ABC123`, the user ID is `4373512`.

Or find it with:
```bash
npm run dev -- members find "your@email.com"
```

---

## Documentation

- [SKILL.md](./SKILL.md) - Claude Code skill reference
- [docs/REFERENCE.md](./docs/REFERENCE.md) - Complete command reference
- [docs/TIME-TRACKING.md](./docs/TIME-TRACKING.md) - Time tracking workflows
- [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) - Common issues and solutions

---

## Development

```bash
npm install      # Install dependencies
npm run dev      # Run without building (uses tsx)
npm run build    # Compile TypeScript
npm test         # Run tests (vitest)
```

### Project Structure
```
src/
├── index.ts           # CLI entry point
├── api/client.ts      # ClickUp API client
├── commands/          # CLI command implementations
│   ├── tasks.ts       # Task CRUD
│   ├── time.ts        # Time entry CRUD
│   └── utils.ts       # Workspaces, spaces, members
├── types/             # TypeScript interfaces
└── utils/             # Formatting, date helpers
```
