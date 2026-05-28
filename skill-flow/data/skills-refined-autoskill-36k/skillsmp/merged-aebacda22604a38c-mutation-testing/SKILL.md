---
name: mutation-testing
description: Use this skill when evaluating Python test suite quality through mutation testing to identify weak tests, validate TDD workflows, and improve test effectiveness.
---

# Mutation Testing with mutmut

Mutation testing assesses test suite quality by introducing small changes (mutations) to source code and verifying that tests fail. If tests don't catch a mutation, it indicates gaps in test coverage or quality.

## Key Concepts

- **Mutant**: Modified version of code with small change
- **Killed**: Test fails when mutation introduced (good)
- **Survived**: Test passes despite mutation (test gap)
- **Mutation Score**: Percentage of mutants killed

## Quick Start

```bash
# Install
pip install mutmut

# Run mutation testing
mutmut run

# View results
mutmut results

# Inspect specific mutant
mutmut show 1

# Apply mutation to see the change
mutmut apply 1

# Reset applied mutations
mutmut apply 0
```

## Configuration

```ini
# setup.cfg or pyproject.toml [tool.mutmut]
[mutmut]
paths_to_mutate=src/
backup=False
runner=python -m pytest -x
tests_dir=tests/
```

## The Mutation Testing Process

1. **Generate mutants**: Introduce small bugs (mutations) into production code.
2. **Run tests**: Execute your test suite against each mutant.
3. **Evaluate results**: If tests fail, the mutant is "killed" (good). If tests pass, the mutant "survived" (bad - your tests missed the bug).

## Common Mutation Operators

| Original | Mutations |
|----------|-----------|
| `>` | `>=`, `<`, `==` |
| `<` | `<=`, `>`, `==` |
| `==` | `!=` |
| `and` | `or` |
| `+` | `-` |
| `return True` | `return False` |
| `return x` | `return x + 1` |

## Improving Mutation Score

When a mutant survives, add tests for:

1. **Boundary conditions**: Test at exact threshold values.
2. **Return values**: Verify actual results, not just truthiness.
3. **All branches**: Cover each conditional path.
4. **Edge cases**: Empty, None, negative, zero.

## CI Integration

```yaml
# .github/workflows/mutation.yml
name: Mutation Testing
on:
  pull_request:
    paths: ['src/**']

jobs:
  mutation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install mutmut pytest
      - run: mutmut run --CI
      - run: mutmut results
```

## Best Practices

- Target critical business logic, not all code.
- Aim for 80%+ mutation score on important modules.
- Review survived mutants to improve tests.
- Test boundaries and edge cases thoroughly.
- Verify actual values, not just code execution.

## Systematic Branch Analysis Process

When analyzing code on a branch, follow this systematic process:

### Step 1: Identify Changed Code

```bash
# Get files changed on the branch
git diff main...HEAD --name-only | grep '\.py$' | grep -v 'test_'

# Get detailed diff for analysis
git diff main...HEAD -- src/
```

### Step 2: Generate Mental Mutants

For each changed function/method, mentally apply mutation operators.

### Step 3: Verify Test Coverage

For each potential mutant, ask:

1. **Is there a test that exercises this code path?**
2. **Would that test FAIL if this mutation were applied?**
3. **Is the assertion specific enough to catch this change?**

### Step 4: Document Findings

Categorize findings:

| Category | Description | Action Required |
|----------|-------------|-----------------|
| Killed | Test would fail if mutant applied | None - tests are effective |
| Survived | Test would pass with mutant | Add/strengthen test |
| No Coverage | No test exercises this code | Add behavior test |
| Equivalent | Mutant produces same behavior | None - not a real bug |

## Strengthening Weak Tests

### Pattern: Add Boundary Value Tests

```python
# Original weak test
def test_validates_age():
    assert is_adult(25) is True
    assert is_adult(10) is False

# Strengthened with boundary values
def test_validates_age_at_boundary():
    assert is_adult(17) is False  # Just below
    assert is_adult(18) is True   # Exactly at boundary
    assert is_adult(19) is True   # Just above
```

### Pattern: Test Both Branches of Conditions

```python
# Original weak test - only tests one branch
def test_returns_access_result():
    assert can_access(True, True) is True

# Strengthened - tests all meaningful combinations
def test_grants_access_when_admin():
    assert can_access(True, False) is True

def test_grants_access_when_owner():
    assert can_access(False, True) is True

def test_denies_access_when_neither():
    assert can_access(False, False) is False
```

### Pattern: Avoid Identity Values

```python
# Weak - uses identity values
def test_calculates():
    assert multiply(10, 1) == 10  # x * 1 = x / 1
    assert add(5, 0) == 5         # x + 0 = x - 0

# Strong - uses values that reveal operator differences
def test_calculates():
    assert multiply(10, 3) == 30  # 10 * 3 != 10 / 3
    assert add(5, 3) == 8         # 5 + 3 != 5 - 3
```

### Pattern: Verify Side Effects

```python
# Weak - no verification of side effects
def test_processes_order():
    process_order(order)
    # No assertions!

# Strong - verifies observable outcomes
def test_processes_order(mock_repository, mock_email):
    process_order(order)
    mock_repository.save.assert_called_once_with(order)
    mock_email.send.assert_called_once()
    assert mock_email.send.call_args[0][0].to == order.customer_email
```

### Pattern: Test None Handling Explicitly

```python
# Weak - doesn't test None case
def test_get_value():
    assert get_value("key") == "value"

# Strong - tests both None and non-None paths
def test_get_value_with_existing_key():
    assert get_value("key") == "value"

def test_get_value_with_missing_key():
    assert get_value("missing", "default") == "default"
```

### Pattern: Test List Comprehension Logic

```python
# Production code
def get_active_users(users: list[User]) -> list[User]:
    return [user for user in users if user.is_active]

# Weak - doesn't verify filtering logic
def test_returns_list():
    users = [User(active=True), User(active=False)]
    result = get_active_users(users)
    assert isinstance(result, list)

# Strong - verifies filtering behavior
def test_returns_only_active_users():
    active = User(name="Alice", active=True)
    inactive = User(name="Bob", active=False)
    users = [active, inactive]

    result = get_active_users(users)

    assert result == [active]
    assert inactive not in result
```

---

## Summary: Mutation Testing Mindset

**The key question for every line of code:**

> "If I introduced a bug here, would my tests catch it?"

**For each test, verify it would catch:**
- Arithmetic operator changes (+, -, *, /, //, %, **)
- Boundary condition shifts (>=, <=)
- Boolean logic inversions (and, or, not)
- Identity check changes (is, ==)
- Membership test inversions (in, not in)
- Removed statements
- Changed return values
- Empty collections
- None values

**Remember:**
- Coverage measures execution, mutation testing measures detection.
- A test that doesn't make assertions can't kill mutants.
- Boundary values are critical for conditional mutations.
- Avoid identity values that make operators interchangeable.
- Test None explicitly with `is None`.
- Test empty collections explicitly.
- Verify side effects with mock assertions.