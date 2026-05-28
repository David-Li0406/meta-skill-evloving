# Automated Cleanup Integration Guide

This guide explains how to set up automated cleanup for reflect memories and metrics to prevent unbounded growth.

## Overview

The `reflect-cleanup-memories.sh` script archives old memories and optionally cleans metrics and external feedback. It can be run:

1. **Manually**: `/reflect cleanup` or direct script invocation
2. **Scheduled**: Via cron (Linux) or launchd (macOS)
3. **On-demand**: As part of maintenance workflows

## Manual Execution

### Basic Cleanup

Archive memories older than 90 days (default):

```bash
/reflect cleanup
```

Or directly:

```bash
~/.claude/scripts/reflect-cleanup-memories.sh
```

### With Options

```bash
# Dry-run first (see what would be archived)
/reflect cleanup --dry-run

# Custom age threshold (60 days)
/reflect cleanup --age-days 60

# Also clean old metrics and feedback
/reflect cleanup --clean-metrics --clean-feedback

# Force (skip confirmation prompts)
/reflect cleanup --force

# Combination
/reflect cleanup --age-days 60 --clean-metrics --clean-feedback --force
```

## Automated Scheduling

### Option 1: Cron (Linux/macOS)

**Recommended frequency**: Monthly

#### Setup

1. Open crontab editor:
   ```bash
   crontab -e
   ```

2. Add monthly cleanup (runs on 1st of each month at 2 AM):
   ```cron
   # Reflect cleanup - archives old memories monthly
   0 2 1 * * $HOME/.claude/scripts/reflect-cleanup-memories.sh --force --clean-metrics --clean-feedback >> $HOME/.claude/cleanup.log 2>&1
   ```

3. Save and exit

#### Verify

List current cron jobs:
```bash
crontab -l
```

#### Cron Schedule Examples

```cron
# Every Sunday at 3 AM
0 3 * * 0 $HOME/.claude/scripts/reflect-cleanup-memories.sh --force

# First day of each month at 2 AM (recommended)
0 2 1 * * $HOME/.claude/scripts/reflect-cleanup-memories.sh --force --clean-metrics --clean-feedback

# Every 3 months on the 1st at 2 AM
0 2 1 */3 * $HOME/.claude/scripts/reflect-cleanup-memories.sh --force --clean-metrics --clean-feedback

# Weekly on Monday at 1 AM
0 1 * * 1 $HOME/.claude/scripts/reflect-cleanup-memories.sh --force --age-days 60
```

---

### Option 2: Launchd (macOS Preferred)

Launchd is the recommended scheduler on macOS (more reliable than cron).

#### Create Launch Agent

1. Create plist file:
   ```bash
   mkdir -p ~/Library/LaunchAgents
   cat > ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist <<'EOF'
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>dev.claude.reflect.cleanup</string>

       <key>ProgramArguments</key>
       <array>
           <string>/Users/YOUR_USERNAME/.claude/scripts/reflect-cleanup-memories.sh</string>
           <string>--force</string>
           <string>--clean-metrics</string>
           <string>--clean-feedback</string>
       </array>

       <key>StartCalendarInterval</key>
       <dict>
           <key>Day</key>
           <integer>1</integer>
           <key>Hour</key>
           <integer>2</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>

       <key>StandardOutPath</key>
       <string>/Users/YOUR_USERNAME/.claude/cleanup.log</string>

       <key>StandardErrorPath</key>
       <string>/Users/YOUR_USERNAME/.claude/cleanup.error.log</string>

       <key>RunAtLoad</key>
       <false/>
   </dict>
   </plist>
   EOF
   ```

2. **IMPORTANT**: Replace `YOUR_USERNAME` with your actual username:
   ```bash
   sed -i '' "s/YOUR_USERNAME/$(whoami)/g" ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist
   ```

3. Load the launch agent:
   ```bash
   launchctl load ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist
   ```

#### Verify Launchd

```bash
# Check if loaded
launchctl list | grep claude.reflect

# View plist
cat ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist

# Test immediately (without waiting for schedule)
launchctl start dev.claude.reflect.cleanup
```

#### Schedule Variations

**Weekly (every Sunday at 3 AM)**:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key>
    <integer>0</integer>  <!-- 0 = Sunday, 1 = Monday, ... -->
    <key>Hour</key>
    <integer>3</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

**Quarterly (every 3 months on 1st at 2 AM)**:
```xml
<!-- Note: Launchd doesn't support "every N months" directly -->
<!-- Instead, create 4 separate intervals for Jan/Apr/Jul/Oct -->
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Month</key>
        <integer>1</integer>
        <key>Day</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>2</integer>
    </dict>
    <dict>
        <key>Month</key>
        <integer>4</integer>
        <key>Day</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>2</integer>
    </dict>
    <dict>
        <key>Month</key>
        <integer>7</integer>
        <key>Day</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>2</integer>
    </dict>
    <dict>
        <key>Month</key>
        <integer>10</integer>
        <key>Day</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>2</integer>
    </dict>
</array>
```

#### Manage Launchd Agent

```bash
# Unload (disable)
launchctl unload ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist

# Load (enable)
launchctl load ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist

# Reload (after editing plist)
launchctl unload ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist
launchctl load ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist

# Remove completely
launchctl unload ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist
rm ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist
```

---

### Option 3: systemd Timer (Linux)

For systems using systemd (most modern Linux distributions).

#### Create Service and Timer

