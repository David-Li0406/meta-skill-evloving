---
name: dqx-phase-commit
description: Complete one implementation phase with TDD, quality gates, and commit
compatibility: opencode
metadata:
  workflow: implementation
  audience: dqx-implement
---

## What I do

Execute a complete implementation phase by composing three core skills: TDD cycle, quality gates, and conventional commit. This is the end-to-end workflow for each phase in the implementation guide.

---

## Phase Workflow

This skill orchestrates the complete phase execution:

```text
Phase N begins
    ↓
1. TDD Cycle (dqx-tdd-cycle)
    ↓
2. Quality Gate (dqx-quality-gate)
    ↓
3. Commit (dqx-conventional-commit)
    ↓
4. Report Progress
    ↓
Phase N complete
```

---

## Step 1: Execute TDD Cycle

Load the TDD cycle skill:
```javascript
skill({ name: "dqx-tdd-cycle" })
```

**What it does**:
- Phase 1 RED: Write failing tests first
- Phase 2 GREEN: Implement minimal code
- Phase 3 REFACTOR: Check coverage (100%)

**Output**: Working code with passing tests

---

## Step 2: Run Quality Gate

Load the quality gate skill:
```javascript
skill({ name: "dqx-quality-gate" })
```

**What it does**:
- Gate 1: All tests pass
- Gate 2: Coverage 100%
- Gate 3: Pre-commit hooks pass (22 hooks)

**Output**: All quality checks passing

---

## Step 3: Create Commit

Load the conventional commit skill:
```javascript
skill({ name: "dqx-conventional-commit" })
```

**What it does**:
- Choose commit type (feat, fix, test, refactor, etc.)
- Add scope (module name)
- Write descriptive subject
- Format properly for commitizen validation

**Output**: Properly formatted commit

---

## Step 4: Report Progress

After successful commit, report:

```text
✓ Phase {N}/{total}: {phase_name}
  • Tests written: {count} tests
  • Implementation: complete
  • All tests: passing ✓
  • Coverage: 100% ✓
  • Pre-commit hooks: passing ✓
  • Committed: {commit_sha} - {commit_message}
```

---

## Complete Example

### Scenario: Implement Phase 2 - Cache Backend Protocol

#### Input from Implementation Guide
```markdown
Phase 2: Cache Backend Protocol
Goal: Define protocol for cache backends
Files to create:
- src/dqx/cache/backend.py
- tests/test_cache_backend.py
Tests to write:
- test_protocol_definition
- test_memory_backend_implementation
- test_backend_type_checking
```

#### Execution

**Step 1: TDD Cycle**
```javascript
skill({ name: "dqx-tdd-cycle" })
```

1. Write tests in `tests/test_cache_backend.py`:
```python
class TestCacheBackend:
    def test_protocol_definition(self) -> None:
        """Test cache backend protocol is defined correctly."""
        # Test code

    def test_memory_backend_implementation(self) -> None:
        """Test in-memory backend implements protocol."""
        # Test code

    def test_backend_type_checking(self) -> None:
        """Test runtime type checking with Protocol."""
        # Test code
```

2. Run tests → FAIL ✓

3. Implement in `src/dqx/cache/backend.py`:
```python
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class CacheBackend(Protocol):
    """Protocol for cache backend implementations."""

    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str) -> None: ...
    def delete(self, key: str) -> None: ...
```

4. Run tests → PASS ✓
5. Check coverage → 100% ✓

**Step 2: Quality Gate**
```javascript
skill({ name: "dqx-quality-gate" })
```

```bash
uv run pytest  # All passing ✓
uv run pytest --cov=src/dqx --cov-report=term-missing  # 100% ✓
uv run pre-commit run --all-files  # All hooks passing ✓
```

**Step 3: Commit**
```javascript
skill({ name: "dqx-conventional-commit" })
```

```bash
git add src/dqx/cache/backend.py tests/test_cache_backend.py
git commit -m "feat(cache): implement cache backend protocol

Define Protocol for cache backend implementations with
get/set/delete operations. Include in-memory reference
implementation for testing."
```

**Step 4: Report**
```text
✓ Phase 2/4: Cache Backend Protocol
  • Tests written: 3 tests
  • Implementation: complete
  • All tests: passing ✓
  • Coverage: 100% ✓
  • Pre-commit hooks: passing ✓
  • Committed: a1b2c3d - feat(cache): implement cache backend protocol
```

---

## When to use me

Use this skill when:
- **Implementing phases** from implementation guide
- **Need complete automation** of phase workflow
- **Want consistent execution** across all phases
- **Following dqx-implement** agent workflow

---

## Error Handling

### If TDD Cycle Fails

**Tests don't pass after implementation**:
```text
⚠️ Phase execution paused: Tests failing

Action: Review implementation, fix logic, re-run tests
Do NOT proceed to quality gate until tests pass
```

### If Quality Gate Fails

**Coverage < 100%**:
```text
⚠️ Phase execution paused: Coverage 95%

Action: Add tests for uncovered lines or use # pragma: no cover
Use: skill({ name: "dqx-coverage-fix" }) for guidance
Do NOT commit until coverage is 100%
```

**Pre-commit hooks fail**:
```text
⚠️ Phase execution paused: Mypy errors

Action: Fix type errors manually, re-run pre-commit
Do NOT commit until all hooks pass
```

### If Commit Fails

**Commitizen validation fails**:
```text
⚠️ Phase execution paused: Invalid commit message

Action: Check message format against conventional commits
Use: skill({ name: "dqx-conventional-commit" }) for guidance
```

---

## Advantages of This Composite Skill

**Consistency**:
- Every phase follows identical workflow
- No steps skipped or forgotten
- Predictable, reliable process

**Quality**:
- All quality gates enforced
- 100% coverage guaranteed
- Proper commit format ensured

**Efficiency**:
- Clear sequence of steps
- Automated verification
- Fast iteration cycle

**Traceability**:
- Each phase = one commit
- Clear commit history
- Easy to review changes

---

## Integration with Implementation Guide

The implementation guide specifies phases:

```markdown
### Phase 1: Core Data Structures
**Goal**: Implement basic cache classes
**Files to create**: src/dqx/cache/core.py, tests/test_cache_core.py
**Tests to write**: [list]
**Commit message**: feat(cache): add core cache data structures
```

**Use this skill for EACH phase**:
```text
Load implementation guide → Read Phase 1
↓
skill({ name: "dqx-phase-commit" })
↓
Execute Phase 1 → Report completion
↓
Load implementation guide → Read Phase 2
↓
skill({ name: "dqx-phase-commit" })
↓
...
```

---

## Success Criteria

A phase is complete when:
- ✅ All phase-specific tests written
- ✅ All phase-specific tests passing
- ✅ Coverage 100% for new/modified code
- ✅ All pre-commit hooks passing
- ✅ Full test suite passing (no regressions)
- ✅ Code committed with conventional commit message
- ✅ Progress reported to user

**All 7 criteria must be met before moving to next phase.**

---

## When NOT to use me

**Don't use this skill when**:
- Fixing bugs (not a planned phase)
- Addressing review feedback (use dqx-feedback workflow)
- Making quick changes (overkill for small edits)
- Not following implementation guide

**Use this ONLY for structured phase-by-phase implementation.**

---

## Reference

This skill composes:
- **dqx-tdd-cycle**: Complete TDD workflow
- **dqx-quality-gate**: All quality checks
- **dqx-conventional-commit**: Proper commit format

See: **dqx-implement.md** for complete agent workflow
