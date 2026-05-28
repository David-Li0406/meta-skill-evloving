---
name: daily
description: Generate daily summary of git activity across all repositories
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, TodoWrite
---

# Daily Summary Skill

Generates and publishes a team-friendly daily summary of work across all git repositories.

## Usage

```bash
/daily           # Uses today's date
/daily 2026-01-05  # Specific date
```

## Configuration

Set these in your environment or `~/.claude/CLAUDE.md`:
- `DAILY_LOGS_REPO` - GitHub repo for publishing summaries (e.g., `myorg/dev-logs`)
- Default dev directory: `~/dev/` (all `org/repo` subdirectories are scanned)

## Data Sources

### 1. Git Commits (Primary)
Raw git log data from all repos under `~/dev/`. Collected via `daily-git-summary.sh`.

### 2. Claude RPG Data (Activity Metrics)
Session-level activity tracked by the claude-rpg system in `~/.claude-rpg/data/`:

| File | Contents |
|------|----------|
| `companions.json` | Cumulative stats per repo: level, XP, tool usage, git ops, commands |
| `events.jsonl` | Timestamped events: tool calls, prompts, git operations |

**Companion Stats Include:**
- Level & XP (100 × 1.5^(n-1) XP per level)
- Tool usage counts (Read, Edit, Bash, Task, etc.)
- Git operations (commits, pushes, PRs created/merged)
- Commands (tests, builds, deploys, lints)
- Blockchain ops (clarinet checks/tests, testnet/mainnet deploys)
- Activity streaks

**Extract today's events:**
```bash
# Filter events.jsonl by date
grep "\"timestamp\":17" ~/.claude-rpg/data/events.jsonl | \
  jq -s '[.[] | select(.timestamp / 1000 | strftime("%Y-%m-%d") == "2026-01-21")]'
```

**Read companion stats:**
```bash
jq '.companions[] | {name, level, totalExperience, "commits": .stats.git.commits}' \
  ~/.claude-rpg/data/companions.json
```

## Workflow

Follow the runbook: `runbook/daily-summary.md` in your knowledge base.

1. **Collect** - Run `daily-git-summary.sh` to gather raw git data
2. **Read RPG** - Pull companion stats from `~/.claude-rpg/data/companions.json`
3. **Verify PR status** - Before listing PRs in Open Threads, check their actual state:
   ```bash
   gh pr view {number} --repo {org/repo} --json state -q '.state'
   ```
   Only list as "Awaiting review" if state is OPEN. Use "Merged" for MERGED PRs.
4. **Interpret** - Create/update team summary using TEMPLATE.md (includes Jekyll front matter)
5. **Sync** - Copy to your configured logs repo `_posts/` directory
6. **Push** - Commit and push to trigger GitHub Pages build

## Files

| File | Purpose |
|------|---------|
| `daily-git-summary.sh` | Bash helper for raw data collection |
| `extract-deployments.ts` | Bun script to extract deployment URLs from wrangler.jsonc |
| `extract-rpg-stats.ts` | Bun script to extract daily RPG activity from claude-rpg data |
| `TEMPLATE.md` | Summary format template |

## Deployment URLs

For repos with Cloudflare Workers (wrangler.jsonc), extract deployment links:

```bash
bun ~/.claude/skills/daily/extract-deployments.ts --from-repos org/repo1,org/repo2
```

This outputs a markdown table with staging/production URLs extracted from wrangler.jsonc routes.

## RPG Stats

Extract Claude session activity from the claude-rpg system:

```bash
# Today's activity
bun ~/.claude/skills/daily/extract-rpg-stats.ts

# Specific date
bun ~/.claude/skills/daily/extract-rpg-stats.ts 2026-01-21

# Companion overview (cumulative stats)
bun ~/.claude/skills/daily/extract-rpg-stats.ts --companions
```

Outputs markdown tables showing:
- XP earned per companion (repo)
- Tool usage breakdown
- Session highlights (prompts, top tools)
