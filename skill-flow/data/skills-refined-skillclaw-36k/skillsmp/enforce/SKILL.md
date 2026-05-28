---
name: enforce
description: Validate atomic specs meet atomicity criteria
allowed-tools: Read, Glob, Task
user-invocable: true
---

# /enforce Skill

## Purpose

Validate that atomic specs are at the right level of granularity—not too coarse (needs splitting) and not too granular (needs merging). Also verifies complete requirements coverage.

## Usage

```
/enforce                      # Validate current spec group
/enforce <spec-group-id>      # Validate specific spec group
/enforce --strict             # Treat warnings as failures
```

## Prerequisites

Before running `/enforce`:
1. Spec group must exist with `manifest.json`
2. `requirements.md` must exist
3. `atomic/` directory must contain atomic specs (from `/atomize`)

## Process

1. **Locate spec group**
   - If no ID provided, look for active spec group
   - Validate required files exist

2. **Dispatch atomicity-enforcer agent**
   ```
   Task: atomicity-enforcer
   Prompt: Validate atomic specs in <spec-group-path>
   Mode: standard | strict
   ```

3. **Generate enforcement report**
   - Agent creates `enforcement-report.md` in spec group
   - Updates `manifest.json` with enforcement status

4. **Report to user**
   - Overall status (PASSING, WARNINGS, FAILING)
   - Summary of issues
   - Next steps

## Validation Criteria

### TOO_COARSE (needs splitting)
- Contains multiple distinct behaviors
- Would require multiple test suites
- Cannot partially roll back
- Reviewer needs sibling context

### TOO_GRANULAR (needs merging)
- Cannot test in isolation
- Cannot deploy meaningfully alone
- Describes code fragment, not behavior
- No standalone user value

### JUST_RIGHT (passing)
- Single testable behavior
- Deployable as standalone PR
- Reviewable without siblings
- Reversible without breaking others

### Coverage
- Every REQ-XXX must appear in at least one atomic spec

## Output

### PASSING

```
Enforcement passed for sg-logout-feature ✓

All 5 atomic specs meet atomicity criteria
Requirements coverage: 100% (4/4)

Spec group ready for user review.
Run /approve or review atomic specs in:
  .claude/specs/groups/sg-logout-feature/atomic/
```

### WARNINGS

```
Enforcement completed with warnings for sg-logout-feature

Status: WARNINGS (2 issues)

Passing: 4/5 atomic specs
Warnings:
  - as-003: Atomicity justification could be stronger

Requirements coverage: 100%

Options:
  1. Proceed to implementation (warnings are advisory)
  2. Run /atomize --refine to address warnings
  3. Run /enforce --strict to enforce stricter standards
```

### FAILING

```
Enforcement failed for sg-logout-feature ✗

Status: FAILING (3 issues)

Issues:
  - as-002: TOO_COARSE — Contains logout AND session cleanup
    → Recommend: Split into as-002a (logout), as-002b (cleanup)

  - as-005: TOO_GRANULAR — Cannot test without as-004
    → Recommend: Merge with as-004

  - MISSING_COVERAGE: REQ-003 not covered by any atomic spec
    → Recommend: Create new spec or expand existing

Next step: Run /atomize --refine to address issues
```

## Strict Mode

With `--strict`:
- All WARNINGS become FAILING
- Used before implementation to ensure maximum atomicity discipline
- Recommended for complex or high-risk features

## Integration with /atomize

The `/atomize --auto-enforce` flag creates a loop:

```
/atomize
    ↓
/enforce (automatic)
    ↓
If FAILING → /atomize --refine → /enforce
    ↓
Repeat until PASSING or max iterations
```

## State Transitions

After `/enforce`:

**If PASSING:**
- `manifest.json`:
  - `atomic_specs.enforcement_status`: "passing"
  - `atomic_specs.last_enforced`: <timestamp>
- Spec group ready for `review_state` → APPROVED

**If WARNINGS:**
- `manifest.json`:
  - `atomic_specs.enforcement_status`: "warnings"
- User decides whether to proceed or refine

**If FAILING:**
- `manifest.json`:
  - `atomic_specs.enforcement_status`: "failing"
- Must run `/atomize --refine` before implementation

## Edge Cases

### No Atomic Specs
```
Error: No atomic specs found in spec group
Run /atomize first to decompose spec.md
```

### Requirements Changed
```
Warning: requirements.md modified since last atomization
Coverage check may be inaccurate
Consider re-running /atomize
```

### Circular Dependencies Detected
```
Error: Circular dependency detected
  as-002 depends on as-003
  as-003 depends on as-002

This indicates specs are not truly atomic.
Run /atomize --refine to restructure.
```
