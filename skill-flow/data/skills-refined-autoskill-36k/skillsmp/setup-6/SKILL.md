---
name: setup
description: Guide for setting up Innie from scratch - global config, memory repo, MCP servers, and scheduler
---

# Innie Setup Guide

Use this skill when helping someone set up Innie for the first time, or when troubleshooting configuration issues.

## Prerequisites

- [OpenCode CLI](https://opencode.ai) installed
- Node.js 18+ and pnpm
- macOS (for calendar skill and scheduler daemon)
- icalBuddy for calendar access (install if needed: `brew install ical-buddy`)

## Setup Steps

### 1. Clone the Innie Repository

```bash
git clone https://github.com/ascorbic/innie.git
cd innie
pnpm install
pnpm build
```

This builds all packages:

- `@innie-ai/memory` – Memory MCP server
- `@innie-ai/scheduler` – Background reminder daemon
- `@innie-ai/hooks` – OpenCode plugin for auto-commit and compaction hooks

### 2. Create the Memory Repository

Innie stores state in a separate private repository. This keeps personal data out of the main codebase.

```bash
# Create a new directory (can be anywhere)
mkdir ~/innie-memory
cd ~/innie-memory
git init

# Create the directory structure
mkdir -p state/projects state/people state/meetings
mkdir -p logs/summaries
mkdir -p index

# Create initial state files
cat > state/today.md << 'EOF'
# Today

## Priorities

- [ ] Get oriented in the codebase
- [ ] Understand current work context

## Notes

First day. Learning the environment.
EOF

cat > state/inbox.md << 'EOF'
# Inbox

Quick capture. Process regularly.

## Pending

*Empty – nothing captured yet*
EOF

cat > state/commitments.md << 'EOF'
# Commitments

Active work items. Archive when complete.

## Active

*No active commitments yet*
EOF

cat > state/ambient-tasks.md << 'EOF'
# Ambient Tasks

Tasks for quiet time when not actively assisting.

## Queue

*Empty*
EOF

# Initial commit
git add .
git commit -m "Initial state setup"
```

### 3. Configure Global OpenCode Settings

Create the global config directory and files:

```bash
mkdir -p ~/.config/opencode/skill
```

**~/.config/opencode/opencode.json** – Global MCP servers:

```json
{
  "mcp": {
    "memory": {
      "type": "local",
      "command": ["npx", "/path/to/innie/packages/memory"],
      "environment": {
        "MEMORY_DIR": "/path/to/innie-memory"
      }
    }
  }
}
```

Replace `/path/to/innie` and `/path/to/innie-memory` with actual paths.

**~/.config/opencode/AGENTS.md** – Global identity instructions:

```markdown
# Identity

You are Innie, a stateful coding agent. Your memory is managed via the `memory` MCP server.

Use your memory tools to:

- Journal important observations with `log_journal`
- Search past context with `search_memory`
- Save session summaries with `save_conversation_summary`

Defer to project-level AGENTS.md for coding conventions.
```

### 4. Configure Permissions for External Directory Access

Innie needs to access the memory repo from any working directory. By default, OpenCode prompts when accessing paths outside the current project (`external_directory` permission). To allow seamless access to state files, add permission rules to your config.

**~/.config/opencode/opencode.json** – Add permissions alongside MCP config:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "/path/to/innie-memory/state/today.md",
    "/path/to/innie-memory/state/inbox.md",
    "/path/to/innie-memory/state/commitments.md"
  ],
  "mcp": {
    "memory": {
      "type": "local",
      "command": ["npx", "/path/to/innie/packages/memory"],
      "environment": {
        "MEMORY_DIR": "/path/to/innie-memory"
      }
    }
  },
  "permission": {
    "external_directory": {
      "/path/to/innie-memory/**": "allow"
    }
  }
}
```

The key permission is `external_directory` – without this, scheduled tasks and sessions running from other repos will prompt for approval when accessing state files.

### 5. Configure Project-Level Settings

In the innie repository, the `opencode.json` should mirror the global config but also include the hooks plugin:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "/path/to/innie-memory/state/today.md",
    "/path/to/innie-memory/state/inbox.md",
    "/path/to/innie-memory/state/commitments.md"
  ],
  "mcp": {
    "memory": {
      "type": "local",
      "command": ["npx", "/path/to/innie/packages/memory"],
      "environment": {
        "MEMORY_DIR": "/path/to/innie-memory"
      }
    }
  },
  "permission": {
    "external_directory": {
      "/path/to/innie-memory/**": "allow"
    }
  },
  "plugin": ["./plugins/hooks/dist/index.mjs"]
}
```

The `instructions` array injects state files into the system prompt so Innie sees current priorities. The `plugin` entry enables auto-commit hooks for state changes.

