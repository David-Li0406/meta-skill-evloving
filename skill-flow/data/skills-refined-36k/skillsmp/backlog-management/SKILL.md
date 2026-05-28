---
name: backlog-management
description: Query, update, and manage the project backlog using the CSV-based system.
---

# Backlog Management Skill

This skill provides workflows for managing the project backlog. The backlog uses a CSV-based system for efficient querying and reduced token usage.

---

## System Overview

```
.claude/plans/backlog/
├── data/
│   ├── backlog.csv      # Main table (source of truth)
│   ├── sprints.csv      # Sprint history
│   ├── changelog.csv    # Audit trail
│   └── SCHEMA.md        # Column definitions
├── scripts/
│   ├── queries.py       # Query interface
│   └── validate.py      # Schema validation
├── items/               # BACKLOG-XXX.md detail files
└── README.md            # Quick start guide
```

---

## Quick Reference

### Query Items

```bash
# By status
python .claude/plans/backlog/scripts/queries.py status pending

# By priority
python .claude/plans/backlog/scripts/queries.py priority high --status pending

# Sprint items
python .claude/plans/backlog/scripts/queries.py sprint SPRINT-042

# Search
python .claude/plans/backlog/scripts/queries.py search "sync"

# Statistics
python .claude/plans/backlog/scripts/queries.py stats
```

### Python Module Usage

```python
import csv

# Load all items
with open('.claude/plans/backlog/data/backlog.csv') as f:
    items = list(csv.DictReader(f))

# Filter to pending high priority
pending_high = [
    i for i in items
    if i['status'].lower() == 'pending'
    and i['priority'].lower() == 'high'
]
```

---

## Workflows

| Workflow | When to Use |
|----------|-------------|
| [Backlog Analysis](workflows/backlog-analysis.md) | Generate health report, find attention items |
| [Add Item](workflows/add-item.md) | Creating a new backlog item |
| [Close Item](workflows/close-item.md) | Completing or obsoleting an item |
| [Sprint Planning](workflows/sprint-planning.md) | Planning a new sprint |

---

## Key Rules

1. **CSV is source of truth** - Always update backlog.csv for status changes
2. **All items need .md files** - Create BACKLOG-XXX.md for every item
3. **Run validation** - Execute `python .claude/plans/backlog/scripts/validate.py` before committing
4. **Log key changes** - Add entries to changelog.csv for significant changes

---

## Status Flow (IMPORTANT)

```
pending → in-progress → testing → completed
                           ↓
                       reopened → in-progress → ...
```

**CRITICAL RULES:**
1. Code merged = `testing` (NOT completed)
2. Only user verification = `completed`
3. Failed testing = `reopened` (NEVER create new task)

### Status Values
- `pending` - Not started
- `in-progress` - Currently being worked on
- `testing` - Code merged, awaiting user verification
- `completed` - Done AND verified by user
- `blocked` - Waiting on something
- `deferred` - Postponed
- `obsolete` - No longer relevant
- `reopened` - Failed testing, needs more work

### Priority
- `critical` - Must be done immediately
- `high` - Important, do soon
- `medium` - Normal priority
- `low` - Nice to have

---

## Related Documentation

- Schema details: `.claude/plans/backlog/data/SCHEMA.md`
- Estimation guidelines: [estimation-guidelines.md](estimation-guidelines.md)
- CSV reference: [csv-reference.md](csv-reference.md)
