---
name: writing-plan
description: Performs gap analysis between specs and code to generate IMPLEMENTATION_PLAN.md. Use when creating, updating, or regenerating the implementation plan.
---

# Writing Implementation Plans

This document defines how to perform gap analysis between specs and implementation, producing tasks in `IMPLEMENTATION_PLAN.md`.

## Overview

Gap analysis compares what specs define (SSOT) against what code implements. The output is a task pool that agents use to close gaps incrementally.

```
specs/*.md (what should exist)
        ↓
   Gap Analysis
        ↓
src/* (what exists)
        ↓
IMPLEMENTATION_PLAN.md (tasks to close gaps)
```

## Prerequisites

Before running gap analysis, verify:

1. **Verification script exists**: `./scripts/verify.sh` must exist and be executable
2. **Script passes**: Run `./scripts/verify.sh` to confirm the project is in a valid state

If the verification script is missing:

```
⚠️ Verification script not found.

Before creating an implementation plan, create ./scripts/verify.sh
See docs/writing-verify-script.md for instructions.
```

Do not proceed with gap analysis until the verification script exists and passes.

## When to Run Gap Analysis

| Trigger | Action |
|---------|--------|
| Initial setup | Generate fresh `IMPLEMENTATION_PLAN.md` |
| Spec changes | Regenerate to capture new requirements |
| Major refactor | Regenerate to reassess implementation state |
| Agent request | Regenerate when asked to "refresh the plan" |

## Regeneration Rules

Regeneration **completely rewrites** `IMPLEMENTATION_PLAN.md`:

1. Discard the existing plan entirely (git history preserves it)
2. Re-analyze all specs against current code
3. Generate fresh tasks for all identified gaps
4. Previously completed work shows as "no gap" and produces no task

Do **not** attempt to preserve completion state or merge with the old plan. Each regeneration is a clean slate based on current reality.

**Note:** `Completed: true` is meaningful only within the current plan snapshot. Tests and `verify.sh` passing are the durable evidence of completion, not the flag itself.

## Gap Analysis Process

### Step 1: Load Context

Read the following to understand the project:

1. `specs/README.md` - Spec index and architecture mapping
2. All files in `specs/*.md` - The source of truth
3. `src/` directory structure - Current implementation layout

### Step 2: For Each Spec, Identify Gaps

For each spec file, compare its requirements against the implementation:

| Spec Section | Check Against |
|--------------|---------------|
| One-Sentence Description | Does the module exist and fulfill this purpose? |
| Public API / Commands | Are all functions/commands implemented? |
| Data Structures | Do types match spec definitions? |
| Process / Algorithm | Does code follow the documented steps? |
| Acceptance Criteria | Are outcomes implemented? Do tests exist? |
| Error Handling | Are all error cases handled as specified? |
| Dependencies | Are listed dependencies actually used? |
| Used By | Do the listed consumers actually call this code? |

#### How to Check Code (Deterministic Procedure)

For each spec, follow these steps:

1. **Identify expected entry points** from the spec:
   - File paths mentioned in Overview
   - Function/struct names in Public API
   - Consumers listed in "Used By"

2. **Search for symbols** in the codebase:
   - Grep for public API function names
   - Locate struct/type definitions
   - Find CLI command wiring (if applicable)

3. **Validate behavior** against spec:
   - Compare algorithm steps to actual code flow
   - Check error handling matches spec's error table
   - Verify dependencies are imported and used

4. **Cross-check "Used By"** section:
   - If spec says `commands::list` uses this, confirm that call exists
   - If code uses something spec doesn't mention, that's a spec gap (note it)

### Step 3: Classify Gap Type

| Gap Type | Description | Example |
|----------|-------------|---------|
| **Missing** | Feature/function doesn't exist | `execute_list` not implemented |
| **Incomplete** | Partial implementation | List command exists but no filters |
| **Mismatch** | Behavior differs from spec | Spec says retry 3x, code retries 5x |
| **Stale** | Code exists but spec removed | Dead code from old feature |

#### Handling Stale Code

When code exists but no spec defines it:

1. Check `specs/README.md` to confirm no spec covers this code
2. **Do not create a task** - there is no spec with AC to copy from
3. Add it to the **Spec Issues** section for resolution

Example:
```markdown
## Spec Issues

- **Unspecified code exists**: `src/core/skill_cache.rs` - no spec covers this module. Needs decision: document in a spec or remove.
```

A task can only be created after a spec exists with complete Acceptance Criteria (whether that spec documents the code or specifies its removal).

### Step 4: Create Tasks

For each gap, create a task entry. One gap = one task. Keep tasks atomic.

**Task sizing guidance:**
- Too big: "Implement list command" (has filters, output, CLI wiring)
- Right size: "Implement list filtering by agent"
- Too small: "Add --agent flag to Args struct"

