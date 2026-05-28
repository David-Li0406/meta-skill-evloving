---
name: dqx-coverage-fix
description: Troubleshoot and fix coverage gaps to reach 100%
compatibility: opencode
metadata:
  workflow: testing
  audience: test-focused-agents
---

## What I do

Help you diagnose and fix test coverage gaps to achieve DQX's mandatory 100% coverage requirement.

---

## DQX Coverage Policy

**STRICT REQUIREMENT**: 100% test coverage - NO EXCEPTIONS

Every line of production code must be covered by tests. This is enforced by CI and must pass before any code can be merged.

---

## Step 1: Identify Uncovered Lines

Run coverage report with missing lines:

```bash
uv run pytest --cov=src/dqx/{module} --cov-report=term-missing
```

**Example output**:
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/dqx/validator.py       45      3    93%   23, 67-68
-----------------------------------------------------
TOTAL                      45      3    93%
```

**Analysis**: Lines 23 and 67-68 are not covered

---

## Step 2: Analyze Uncovered Code

Look at the uncovered lines to understand why they're not covered.

### Scenario A: Missing Tests (Most Common)

**Uncovered line**:
```python
# Line 23 in validator.py
if not tag:
    raise ValueError("Tag cannot be empty")  # ← Not covered
```

**Reason**: No test calls the function with empty tag

**Solution**: Add test
```python
def test_validate_tag_empty(self) -> None:
    """Test validation rejects empty tag."""
    with pytest.raises(ValueError, match="Tag cannot be empty"):
        validate_tag("")
```

---

### Scenario B: Missing Edge Case Tests

**Uncovered lines**:
```python
# Lines 67-68 in validator.py
if len(tags) > MAX_TAGS:
    raise ValueError(f"Too many tags: {len(tags)}")  # ← Not covered
```

**Reason**: No test with > MAX_TAGS

**Solution**: Add edge case test
```python
def test_validate_tags_too_many(self) -> None:
    """Test validation rejects excessive tags."""
    tags = [f"tag{i}" for i in range(MAX_TAGS + 1)]
    with pytest.raises(ValueError, match="Too many tags"):
        validate_tags(tags)
```

---

### Scenario C: Missing Error Path Tests

**Uncovered line**:
```python
# Line 89 in validator.py
try:
    connect_to_service()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")  # ← Not covered
    raise
```

**Reason**: No test triggers ConnectionError

**Solution**: Mock the error
```python
from unittest.mock import patch


def test_process_connection_error(self) -> None:
    """Test handling of connection errors."""
    with patch("dqx.validator.connect") as mock_connect:
        mock_connect.side_effect = ConnectionError("Network error")

        with pytest.raises(ConnectionError):
            process_data()
```

---

### Scenario D: Defensive Code (Use `# pragma: no cover`)

**Uncovered line**:
```python
# Line 45 in validator.py
if self._internal is None:  # pragma: no cover
    # Defensive: constructor ensures _internal is never None
    raise RuntimeError("Unexpected None value")
```

**When to use `# pragma: no cover`**:
- ✅ Defensive code that should NEVER execute
- ✅ Constructor guarantees ensure condition is impossible
- ✅ Only for truly unreachable code

**Justification required**: Add comment explaining why

---

### Scenario E: Abstract Methods

**Uncovered line**:
```python
# Line 12 in base.py
def process(self) -> str:  # pragma: no cover
    """Subclasses must implement this method."""
    raise NotImplementedError("Subclass must implement process()")
```

**When to use `# pragma: no cover`**:
- ✅ Abstract methods in base classes
- ✅ Must be overridden by subclasses
- ✅ Never called directly

---

### Scenario F: Trivial Methods

**Uncovered line**:
```python
# Line 34 in models.py
def __repr__(self) -> str:  # pragma: no cover
    """String representation for debugging."""
    return f"MyClass(value={self.value})"
```

