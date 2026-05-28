# Plan Complete Examples

## Basic Completion

Complete a successfully implemented plan:

```bash
/plan-complete plan-design-linking-phase-1
```

**What happens:**

1. Validates plan is completed (status, progress)
2. Updates linked design docs to current status
3. Adds completion metadata to design docs
4. Deletes the plan file

**Output:**

```text
Completing plan: plan-design-linking-phase-1

Plan metadata:
  Title: Plan-Design Linking System - Phase 1 Implementation
  Status: completed
  Progress: 100%

✓ Plan meets completion requirements

Updating linked design docs:
  Processing: design-doc-system/plan-aware-enhancements.md
    Current status: draft
    ✓ Updated status to current
    ✓ Updated last-synced to 2026-01-18
    ✓ Added completion metadata

  Processing: design-doc-system/hook-automation-system.md
    Current status: draft
    ✓ Updated status to current
    ✓ Updated last-synced to 2026-01-18
    ✓ Added completion metadata

✓ Deleted plan file: .claude/plans/plan-design-linking-phase-1.md

✓ Plan completion successful!

Summary:
  Plan: plan-design-linking-phase-1
  Outcome: success
  Design docs updated: 2
  Plan file: Deleted
```

## Partial Completion

When implementation is partial but still valuable:

```bash
/plan-complete cache-optimization --outcome=partial
```

**Use when:**

- Core features implemented, some deferred
- POC completed, full implementation pending
- Foundation laid, advanced features skipped

**Design doc metadata:**

```yaml
completed-plans:
  - name: "cache-optimization"
    completed: "2026-01-18"
    outcome: "partial"
```

## Failed Implementation

Record failed attempts (knowledge is still valuable):

```bash
/plan-complete experimental-approach --outcome=failed
```

**Use when:**

- Approach didn't work but documented why
- Technical constraints discovered
- Alternative chosen, this path abandoned

**Value:** Design doc explains what was tried and why it failed.

## Dry Run Preview

Preview changes before executing:

```bash
/plan-complete subagent-integration --dry-run
```

**Output:**

```text
Completing plan: subagent-integration

✓ Plan meets completion requirements

Updating linked design docs:
  Processing: design-doc-system/subagent-integration.md
    Current status: draft
    [DRY RUN] Would update:
      - status: current
      - last-synced: 2026-01-18
      - Add completion metadata

[DRY RUN] Would delete plan file: .claude/plans/subagent-integration.md

✓ Plan completion successful!
```

**Use when:**

- Verifying which design docs will be updated
- Checking completion requirements
- Testing before actual execution

## Keep Plan File

Complete but keep the plan for reference:

```bash
/plan-complete major-refactor --keep
```

**Use when:**

- Plan has detailed implementation notes
- Want to reference approach later
- Multiple people need to review

**Result:** Design docs updated, plan file remains

## Multiple Design Docs

Plan implementing multiple design docs:

```yaml
# Plan frontmatter
implements:
  - design-doc-system/plan-schema.md
  - design-doc-system/plan-validation.md
  - design-doc-system/plan-skills.md
```

```bash
/plan-complete multi-doc-plan
```

**Result:** All three design docs updated to current status with completion metadata.

## Error: Plan Not Completed

Attempting to complete an in-progress plan:

```bash
/plan-complete active-work
```

**Output:**

```text
Plan metadata:
  Title: Active Work In Progress
  Status: in-progress
  Progress: 75%

⚠  Status is 'in-progress' (expected 'completed')
⚠  Progress is 75% (expected 100%)

✗ Plan does not meet completion requirements
Fix these issues before completing the plan
```

**Fix:**

1. Update plan frontmatter: status to completed, progress to 100
2. Run complete again

## Error: Missing Design Doc

Plan links to non-existent design doc:

```bash
/plan-complete broken-links
```

**Output:**

```text
✓ Plan meets completion requirements

Updating linked design docs:
  ✗ Design doc not found: design-doc-system/missing-doc.md

Summary:
  Plan: broken-links
  Outcome: success
  Design docs updated: 0
  Plan file: Deleted
```

**Fix:** Create the design doc before completing, or fix the path in plan frontmatter.

## Workflow: Complete After Review

Typical completion workflow:

```bash
# 1. Validate plan is ready
/plan-validate plan-design-linking-phase-1

# 2. Sync design docs with implementation
/design-sync design-doc-system

# 3. Preview completion
/plan-complete plan-design-linking-phase-1 --dry-run

# 4. Complete for real
/plan-complete plan-design-linking-phase-1

# 5. Verify design docs updated
/design-review design-doc-system
```

## Integration with Git

Typical git workflow:

```bash
# Complete the plan (updates design docs, deletes plan)
/plan-complete my-feature

# Review changes
git status
git diff .claude/design/

# Commit completion
git add .claude/design/
git commit -m "feat: complete my-feature plan

- Update design docs to current status
- Record completion metadata
- Remove transitory plan file"
```
