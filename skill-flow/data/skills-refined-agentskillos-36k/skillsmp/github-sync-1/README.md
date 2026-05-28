# github-sync

Daily git health check at session start. Finds uncommitted changes, unpushed commits, and commits to pull across all repositories.

## Quick Start

Runs automatically once per day at session start.

To force a check:
```bash
~/.claude/plugins/marketplaces/Folly/skills/github-sync/git-sync-check.sh --force
```

## How It Works

```
┌─────────────────────────────────────────────────────┐
│  Session Start                                      │
│  (runs automatically once per 24 hours)             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Scan for Git Repositories                          │
│  find ~ -maxdepth 4 -name ".git" -type d            │
│  (excludes: node_modules, .cache, Library, etc.)   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  For Each Repository:                               │
│  - git fetch origin                                 │
│  - Check for uncommitted changes                    │
│  - Check for unpushed commits                       │
│  - Check if behind remote                           │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌───────────────┐            ┌───────────────┐
│  Issues Found │            │  All Clean    │
│               │            │               │
│  Report to    │            │  Proceed      │
│  user         │            │  silently     │
└───────────────┘            └───────────────┘
```

## Action Matrix

| Status | Action |
|--------|--------|
| Behind remote | `git pull origin main` and tell user |
| Uncommitted changes | Ask user: commit or review? |
| Unpushed commits | Ask user: push now? |
| Everything clean | Proceed silently |

## Commands

| Script | Description |
|--------|-------------|
| `git-sync-check.sh` | Main check script (auto-limits to 24h) |
| `git-sync-check.sh --force` | Bypass 24h limit |
| `git-sync-all.sh` | Sync all repos (git pull/push) |
| `sync-mcp-oauth.sh push` | Push MCP OAuth tokens to iCloud |
| `sync-mcp-oauth.sh pull` | Pull MCP OAuth tokens from iCloud |

## What Gets Scanned

The script finds git repos up to 4 levels deep, excluding:
- `~/.claude/` (managed separately)
- `Library/`, `.Trash/`, `node_modules/`
- `.npm/`, `.cache/`, `.local/`
- `.cargo/`, `.rustup/`, `vendor/`
- `.gem/`, `go/pkg/`, `.cocoapods/`, `Pods/`

## MCP OAuth Sync

The skill also handles automatic syncing of MCP OAuth tokens across Macs:

| When | Action |
|------|--------|
| Session start | Pull latest tokens from iCloud |
| Session end | Push updated tokens to iCloud |

Tokens are encrypted with AES-256-CBC using your deep-env password.

### Manual OAuth Commands

```bash
# Push credentials to iCloud
~/claudesync/skills/github-sync/sync-mcp-oauth.sh push

# Pull credentials from iCloud
~/claudesync/skills/github-sync/sync-mcp-oauth.sh pull

# Check sync status
~/claudesync/skills/github-sync/sync-mcp-oauth.sh status
```

## For Claude Code

At session start, run the git sync check (auto-skips if already run today):
```bash
~/.claude/plugins/marketplaces/Folly/skills/github-sync/git-sync-check.sh
```

Based on results:
- **Behind remote**: Pull and tell user
- **Uncommitted changes**: Ask if user wants to commit or review
- **Unpushed commits**: Ask if user wants to push
- **Clean or already checked**: Proceed silently