**When to use `# pragma: no cover`**:
- ✅ Trivial `__repr__` methods
- ✅ Trivial `__str__` methods
- ✅ Only for truly trivial implementations

**Warning**: Use SPARINGLY. If method has any logic, write tests!

---

## Decision Tree

```
Is the line uncovered?
├─ YES
│  └─ Is there a test scenario for this line?
│     ├─ NO → Add test (Scenario A, B, or C)
│     └─ YES, but test doesn't reach it
│        └─ Is it an error path?
│           ├─ YES → Mock the error (Scenario C)
│           └─ NO → Fix test to reach the line
└─ Is it reachable code?
   ├─ YES → Add test
   └─ NO → Can I justify # pragma: no cover?
      ├─ Defensive code? → YES, add pragma (Scenario D)
      ├─ Abstract method? → YES, add pragma (Scenario E)
      ├─ Trivial __repr__? → YES, add pragma (Scenario F)
      └─ None of above → Add test anyway
```

---

## Common Coverage Issues

### Issue 1: Branch Not Covered

**Code**:
```python
if condition:
    # Covered
    do_something()
else:
    # Not covered ← Missing test for false branch
    do_something_else()
```

**Solution**: Add test for false branch
```python
def test_function_when_condition_false(self) -> None:
    """Test behavior when condition is false."""
    result = function(condition=False)
    assert result == expected_for_false
```

---

### Issue 2: Exception Not Raised in Test

**Code**:
```python
if invalid:
    raise ValueError("Invalid input")  # Not covered
```

**Solution**: Test the exception
```python
def test_function_invalid_input(self) -> None:
    """Test exception raised for invalid input."""
    with pytest.raises(ValueError, match="Invalid input"):
        function(invalid_input)
```

---

### Issue 3: Early Return Not Covered

**Code**:
```python
if quick_check():
    return early_result  # Not covered

# Rest of function
```

**Solution**: Add test that triggers early return
```python
def test_function_early_return(self) -> None:
    """Test early return path."""
    result = function(trigger_quick_check=True)
    assert result == early_result
```

---

## Coverage Commands Reference

**Check specific module**:
```bash
uv run pytest tests/test_module.py \
  --cov=src/dqx/module \
  --cov-report=term-missing
```

**Check all code**:
```bash
uv run pytest \
  --cov=src/dqx \
  --cov-report=term-missing
```

**Generate HTML report** (for detailed analysis):
```bash
uv run pytest \
  --cov=src/dqx \
  --cov-report=html

# Open htmlcov/index.html in browser
```

**Check coverage for specific test**:
```bash
uv run pytest tests/test_module.py::test_function \
  --cov=src/dqx/module \
  --cov-report=term-missing
```

---

## When to use me

Use this skill when:
- **Coverage < 100%** after implementation
- **CI fails** due to coverage check
- **Unsure how to reach** certain lines
- **Deciding whether** to use `# pragma: no cover`

---

## Best Practices

### DO:
✅ Write tests to cover lines (preferred solution)
✅ Test both happy path and error paths
✅ Test edge cases (empty, None, boundaries)
✅ Mock external dependencies to test error handling
✅ Justify every `# pragma: no cover` with comment

### DON'T:
❌ Use `# pragma: no cover` to avoid writing tests
❌ Accept coverage < 100% in any situation
❌ Skip error path testing
❌ Assume code is unreachable without verification
❌ Use pragma on complex logic

---

## Integration with Quality Gate

Coverage check is Gate 2 in quality gate:

```javascript
skill({ name: "dqx-quality-gate" })
```

If coverage fails:
```javascript
skill({ name: "dqx-coverage-fix" })  // Use this skill
```

Then re-run quality gate.

---

## Reference

Complete details: **AGENTS.md §coverage-requirements**

See also:
- Testing standards: AGENTS.md §testing-standards
- Testing patterns: AGENTS.md §testing-patterns