A gap should be **one user-visible behavior or one contract item** from the spec. If closing the gap requires multiple layers (API + CLI + tests), keep one task if it's the smallest end-to-end slice.

#### Cross-Cutting and Multi-Spec Gaps

When a gap spans multiple specs:

- Each task has **one primary spec** (the `Spec:` field)
- List related specs in `Notes:` if helpful
- Prefer creating **separate tasks per spec** unless inseparable in implementation

Example:
```markdown
### Add JSON output to list command
- **Spec:** cli-output.md
- **Gap:** --json flag defined but not implemented for list
- **Completed:** false
- **Notes:** Related: skill-discovery.md (defines list behavior)
```

## IMPLEMENTATION_PLAN.md Structure

```markdown
# Implementation Plan

## General Verification

`./scripts/verify.sh`

## Spec Issues

[List specs with missing or incomplete Acceptance Criteria - these block task creation]

- **skill-scanner.md**: Missing AC section - behavior described in algorithm but no testable criteria
- **cache.md**: AC incomplete - invalidation behavior not specified

## Tasks

### [Short descriptive title]
- **Spec:** [spec-filename.md]
- **Gap:** [What the spec defines that code doesn't have]
- **Completed:** false
- **Acceptance Criteria:**
  - [Observable outcome 1]
  - [Observable outcome 2]
- **Tests:** [Optional initially, required when complete: test file(s) and test name(s)]
- **Location:** [Optional: primary file path, e.g., src/core/scanner.rs]
- **Notes:** [Optional: context, discoveries, blockers]
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| Title | Yes | Brief action-oriented description |
| Spec | Yes | Link to source spec (filename only) |
| Gap | Yes | Specific gap being addressed |
| Completed | Yes | `true` or `false` |
| Acceptance Criteria | Yes | Copied verbatim from spec's Acceptance Criteria section |
| Tests | On completion | Test file(s) and name(s) covering the acceptance criteria |
| Location | No | Primary file to modify (helps agents jump to code) |
| Notes | No | Context added during implementation |

### Acceptance Criteria Guidelines

Acceptance criteria define **what success looks like**, not how to build it:

- ✓ "Second scan of unchanged directory uses cached results" (outcome)
- ✓ "`sikil list --agent claude` shows only Claude skills" (observable)
- ✓ "Exit code is 3 when skill not found" (verifiable)
- ✗ "Add cache field to Scanner struct" (implementation detail)
- ✗ "Use HashMap for storage" (implementation detail)

**Copy criteria verbatim** from the spec's Acceptance Criteria section as a **verbatim subset** - the exact bullets this task is responsible for. Do not reword, merge, split, or create new bullets.

If the spec's Acceptance Criteria section is missing or incomplete:
1. **Do not create a task** for that gap
2. **Report it** as a spec quality issue in the plan (see Spec Issues section)
3. Spec must be fixed before tasks can be created for that area

**Do not invent new criteria in tasks.** Specs are the source of truth. Missing AC indicates a stale or incomplete spec that needs maintenance.

### Task Title Guidelines

Use action verbs:
- ✓ "Integrate cache with scanner"
- ✓ "Add --json flag to list command"
- ✓ "Handle broken symlink errors"
- ✗ "Cache integration" (noun phrase)
- ✗ "List command improvements" (vague)

## Example Gap Analysis

**Spec excerpt (skill-scanner.md):**
```markdown
## Dependencies

| Dependency | Purpose |
|------------|---------|
| `SqliteCache` | Optional caching layer for scan results |
```

**Code check:**
```rust
// src/core/scanner.rs
pub struct Scanner {
    config: Config,
    // No cache field
}
```

**Gap identified:** SqliteCache listed as dependency but not used in Scanner.

**Task created:**
```markdown
### Integrate cache with scanner
- **Spec:** skill-scanner.md
- **Gap:** SqliteCache dependency not integrated in scan flow
- **Completed:** false
- **Acceptance Criteria:**
  - Second scan of unchanged directory returns cached metadata
  - Modified SKILL.md invalidates cache for that skill
  - `--no-cache` flag bypasses cache entirely
- **Tests:**
- **Location:** src/core/scanner.rs
- **Notes:**
```

### Example: Mismatch Gap

**Spec excerpt (error-handling.md):**
```markdown
## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Invalid arguments |
| 3 | Skill not found |
```

**Code check:**
```rust
// src/cli/mod.rs
Err(_) => std::process::exit(1)  // Always exits 1 on error
```

**Gap identified:** Exit codes don't match spec (code uses 1, spec defines 2/3).

**Task created:**
```markdown
### Fix exit codes to match spec
- **Spec:** error-handling.md
- **Gap:** All errors exit with 1, spec defines distinct codes (2, 3)
- **Completed:** false
- **Acceptance Criteria:**
  - Invalid arguments exit with code 2
  - Skill not found exits with code 3
  - Success exits with code 0
