---
description: Consolidate auto-captured session files into daily summaries
---

# Consolidate - Session File Merger

รวม session files ที่เกี่ยวข้องเข้าด้วยกันเป็น daily summary เพื่อลดความกระจัดกระจาย

## Usage

```
/consolidate                       # Preview today's consolidation
/consolidate --date YYYY-MM-DD     # Preview specific date
/consolidate [options] --execute   # Execute consolidation
```

## Instructions

### Step 1: Parse Arguments and Show Current State

```bash
export TZ='Asia/Bangkok'

echo "=== Auto-captured Files ==="
find docs/auto-captured -type f -name "*.md" ! -name "daily-summary.md" 2>/dev/null | wc -l | xargs echo "Total session files:"

echo ""
echo "=== Today's Sessions ==="
TODAY=$(date '+%Y-%m/%d')
if [ -d "docs/auto-captured/$TODAY" ]; then
    find "docs/auto-captured/$TODAY" -type f -name "*.md" ! -name "daily-summary.md" 2>/dev/null | wc -l | xargs echo "Files:"
else
    echo "No sessions for today"
fi

echo ""
echo "=== Existing Summaries ==="
find docs/auto-captured -name "daily-summary.md" 2>/dev/null | wc -l | xargs echo "Daily summaries:"
```

### Step 2: Determine Mode

| Argument | Mode |
|----------|------|
| (none) | Dry-run, today's date |
| `--date YYYY-MM-DD` | Dry-run, specific date |
| `--execute` | Execute consolidation |
| `--time-window N` | Set time proximity window (default: 30 min) |
| `--overlap N` | Set file overlap threshold (default: 50%) |

### Step 3: Run Consolidate Script

**Dry-run mode (default):**

```bash
cd "$PROJECT_ROOT"
./scripts/consolidate.sh --date [DATE] --dry-run [--time-window N] [--overlap N]
```

**Execute mode:**

```bash
cd "$PROJECT_ROOT"
./scripts/consolidate.sh --date [DATE] --execute [--time-window N] [--overlap N]
```

### Step 4: Show Results

Display the script output showing:
- Sessions found for the date
- Groups formed (by issue, files, time)
- Sessions in each group
- Ungrouped sessions

### Step 5: Confirm and Suggest Next Steps

```markdown
## Consolidation Summary

| Metric | Value |
|--------|-------|
| Date | [date] |
| Sessions Found | [count] |
| Groups Formed | [count] |
| Ungrouped | [count] |

### Next Steps

1. Review consolidated file at `docs/auto-captured/[date]/daily-summary.md`
2. Run `/cleanup` to manage old session files (optional)
3. Use `/distill` to extract patterns from consolidated sessions
```

## Grouping Algorithm

Sessions are grouped by priority:

| Priority | Criterion | Description |
|----------|-----------|-------------|
| 1 | Issue Number | Sessions mentioning same #123 or PROJ-123 |
| 2 | File Overlap | Sessions with >50% overlapping files changed |
| 3 | Time Proximity | Sessions within 30-minute windows |

## Output Format

**File:** `docs/auto-captured/YYYY-MM/DD/daily-summary.md`

```markdown
---
type: daily-summary
date: YYYY-MM-DD
sessions_merged: N
groups_formed: N
---

# Daily Summary: YYYY-MM-DD

## Group 1: Task #38
> 3 sessions merged | 10:30 - 14:45

### Sessions Included
| Time | Session ID |
|------|------------|
| 10:30 | session-12345 |

### Combined Content
[merged content from all sessions]

---

## Ungrouped Sessions
[sessions that didn't match any criteria]
```

## Examples

```bash
# Preview today's consolidation
/consolidate

# Preview specific date
/consolidate --date 2026-01-13

# Execute consolidation for today
/consolidate --execute

# Use custom time window (60 minutes)
/consolidate --time-window 60 --execute

# Consolidate with lower overlap threshold
/consolidate --overlap 30 --execute
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/cleanup` | Delete old session files |
| `/distill` | Extract patterns from sessions |
| `/td` | Create retrospective |
