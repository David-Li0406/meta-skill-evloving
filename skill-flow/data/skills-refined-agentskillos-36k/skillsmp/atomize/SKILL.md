---
name: atomize
description: Decompose high-level specs into atomic specs
allowed-tools: Read, Glob, Task
user-invocable: true
---

# /atomize Skill

## Purpose

Decompose a high-level spec (`spec.md`) into atomic specs—units that are independently testable, deployable, reviewable, and reversible.

## Usage

```
/atomize                      # Decompose current spec group
/atomize <spec-group-id>      # Decompose specific spec group
/atomize --refine             # Re-run with enforcer feedback
/atomize --auto-enforce       # Decompose + iterate until /enforce passes
```

## Prerequisites

Before running `/atomize`:
1. Spec group must exist with `manifest.json`
2. `requirements.md` must exist (from `/prd sync` or `/pm`)
3. `spec.md` must exist (from `/spec`)

## Process

### Standard Mode

1. **Locate spec group**
   - If no ID provided, look for active spec group in `.claude/specs/groups/`
   - Validate `manifest.json`, `requirements.md`, `spec.md` exist

2. **Dispatch atomizer agent**
   ```
   Task: atomizer
   Prompt: Decompose spec.md into atomic specs
   Input: <spec-group-path>
   ```

3. **Review output**
   - Atomizer creates `atomic/as-XXX-*.md` files
   - Updates `manifest.json` with counts and coverage

4. **Report to user**
   - Number of atomic specs created
   - Requirements coverage percentage
   - Suggest running `/enforce` to validate

### Refine Mode (`--refine`)

1. **Read enforcement report**
   - Look for `enforcement-report.md` in spec group
   - Extract TOO_COARSE, TOO_GRANULAR, MISSING_COVERAGE items

2. **Dispatch atomizer with feedback**
   ```
   Task: atomizer
   Prompt: Refine atomic specs based on enforcement feedback
   Input: <spec-group-path>, <enforcement-report>
   ```

3. **Report changes**
   - Which specs were split
   - Which specs were merged
   - New coverage percentage

### Auto-Enforce Mode (`--auto-enforce`)

1. Run standard decomposition
2. Automatically run `/enforce`
3. If FAILING:
   - Run `--refine` with feedback
   - Re-run `/enforce`
   - Repeat until PASSING or max iterations (3)
4. Report final status

## Output

### On Success

```
Atomization complete for sg-logout-feature

Created 5 atomic specs:
  - as-001-logout-button-ui
  - as-002-auth-token-clear
  - as-003-session-invalidation
  - as-004-redirect-to-login
  - as-005-error-handling

Requirements coverage: 100% (4/4 requirements)

Next step: Run /enforce to validate atomicity criteria
```

### On Failure

```
Atomization failed for sg-logout-feature

Error: requirements.md not found
Run /pm or /prd sync first to generate requirements
```

## Integration with Workflow

```
/pm or /prd sync
    ↓
requirements.md created
    ↓
/spec
    ↓
spec.md created
    ↓
/atomize          ← YOU ARE HERE
    ↓
atomic/ specs created
    ↓
/enforce
    ↓
(if failing) /atomize --refine
    ↓
User reviews summary → APPROVED
    ↓
/implement + /test
```

## Edge Cases

### No Active Spec Group
```
Error: No active spec group found
Create one with /prd sync <doc-id> or /pm
```

### Already Has Atomic Specs
```
Warning: Spec group already has 3 atomic specs
Options:
  1. /atomize --refine (preserve and refine)
  2. /atomize --fresh (delete and recreate)
```

### Requirements Changed After Atomization
```
Warning: requirements.md modified after last atomization
Re-run /atomize to ensure coverage
```

## State Transitions

After successful `/atomize`:
- `manifest.json` updated:
  - `atomic_specs.count`: N
  - `atomic_specs.coverage`: "X%"
  - `atomic_specs.enforcement_status`: "not_run"
- Decision log entry added
- Spec group remains in current `review_state` (still needs `/enforce` + user approval)
