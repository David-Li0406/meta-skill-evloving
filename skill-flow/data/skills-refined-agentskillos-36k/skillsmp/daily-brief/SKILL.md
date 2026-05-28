---
name: daily-brief
description: Review logs from ~/logs and remote log APIs to provide orientation and context for the day. Use when starting a work session, checking what happened recently, or needing context on recent activity. Reads daily summaries, meeting notes, test runs, and worker logs.
allowed-tools: Bash, Read, Glob, Grep, Task, WebFetch
---

# Daily Brief Skill

Reads and synthesizes logs from local `~/logs` and remote log APIs to orient you for work.

## Usage

```bash
/daily-brief                  # Yesterday + today (default)
/daily-brief today            # Just today
/daily-brief week             # Last 7 days
/daily-brief 2026-01-15       # Specific date
/daily-brief 2026-01-10 2026-01-15  # Date range
/daily-brief --deep           # More informed analysis
/daily-brief week --deep      # Weekly retrospective
/daily-brief --remote         # Include remote worker logs
/daily-brief --remote-only    # Only remote logs (skip local)
```

## Modes

### Quick Mode (default)
Fast direct reads for daily orientation from local logs.

### Deep Mode (`--deep`)
Same compact output, but more informed:
- Verify PR/issue status with `gh` before reporting
- Cross-reference test failures against recent commits
- Richer context from meeting notes and patterns
- Include remote worker logs

Deep mode means **better accuracy**, not more verbosity.

### Remote Mode (`--remote` or `--remote-only`)
Fetches logs from remote worker-logs APIs. Use `--remote` to combine with local logs, or `--remote-only` for just remote.

## Log Sources

### Local Logs (`~/logs`)

```
~/logs/
├── daily/                    # Daily summaries (YYYY-MM-DD-daily-summary.md)
│   └── raw/                  # Raw git data from daily skill
├── meetings/                 # Meeting notes and agendas
├── archive/                  # Archived logs
├── aibtc-x402-test-runs/     # Symlinked test logs
└── stx402-test-runs/         # Symlinked test logs
```

### Remote Log APIs

Three worker-logs instances with centralized logging from Cloudflare Workers:

| Service | URL | Env File |
|---------|-----|----------|
| wbd.host | `https://logs.wbd.host` | `~/dev/whoabuddy/worker-logs/.env` |
| aibtc.com (prod) | `https://logs.aibtc.com` | `~/dev/aibtcdev/worker-logs/.env` |
| aibtc.dev (staging) | `https://logs.aibtc.dev` | `~/dev/aibtcdev/worker-logs/.env` |

## Workflow

1. **Parse arguments** - Date range, `--deep`, `--remote`, `--remote-only` flags
2. **Read local daily summaries** - Primary source (already synthesized)
3. **Fetch remote logs** - If `--remote` or `--remote-only` or `--deep`
4. **Check open threads** - From logs, then verify with `gh` if `--deep`
5. **Scan test logs** - Only flag failures not fixed by subsequent commits
6. **Present brief** - Compact output focused on action

### Remote Log Fetching

To fetch from remote APIs, source the admin key and use curl:

```bash
# Source admin key for wbd.host
source ~/dev/whoabuddy/worker-logs/.env

# List all registered apps
curl -s -H "X-Admin-Key: $ADMIN_API_KEY" https://logs.wbd.host/apps

# Get logs for a specific app (last 24 hours)
curl -s -H "X-Admin-Key: $ADMIN_API_KEY" \
  "https://logs.wbd.host/logs?app_id=my-app&since=$(date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%SZ)"

# Get stats for an app (last 7 days)
curl -s -H "X-Admin-Key: $ADMIN_API_KEY" \
  "https://logs.wbd.host/stats/my-app?days=7"
```

For aibtc logs (same API, different env):

```bash
# Source admin key for aibtc (works for both prod and staging)
source ~/dev/aibtcdev/worker-logs/.env

# Production logs
curl -s -H "X-Admin-Key: $ADMIN_API_KEY" https://logs.aibtc.com/apps

# Staging logs
curl -s -H "X-Admin-Key: $ADMIN_API_KEY" https://logs.aibtc.dev/apps
```

### API Endpoints Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/apps` | GET | Admin | List all registered apps |
| `/apps/:app_id` | GET | Admin | Get app details |
| `/logs` | GET | Admin + app_id param | Query logs with filters |
| `/stats/:app_id` | GET | Admin | Daily stats (debug/info/warn/error counts) |