1. Create service file:
   ```bash
   mkdir -p ~/.config/systemd/user
   cat > ~/.config/systemd/user/reflect-cleanup.service <<EOF
   [Unit]
   Description=Claude Reflect Memory Cleanup
   After=network.target

   [Service]
   Type=oneshot
   ExecStart=$HOME/.claude/scripts/reflect-cleanup-memories.sh --force --clean-metrics --clean-feedback
   StandardOutput=append:$HOME/.claude/cleanup.log
   StandardError=append:$HOME/.claude/cleanup.error.log

   [Install]
   WantedBy=default.target
   EOF
   ```

2. Create timer file:
   ```bash
   cat > ~/.config/systemd/user/reflect-cleanup.timer <<EOF
   [Unit]
   Description=Run Claude Reflect Cleanup Monthly
   Requires=reflect-cleanup.service

   [Timer]
   # Run on the 1st of each month at 2 AM
   OnCalendar=monthly
   # Alternative: OnCalendar=*-*-01 02:00:00
   Persistent=true

   [Install]
   WantedBy=timers.target
   EOF
   ```

3. Enable and start the timer:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable reflect-cleanup.timer
   systemctl --user start reflect-cleanup.timer
   ```

#### Verify systemd Timer

```bash
# Check timer status
systemctl --user status reflect-cleanup.timer

# List all timers
systemctl --user list-timers

# View timer details
systemctl --user list-timers --all | grep reflect

# View logs
journalctl --user -u reflect-cleanup.service
```

#### Timer Schedule Examples

```ini
# Weekly on Sunday at 3 AM
OnCalendar=Sun *-*-* 03:00:00

# Monthly on the 1st at 2 AM
OnCalendar=*-*-01 02:00:00

# Quarterly (Jan, Apr, Jul, Oct on 1st at 2 AM)
OnCalendar=*-01,04,07,10-01 02:00:00

# Every 2 weeks
OnCalendar=weekly
OnUnitActiveSec=2w
```

---

## Monitoring Cleanup

### Check Logs

**Cron**:
```bash
tail -f ~/.claude/cleanup.log
```

**Launchd**:
```bash
tail -f ~/.claude/cleanup.log
tail -f ~/.claude/cleanup.error.log
```

**systemd**:
```bash
journalctl --user -u reflect-cleanup.service -f
```

### Verify Archives

```bash
# List archived memories
ls -lah ~/.claude/memories-archive/

# View archive for specific month
ls -lah ~/.claude/memories-archive/2026-01/
```

### Check Metrics Size

```bash
# Count lines in metrics file
wc -l ~/.claude/reflect-metrics.jsonl

# Check file size
ls -lh ~/.claude/reflect-metrics.jsonl
```

---

## Cleanup Policies

### Recommended Settings

**Monthly cleanup** (recommended for most users):
- Age: 90 days (default)
- Clean metrics: Yes (180+ days)
- Clean feedback: Yes (30+ days)

```bash
/reflect cleanup --force --clean-metrics --clean-feedback
```

**Aggressive cleanup** (for users with high activity):
- Age: 60 days
- Clean metrics: Yes (90+ days)
- Clean feedback: Yes (14+ days)
- Frequency: Weekly or bi-weekly

**Conservative cleanup** (for users wanting long history):
- Age: 180 days
- Clean metrics: No
- Clean feedback: No
- Frequency: Quarterly

### What Gets Archived

**Memories** (after N days of no modification):
- `~/.claude/memories/*.md` → `~/.claude/memories-archive/YYYY-MM/`
- Excludes: `README.md` (never archived)

**Metrics** (if `--clean-metrics`):
- Entries older than 180 days removed from `reflect-metrics.jsonl`

**External Feedback** (if `--clean-feedback`):
- Files older than 30 days removed from `reflect-external-feedback/`

### Restoration

If you need to restore an archived memory:

```bash
# Copy back from archive
cp ~/.claude/memories-archive/2026-01/old-prefs.md \
   ~/.claude/memories/skill-prefs.md

# Update timestamp
sed -i '' "s/Last updated: .*/Last updated: $(date +%Y-%m-%d)/" \
   ~/.claude/memories/skill-prefs.md
```

---

## Troubleshooting

### Cleanup Not Running

**Cron**:
- Check cron service: `sudo systemctl status cron` (Linux) or `sudo launchctl list | grep cron` (macOS)
- Verify crontab: `crontab -l`
- Check logs: `grep CRON /var/log/syslog` (Linux)

**Launchd**:
- Check if loaded: `launchctl list | grep claude.reflect`
- View errors: `cat ~/.claude/cleanup.error.log`
- Test manually: `launchctl start dev.claude.reflect.cleanup`

**systemd**:
- Check timer: `systemctl --user status reflect-cleanup.timer`
- Check service: `systemctl --user status reflect-cleanup.service`
- View logs: `journalctl --user -u reflect-cleanup.service`

### Permission Errors

Ensure script is executable:
```bash
chmod +x ~/.claude/scripts/reflect-cleanup-memories.sh
```

### No Files Archived

This is normal if:
- No files older than threshold (default 90 days)
- Script was run recently
- All memories are actively used

Run with `--verbose` to see what's being checked:
```bash
/reflect cleanup --dry-run --verbose
```

---

## Best Practices

1. **Start with dry-run**: Always test with `--dry-run` first
2. **Monitor initially**: Check logs after first few automated runs
3. **Adjust thresholds**: Tune `--age-days` based on your usage patterns
4. **Regular reviews**: Periodically review archives (keep or delete)
5. **Backup before cleanup**: Optional extra safety measure

---

*Part of Phase 5: Advanced Features*
*Last updated: 2026-01-17*
