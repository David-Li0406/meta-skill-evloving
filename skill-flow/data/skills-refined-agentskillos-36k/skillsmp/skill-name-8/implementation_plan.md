---
template: implementation_plan
status: draft
date: {{DATE}}
backlog_id: {{BACKLOG_ID}}
title: "{{TITLE}}"
author: Hephaestus
lifecycle_phase: plan
session: {{SESSION}}
version: "1.5"
generated: 2025-12-21
last_updated: 2025-12-22T12:41:28
---
# Implementation Plan: {{TITLE}}

@docs/README.md
@docs/epistemic_state.md

---

<!-- TEMPLATE GOVERNANCE (v1.4)

     SKIP RATIONALE REQUIREMENT:
     If ANY section below is omitted or marked N/A, you MUST provide rationale.

     Format for skipped sections:

     ## [Section Name]

     **SKIPPED:** [One-line rationale explaining why this section doesn't apply]

     Examples:
     - "SKIPPED: New feature, no existing code to show current state"
     - "SKIPPED: Pure documentation task, no code changes"
     - "SKIPPED: Trivial fix, single line change doesn't warrant detailed design"

     This prevents silent section deletion and ensures conscious decisions.
-->

---

## Pre-Implementation Checklist (RFC 2119)

| Requirement | Level | Action |
|-------------|-------|--------|
| Tests before code | MUST | Write failing tests in "Tests First" section before implementation |
| Query prior work | SHOULD | Search memory for similar implementations before designing |
| Document design decisions | MUST | Fill "Key Design Decisions" table with rationale |
| Ground truth metrics | MUST | Use real file counts from Glob/wc, not guesses |

---

## Goal

[One sentence: What capability will exist after this plan is complete?]

---

## Effort Estimation (Ground Truth)

> **MUST** be based on actual file/code analysis, not guesses.

### Scope Metrics

| Metric | Value | Source |
|--------|-------|--------|
| Files to modify | [N] | `Glob pattern` or explicit list |
| Lines of code affected | [~N] | `wc -l` on target files |
| New files to create | [N] | List them |
| Tests to write | [N] | Based on test strategy |
| Dependencies | [N] | Modules that import changed code |

### Complexity Factors

| Factor | Level | Notes |
|--------|-------|-------|
| Integration points | [Low/Med/High] | How many systems touched |
| Risk of regression | [Low/Med/High] | Existing test coverage |
| External dependencies | [Low/Med/High] | APIs, services, config |

### Effort Estimate

| Phase | Estimate | Confidence |
|-------|----------|------------|
| [Phase 1] | [X min/hr] | [High/Med/Low] |
| [Phase 2] | [X min/hr] | [High/Med/Low] |
| **Total** | [X min/hr] | |

---

## Current State vs Desired State

### Current State

```python
# [file:line] - Describe what exists now
def current_function():
    # Current implementation
```

**Behavior:** [What the system does now]

**Result:** [What outcome this produces - the problem]

### Desired State

```python
# [file:line] - Describe target implementation
def desired_function():
    # Target implementation
```

**Behavior:** [What the system should do]

**Result:** [What outcome this produces - the solution]

---

## Tests First (TDD)

<!-- Write tests BEFORE implementation. Each test should have:
     - Descriptive name
     - Setup (if needed)
     - Assertion that defines success -->

### Test 1: [Descriptive Name]
```python
def test_[descriptive_name]():
    # Setup
    # Action
    assert [expected outcome]
```

### Test 2: [Descriptive Name]
```python
def test_[descriptive_name]():
    assert [expected outcome]
```

### Test 3: Backward Compatibility
```python
def test_existing_behavior_unchanged():
    # Verify default behavior matches current behavior
    assert new_result == old_result
```

---

## Detailed Design

<!-- REQUIRED: Document HOW the implementation works, not just WHAT it does.
     Future agents should be able to implement from this section alone.
     This section bridges the gap between tests (WHAT) and steps (HOW).

     MUST INCLUDE (per Session 88 enhancement):
     1. Actual current code that will be changed (copy from source)
     2. Exact diff/change to be made
     3. Function signature details with context
     4. Input/output examples with REAL data from the system

     PATTERN VERIFICATION (E2-255 Learning):
     IF creating a new module that imports from siblings:
       - MUST read at least one sibling module for import/error patterns
       - Verify: try/except conditional imports? sys.path manipulation? error types?
       - Use the SAME patterns as existing siblings (consistency > preference)

     IF modifying existing module:
       - Follow existing patterns in that file

     IF creating module with no siblings (new directory):
       - Document chosen patterns in Key Design Decisions with rationale -->

### Exact Code Change

<!-- REQUIRED: Show the actual code, not pseudocode -->

**File:** `[path/to/file.py]`
**Location:** Lines X-Y in `function_name()`

**Current Code:**
```python
# [file:line-range] - Copy exact current implementation
        existing_code = """
            SELECT ...
        """
```

**Changed Code:**
```python
# [file:line-range] - Show exact target implementation
        modified_code = """
            SELECT ...
            WHERE new_condition   # <-- NEW
        """
```

**Diff:**
```diff
         existing_line
+        new_line_added
-        old_line_removed
```

### Call Chain Context

<!-- Show where this code fits in the larger system -->

```
caller_function()
    |
    +-> THIS_FUNCTION()     # <-- What we're changing
    |       Returns: [Type]
    |
    +-> downstream_function()
```

### Function/Component Signatures

```python
# Current signature (if changing) or target signature (if new)
def function_name(param: Type) -> ReturnType:
    """
    [One-line description]

    Args:
        param: [Description and constraints]

    Returns:
        [Description of return value]

    Raises:
        [Exceptions and when they occur]
    """
```

### Behavior Logic

<!-- Use flowchart showing CURRENT (buggy) vs FIXED behavior -->

**Current Flow (if buggy):**
```
Input → [Step causing problem] → Wrong Output
```

**Fixed Flow:**
```
Input → [Step 1] → [Decision Point?]
                      ├─ YES → [Path A] → Output
                      └─ NO  → [Path B] → Output
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Decision point] | [What was chosen] | [WHY this choice - this is the most important part] |

### Input/Output Examples

<!-- REQUIRED: Use REAL data from the system, not hypothetical examples -->

**Before Fix (with real data):**
```
Run 1: function(param=X)
  Returns: [actual current output from system]
  Problem: [why this is wrong]
```

**After Fix (expected):**
```
Run 1: function(param=X)
  Returns: [expected correct output]
  Improvement: [what's better]
```

**Real Example with Current Data:**
```
Current system state:
  - [Query database or read files to get actual numbers]
  - [Show real IDs, counts, or values]

After fix:
  - [Expected new behavior with same real data]
```

### Edge Cases

| Case | Handling | Test Coverage |
|------|----------|---------------|
| [Edge case] | [How it's handled] | Test N |

### Open Questions

<!-- Surface any uncertainties discovered during design -->

**Q: [Question about behavior or design]**

[Answer based on code analysis, or mark as "TBD - verify during implementation"]

---

## Open Decisions (MUST resolve before implementation)

<!-- Decisions from work item's operator_decisions field.
     If ANY row has [BLOCKED] in Chosen column, plan-validation-cycle will BLOCK.

     POPULATE FROM: Work item frontmatter `operator_decisions` field
     - question -> Decision column
     - options -> Options column
     - chosen -> Chosen column (null = [BLOCKED])
     - rationale -> Rationale column (filled when resolved) -->

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| [From work item operator_decisions] | [A, B] | [BLOCKED] | [Why this choice - filled when resolved] |

---

## Implementation Steps

<!-- Each step references which tests turn green -->

### Step 1: Write Failing Tests
- [ ] Add tests to appropriate test file
- [ ] Verify all tests fail (red)

### Step 2: [First Implementation Slice]
- [ ] [Specific code change]
- [ ] Tests [N, M] pass (green)

### Step 3: [Second Implementation Slice]
- [ ] [Specific code change]
- [ ] Tests [X, Y] pass (green)

### Step 4: Integration Verification
- [ ] All tests pass
- [ ] Run full test suite (no regressions)

### Step 5: README Sync (MUST)
- [ ] **MUST:** Update README.md in each directory with new/changed files
- [ ] **MUST:** Update parent directory READMEs if structure changed
- [ ] **MUST:** Verify README content matches actual file state

### Step 6: Consumer Verification (MUST for migrations/refactors)
<!-- When migrating, renaming, or moving code, ALL consumers must be updated -->
- [ ] **MUST:** Grep for references to migrated/renamed code
- [ ] **MUST:** Update all consumers (commands, skills, hooks, docs)
- [ ] **MUST:** Verify no stale references remain

**Consumer Discovery Pattern:**
```bash
# Find all references to the old path/name
Grep(pattern="old_path|OldName", path=".", glob="**/*.{md,py,json}")
```

> **Anti-pattern prevented:** "Ceremonial Completion" - code migrated but consumers still reference old location (see epistemic_state.md)

---

## Verification

- [ ] Tests pass
- [ ] **MUST:** All READMEs current (upstream and downstream of changes)
- [ ] Code review complete

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Medium/Low] | [Mitigation strategy] |

---

## Progress Tracker

<!-- ADR-033: Track session progress against this plan -->
<!-- Update this section when creating checkpoints that reference this plan -->

| Session | Date | Checkpoint | Status | Notes |
|---------|------|------------|--------|-------|
| - | - | - | - | No progress recorded yet |

---

## Ground Truth Verification (Before Closing)

> **MUST** read each file below and verify state before marking plan complete.
> This forces actual verification - not claims, but evidence.

### WORK.md Deliverables Check (MUST - Session 192)

**MUST** read `docs/work/active/{{BACKLOG_ID}}/WORK.md` and verify ALL deliverables:

| Deliverable | Complete | Evidence |
|-------------|----------|----------|
| [Copy each deliverable from WORK.md] | [ ] | [How you verified it] |

> **Anti-pattern prevented:** "Tests pass = Done" (E2-290). Tests verify code works. Deliverables verify scope is complete. Both required.

### File Verification

| File | Expected State | Verified | Notes |
|------|---------------|----------|-------|
| `[path/to/implementation.py]` | [Function X exists, does Y] | [ ] | |
| `[tests/test_file.py]` | [Tests exist and cover cases] | [ ] | |
| `[modified_dir/README.md]` | **MUST:** Reflects actual files present | [ ] | |
| `[parent_dir/README.md]` | **MUST:** Updated if structure changed | [ ] | |
| `Grep: old_path\|OldName` | **MUST:** Zero stale references (migrations only) | [ ] | |

**Verification Commands:**
```bash
# Paste actual output when verifying
pytest [test_file] -v
# Expected: X tests passed
```

**Binary Verification (Yes/No):**

| Question | Answer | Notes |
|----------|--------|-------|
| All listed files verified by reading? | [Yes/No] | |
| Test output pasted above? | [Yes/No] | |
| Any deviations from plan? | [Yes/No] | Explain: |

---

**Completion Criteria (DoD per ADR-033):**
- [ ] Tests pass
- [ ] **MUST:** All WORK.md deliverables verified complete (Session 192)
- [ ] **Runtime consumer exists** (code is called by system, not just tests)
- [ ] WHY captured (reasoning stored to memory)
- [ ] **MUST:** READMEs updated in all modified directories (upstream and downstream)
- [ ] **MUST:** Consumer verification complete (for migrations: zero stale references)
- [ ] All traced files complete
- [ ] Ground Truth Verification completed above

> **E2-250 Learning:** "Tests pass" proves code works. "Runtime consumer exists" proves code is used. Code without consumers is a prototype, not done.
> **E2-290 Learning (Session 192):** "Tests pass" ≠ "Deliverables complete". Agent declared victory after tests passed but skipped 2 of 7 deliverables.

---

## References

- [Related ADR or spec]
- [Related checkpoint]

---