- **Tests:**
- **Location:** src/cli/mod.rs
- **Notes:**
```

## Handling Discoveries

When implementing a task, you may discover behavior not specified in the spec:

1. **Do not add it to the task** - You cannot invent acceptance criteria
2. Add a note to the current task describing the discovery
3. Add the spec to the **Spec Issues** section with details
4. Complete the current task with only its original AC
5. The spec issue blocks further tasks for that specific spec until resolved

Example:
```markdown
## Spec Issues

- **cache.md**: Discovered during scanner work - invalidation behavior not specified

## Tasks

### Integrate cache with scanner
- **Spec:** skill-scanner.md
- **Gap:** SqliteCache dependency not integrated
- **Completed:** true
- **Tests:** tests/scanner_cache_test.rs::test_cache_integration
- **Notes:** Discovered cache invalidation not specified in cache.md. Added to Spec Issues.
```

## Resolving Spec Issues

Spec Issues block task creation for that specific spec. To unblock:

1. **Stop planning** for the affected spec
2. **Fix the spec** - Add missing AC, clarify ambiguous behavior, or document removal
3. **Re-run gap analysis** after spec is fixed
4. Previously blocked gaps now become valid tasks

Tasks for unrelated specs may proceed while a Spec Issue is open.

**Spec-fix workflow (one session):**

1. Pick one Spec Issue from `IMPLEMENTATION_PLAN.md`
2. Update the spec with missing AC or clarification
3. Commit spec changes
4. Exit

Then re-run gap analysis in a subsequent session.

**Do not:**
- Create tasks without AC (violates SSOT)
- Invent AC during planning (specs are source of truth)
- Skip Spec Issues and proceed with partial plan for that spec

Spec maintenance is valid work. If many Spec Issues exist, prioritize fixing specs before implementation.

## Task Ordering

Tasks are **not pre-prioritized**. The implementing agent picks based on:

1. **Dependencies** - Can't implement B if A doesn't exist
2. **Impact** - User-facing features may be more valuable
3. **Context** - Related tasks may be efficient to batch
4. **Judgment** - Agent decides what's most important now

## Implementation Agent Workflow

1. Read `IMPLEMENTATION_PLAN.md`
2. Pick one uncompleted task
3. Read the linked spec thoroughly
4. **Write tests first** for acceptance criteria (TDD)
5. Run tests - confirm they fail for the right reason (red), not due to compile errors
6. Implement until tests pass (green)
7. Refactor if needed
8. Run `./scripts/verify.sh`
9. Confirm Definition of Done (see below)
10. Update the task:
    - Set `Completed: true`
    - Populate Tests field with test file(s) and name(s)
    - Add Notes if relevant
11. Commit all changes (tests + code + plan update)
12. Exit

### Definition of Done

A task is complete when:

- [ ] Automated tests written for all automatable acceptance criteria
- [ ] Tests field populated with test file(s) and name(s)
- [ ] Manual criteria verified and noted (only if automation not possible, with justification)
- [ ] All tests pass
- [ ] Implementation matches spec behavior
- [ ] `./scripts/verify.sh` passes
- [ ] Task marked `Completed: true`

## Verification

### General Verification

The verification script (`./scripts/verify.sh`) runs all project quality checks. See [writing-verify-script.md](writing-verify-script.md) for setup instructions.

| Project Type | Typical Checks |
|--------------|----------------|
| Rust | `cargo test`, `cargo clippy`, `cargo fmt --check` |
| Node/TypeScript | `npm test`, `eslint`, `prettier --check`, `tsc --noEmit` |
| Go | `go test ./...`, `golangci-lint run`, `gofmt` |
| Python | `pytest`, `mypy`, `flake8`, `black --check` |

All tasks must pass `./scripts/verify.sh` before completion.

### Acceptance Criteria as Tests

Acceptance criteria drive test creation:

| Criterion Type | Test Approach |
|----------------|---------------|
| Behavioral outcome | Unit or integration test asserting the outcome |
| CLI output/exit code | CLI test framework (e.g., `assert_cmd`, subprocess assertions) |
| API response | HTTP client test with expected status/body |
| Performance | Benchmark test with threshold |
| Error condition | Test that triggers error and asserts handling |

Automate criteria whenever possible. Only resort to manual verification when automation is truly not feasible (e.g., visual appearance, hardware interaction). Note manual verification results in the task's Notes field.

## Checklist for Gap Analysis

Before finalizing `IMPLEMENTATION_PLAN.md`:

- [ ] All specs in `specs/` have been reviewed
- [ ] Specs with missing/incomplete AC are listed in Spec Issues section
- [ ] No tasks created for specs with AC issues
- [ ] Each task links to exactly one spec
- [ ] Task AC copied verbatim from spec AC section
- [ ] Gap descriptions are specific, not vague
- [ ] No duplicate tasks for same gap
- [ ] Task titles are action-oriented
- [ ] Completed field is set to `false` for new tasks
