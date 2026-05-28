---
name: meatycapture-capture
description: Use this skill to capture bugs, enhancements, and ideas into request-logs efficiently, utilizing quick commands or scripts for streamlined operations.
---

# Skill body

## Capture Method Selection

| Scenario | Method | Tokens/Effort |
|----------|--------|---------------|
| Single capture during development | `mc-quick.sh` | ~50 tokens |
| AI agent capturing findings | `mc-quick.sh` | ~50 tokens |
| Batch capture (3+ items) | Direct CLI | ~200+ tokens |
| Complex notes or custom fields | Direct CLI | ~200+ tokens |
| Appending to existing docs | Direct CLI | ~150 tokens |
| Post-commit: update docs + close item | `update-bug-docs.py` | ~20 tokens |
| Batch file bugs (3+) from JSON/CSV | `batch-file-bugs.sh` | ~30 tokens |

## Quick Capture Script

Use the following command to quickly capture a bug or enhancement:

```bash
mc-quick.sh TYPE DOMAIN SUBDOMAIN "Title" "Problem" "Goal" [notes...]

# Examples:
mc-quick.sh enhancement web deployments "Add remove button" "Button not implemented" "Full removal workflow"
mc-quick.sh bug api validation "Fix timeout" "Sessions expire early" "Extend TTL to 24h"

# With environment variables:
MC_PROJECT=other-project MC_PRIORITY=high mc-quick.sh bug cli commands "Title" "Problem" "Goal"
```

**Environment Variables**: 
- `MC_PROJECT` (default: skillmeat)
- `MC_PRIORITY` (default: medium)
- `MC_STATUS` (default: triage)

## Quick Commands (use `/mc` for simple operations)

| Command | Example |
|---------|---------|
| List | `meatycapture log list PROJECT --json` |
| View | `meatycapture log view PATH --json` |
| Search | `meatycapture log search "query" PROJECT --json` |
| Capture | `meatycapture log create --json < input.json` |
| Note Add | `meatycapture log note add DOC ITEM -c "text"` |
| Update | `meatycapture log item update DOC ITEM --status done` |

## Workflows (load only when needed)

| Action | When to Load |
|--------|--------------|
| [Capture](./workflows/capturing.md) | Batch capture, validation, templates |
| [View/Search](./workflows/viewing.md) | Advanced filters, output formats |
| [Status Update](./workflows/updating.md) | Change item status, add notes |
| [Projects](./workflows/managing.md) | Configure projects, defaults |

## Field Reference

Refer to the field options documentation for valid values.