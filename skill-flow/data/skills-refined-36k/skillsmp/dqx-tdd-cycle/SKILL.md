---
name: dqx-tdd-cycle
description: Execute one complete TDD cycle (tests first, then implementation)
compatibility: opencode
metadata:
  workflow: implementation
  audience: dqx-implement
---

## What I do

Guide you through one complete Test-Driven Development (TDD) cycle for a specific module or feature. This is the core development pattern for all DQX implementation work.

---

## TDD Overview

**Red → Green → Refactor**

1. **RED**: Write failing tests first
2. **GREEN**: Implement minimal code to pass tests
3. **REFACTOR**: Check coverage and clean up

---

## Phase 1: RED - Write Failing Tests

### Step 1: Create/Update Test File

**File naming convention**:
- Source: `src/dqx/module.py`
- Tests: `tests/test_module.py`

**Test organization**:
```python
from __future__ import annotations

import pytest

from dqx.module import FeatureName


class TestFeatureName:
    """Tests for FeatureName functionality."""

    def test_creation_with_valid_input(self) -> None:
        """Test creating instance with valid input."""
        feature = FeatureName(arg="valid")
        assert feature.arg == "valid"

    def test_creation_with_invalid_input(self) -> None:
        """Test error handling for invalid input."""
        with pytest.raises(ValueError, match="Invalid arg"):
            FeatureName(arg=None)

    def test_key_operation_success(self) -> None:
        """Test main operation with valid data."""
        feature = FeatureName(arg="valid")
        result = feature.process()
        assert result == expected_value

    def test_key_operation_edge_case(self) -> None:
        """Test operation with edge case input."""
        feature = FeatureName(arg="")
        result = feature.process()
        assert result == default_value
```

### Step 2: Write ALL Test Functions

Include tests for:
- ✅ **Happy path**: Normal, expected usage
- ✅ **Error cases**: Invalid input, exceptions
- ✅ **Edge cases**: Empty, None, boundaries
- ✅ **Integration**: How it works with other components (if applicable)

**Test naming convention**:
- `test_<what>_<scenario>` (e.g., `test_validation_with_empty_string`)
- Be descriptive and specific
- One test per scenario

### Step 3: Verify Tests FAIL

**CRITICAL**: Tests must fail before implementation!

```bash
uv run pytest tests/test_module.py -v
```

**Expected output**:
```
tests/test_module.py::TestFeatureName::test_creation_with_valid_input FAILED
tests/test_module.py::TestFeatureName::test_creation_with_invalid_input FAILED
tests/test_module.py::TestFeatureName::test_key_operation_success FAILED
```

**If tests pass** → Something is wrong! Tests aren't testing the right thing.

---

## Phase 2: GREEN - Implement Minimal Code

### Step 1: Create/Update Source File

Implement **minimal code** to make tests pass:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureName:
    """Brief description of what this does.

    Args:
        arg: Description of argument.

    Raises:
        ValueError: If arg is invalid.
    """

    arg: str

    def __post_init__(self) -> None:
        """Validate arguments after initialization."""
        if self.arg is None:
            raise ValueError("Invalid arg: cannot be None")

    def process(self) -> str:
        """Process the feature and return result.

        Returns:
            Processed result string.
        """
        if not self.arg:
            return "default"
        return f"processed: {self.arg}"
```

### Step 2: Follow Code Standards

Use `dqx-code-standards` skill for quick reference:
```javascript
skill({ name: "dqx-code-standards" })
```

**Key standards**:
- `from __future__ import annotations` at top
- Complete type hints for all functions
- Google-style docstrings for public APIs
- Proper import order
- Use `frozen=True` for dataclasses

### Step 3: Verify Tests PASS

```bash
uv run pytest tests/test_module.py -v
```

**Expected output**:
```
tests/test_module.py::TestFeatureName::test_creation_with_valid_input PASSED
tests/test_module.py::TestFeatureName::test_creation_with_invalid_input PASSED
tests/test_module.py::TestFeatureName::test_key_operation_success PASSED
tests/test_module.py::TestFeatureName::test_key_operation_edge_case PASSED
```

**All tests should be GREEN now!**

---

## Phase 3: REFACTOR - Check Coverage

### Step 1: Run Coverage Check

```bash
uv run pytest tests/test_module.py \
  --cov=src/dqx/module \
  --cov-report=term-missing
