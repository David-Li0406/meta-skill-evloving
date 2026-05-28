# Phase 8: Implementation Workflow

## Purpose

Execute TDD implementation following tasks.md, story by story. Creates code, tests, and verification reports.

**Command**: `/implement plan.md` or `/implement`
**Requires**: `audit-report.md` with PASS status
**Output**: Code, tests, `verification-report-{story}.md` per story
**Updates**: `tasks.md` (mark complete), `memory/` (auto-sync)

---

## Prerequisites

```bash
# Verify audit passed
if ! grep -q "Result: \*\*PASS\*\*" specs/$FEATURE/audit-report.md; then
  echo "ERROR: Audit did not pass. Run /audit and fix issues."
  exit 1
fi
```

---

## Step 1: Load Implementation Context

**Read required artifacts:**

```bash
# Load task list
cat specs/$FEATURE/tasks.md

# Load plan for architecture context
cat specs/$FEATURE/plan.md

# Load research if exists
cat specs/$FEATURE/research.md 2>/dev/null
```

**Extract:**
- Task dependency order
- Parallelization opportunities
- AC checklist per task

---

## Step 2: Story-by-Story TDD Loop

**For each user story in P1 → P2 → P3 order:**

### 2.1 Select Story

```markdown
## Implementing US-X: [Story Title]

**Priority**: P1/P2/P3
**Tasks**: TX.1, TX.2, TX.3, ...
**ACs**: AC-X.1, AC-X.2, AC-X.3
```

### 2.2 Write Tests First (Red Phase)

**Before any implementation:**

```python
# tests/test_$feature.py

import pytest
from nikita.$module import $Class

class Test$Feature:
    """Tests for US-X: [Story Title]"""

    def test_ac_x_1_criterion_description(self):
        """AC-X.1: [Criterion text]"""
        # Arrange
        # Act
        # Assert
        assert result == expected

    def test_ac_x_2_criterion_description(self):
        """AC-X.2: [Criterion text]"""
        pass  # Will fail initially
```

**Run tests to verify they fail:**

```bash
pytest tests/test_$feature.py -v
# Expected: FAILED (tests exist but implementation missing)
```

### 2.3 Implement Minimum Code (Green Phase)

**Implement just enough to pass tests:**

```python
# nikita/$module/$file.py

class $Class:
    """Implementation for US-X"""

    def method(self) -> Result:
        # Minimum implementation to pass tests
        pass
```

**Run tests again:**

```bash
pytest tests/test_$feature.py -v
# Expected: PASSED
```

### 2.4 Refactor (Blue Phase)

**Improve code quality without changing behavior:**

- Remove duplication
- Improve naming
- Extract helper methods
- Add type hints

**Verify tests still pass:**

```bash
pytest tests/test_$feature.py -v
```

---

## Step 3: Task Completion Updates

**After each task completes, IMMEDIATELY update tasks.md:**

```markdown
### TX.Y: Task Name
- **Status**: [x] Complete  ← UPDATE THIS
- **Completed**: 2025-12-30  ← ADD DATE
- **ACs**:
  - [x] AC-TX.Y.1: First criterion  ← CHECK ALL
  - [x] AC-TX.Y.2: Second criterion
```

**Also update Progress Summary:**

```markdown
| Phase/User Story | Tasks | Completed | Status |
|------------------|-------|-----------|--------|
| US-1: [Title] | 5 | 3 | In Progress |
```

---

## Step 4: Story Verification

**After all tasks in a story complete:**

### 4.1 Run All Story Tests

```bash
pytest tests/test_$feature.py -v --tb=short
```

### 4.2 Create Verification Report

