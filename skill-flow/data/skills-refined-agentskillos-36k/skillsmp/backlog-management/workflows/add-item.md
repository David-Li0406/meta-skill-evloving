# Add Backlog Item Workflow

## When to Use

Use this workflow when adding a new feature request, bug report, or task to the backlog.

---

## Steps

### 1. Determine Next ID

```bash
# Find the highest existing ID
tail -1 .claude/plans/backlog/data/backlog.csv | cut -d',' -f1
```

Or use Python:
```python
import csv
with open('.claude/plans/backlog/data/backlog.csv') as f:
    items = list(csv.DictReader(f))
    last_id = int(items[-1]['id'].replace('BACKLOG-', ''))
    next_id = f"BACKLOG-{last_id + 1:03d}"
```

### 2. Create Detail File

Create `.claude/plans/backlog/items/BACKLOG-XXX.md`:

```markdown
# BACKLOG-XXX: Title Here

## Problem Statement
What issue does this address?

## Proposed Solution
How should it be solved?

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
Any implementation details or constraints.

## Dependencies
List any blocking items (BACKLOG-XXX).
```

### 3. Add CSV Row

Append to `.claude/plans/backlog/data/backlog.csv`:

```csv
BACKLOG-XXX,Title Here,category,priority,pending,-,-,-,-,[BACKLOG-XXX.md]
```

**Fields:**
- `id`: BACKLOG-XXX
- `title`: Brief description
- `category`: bug/feature/enhancement/refactor/tech-debt/test/docs/infra/security/schema/service/ui/ipc/config
- `priority`: critical/high/medium/low
- `status`: pending (for new items)
- `sprint`: - (not assigned)
- `est_tokens`: - (or estimate like ~30K)
- `actual_tokens`: -
- `variance`: -
- `file`: [BACKLOG-XXX.md]

### 4. Validate

```bash
python .claude/plans/backlog/scripts/validate.py
```

### 5. Log Change (Optional)

For significant items, add to changelog.csv:

```csv
2026-01-17,create,Added BACKLOG-XXX: Title,BACKLOG-XXX
```

---

## Example

Adding a new sync feature:

```bash
# 1. Check last ID
echo "Last ID: $(tail -1 .claude/plans/backlog/data/backlog.csv | cut -d',' -f1)"

# 2. Create detail file
cat > .claude/plans/backlog/items/BACKLOG-303.md << 'EOF'
# BACKLOG-303: Add Retry Logic to Sync

## Problem Statement
Sync operations fail silently on network errors.

## Proposed Solution
Add exponential backoff retry with max 3 attempts.

## Acceptance Criteria
- [ ] Retry on transient network errors
- [ ] Exponential backoff (1s, 2s, 4s)
- [ ] Log retry attempts
- [ ] Surface permanent failures to UI
EOF

# 3. Add to CSV
echo 'BACKLOG-303,Add Retry Logic to Sync,feature,medium,pending,-,~15K,-,-,[BACKLOG-303.md]' >> .claude/plans/backlog/data/backlog.csv

# 4. Validate
python .claude/plans/backlog/scripts/validate.py
```
