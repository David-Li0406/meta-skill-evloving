---
description: Manage PR review polling daemon for automatic notifications
---

# PR Poll - Automatic PR Review Notifications

จัดการ polling daemon ที่ตรวจสอบ PR reviews และส่ง notification อัตโนมัติ

## Usage

```
/pr-poll              # Show status
/pr-poll start        # Start daemon (notification only)
/pr-poll auto         # Start daemon with auto-respond (Claude handles reviews)
/pr-poll stop         # Stop daemon
/pr-poll check        # Check once (no daemon)
```

## Instructions

### Step 1: Parse Command

**ถ้าไม่มี argument หรือ `status`:**
→ แสดงสถานะ daemon

**ถ้า `start`:**
→ Start daemon (notification only)

**ถ้า `auto`:**
→ Start daemon with auto-respond (Claude handles reviews automatically)

**ถ้า `stop`:**
→ Stop daemon

**ถ้า `check`:**
→ Run once and exit

### Step 2: Execute Action

#### Status (default)

```bash
./scripts/pr-review-poll-status.sh
```

**Output:**
- Daemon status (running/stopped)
- Tracked PRs
- Last log entries

#### Start Daemon (Notification Only)

```bash
./scripts/pr-review-poll-start.sh --interval 300
```

**Options:**
- `--interval N` - Polling interval in seconds (default: 300 = 5 minutes)
- `--repo OWNER/REPO` - Specific repo to monitor

**Output:**
```
✓ Daemon started (PID: 12345)

Log file: ~/.pr-review-poll.log
To view logs: tail -f ~/.pr-review-poll.log
To stop: ./pr-review-poll-stop.sh
```

#### Start Daemon with Auto-Respond

```bash
# Get current working directory
WORKING_DIR=$(pwd)

# Start with auto-respond enabled
./scripts/pr-review-poll-start.sh --interval 300 --auto-respond --working-dir "$WORKING_DIR"
```

**Options:**
- `--auto-respond` - Enable automatic Claude CLI spawning
- `--working-dir DIR` - Working directory for Claude (required with --auto-respond)

**Output:**
```
✓ Daemon started (PID: 12345)
🤖 Auto-respond: ENABLED
📂 Working dir: /path/to/repo

Log file: ~/.pr-review-poll.log
To view logs: tail -f ~/.pr-review-poll.log
To stop: ./pr-review-poll-stop.sh
```

**How Auto-Respond Works:**
1. Daemon detects new PR review
2. Spawns Claude CLI with `/pr-review` prompt
3. Claude analyzes and responds to review feedback
4. Log file created: `~/.pr-review-claude-{pr}-{timestamp}.log`

**Important Notes:**
- Requires `claude` CLI to be installed and in PATH
- Uses `--dangerously-skip-permissions` for non-interactive execution
- Each Claude session runs in background with separate log file

#### Stop Daemon

```bash
./scripts/pr-review-poll-stop.sh
```

**Output:**
```
✓ Daemon stopped
```

#### Check Once

```bash
./scripts/pr-review-poll.sh --once
```

**Output:**
- Lists checked PRs
- Sends notifications for new reviews

### Step 3: Display Summary

```markdown
## PR Poll Status

| Metric | Value |
|--------|-------|
| Status | Running / Stopped |
| PID | [pid] |
| Interval | [seconds]s |
| Tracked PRs | [count] |

### Recent Activity
[last 5 log lines]

### Commands
- Start: `/pr-poll start`
- Stop: `/pr-poll stop`
- Check now: `/pr-poll check`
```

## How It Works

1. **Polling**: Daemon checks GitHub every N seconds for user's open PRs
2. **Detection**: Compares current reviews with stored state
3. **Notification**: Sends macOS notification for new reviews
4. **Action**: Notification suggests running `/pr-review`

## Notification Types

| Review State | Sound | Message |
|--------------|-------|---------|
| APPROVED | Glass | "Approved by @reviewer" |
| CHANGES_REQUESTED | Basso | "Changes requested by @reviewer" |
| COMMENTED | Ping | "@reviewer left a comment" |

## Files

| File | Purpose |
|------|---------|
| `~/.pr-review-poll.pid` | Daemon PID file |
| `~/.pr-review-poll.log` | Daemon log file |
| `~/.pr-review-state.json` | PR review state |

## Examples

```bash
# Start daemon with 5-minute interval (default, notification only)
/pr-poll start

# Start with auto-respond - Claude handles reviews automatically
/pr-poll auto

# Start with 1-minute interval for active development
./scripts/pr-review-poll-start.sh --interval 60

# Auto-respond with 1-minute interval
./scripts/pr-review-poll-start.sh --interval 60 --auto-respond --working-dir "$(pwd)"

# Monitor specific repo with auto-respond
./scripts/pr-review-poll-start.sh --repo owner/repo --auto-respond --working-dir /path/to/repo

# Quick check without starting daemon
/pr-poll check
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Daemon not starting | Check `gh auth status` |
| No notifications | Check macOS notification settings |
| Too many notifications | Increase poll interval |
| Stale state | Delete `~/.pr-review-state.json` |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/pr-review` | Handle PR review feedback |
| `/pr` | Create PR |
| `/focus` | Set current task |
