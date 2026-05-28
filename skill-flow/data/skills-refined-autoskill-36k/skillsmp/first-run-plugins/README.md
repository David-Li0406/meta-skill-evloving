# first-run-plugins

Shows plugin recommendations on first run after claudesync setup.

## Quick Start

This skill triggers automatically when `CLAUDESYNC_FIRST_RUN=true` is detected in the session start hook output. It only runs once.

## How It Works

```
┌─────────────────────────────────────────────────────┐
│  Session Start Hook                                 │
│  Detects ~/.claude/.claudesync-first-run exists     │
│  Outputs: CLAUDESYNC_FIRST_RUN=true                 │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Show Welcome + Plugin Recommendation               │
│                                                     │
│  "Welcome to claudesync!                            │
│   I recommend the compound-engineering plugin..."   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  AskUserQuestion                                    │
│  [Install it] [Skip for now]                        │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌───────────────┐            ┌───────────────┐
│  Install      │            │  Skip         │
│               │            │               │
│  Run CLI      │            │  Continue     │
│  commands     │            │  session      │
└───────────────┘            └───────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Delete flag file                                   │
│  rm ~/.claude/.claudesync-first-run                 │
│  touch ~/.claude/.claudesync-first-run.done         │
└─────────────────────────────────────────────────────┘
```

## Trigger Condition

The skill triggers when:
1. Hook output contains `CLAUDESYNC_FIRST_RUN=true`
2. Flag file exists: `~/.claude/.claudesync-first-run`

## Plugin Recommendation

Currently recommends:
- **compound-engineering** - Advanced workflows, code review skills, planning tools

Install commands:
```bash
claude plugin marketplace add https://github.com/EveryInc/every-marketplace
claude plugin install compound-engineering
```

## Files

| File | Purpose |
|------|---------|
| `~/.claude/.claudesync-first-run` | Flag file that triggers the skill |
| `~/.claude/.claudesync-first-run.done` | Marker that recommendation was shown |

## For Claude Code

When you detect `CLAUDESYNC_FIRST_RUN=true` in session start:

1. **Show welcome message** with plugin recommendation
2. **Use AskUserQuestion** to let user choose: "Install it" or "Skip for now"
3. **If install**: Run the CLI commands to add marketplace and install plugin
4. **Delete flag file**: `rm ~/.claude/.claudesync-first-run`
5. **Create done marker**: `touch ~/.claude/.claudesync-first-run.done`

**Important**: Always ask before installing. Never install plugins without user consent.
