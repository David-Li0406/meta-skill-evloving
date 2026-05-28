---
name: tmux-monitor
description: Use this skill when you need to monitor and report the status of all tmux sessions, including development environments, spawned agents, and running processes.
---

# Skill body

## Purpose

Provide comprehensive visibility into all active tmux sessions, running processes, and spawned agents. This skill enables checking what's running where without needing to manually inspect each session.

## Capabilities

1. **Session Discovery**: Find and categorize all tmux sessions.
2. **Process Inspection**: Identify running servers, development environments, and agents.
3. **Port Mapping**: Show which ports are in use and by what.
4. **Status Reporting**: Generate detailed reports with recommendations.
5. **tmuxwatch Integration**: Use tmuxwatch for enhanced real-time monitoring.
6. **Metadata Extraction**: Read session metadata from `.tmux-dev-session.json` and agent JSON files.

## When to Use

- When a user asks "what's running?"
- Before starting new development environments (to check for port conflicts).
- After spawning agents (to verify they started correctly).
- When debugging server/process issues.
- Before session cleanup.
- When context switching between projects.

## Implementation

### Step 1: Check tmux Availability

```bash
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux is not installed"
    exit 1
fi

if ! tmux list-sessions 2>/dev/null; then
    echo "✅ No tmux sessions currently running"
    exit 0
fi
```

### Step 2: Discover All Sessions

```bash
# Get all sessions with metadata
SESSIONS=$(tmux list-sessions -F '#{session_name}|#{session_windows}|#{session_created}|#{session_attached}')

# Count sessions
TOTAL_SESSIONS=$(echo "$SESSIONS" | wc -l | tr -d ' ')
```

### Step 3: Categorize Sessions

Group by prefix pattern:

- `dev-*` → Development environments
- `agent-*` → Spawned agents
- `claude-*` → Claude Code sessions
- `monitor-*` → Monitoring sessions
- Others → Miscellaneous

```bash
DEV_SESSIONS=$(echo "$SESSIONS" | grep "^dev-" || true)
AGENT_SESSIONS=$(echo "$SESSIONS" | grep "^agent-" || true)
CLAUDE_SESSIONS=$(echo "$SESSIONS" | grep "^claude-" || true)
```

### Step 4: Extract Details for Each Session

For each session, gather:

**Window Information**:
```bash
tmux list-windows -t "$SESSION" -F '#{window_index}:#{window_name}:#{window_panes}'
```

**Running Processes** (from the first pane of each window):
```bash
tmux capture-pane -t "$SESSION:0.0" -p -S -10 -E 0
```

**Port Detection** (check for listening ports):
```bash
# Add your port detection logic here
```