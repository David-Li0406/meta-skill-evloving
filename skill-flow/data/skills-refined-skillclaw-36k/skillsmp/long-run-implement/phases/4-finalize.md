# Phase 4: Finalize

## Purpose
Complete the long-run session and present summary to user.

## Inputs (from Phase 3)
- `completed_plans`: Count of successfully completed plans
- `failed_plans`: List of failed plan numbers
- `skipped_plans`: List of skipped plan numbers
- `total_commits`: Total number of commits made
- `spec_path`: Path to spec folder
- `state_path`: Path to .long-run/ directory

## Workflow

### Step 1: Aggregate Results

```
Read all SUMMARY.md files from {state_path}/summaries/

Aggregate:
  - Total tasks completed
  - Total files modified
  - Total commits
  - Deviations applied (Rules 1-3)
  - Issues logged (Rule 5)
  - Decisions made (Rule 4)
```

### Step 2: Calculate Metrics

```
metrics = {
  plans: {
    total: count plans,
    completed: count status=="completed",
    failed: count status=="failed",
    skipped: count status=="skipped",
    partial: count status=="partial"
  },
  tasks: {
    total: sum all task counts,
    completed: sum completed tasks
  },
  commits: total_commits,
  duration: end_time - start_time,
  files_modified: unique file list
}
```

### Step 3: Update STATE.md

```
Update STATE.md:
  - Status: Complete
  - Last activity: {timestamp} - Execution completed
  - Progress: [██████████] 100%

  Execution Metrics:
    - Plans completed: {metrics.plans.completed}/{metrics.plans.total}
    - Tasks completed: {metrics.tasks.completed}/{metrics.tasks.total}
    - Total commits: {metrics.commits}
    - Duration: {metrics.duration}
```

### Step 4: Generate Final Summary

```
Output to user:

"═══════════════════════════════════════════════════════
 Long-Run Implementation Complete
═══════════════════════════════════════════════════════

📊 Results:
   Plans:   {completed}/{total} completed
   Tasks:   {tasks_completed}/{tasks_total} completed
   Commits: {commit_count}
   Duration: {duration}

✅ Completed Plans:
   {list of completed plans with task counts}

{IF failed_plans.length > 0}
❌ Failed Plans:
   {list with failure reasons}

{IF skipped_plans.length > 0}
⏭️  Skipped Plans:
   {list with skip reasons}

📁 Files Modified:
   {list of unique files}

📝 Deferred Issues ({issue_count}):
   See: {state_path}/ISSUES.md

🔍 Verification:
   Run: npm test
   Check: git log --oneline -{commit_count}

═══════════════════════════════════════════════════════"
```

### Step 5: Verification Prompt

```
IF any plans failed or skipped:
  Output:
    "⚠️  Some plans were not completed.

     Options:
     1. Review failed/skipped plans
     2. Retry failed plans
     3. Run verification anyway
     4. Exit"

ELSE:
  Output:
    "Would you like to run verification? [y/n]"

  IF yes:
    Execute verification commands from last PLAN.md
    Report results
```

### Step 6: Cleanup Options

```
Output:
  "Long-run state preserved at: {state_path}

   Options:
   1. Keep state (for future reference/audit)
   2. Archive state (move to .long-run-archive/)
   3. Clean up (remove .long-run/)

   Select (1-3):"

Handle user choice:
  1. Keep: Do nothing
  2. Archive: mv .long-run .long-run-archive-{timestamp}
  3. Clean: rm -rf .long-run (after confirmation)
```

## Final Report Template

```markdown
# Long-Run Implementation Report

## Spec: {spec_name}
**Started:** {start_date}
**Completed:** {end_date}
**Duration:** {duration}

## Summary

| Metric | Value |
|--------|-------|
| Plans | {completed}/{total} |
| Tasks | {tasks_completed}/{tasks_total} |
| Commits | {commit_count} |
| Files Modified | {file_count} |

## Plans Executed

### Completed
| Plan | Tasks | Commits | Duration |
|------|-------|---------|----------|
{for each completed plan}

### Failed
| Plan | Failed At | Error |
|------|-----------|-------|
{for each failed plan}

### Skipped
| Plan | Reason |
|------|--------|
{for each skipped plan}

## Deviations Applied

### Auto-Fixed (Rules 1-3)
{list from all summaries}

### Deferred (Rule 5)
{list from ISSUES.md}

## Decisions Made
{list from all summaries}

## Commits
```
git log --oneline -{commit_count}
```

## Next Steps
- Review ISSUES.md for deferred items
- Run full test suite
- Manual verification of UI/UX elements
```

## Error Handling

```
ON aggregation error:
  Log warning
  Present partial results
  Offer manual inspection option
```
