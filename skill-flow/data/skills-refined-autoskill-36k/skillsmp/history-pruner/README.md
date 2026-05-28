# history-pruner

Prunes old Claude Code conversation history to save disk space.

## Quick Start

Check file sizes:
```bash
du -sh ~/.claude/projects/**/*.jsonl | sort -hr | head -10
```

Run pruning:
```bash
~/.claude/plugins/marketplaces/Folly/skills/history-pruner/prune-history.sh [conservative|aggressive]
```

Dry run (see what would be pruned):
```bash
~/.claude/plugins/marketplaces/Folly/skills/history-pruner/prune-history.sh --dry-run
```

## How It Works

```
┌─────────────────────────────────────────────────────┐
│  Project Files (*.jsonl)                            │
│  - Messages (keep)                                  │
│  - Summaries (keep)                                 │
│  - Tool results with full output (PRUNE)            │
│  - Thinking blocks (prune old)                      │
│  - File history snapshots (prune old)               │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌───────────────┐            ┌───────────────┐
│  Conservative │            │  Aggressive   │
│               │            │               │
│  Keep 7 days  │            │  Keep 3 days  │
│  Truncate to  │            │  Remove tool  │
│  500 chars    │            │  results      │
└───────────────┘            └───────────────┘
```

## Pruning Modes

### Conservative (default)
- Keep last 7 days of full history
- For older entries: truncate `tool_result` content to 500 chars
- Keep all summaries and message structure intact

### Aggressive
- Keep last 3 days of full history
- For older entries: remove `tool_result` content entirely
- Remove thinking blocks older than 7 days
- Remove file-history-snapshots older than 14 days

## Commands

| Command | Description |
|---------|-------------|
| `prune-history.sh` | Run conservative pruning |
| `prune-history.sh conservative` | Explicit conservative mode |
| `prune-history.sh aggressive` | Aggressive pruning |
| `prune-history.sh --dry-run` | Preview what would be pruned |

## When to Use

Invoke this skill when:
- User mentions disk space issues with Claude Code
- User asks to clean up or prune conversation history
- Project files exceed 50MB
- User wants to do maintenance on Claude Code storage
- Before syncing if files are getting too large for GitHub

## Manual Pruning

If the script isn't available:

```bash
# 1. Identify large files
du -sh ~/.claude/projects/**/*.jsonl | sort -hr | head -5

# 2. Backup before pruning
cp large-file.jsonl large-file.jsonl.bak

# 3. Prune with jq (truncate old tool results)
CUTOFF=$(date -v-7d +%s)000
jq -c 'if .timestamp and .timestamp < '$CUTOFF' and .type == "tool_result" then .content = (.content[:500] + "... [truncated]") else . end' file.jsonl > file.pruned.jsonl

# 4. Verify and replace
wc -l file.jsonl file.pruned.jsonl  # Should have same line count
mv file.pruned.jsonl file.jsonl
```

## Automation

For weekly automated cleanup:
```bash
# Add to crontab for Sunday 3am cleanup
0 3 * * 0 ~/.claude/plugins/marketplaces/Folly/skills/history-pruner/prune-history.sh conservative
```

## For Claude Code

When user mentions disk space issues or asks to clean up history:

1. Check file sizes: `du -sh ~/.claude/projects/**/*.jsonl | sort -hr | head -10`
2. If files are large (>50MB), suggest pruning
3. Ask user which mode they prefer (conservative vs aggressive)
4. Run the pruning script
5. Report results (space saved, files processed)

Always backup before aggressive pruning. Pruning removes ability to see full old tool outputs, but summaries are preserved so conversation context remains.
