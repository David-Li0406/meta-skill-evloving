# Time Tracking Guide

Workflows and patterns for effective time tracking with the ClickUp CLI.

## Daily Workflows

### Morning Check

See what you tracked yesterday and what's in progress:

```bash
# Yesterday's time
npm run dev -- time list --date yesterday

# Tasks you're assigned to
npm run dev -- tasks search "" --assignee me --status "in progress" --table
```

### End of Day

Log time and verify totals:

```bash
# See what's logged today
npm run dev -- time list

# Add missing time
npm run dev -- time add TCG-4752 --duration "2h" --description "Code review"

# Verify total
npm run dev -- time list  # Check total at bottom
```

### Fix Misplaced Time Entry

If you logged time to the wrong date:

```bash
# Find the entry ID
npm run dev -- time list --date 2026-01-19

# Move to correct date (preserves time of day)
npm run dev -- time move 4919362882926207451 --to 2026-01-20
```

### Delete Duplicate Entry

```bash
# Find entries
npm run dev -- time list --date 2026-01-20

# Preview delete
npm run dev -- time delete 4919362882926207451

# Confirm delete
npm run dev -- time delete 4919362882926207451 --force
```

---

## Weekly Workflows

### Weekly Report

```bash
# Current week (Mon-Sun)
npm run dev -- time report

# Previous week
npm run dev -- time report --week 2026-01-13

# Export as JSON for processing
npm run dev -- time report --json > weekly-report.json
```

### Report Output

```
Weekly Time Report: Jan 19, 2026 - Jan 25, 2026

Daily Breakdown:
┌────────────┬──────────────┬──────────┬────────┐
│ Day        │ Date         │ Hours    │ Entries│
├────────────┼──────────────┼──────────┼────────┤
│ Monday     │ 2026-01-19   │ 0.00     │ 0      │
│ Tuesday    │ 2026-01-20   │ 8.00     │ 4      │
│ Wednesday  │ 2026-01-21   │ 0.00     │ 0      │
...

By Task:
┌──────────────────────────────────────────────────┬──────────┐
│ Task                                             │ Hours    │
├──────────────────────────────────────────────────┼──────────┤
│ TCG-2990 - RBS Sprint 13 Meetings                │ 2.00     │
│ TCG-4760 - Step 4 Manual Imports: Frontend       │ 4.50     │
│ TCG-4752 - Billing Calculation Engine Phase 1    │ 1.50     │
└──────────────────────────────────────────────────┴──────────┘

Total: 8.00 hours
```

---

## Time Entry Patterns

### Log by Duration

Best for when you know total time spent:

```bash
npm run dev -- time add TCG-4752 --duration "2h 30m" --date "2026-01-20"
```

### Log by Time Range

Best for meetings or specific work blocks:

```bash
npm run dev -- time add TCG-4752 \
  --start "2026-01-20 10:30" \
  --end "2026-01-20 15:00" \
  --description "Frontend integration work"
```

### Real-time Tracking

Start/stop timer as you work:

```bash
# Start working
npm run dev -- time start TCG-4752 --description "Working on feature"

# Check status
npm run dev -- time current

# Stop when done
npm run dev -- time stop
```

---

## Bulk Operations

### Find All Entries for a Task

```bash
npm run dev -- time list --task TCG-4752 --start 2026-01-01 --end 2026-01-31
```

### Export for Spreadsheet

```bash
npm run dev -- time list --date 2026-01-20 --json | jq -r '.[] | [.id, .task.name, .duration] | @csv'
```

---

## Duration Formats

The CLI accepts flexible duration inputs:

| Input | Interpretation |
|-------|----------------|
| `2h` | 2 hours |
| `30m` | 30 minutes |
| `2h 30m` | 2 hours 30 minutes |
| `2.5h` | 2 hours 30 minutes |
| `150` | 150 minutes |

---

## Tips

1. **Use custom IDs**: `TCG-4752` is easier than `86dz8kbp5`

2. **Add descriptions**: Makes reports more meaningful
   ```bash
   npm run dev -- time add TCG-4752 --duration "2h" --description "PR review and fixes"
   ```

3. **Check before submitting**: Use `time list` to verify entries before EOD

4. **Move vs Update**: Use `move` to change dates (preserves time), `update` for other changes

5. **Weekly ritual**: Run `time report` every Friday to verify hours