```

**Required**: Coverage MUST be 100%

### Step 2: Handle Uncovered Lines

**If coverage < 100%**, you have two options:

#### Option 1: Add Tests (Preferred)

```python
def test_missing_scenario(self) -> None:
    """Test the scenario that wasn't covered."""
    # Add test for uncovered lines
    result = feature.uncovered_method()
    assert result == expected
```

#### Option 2: Use `# pragma: no cover` (Rare)

**Only for**:
- Defensive code that should never execute
- Abstract methods that must be overridden
- Trivial `__repr__` or `__str__` methods

```python
def __repr__(self) -> str:  # pragma: no cover
    """String representation."""
    return f"FeatureName(arg={self.arg})"


def defensive_check(self) -> None:
    if self._internal is None:  # pragma: no cover
        # Defensive: constructor ensures _internal is never None
        raise RuntimeError("Unexpected None")
```

### Step 3: Verify 100% Coverage

```bash
uv run pytest tests/test_module.py \
  --cov=src/dqx/module \
  --cov-report=term-missing
```

**Expected output**:
```
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src/dqx/module.py      45      0   100%
-------------------------------------------------
TOTAL                  45      0   100%
```

---

## Complete TDD Cycle Example

### Scenario: Implement Tag Validator

#### Phase 1: RED (Write Tests)

```python
# tests/test_validator.py
class TestTagValidator:
    def test_valid_tag(self) -> None:
        """Test validation of valid tag."""
        assert validate_tag("user123") is True

    def test_invalid_tag_empty(self) -> None:
        """Test validation rejects empty tag."""
        with pytest.raises(ValueError, match="Tag cannot be empty"):
            validate_tag("")

    def test_invalid_tag_special_chars(self) -> None:
        """Test validation rejects special characters."""
        with pytest.raises(ValueError, match="alphanumeric"):
            validate_tag("user@123")
```

Run: `uv run pytest tests/test_validator.py -v` → **All FAIL** ✓

#### Phase 2: GREEN (Implement)

```python
# src/dqx/validator.py
from __future__ import annotations

import re


def validate_tag(tag: str) -> bool:
    """Validate tag contains only alphanumeric characters.

    Args:
        tag: Tag string to validate.

    Returns:
        True if valid.

    Raises:
        ValueError: If tag is empty or contains invalid characters.
    """
    if not tag:
        raise ValueError("Tag cannot be empty")

    if not re.match(r"^[a-zA-Z0-9]+$", tag):
        raise ValueError("Tag must contain only alphanumeric characters")

    return True
```

Run: `uv run pytest tests/test_validator.py -v` → **All PASS** ✓

#### Phase 3: REFACTOR (Coverage)

```bash
uv run pytest tests/test_validator.py \
  --cov=src/dqx/validator \
  --cov-report=term-missing
```

Output: **100% coverage** ✓

---

## When to use me

Use this skill when:
- **Implementing features** from design documents
- **Starting new modules** or classes
- **Adding functionality** to existing code
- **Following TDD** best practices

This is the core development loop for ALL DQX code.

---

## Common Mistakes to Avoid

❌ **Don't skip RED phase**
- Always write tests first
- Verify they fail before implementing

❌ **Don't write all code then test**
- This is waterfall, not TDD
- Write small iterations: test → code → test → code

❌ **Don't accept coverage < 100%**
- DQX has ZERO tolerance for missing coverage
- Add tests or justify `# pragma: no cover`

❌ **Don't write implementation details in tests**
- Test behavior, not implementation
- Tests should pass even if you refactor

---

## Integration with Other Skills

**After TDD cycle**, run quality gate:
```javascript
skill({ name: "dqx-quality-gate" })
```

**Before committing**, use conventional commit:
```javascript
skill({ name: "dqx-conventional-commit" })
```

---

## Reference

Complete details: **AGENTS.md §testing-standards**

See also:
- Code standards: Use `dqx-code-standards` skill
- Coverage requirements: AGENTS.md §coverage-requirements (100%)
- Testing patterns: AGENTS.md §testing-patterns
