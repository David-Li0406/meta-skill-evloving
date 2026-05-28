---
name: history-pruner
description: Prunes old Claude Code conversation history to save disk space. Use when project files get large (>50MB) or periodically for maintenance.
---

# history-pruner - Conversation History Cleanup

Automatically prunes old Claude Code conversation history files to prevent them from growing too large.

## When to Use This Skill

Invoke this skill when:
- User mentions disk space issues with Claude Code
- User asks to clean up or prune conversation history
- Project files in `~/claudesync/projects/` exceed 50MB
- User wants to do maintenance on Claude Code storage
- Before syncing if files are getting too large for GitHub

## How It Works

Project files (`~/claudesync/projects/**/*.jsonl`) store full conversation history including:
- Messages (keep)
- Summaries (keep)
- Tool results with full output (PRUNE - this is the bulk of the data)
- Thinking blocks (prune old ones)
- File history snapshots (prune old ones)

## Pruning Strategy

### Conservative (default)
- Keep last 7 days of full history
- For older entries: truncate `tool_result` content to 500 chars
- Keep all summaries and message structure intact

### Aggressive
- Keep last 3 days of full history
- For older entries: remove `tool_result` content entirely (keep metadata)
- Remove thinking blocks older than 7 days
- Remove file-history-snapshots older than 14 days

## Commands

### Check current sizes
```bash
du -sh ~/claudesync/projects/-Users-andrewwilkinson/*.jsonl | sort -hr | head -10
```

### Run pruning script
```bash
~/claudesync/skills/history-pruner/prune-history.sh [conservative|aggressive]
```

### Dry run (see what would be pruned)
```bash
~/claudesync/skills/history-pruner/prune-history.sh --dry-run
```

## Manual Pruning Steps

If the script isn't available, prune manually:

1. **Identify large files:**
   ```bash
   du -sh ~/claudesync/projects/**/*.jsonl | sort -hr | head -5
   ```

2. **Backup before pruning:**
   ```bash
   cp large-file.jsonl large-file.jsonl.bak
   ```

3. **Prune with jq (truncate old tool results):**
   ```bash
   # Keep entries from last 7 days, truncate older tool_results
   CUTOFF=$(date -v-7d +%s)000
   jq -c 'if .timestamp and .timestamp < '$CUTOFF' and .type == "tool_result" then .content = (.content[:500] + "... [truncated]") else . end' file.jsonl > file.pruned.jsonl
   ```

4. **Verify and replace:**
   ```bash
   wc -l file.jsonl file.pruned.jsonl  # Should have same line count
   mv file.pruned.jsonl file.jsonl
   ```

## Automation

To run weekly, add to the sync launchd job or create a separate one:
```bash
# Add to crontab for weekly Sunday 3am cleanup
0 3 * * 0 ~/claudesync/skills/history-pruner/prune-history.sh conservative
```

## Important Notes

- Always backup before aggressive pruning
- Pruning removes ability to see full old tool outputs
- Summaries are preserved so conversation context remains
- This won't break Claude Code - it handles missing/truncated data gracefully
