# Execution State: {spec_name}

## Status
- **Phase:** Ready to Execute
- **Current Task:** Task 1 - {first_task_name}
- **Progress:** [░░░░░░░░░░] 0/{total} tasks

**Progress Calculation:** `(completed_plans / total_plans) * 100`
- Use 10-character bar: each █ = 10%
- Example: 3/5 plans = 60% = `[██████░░░░] 60%`

## Task Groups

| # | Task Group | Agent | Status |
|---|------------|-------|--------|
| 1 | {name} | long-run-executor | Pending |

## Metrics
- **Started:** {date}
- **Commits:** 0
- **Files Modified:** 0

## Rollback Reference
- **start_commit:** (set by orchestrator on first execution)

## Accumulated Context

### Decisions Made
| Plan | Decision | Rationale |
|------|----------|-----------|

### Deferred Issues
- (none)

## Session Continuity
- **Last session:** (not started)
- **Stopped at:** (not started)
- **Resume agent:** None

## Configuration
clarification_timeout_minutes: 10
timeout_per_plan_minutes: 30
timeout_action: prompt
