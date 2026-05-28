# Close Backlog Item Workflow

## When to Use

Use this workflow when:
- A backlog item's code has been merged (→ testing)
- User has verified the item works (→ completed)
- User found issues during testing (→ reopened)
- An item is no longer relevant (→ obsolete)

---

## IMPORTANT: Status Flow

```
pending → in-progress → testing → completed
                           ↓
                       reopened → in-progress → testing → ...
```

**CRITICAL RULES:**
1. **NEVER mark "completed" until user has tested**
2. **NEVER create a new task for failed testing** - reopen the original
3. **Code merged = "testing"**, not "completed"

---

## Steps

### 1. After PR Merged (Engineer)

When code is merged, move to "testing" status:
```csv
BACKLOG-XXX,Title,category,priority,testing,SPRINT-XXX,~30K,-,-,[BACKLOG-XXX.md]
```

This signals: "Ready for user verification"

### 2. After User Testing

**If user confirms it works:**
```csv
BACKLOG-XXX,Title,category,priority,completed,SPRINT-XXX,~30K,28K,-7%,[BACKLOG-XXX.md]
```

**If user finds issues (DO NOT create new task!):**
```csv
BACKLOG-XXX,Title,category,priority,reopened,SPRINT-XXX,~30K,-,-,[BACKLOG-XXX.md]
```

Then work on the SAME item again until it passes testing.

### 3. For Obsolete Items

```csv
BACKLOG-XXX,Title,category,priority,obsolete,-,-,-,-,[BACKLOG-XXX.md]
```

### 3. Update Detail File (Optional)

Add completion notes to the BACKLOG-XXX.md file:

```markdown
## Completion Notes
- Completed in SPRINT-XXX
- PR #YYY
- Actual effort: 28K tokens
```

### 4. Log Change

Add to changelog.csv:

```csv
2026-01-17,complete,Completed BACKLOG-XXX via PR #YYY,BACKLOG-XXX
```

For reopened items:
```csv
2026-01-17,status_change,Reopened BACKLOG-XXX: reason here,BACKLOG-XXX
```

### 5. Validate

```bash
python .claude/plans/backlog/scripts/validate.py
```

---

## Bulk Close

When completing multiple items in a sprint:

```python
import csv

# Items to close
completed = ['BACKLOG-220', 'BACKLOG-221', 'BACKLOG-222']
sprint = 'SPRINT-042'

# Read, update, write
with open('.claude/plans/backlog/data/backlog.csv') as f:
    rows = list(csv.DictReader(f))

for row in rows:
    if row['id'] in completed:
        row['status'] = 'completed'
        row['sprint'] = sprint

# Write back
with open('.claude/plans/backlog/data/backlog.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
```

---

## Status Transitions

| From | To | When |
|------|----|------|
| pending | in-progress | Work started |
| pending | deferred | Postponed |
| pending | obsolete | No longer needed |
| in-progress | completed | Work done |
| in-progress | blocked | Waiting on dependency |
| completed | reopened | Bug found or incomplete |
| blocked | in-progress | Dependency resolved |
| deferred | pending | Ready to work |
