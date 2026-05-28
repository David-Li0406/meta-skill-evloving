# Validation Fixes

This reference describes how to fix validation issues, both automatic and manual.

## Auto-Fixable Issues

These issues are fixed automatically by `spec action="fix"`:

| Issue | Fix Action | Notes |
|-------|------------|-------|
| Incorrect task counts | Recalculates from hierarchy | Safe, no data loss |
| Missing metadata blocks | Adds empty metadata | Adds `{}` where missing |
| Orphaned nodes | Reconnects to parent | Uses position hints |
| Malformed timestamps | Converts to ISO 8601 | Preserves date/time info |
| Invalid status values | Resets to `pending` | Logs original value |
| Parent/child mismatches | Corrects references | Bi-directional sync |
| Missing required fields | Adds with defaults | Uses schema defaults |

## Manual-Only Issues

These require human judgment:

| Issue | Why Manual | Resolution |
|-------|-----------|------------|
| Circular dependencies | Requires intent understanding | Remove weakest edge |
| Orphaned dep references | Typo vs intentional | Fix typo or remove ref |
| Semantic inconsistencies | Business logic | Review spec intent |
| Custom metadata errors | Unknown structure | Requires context |
| Duplicate task titles | May be intentional | Merge or differentiate |
| Similar descriptions | Context-dependent | Review scope overlap |
| Overlapping criteria | Verification design | Narrow scope or consolidate |

## Fixing Circular Dependencies

1. Identify the cycle from validation output
2. Understand the intent of each dependency
3. Remove the dependency that represents "nice to have" vs "must have"
4. Re-validate to confirm cycle is broken

**Example:**
```
Cycle: task-3-2 -> task-3-5 -> task-3-2

Analysis:
- task-3-2 "Create API client" depends on task-3-5 "Define interfaces"
- task-3-5 "Define interfaces" depends on task-3-2 "Create API client"

Resolution: Interfaces should be defined first
Remove: task-3-5's dependency on task-3-2
```

## Fixing Orphaned Dependencies

1. Check if the referenced task ID is a typo
2. If typo: correct the task ID
3. If intentional removal: delete the dependency reference

## Fixing Duplicate Tasks

Detected via `spec action="duplicate-detection"`.

### Exact Title Matches

```
Issue: task-2-3 and task-4-1 both titled "Add user validation"
Resolution options:
1. Merge: Combine into single task if truly duplicate
2. Differentiate: Rename to "Add user validation (API)" and "Add user validation (UI)"
3. Keep: If intentionally same work in different phases (rare)
```

### Similar Descriptions

```
Issue: 85% match between task-1-5 and task-3-2
Resolution options:
1. Clarify scope: Add distinguishing context to each description
2. Merge: If covering same functionality
3. Accept: If similar but different phases/contexts
```

### Overlapping Acceptance Criteria

```
Issue: verify-2-1 and verify-3-1 both check "all tests pass"
Resolution options:
1. Scope: "All phase-2 tests pass" vs "All phase-3 tests pass"
2. Consolidate: Single verify task covering both phases
3. Remove: If redundant verification
```

### When to Ignore Duplicates

Duplicates may be intentional when:
- Same validation in different phases (staged rollout)
- Parallel implementations for comparison
- Template-based spec generation

## When to Stop Auto-Fixing

Switch to manual intervention when:
- Error count unchanged for 2+ passes (plateau)
- Fix reports "skipped issues requiring manual intervention"
- All remaining issues need context or human judgment

## Rollback

If fixes cause problems, use backup to restore:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="history" spec_id="{spec-id}"
mcp__plugin_foundry_foundry-mcp__authoring action="spec-rollback" spec_id="{spec-id}" version="{timestamp}"
```

Backups are created automatically before each fix operation.