Query parameters for `/logs`:
- `app_id` - Required when using admin key
- `since` - ISO timestamp (e.g., `2026-01-20T00:00:00Z`)
- `until` - ISO timestamp
- `level` - Filter by level (DEBUG, INFO, WARN, ERROR)
- `limit` - Max entries (default 100)

### Deep Mode Additions

When `--deep` is specified:
- Run `gh pr list` and `gh issue list` to verify actual status
- Cross-reference test failures against commits after the test date
- Include meeting context if relevant to current work
- **Automatically fetch remote logs** from all three endpoints

## Output Format

Keep it compact. One format for both modes (deep just means more accurate).

```markdown
# Daily Brief - [date range]

## What Got Done
**[Date]** - [commit count] commits
- [Accomplishment 1]
- [Accomplishment 2]

**[Date]** - [commit count] commits
- [Accomplishment 1]

## Open Threads
| Item | Status | Context |
|------|--------|---------|
| [org/repo#N](url) | Awaiting review | Brief description |

## Worker Activity
| Service | Apps | Logs (24h) | Errors |
|---------|------|------------|--------|
| wbd.host | 3 | 1,234 | 2 |
| aibtc.com | 5 | 8,901 | 0 |
| aibtc.dev | 5 | 456 | 12 |

**Notable Events:**
- [app-name] 12 errors: "Connection timeout to X"
- [app-name] Spike in activity at 14:00 UTC

## Focus Areas
- [Priority 1 based on momentum and open work]
- [Priority 2]

## Notes
[Only if relevant meeting context or important observations]
```

When remote logs have errors or notable patterns, surface them. Skip the Worker Activity section if all services are healthy with no errors.

## Verifying Open Threads (Deep Mode)

Use `gh` to check actual PR/issue status:

```bash
# Check PR status
gh pr view org/repo#N --json state,mergedAt

# List open PRs for user
gh pr list --author @me --state open

# Check issue status
gh issue view org/repo#N --json state
```

Only report items that are actually still open. PRs listed in logs may have been merged since.

## Test Log Handling

Parse test logs for pass/fail, but before flagging failures:
1. Note the test date
2. Check if commits after that date mention fixing the issue
3. Only flag if failure appears unresolved

Example: A test failure from Jan 14 shouldn't be flagged as a blocker if Jan 15+ commits show "fix: registry delete endpoint".

## Date Matching

Match files with dates in their names:
- `2026-01-19-daily-summary.md` - Daily summary
- `2026-01-19T*.md` - Timestamped raw logs
- `2026-01-19-*.md` - Any dated file

Use glob patterns like `*2026-01-19*` to find all files for a given date.

## Deep Mode Agent Prompt

When using Task tool for deep analysis:

```
Analyze logs from ~/logs and remote APIs for [DATE RANGE]. The user makes consistent daily progress.

Provide a COMPACT brief with:
1. **What Got Done** - Key accomplishments by date
2. **Open Threads** - Only items still actually open (verify with gh if uncertain)
3. **Worker Activity** - Summary of remote logs (only if errors or notable patterns)
4. **Focus Areas** - 2-3 suggested priorities based on momentum

Do NOT:
- Flag old test failures without checking for fixes in later commits
- Report PRs/issues as open without verification
- Duplicate information across sections
- Be verbose - keep it scannable
- Include Worker Activity section if all services are healthy

For remote logs, focus on:
- Error counts and patterns (especially repeated errors)
- Unusual activity spikes
- Health check failures
- Any WARN/ERROR logs from the date range

Logs:
[CONTENT]
```

## Tips

- Daily summaries are pre-synthesized - use them as primary source
- Assume progress is being made - frame positively
- Old test failures may already be fixed - check before flagging
- Keep output scannable - busy people need quick orientation
- `--deep` = more accurate, not more words

### Remote Logs Tips

- Use `--remote` sparingly - API calls add latency
- Focus on errors and warnings, not debug/info noise
- The env files contain `ADMIN_API_KEY` - source them before curl calls
- All three services use the same API (worker-logs codebase)
- wbd.host is personal projects, aibtc.com/dev are AIBTC team projects
- Staging (aibtc.dev) may have more test noise - weight production errors higher
