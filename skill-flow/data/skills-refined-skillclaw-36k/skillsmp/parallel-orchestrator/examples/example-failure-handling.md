# Example: Failure Handling in Parallel Execution

## Scenario
3 of 5 parallel tasks complete successfully, 2 fail.

## Progress with Failures

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ Execution Mode: PARALLEL                                 │
│    Progress: [████████████░░░░████] 3/5 complete, 2 failed  │
│                                                             │
│    ✅ Agent 1: sidebar.tsx (QA approved)                    │
│    ✅ Agent 2: header.tsx (QA approved)                     │
│    ❌ Agent 3: footer.tsx (TASK_FAILED after 3 retries)     │
│    ❌ Agent 4: nav.tsx (QA rejected - type errors)          │
│    ✅ Agent 5: stat-bar.tsx (QA approved)                   │
└─────────────────────────────────────────────────────────────┘
```

## Failure Details

### Agent 3: Task Failed

```
TASK_FAILED: task-3 (footer.tsx)

## Failure Report

### Error
Cannot find module '@/components/Icon' from 'components/Footer.tsx'

### Attempts
1. Tried creating Icon component → still failed (wrong path)
2. Tried updating import path → introduced new errors
3. Tried using different icon library → type conflicts

### Root Cause
Missing Icon component that should have been created in separate task.
Dependency not properly tracked in decomposition.

### Recommended Action
1. Add Icon component as prerequisite task
2. Re-run task-3 after Icon is available
```

### Agent 4: QA Rejected

```
TASK_REJECTED: task-4 (nav.tsx)

## QA Verification Report

### Failures Detected

#### Type Errors (2)
src/components/Nav.tsx:15:5
  error TS2322: Type 'string[]' is not assignable to type 'NavItem[]'

src/components/Nav.tsx:28:3
  error TS7006: Parameter 'item' implicitly has an 'any' type

### Recommendation
Return to task-executor for fixes:
1. Define proper NavItem type
2. Add explicit type to map callback
```

## Orchestrator Decision

```
┌─────────────────────────────────────────────────────────────┐
│ Parallel Group 1 Summary                                    │
│                                                             │
│    Completed: 3/5                                           │
│    Failed: 2/5                                              │
│                                                             │
│    Options:                                                 │
│    A) Retry failed tasks (if fixable)                       │
│    B) Proceed with partial merge (3 tasks)                  │
│    C) Abort and investigate                                 │
│                                                             │
│    Selected: A - Retry failed tasks                         │
│                                                             │
│    Actions:                                                 │
│    1. task-3: Add missing dependency, requeue               │
│    2. task-4: Return to task-executor with QA feedback      │
└─────────────────────────────────────────────────────────────┘
```

## Retry Tracking

```yaml
# .claude/auto-progress.yaml
tasks:
  task-3:
    status: pending_retry
    retry_count: 1
    last_error: "Missing dependency: Icon component"
    dependency_added: true
  task-4:
    status: pending_fix
    qa_feedback: |
      - Fix type error at Nav.tsx:15
      - Fix type error at Nav.tsx:28
    return_to_executor: true
```

## After Successful Retry

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ Execution Mode: PARALLEL                                 │
│    Progress: [████████████████████] 5/5 complete            │
│                                                             │
│    ✅ Agent 1: sidebar.tsx (QA approved)                    │
│    ✅ Agent 2: header.tsx (QA approved)                     │
│    ✅ Agent 3: footer.tsx (QA approved, retry 1)            │
│    ✅ Agent 4: nav.tsx (QA approved, retry 1)               │
│    ✅ Agent 5: stat-bar.tsx (QA approved)                   │
│                                                             │
│    Ready for integration phase.                             │
└─────────────────────────────────────────────────────────────┘
```
