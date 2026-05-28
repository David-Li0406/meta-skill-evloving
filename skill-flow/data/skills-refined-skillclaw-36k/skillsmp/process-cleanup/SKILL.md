---
name: process-cleanup
description: Comprehensive process cleanup workflow for detecting and removing orphaned Claude Code sessions
category: Maintenance
difficulty: intermediate
tags:
  - process-management
  - cleanup
  - multi-instance
  - maintenance
---

# Process Cleanup Skill

This skill provides a comprehensive workflow for managing orphaned Claude Code processes that remain after crashes or force-kills.

## What This Skill Does

1. **Scans** for orphaned Claude Code sessions using multi-factor detection
2. **Analyzes** session metadata to determine orphan status with 5-layer safety checks
3. **Reports** findings with detailed session information
4. **Cleans up** orphaned processes and files with user confirmation

## When to Use This Skill

Use this skill when:
- Multiple Claude Code instances have been running and some crashed
- You suspect orphaned processes consuming resources
- You want to audit all running Claude Code sessions
- You need to clean up after abnormal session termination

## Safety Features

This skill implements **5 layers of safety checks**:

1. **Active Process Check**: Verifies PID exists or is zombie
2. **Heartbeat Staleness**: Checks last heartbeat > 5 minutes ago
3. **Current Session Whitelist**: Never cleans current session
4. **Hostname Verification**: Only cleans local sessions
5. **Grace Period**: Sessions < 10 minutes old are protected

## Workflow

### Step 1: Scan for Orphaned Sessions

First, scan to identify any orphaned sessions:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-scan.sh
```

This is a **safe, read-only** operation that identifies orphaned sessions without making changes.

### Step 2: Review Detailed Report

Generate a comprehensive report of all tracked sessions:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-report.sh
```

This shows:
- Current session status
- All active sessions
- All orphaned sessions with reasons
- Session metadata (PID, start time, working directory, heartbeat)

### Step 3: Preview Cleanup (Dry-Run)

Preview what would be cleaned up without making changes:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-processes.sh --dry-run
```

This shows exactly which processes would be terminated and which files would be removed.

### Step 4: Execute Cleanup

After reviewing, execute the cleanup:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-processes.sh --execute
```

This will:
1. Display summary of orphaned sessions
2. Request confirmation
3. Terminate orphaned processes gracefully (SIGTERM → SIGKILL)
4. Clean up session files and locks
5. Display completion summary

## Automated Cleanup

For automated workflows (cron, CI/CD), use auto mode:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-processes.sh --auto --quiet
```

This executes cleanup without prompts or verbose output.

## Configuration

Customize behavior in `~/.claude/process-janitor-config.json`:

```json
{
  "auto_cleanup_on_start": false,
  "min_session_age_minutes": 10,
  "heartbeat_interval_seconds": 60,
  "stale_heartbeat_threshold_minutes": 5,
  "cleanup_mode": "interactive",
  "notification_enabled": true,
  "dry_run_default": true
}
```

### Configuration Options

- **auto_cleanup_on_start**: Run cleanup automatically when sessions start
- **min_session_age_minutes**: Grace period before session can be cleaned (default: 10)
- **heartbeat_interval_seconds**: How often heartbeat updates (default: 60)
- **stale_heartbeat_threshold_minutes**: When to consider heartbeat stale (default: 5)
- **cleanup_mode**: "interactive" or "auto"
- **notification_enabled**: Show desktop notifications
- **dry_run_default**: Default to dry-run mode for safety

## Example Usage

### Interactive Cleanup

```bash
# 1. Scan for orphans
/cleanup scan

# 2. Review detailed report
/cleanup report

# 3. Execute cleanup (with confirmation)
/cleanup run
```

### Automated Cleanup

```bash
# Enable auto-cleanup on session start
# Edit ~/.claude/process-janitor-config.json:
{
  "auto_cleanup_on_start": true
}

# Or run manually without prompts
/cleanup auto
```

## Troubleshooting

### No Orphaned Sessions Detected

This is normal! It means all tracked sessions are active or properly terminated.

### Session Not Cleaning Up

Check if session passes all safety checks:
- Is it older than 10 minutes? (grace period)
- Is it on the same machine? (hostname check)
- Is it actually orphaned? (process + heartbeat checks)

### Heartbeat Not Updating

The heartbeat process should run in the background. If it's not updating:
1. Check if heartbeat PID is running: `ps aux | grep heartbeat`
2. Restart the session to re-initialize tracking
3. Check logs for errors

## Advanced Usage

### Manual Session Investigation

```bash
# List all tracked sessions
ls ~/.claude/sessions/

# View session metadata
cat ~/.claude/sessions/<session-id>/metadata.json

# Check heartbeat status
cat ~/.claude/sessions/<session-id>/heartbeat.pid
```

### Force Cleanup (Use with Caution)

If you need to bypass safety checks (NOT RECOMMENDED):

```bash
# Manually remove session directory
rm -rf ~/.claude/sessions/<session-id>

# Or manually kill process
kill -9 <PID>
```

## Integration with Hooks

This plugin integrates with Claude Code lifecycle hooks:

- **SessionStart**: Auto-registers session and optionally runs cleanup
- **SessionEnd**: Cleans up child processes and updates status
- **Stop**: Final cleanup before exit

## Best Practices

1. **Run scans regularly**: Use `/cleanup scan` to monitor session health
2. **Enable auto-cleanup cautiously**: Only enable if you frequently have crashes
3. **Check reports before cleanup**: Always review `/cleanup report` first
4. **Use dry-run mode**: Preview changes before executing
5. **Monitor grace period**: Don't set too low (<5 minutes)

## Technical Details

### Orphan Detection Algorithm

```
For each session:
  1. Skip if current session → ACTIVE
  2. Skip if not on same hostname → SKIP
  3. Skip if < grace period → ACTIVE
  4. Check process running:
     - Not running → ORPHANED
     - Running but heartbeat stale → ORPHANED
     - Running with fresh heartbeat → ACTIVE
```

### Process Termination

1. Send SIGTERM (graceful)
2. Wait 5 seconds
3. If still running, send SIGKILL (force)
4. Verify process terminated

### File Cleanup

Removes:
- `~/.claude/sessions/<session-id>/` (session directory)
- `~/.claude/sessions/<session-id>.lock.dir/` (lock directory)
- Registry entries marked as cleaned

## Security Considerations

- **Path validation**: All paths validated to prevent traversal
- **PID validation**: PIDs checked before termination
- **Command injection**: Uses arrays, not string concatenation
- **File permissions**: Session files set to 600 (owner-only)
- **Hostname checks**: Only cleans local sessions

## Support

For issues or questions:
- Check logs for error messages
- Review configuration file
- Verify session metadata files exist
- Ensure required commands available (bash, ps, kill)