```markdown
# Verification Report: US-X

**Story**: US-X: [Story Title]
**Verified**: [timestamp]
**Result**: **PASS** / **FAIL**

---

## Test Results

| Test | AC | Status | Notes |
|------|-----|--------|-------|
| test_ac_x_1 | AC-X.1 | ✅ PASS | |
| test_ac_x_2 | AC-X.2 | ✅ PASS | |
| test_ac_x_3 | AC-X.3 | ✅ PASS | |

**Coverage**: X%

---

## AC Verification

| AC | Tested | Implemented | Verified |
|----|--------|-------------|----------|
| AC-X.1 | ✅ | ✅ | ✅ |
| AC-X.2 | ✅ | ✅ | ✅ |
| AC-X.3 | ✅ | ✅ | ✅ |

---

## Files Changed

| File | Lines | Changes |
|------|-------|---------|
| nikita/$module/$file.py | +50 | New service |
| tests/test_$feature.py | +80 | New tests |

---

## Next Story

**Proceed to**: US-Y
```

---

## Step 5: Parallel Task Execution

**For tasks marked [P] in tasks.md:**

```markdown
| ID | Task | Deps | [P] |
|----|------|------|-----|
| T1.1 | Model A | - | |
| T1.2 | Model B | - | [P] T1.1 |
```

**Execute in parallel:**

1. Start both T1.1 and T1.2 simultaneously
2. Write tests for both
3. Implement both
4. Verify both independently
5. Mark both complete

---

## Step 6: Memory Auto-Sync

**After significant implementation milestones:**

```bash
# Update memory files if architecture/patterns changed
# This is automatic based on what was implemented

# Examples:
# - New API endpoint → update memory/backend.md
# - New data model → update memory/architecture.md
# - New integration → update memory/integrations.md
```

---

## Step 7: Feature Completion

**After all stories complete:**

### 7.1 Final Test Run

```bash
# Run all feature tests
pytest tests/ -k "$feature" -v

# Run related integration tests
pytest tests/integration/ -k "$feature" -v
```

### 7.2 Update Master Todo

```markdown
### Spec $NUMBER: [Feature Name]
- Status: ✅ Complete
- Spec: [specs/$FEATURE/spec.md](specs/$FEATURE/spec.md)
- Plan: [specs/$FEATURE/plan.md](specs/$FEATURE/plan.md)
- Tasks: [specs/$FEATURE/tasks.md](specs/$FEATURE/tasks.md)
- Progress: X/X tasks (100%)
```

### 7.3 Final Verification Report

```markdown
# Final Verification: $FEATURE

**Completed**: [timestamp]
**Result**: **PASS**

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | X |
| Completed | X |
| Test Coverage | Y% |
| User Stories | Z |

---

## Deliverables

### Code
- [ ] All implementation files created
- [ ] All tests passing
- [ ] Code reviewed (if applicable)

### Documentation
- [ ] tasks.md fully updated
- [ ] Verification reports created
- [ ] Memory files synced

### Deployment
- [ ] Ready for deployment
- [ ] No known issues
```

---

## Quality Gates

| Gate | Requirement | Enforcement |
|------|-------------|-------------|
| TDD | Tests before code | Fail if tests added after |
| AC Coverage | All ACs tested | Check test docstrings |
| Task Updates | Immediate completion marking | Verify timestamps |
| Test Pass | All tests green | CI/CD blocks on failure |
| Story Verification | Report per story | File exists check |

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Code before tests | Not TDD | Enforce red-green-refactor |
| Batch task updates | Lost progress | Update after each task |
| Skipping refactor | Tech debt | Schedule refactor phase |
| Missing verification | Unknown state | Require reports |

---

## Commit Strategy

**Commit per task or logical unit:**

```bash
# Format: type(scope): description
git commit -m "feat($feature): implement TX.Y - task description"
```

**Example sequence:**
```bash
git commit -m "test($feature): add tests for US-1 ACs"
git commit -m "feat($feature): implement T1.1 - create data model"
git commit -m "feat($feature): implement T1.2 - create repository"
git commit -m "refactor($feature): extract common logic to utils"
```

---

## Rollback Procedure

**If implementation fails:**

1. Identify failing task
2. Revert to last known good state
3. Update tasks.md to reflect actual status
4. Re-attempt with different approach
5. Document in verification report

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
