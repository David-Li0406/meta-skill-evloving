# Rollback Strategies

Guide to implementing rollback for multi-step workflows.

## Rollback Principles

1. **Reverse Order**: Rollback executes steps in reverse
2. **Best Effort**: Continue rollback even if a step fails
3. **Idempotent**: Rollback operations should be safe to retry
4. **Logged**: Every rollback action must be recorded

## Rollback Flow

```
Execute: Step 1 → Step 2 → Step 3 → FAIL at Step 4
                                         │
Rollback: Step 3 ← Step 2 ← Step 1 ←────┘
```

## Defining Rollback Actions

### Simple Rollback

```yaml
- id: "create-branch"
  skill: "git-operations"
  action: "create-branch"
  params:
    name: "feature/PROJ-123"
  rollback:
    action: "delete-branch"
    params:
      name: "feature/PROJ-123"
```

### Conditional Rollback

```yaml
- id: "update-status"
  skill: "jira-write"
  action: "transition"
  params:
    issue: "PROJ-123"
    transition: "In Progress"
  rollback:
    action: "transition"
    params:
      issue: "PROJ-123"
      transition: "To Do"
    condition: "previous_status == 'To Do'"
```

### No Rollback (Irreversible)

```yaml
- id: "send-notification"
  skill: "notification"
  action: "send"
  params:
    message: "Deployment started"
  rollback: null  # Cannot unsend notification
```

## Rollback by Operation Type

### Git Operations

| Action | Rollback | Notes |
|--------|----------|-------|
| Create branch | Delete branch | Only if not merged |
| Commit | Revert commit | Creates new commit |
| Push | Force push previous | Requires approval |
| Merge | Revert merge commit | Creates revert commit |

```yaml
rollback:
  action: "delete-branch"
  params:
    name: "{{ step.params.name }}"
    force: false
```

### Jira Operations

| Action | Rollback | Notes |
|--------|----------|-------|
| Create issue | Delete issue | Requires permission |
| Update fields | Restore previous | Store original values |
| Transition | Reverse transition | May not be available |
| Add comment | Delete comment | Store comment ID |

```yaml
rollback:
  action: "restore-fields"
  params:
    issue: "{{ step.params.issue }}"
    fields: "{{ step.original_values }}"
```

### File Operations

| Action | Rollback | Notes |
|--------|----------|-------|
| Create file | Delete file | - |
| Modify file | Restore backup | Create backup first |
| Delete file | Restore from backup | Must backup before |

## State Tracking

Store state for rollback:

```yaml
- id: "update-issue"
  skill: "jira-write"
  action: "update"
  params:
    issue: "PROJ-123"
    summary: "New title"
  storeState:
    - field: "summary"
      as: "original_summary"
  rollback:
    action: "update"
    params:
      issue: "PROJ-123"
      summary: "{{ original_summary }}"
```

## Rollback Scenarios

### Partial Failure

```
Step 1: Create branch     ✓ (rollback: delete branch)
Step 2: Update Jira       ✓ (rollback: revert status)
Step 3: Run tests         ✗ FAILED
Step 4: Create PR         - (skipped)

Rollback sequence:
1. Revert Jira status
2. Delete branch
```

### Rollback Failure

```
Rollback Step 2: Revert Jira  ✗ FAILED (permission denied)
Rollback Step 1: Delete branch ✓

Result: Partial rollback
Action: Manual intervention needed for Jira
```

## Error Handling

```yaml
rollback_config:
  on_failure: "continue"  # continue | abort
  max_retries: 3
  retry_delay: 1000  # ms
  notify_on_failure: true
  manual_steps:
    - "Check Jira issue PROJ-123 status"
    - "Verify branch was deleted"
```

## Best Practices

1. **Always define rollback** for state-changing operations
2. **Store original state** before modifications
3. **Test rollback paths** in development
4. **Log all rollback actions** with timestamps
5. **Have manual fallback** for critical operations
6. **Notify on partial rollback** for manual review