### 6. Install the Scheduler Daemon (Optional)

The scheduler enables background reminders and scheduled tasks. It watches `schedule.json` in `MEMORY_DIR` and spawns opencode when events fire.

```bash
cd packages/scheduler

# Copy the launchd plist
cp gg.mk.innie.scheduler.plist ~/Library/LaunchAgents/
```

Edit the plist to set correct paths. The template contains hardcoded paths that must be updated:

```xml
<!-- Update these in ~/Library/LaunchAgents/gg.mk.innie.scheduler.plist -->
<key>ProgramArguments</key>
<array>
    <string>/path/to/node</string>  <!-- e.g., ~/.nvm/versions/node/v22.x.x/bin/node -->
    <string>/path/to/innie/packages/scheduler/dist/index.mjs</string>
</array>

<key>EnvironmentVariables</key>
<dict>
    <key>MEMORY_DIR</key>
    <string>/path/to/innie-memory</string>
</dict>

<key>StandardOutPath</key>
<string>/path/to/innie-memory/logs/scheduler.log</string>

<key>StandardErrorPath</key>
<string>/path/to/innie-memory/logs/scheduler.error.log</string>

<key>WorkingDirectory</key>
<string>/path/to/innie</string>
```

Load the daemon:

```bash
launchctl load ~/Library/LaunchAgents/gg.mk.innie.scheduler.plist
```

To check status:

```bash
launchctl list | grep innie
# Check logs
tail -f /path/to/innie-memory/logs/scheduler.log
```

To unload:

```bash
launchctl unload ~/Library/LaunchAgents/gg.mk.innie.scheduler.plist
```

To reload after plist changes:

```bash
launchctl unload ~/Library/LaunchAgents/gg.mk.innie.scheduler.plist
launchctl load ~/Library/LaunchAgents/gg.mk.innie.scheduler.plist
```

### 7. Verify the Setup

Run these checks to confirm everything works:

```bash
# Start opencode in the innie directory
cd /path/to/innie
opencode
```

Inside the session, test:

1. **Memory tools**: Run `log_journal` with a test entry
2. **Search**: Run `search_memory` to verify indexing
3. **Calendar**: Run `icalBuddy eventsToday` to test calendar access
4. **State files**: Confirm today.md, inbox.md, commitments.md appear in system prompt
5. **Scheduler**: Use `schedule_once` to set a reminder a few minutes out, then check if it fires and can access state files

## Environment Variables

| Variable     | Purpose                        | Default                   |
| ------------ | ------------------------------ | ------------------------- |
| `MEMORY_DIR` | Root directory for memory repo | Current working directory |

## File Structure Reference

```
innie/                          # Main repo (public)
├── AGENTS.md                   # Project identity and conventions
├── opencode.json               # Project MCP config
├── packages/
│   ├── memory/                 # Memory MCP server
│   └── scheduler/              # Background daemon
├── plugins/
│   └── hooks/                  # OpenCode hooks
└── .opencode/
    └── skill/                  # Skills directory

innie-memory/                   # Memory repo (private)
├── state/
│   ├── today.md                # Daily focus (~30 lines)
│   ├── inbox.md                # Quick capture (~20 lines)
│   ├── commitments.md          # Active work (~40 lines)
│   ├── ambient-tasks.md        # Quiet-time tasks (~30 lines)
│   ├── projects/*.md           # Project context
│   ├── people/*.md             # People context
│   └── meetings/*/             # Meeting artifacts
├── logs/
│   ├── journal.jsonl           # Timestamped observations
│   └── summaries/              # Conversation summaries
└── index/                      # Semantic search index (auto-generated)
```

## Troubleshooting

**Memory tools not available**: Check that the memory MCP server path is correct in opencode.json and the package is built.

**Calendar not working**: Ensure icalBuddy is installed (`brew install ical-buddy`) and grant calendar access when prompted.

**State files not in prompt**: Verify the `instructions` array in opencode.json points to the correct absolute paths.

**Scheduler not running**: Check logs with `log show --predicate 'subsystem == "gg.mk.innie.scheduler"' --last 1h`

**Scheduled tasks can't access state files**: Add the `external_directory` permission rule to your config. Without this, OpenCode prompts for approval when accessing paths outside the current working directory.

**Search returning no results**: Run `rebuild_memory_index` to regenerate the semantic index.

## Output

After walking through setup, confirm:

- All packages built successfully
- Memory repo created with initial state files
- Global and project config files in place
- Permissions configured for external directory access
- Memory MCP server responding
- Calendar skill working (icalBuddy)
- State files visible in system prompt
- Scheduled tasks can access state files without prompts
