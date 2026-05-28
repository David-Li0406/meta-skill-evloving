# Failure Verification Guide
**Version:** {{VERSION}}

Techniques for verifying tests fail correctly in the RED phase of TDD.

---

## Why Verify Failures?

In RED phase, tests must fail for the **right reason**:
- Confirms test actually tests what you intend
- Ensures test will catch real bugs
- Validates test is not always passing (false positive)

---

## Intentional Failure Techniques

### Technique 1: Run Before Implementation

```python
def test_user_can_login():
    user = create_user("test@example.com", "password123")
    result = login(user.email, "password123")
    assert result.success == True

# Run this BEFORE writing login() function
# Expected: NameError or AttributeError (function doesn't exist)
```

### Technique 2: Assert the Opposite

Temporarily flip your assertion to verify it can fail:

```python
# Original assertion
assert result == expected_value

# Temporary verification (should fail)
assert result != expected_value

# Revert to original after confirming test works
```

### Technique 3: Hardcode Wrong Value

```python
def calculate_total(items):
    return 0  # Intentionally wrong

def test_calculates_total():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30  # Should fail with 0 != 30
```

---

## Error Message Verification

### Read the Failure Message

Good test failures tell you:
- What was expected
- What was received
- Where it failed

```
AssertionError: assert 0 == 30
  Expected: 30
  Actual: 0
```

### Verify Message is Helpful

Ask yourself:
- Does the message explain what failed?
- Can you diagnose the issue from the message alone?
- Would another developer understand it?

### Improve Assertion Messages

```python
# Basic
assert total == 30

# Better (with context)
assert total == 30, f"Cart total should be 30, got {total}"
```

---

## Boundary Testing

### Test at Boundaries

| Boundary | Test Cases |
|----------|------------|
| Empty | `[]`, `""`, `None`, `0` |
| One | Single item, single char |
| Many | Multiple items |
| Limits | Max values, min values |

### Example: List Processing

```python
def test_empty_list_returns_zero():
    assert sum_prices([]) == 0

def test_single_item_returns_its_price():
    assert sum_prices([Item(10)]) == 10

def test_multiple_items_returns_sum():
    assert sum_prices([Item(10), Item(20)]) == 30
```

---

## Common Verification Mistakes

### Mistake 1: Test Never Fails

```python
# BAD: Always passes regardless of implementation
def test_user_exists():
    user = User()
    assert user is not None  # User() always creates object
```

**Fix:** Test behavior, not existence.

### Mistake 2: Wrong Failure Reason

```python
# Test fails, but for wrong reason
def test_login():
    result = login("user", "pass")
    assert result.token != None

# Fails with: AttributeError: 'NoneType' has no 'token'
# Should fail with: AssertionError (token is None)
```

**Fix:** Ensure failure is at assertion, not setup.

### Mistake 3: Tautological Test

```python
# BAD: Tests nothing real
def test_math():
    assert 2 + 2 == 4  # Always true, tests Python not your code
```

**Fix:** Test your code, not the language.

---

## Verification Checklist

Before moving to GREEN phase:

- [ ] Test fails when run
- [ ] Failure is at the assertion (not setup/syntax)
- [ ] Error message describes expected vs actual
- [ ] Test would catch a real bug in implementation
- [ ] Boundary cases have dedicated tests

---

## Quick Reference

| Technique | When to Use |
|-----------|-------------|
| Run before implementation | Always (first step) |
| Assert opposite | Verify existing tests |
| Hardcode wrong | Check assertion logic |
| Read error message | Every failure |
| Boundary tests | Edge cases |
