# Backlog Analysis Workflow

## When to Use

Use this workflow when you need to:
- Get a snapshot of the backlog state
- Prepare for sprint planning
- Identify items needing attention
- Report on project health
- Find high-priority unassigned work

---

## Quick Commands

```bash
# Full detailed report
python .claude/plans/backlog/scripts/analyze.py

# Quick summary (one-liner)
python .claude/plans/backlog/scripts/analyze.py --summary

# JSON output (for programmatic use)
python .claude/plans/backlog/scripts/analyze.py --json
```

---

## Report Sections

### 1. Summary
- Total items, open items, completed, obsolete
- Quick health check

### 2. Status Breakdown
- Items by status (pending, in-progress, testing, completed, etc.)
- Visual bar chart

### 3. Priority Breakdown (Open Items)
- Critical, High, Medium, Low counts
- Helps prioritize sprint planning

### 4. Category Breakdown
- Bug, Feature, Refactor, UI, etc.
- Identifies where most work is concentrated

### 5. Effort Analysis
- Items with/without estimates
- Total estimated tokens
- Effort buckets: small (<20K), medium (20-50K), large (50-100K), xlarge (>100K)

### 6. Sprint Health
- Active sprints
- Items assigned vs unassigned
- Sprint status breakdown

### 7. Attention Needed (⚠️ Important)
- **High priority unassigned**: Critical/High items not in any sprint
- **Blocked items**: Items waiting on something
- **Testing items**: Awaiting user verification
- **Reopened items**: Failed testing, need rework

### 8. Velocity
- Items completed with token tracking
- Total actual tokens spent

---

## Interpreting the Report

### Healthy Backlog Signs ✓
- Low number of blocked items (< 3)
- No reopened items lingering
- Critical items assigned to sprints
- Good balance of effort sizes
- Most items have estimates

### Warning Signs ⚠️
- Many high-priority unassigned items
- Growing number of blocked items
- Reopened items not being addressed
- Too many items without estimates
- Single category dominating (imbalance)

---

## Using for Sprint Planning

Before planning a new sprint:

```bash
# 1. Run analysis to see current state
python .claude/plans/backlog/scripts/analyze.py

# 2. Check high-priority unassigned items
python .claude/plans/backlog/scripts/queries.py ready | head -20

# 3. Review blocked items (might be unblocked now)
python .claude/plans/backlog/scripts/queries.py status blocked -v

# 4. Plan sprint based on findings
```

---

## Example Output

```
======================================================================
BACKLOG ANALYSIS REPORT
Generated: 2026-01-17T21:30:00
======================================================================

## SUMMARY
  Total Items:     280
  Open Items:      170
  Completed:       103
  Obsolete:        7

## STATUS BREAKDOWN
  pending            170 (60.7%) ████████████
  completed          103 (36.8%) ███████
  obsolete             7 ( 2.5%)

## PRIORITY BREAKDOWN (Open Items Only)
  critical            7 ( 4.1%)
  high               50 (29.4%) █████
  medium            100 (58.8%) ███████████
  low                13 ( 7.6%) █

## ATTENTION NEEDED

  High Priority Unassigned (57 total):
    [critical] BACKLOG-229: Binary Plist Text Still Showing...
    [critical] BACKLOG-234: Fix Race Condition in Sync...
    [high    ] BACKLOG-008: Redesign New Transaction Flow
    ... and 54 more
```

---

## Automation Ideas

### Weekly Report
```bash
# Add to a cron or scheduled task
python analyze.py --summary >> backlog-weekly.log
```

### Pre-Sprint Check
```bash
# Run before any sprint planning session
python analyze.py | head -50
```

### JSON for Dashboards
```bash
# Export for external tools
python analyze.py --json > backlog-state.json
```
