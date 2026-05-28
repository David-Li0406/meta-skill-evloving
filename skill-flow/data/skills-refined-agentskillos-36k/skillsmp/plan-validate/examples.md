# Plan Validate Examples

## Basic Validation

### Validate Specific Plan

```bash
/plan-validate plan-design-linking-phase-1
```

**Output:**

```text
Validating plan: .claude/plans/plan-design-linking-phase-1.md

Checking required fields...
✓ Required field 'name' present
✓ Required field 'title' present
✓ Required field 'created' present
✓ Required field 'status' present
✓ Required field 'progress' present

Validating field values...
✓ name: 'plan-design-linking-phase-1' (valid kebab-case)
✓ status: 'ready' (valid)
✓ progress: 0% (valid)
✓ created: 2026-01-18 (valid format)
✓ updated: 2026-01-18 (valid format)
✓ Status 'ready' with progress 0% (aligned)

----------------------------------------
✓ Validation passed! No errors found.
```

### Validate All Plans

```bash
/plan-validate --all
```

**Output:**

```text
Validating all plans in .claude/plans/

Plan 1/3: plan-design-linking-phase-1.md
✓ Validation passed

Plan 2/3: subagent-integration-plan.md
✓ Validation passed

Plan 3/3: indexed-wishing-kurzweil.md
✗ Validation failed (2 errors)
  ✗ Missing required field: status
  ⚠ No updates in 45 days (stale)

----------------------------------------
Summary: 2 passed, 1 failed
```

## Error Scenarios

### Missing Required Fields

**Plan with missing status:**

```yaml
---
name: my-feature-plan
title: "My Feature"
created: 2026-01-18
# status: ready  # MISSING
progress: 0
---
```

**Output:**

```text
✗ Validation failed: my-feature-plan

Errors (1):
  ✗ Missing required field: status

Fix: Add 'status: ready|in-progress|blocked|completed|abandoned'
     to the plan frontmatter
```

### Invalid Status Value

**Plan with typo in status:**

```yaml
---
name: my-feature-plan
title: "My Feature"
created: 2026-01-18
status: inprogress  # Invalid (should be 'in-progress')
progress: 50
---
```

**Output:**

```text
✗ Validation failed: my-feature-plan

Errors (1):
  ✗ status: 'inprogress' (must be one of: ready, in-progress, blocked,
    completed, abandoned)

Fix: Change status to 'in-progress' (note the hyphen)
```

### Status-Progress Misalignment

**Plan marked ready but has progress:**

```yaml
---
name: my-feature-plan
title: "My Feature"
created: 2026-01-18
status: ready
progress: 25  # Should be 0 for 'ready' status
---
```

**Output:**

```text
⚠ Validation warning: my-feature-plan

Warnings (1):
  ⚠ Status 'ready' should have progress 0%, found 25%

Recommendation: Either:
  1. Set progress to 0 if work hasn't started
  2. Change status to 'in-progress' if work has begun
```

### Completed Plan Missing Outcome

**Completed plan without outcome:**

```yaml
---
name: my-feature-plan
title: "My Feature"
created: 2026-01-10
status: completed
progress: 100
completed: 2026-01-18
# outcome: success  # MISSING
---
```

**Output:**

```text
✗ Validation failed: my-feature-plan

Errors (1):
  ✗ Status 'completed' requires 'outcome' field

Fix: Add one of:
  - outcome: success (plan fully completed)
  - outcome: partial (partially completed)
  - outcome: failed (plan abandoned/failed)
```

### Invalid Date Format

**Plan with wrong date format:**

```yaml
---
name: my-feature-plan
title: "My Feature"
created: 01/18/2026  # Wrong format
status: ready
progress: 0
---
```

**Output:**

```text
✗ Validation failed: my-feature-plan

Errors (1):
  ✗ created: 01/18/2026 (must be YYYY-MM-DD)

Fix: Change to: created: 2026-01-18
```

