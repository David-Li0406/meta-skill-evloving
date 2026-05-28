---
name: audit
description: Run all HAIOS audit checks to find drift, gaps, and stale items. Use
  before starting a new session or after completing a milestone.
generated: 2025-12-24
last_updated: '2025-12-28T13:28:00'
---

# Audit Skill

Run all HAIOS audit checks to find drift, gaps, and stale items.

## When to Use

- Before starting a new session (health check)
- After completing a milestone
- When things feel "off" or out of sync

## What It Checks

1. **Sync Drift** (`just audit-sync`): Investigations marked active but work file archived
2. **Completion Gaps** (`just audit-gaps`): Work items with complete plans but still active
3. **Stale Items** (`just audit-stale`): Investigations older than 10 sessions
4. **Uncaptured Observations** (`just scan-observations`): Work items with pending/missing observations (E2-217)

## Usage

Run all audits:
```bash
just audit-sync && just audit-gaps && just audit-stale && just scan-observations
```

## Interpreting Results

| Finding | Action |
|---------|--------|
| Sync drift | Close investigation or reopen work file |
| Gaps | Close work item or update plan status |
| Stale | Conclude investigation or document why still active |
| Uncaptured observations | Review observations.md and populate or check "None observed" |

## Related

- `/workspace` - Shows outstanding work
- `/status` - System health overview
