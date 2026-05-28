---
name: dqx-quality-gate
description: Run all DQX quality checks (tests, coverage, pre-commit hooks)
compatibility: opencode
metadata:
  workflow: pre-commit
  audience: all-agents
---

## What I do

Run the complete DQX quality gate sequence before committing code. All three gates must pass for code to be commit-ready.

---

## Quality Gate Sequence

Execute these checks **in order**:

### Gate 1: All Tests Pass

```bash
uv run pytest
```

**What it checks**:
- All test files in `tests/` directory
- Unit tests, integration tests, e2e tests
- No test failures or errors

**Success criteria**: All tests passing (exit code 0)

**If fails**:
```bash
# Run with verbose output to see failures
uv run pytest -v

# Run specific failing test
uv run pytest tests/test_module.py::test_function -vv

# Run with print statements visible
uv run pytest tests/test_module.py -s
```

---

### Gate 2: 100% Coverage

```bash
uv run pytest --cov=src/dqx --cov-report=term-missing
```

**What it checks**:
- Test coverage for all code in `src/dqx/`
- Reports which lines are not covered
- DQX requires 100% coverage - NO EXCEPTIONS

**Success criteria**: Coverage = 100%

**If coverage < 100%**:

Option 1 - Add tests (preferred):
```python
# Write tests for uncovered lines
def test_edge_case() -> None:
    """Test the uncovered edge case."""
    result = my_function(edge_case_input)
    assert result == expected
```

Option 2 - Use `# pragma: no cover` (only for unreachable code):
```python
def method(self):
    if self._value is None:  # pragma: no cover
        # Defensive: constructor ensures _value is never None
        raise RuntimeError("Unexpected None")
```

**When to use `# pragma: no cover`**:
- Defensive code that should never execute
- Abstract methods that must be overridden
- Trivial `__repr__` or `__str__` methods

---

### Gate 3: Pre-commit Hooks Pass

```bash
uv run pre-commit run --all-files
```

**What it checks** (22 hooks):
- ✓ Python syntax
- ✓ Private key detection
- ✓ Merge conflicts
- ✓ Debug statements
- ✓ Trailing whitespace
- ✓ End of files
- ✓ Case conflicts
- ✓ Mixed line endings
- ✓ UTF-8 BOM
- ✓ YAML/TOML/JSON validation
- ✓ Large files
- ✓ Docstring placement
- ✓ Shell scripts (shellcheck, shfmt)
- ✓ Docs formatting (blacken-docs)
- ✓ YAML linting (yamllint)
- ✓ **ruff format** (auto-fixes)
- ✓ **ruff check** (auto-fixes)
- ✓ **mypy** (type check - must fix manually)
- ✓ **commitizen** (commit message format)

**Success criteria**: All hooks pass

**If hooks fail**, run in sequence:

1. **Format first**:
```bash
uv run ruff format .
```

2. **Lint second**:
```bash
uv run ruff check --fix .
```

3. **Type check third** (fix manually):
```bash
uv run mypy src tests
```

4. **Re-run pre-commit**:
```bash
uv run pre-commit run --all-files
```

---

## When to use me

Run this skill before:
- **Committing code** (dqx-implement after each phase)
- **Creating PR** (dqx-pr before pushing)
- **Pushing fixes** (dqx-feedback after addressing feedback)
- **Final verification** (any code changes)

---

## Success Output

When all gates pass:
```text
✓ Gate 1: All tests passing (pytest)
✓ Gate 2: Coverage 100%
✓ Gate 3: Pre-commit hooks passing (22/22)

✓ Ready to commit
```

---

## Failure Handling

### Tests fail
```text
⚠️ Gate 1: Tests failing

Failed tests:
- tests/test_api.py::test_validation - AssertionError
- tests/test_parser.py::test_edge_case - KeyError

Action: Fix failing tests, then re-run quality gate
```

### Coverage < 100%
```text
⚠️ Gate 2: Coverage 95% (need 100%)

Uncovered lines:
- src/dqx/analyzer.py: lines 45-47, 89
- src/dqx/validator.py: line 123

Action: Add tests or use # pragma: no cover with justification
```

### Pre-commit fails
```text
⚠️ Gate 3: Pre-commit hooks failing

Failed hooks:
- ruff format: 3 files reformatted
- mypy: 2 type errors in src/dqx/api.py

Action: Run 'uv run ruff format .' then fix mypy errors manually
```

---

## Reference

Complete details: **AGENTS.md §quality-gates**

See also:
- Testing: AGENTS.md §testing-standards
- Coverage: AGENTS.md §coverage-requirements (100%)
- Pre-commit: AGENTS.md §pre-commit-requirements