## Strict Mode

### Basic Strict Validation

```bash
/plan-validate my-feature-plan --strict
```

Strict mode adds:

- **Stale check**: Warn if no updates >30 days
- **Bidirectional links**: Verify design docs reference this plan
- **Orphan check**: Warn if plan has no `implements` field
- **Effort alignment**: Check estimated vs actual effort

**Output:**

```text
✓ Validation passed: my-feature-plan

Strict Mode Checks:
  ✓ Last updated 5 days ago (not stale)
  ✓ Linked to 1 design doc (cache-optimization.md)
  ✓ Design doc references this plan (bidirectional)
  ⚠ No estimated-effort field (recommendation: add estimate)

----------------------------------------
✓ Strict validation passed with 1 recommendation
```

### Stale Plan Detection

```bash
/plan-validate old-feature-plan --strict
```

**Output:**

```text
⚠ Validation warning: old-feature-plan

Strict Mode Issues:
  ⚠ Last updated 62 days ago (stale threshold: 30 days)
  ⚠ Status is 'in-progress' but no recent activity

Recommendations:
  1. Update plan status if work has stopped
  2. Mark as 'blocked' if waiting on dependencies
  3. Mark as 'abandoned' if no longer relevant
  4. Update progress and 'updated' date if still active
```

### Orphaned Plan

```bash
/plan-validate orphan-plan --strict
```

**Output:**

```text
⚠ Validation warning: orphan-plan

Strict Mode Issues:
  ⚠ No 'implements' field (orphaned plan)
  ⚠ Plan is not linked to any design documentation

Recommendations:
  1. Add 'implements: [design-doc-path]' to link to design docs
  2. If this is an operational task, add 'categories: [operations]'
  3. Consider if recurring operational tasks should become design docs
```

## Fix Mode

### Auto-Fix Issues

```bash
/plan-validate my-feature-plan --fix
```

**Auto-fixes:**

- Update `updated` field to current date
- Format dates to YYYY-MM-DD
- Normalize kebab-case names
- Calculate progress from phases (if present)

**Output:**

```text
Validating plan: my-feature-plan.md (fix mode)

Auto-fixes applied:
  ✓ Updated 'updated' field to 2026-01-18
  ✓ Formatted created date to YYYY-MM-DD
  ✓ Calculated progress from phases: 40%

Remaining issues:
  ✗ Missing required field: status (cannot auto-fix)

Fix manually: Add 'status: ready|in-progress|...' to frontmatter
```

## CI/CD Integration

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate changed plan files
git diff --cached --name-only | \
  grep '.claude/plans/.*\.md$' | \
  while read plan; do
    if [[ -f "$plan" ]]; then
      .claude/scripts/validate-plan.sh "$plan" || exit 1
    fi
  done
```

### GitHub Actions

```yaml
name: Validate Plans
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate plans
        run: |
          for plan in .claude/plans/*.md; do
            .claude/scripts/validate-plan.sh "$plan" || exit 1
          done
```

## Integration with Other Skills

### After Creating Plan

```bash
# Create plan
/plan-create "My Feature Implementation" --module=effect-type-registry

# Immediately validate
/plan-validate my-feature-implementation
```

### Before Updating Design Doc

```bash
# Validate plan is complete
/plan-validate cache-optimization-plan

# If valid and completed, update design doc
/design-update effect-type-registry cache-optimization.md --status=current
```

### Weekly Health Check

```bash
# Check all plans for staleness
/plan-validate --all --strict
```

**Output:**

```text
Plan Health Report:

Active Plans (3):
  ✓ plan-design-linking-phase-1 (updated 2 days ago)
  ⚠ cache-optimization-plan (updated 45 days ago - STALE)
  ✓ observability-phase-2 (updated 1 day ago)

Completed Plans (7):
  ✓ All completed plans archived

Recommendations:
  - Review stale cache-optimization plan
  - Archive completed plans older than 30 days
```
