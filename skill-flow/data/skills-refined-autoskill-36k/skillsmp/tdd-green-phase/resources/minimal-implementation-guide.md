# Minimal Implementation Guide
**Version:** {{VERSION}}

Guidance for writing just enough code to pass tests in the GREEN phase of TDD.

---

## The GREEN Phase Goal

**Write the simplest code that makes the test pass.**

Not the best code. Not the most complete code. Just passing code.

---

## YAGNI Principle

**Y**ou **A**in't **G**onna **N**eed **I**t

### What It Means

Don't implement features until you have a test requiring them.

### Example: User Registration

**Test requires:**
```python
def test_user_has_email():
    user = User("test@example.com")
    assert user.email == "test@example.com"
```

**YAGNI implementation:**
```python
class User:
    def __init__(self, email):
        self.email = email
```

**Over-engineered (violates YAGNI):**
```python
class User:
    def __init__(self, email, name=None, age=None, phone=None):
        self.email = email
        self.name = name
        self.age = age
        self.phone = phone
        self.created_at = datetime.now()
        self.is_active = True
        self.validate_email()  # No test for this!
```

### YAGNI Checklist

Before adding code, ask:
- [ ] Does a failing test require this?
- [ ] Will the test fail without it?
- [ ] Am I guessing future needs?

If no test requires it → don't write it.

---

## Avoiding Premature Optimization

### The Rule

**Make it work, then make it right, then make it fast.**

In GREEN phase, focus only on "make it work."

### Example: Finding Maximum

**Test:**
```python
def test_finds_maximum():
    assert find_max([3, 1, 4, 1, 5]) == 5
```

**Simple (correct for GREEN):**
```python
def find_max(numbers):
    return max(numbers)
```

**Premature optimization (wrong for GREEN):**
```python
def find_max(numbers):
    # "Optimized" manual implementation
    if not numbers:
        return None
    maximum = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] > maximum:
            maximum = numbers[i]
    return maximum
```

### When to Optimize

- After tests pass (REFACTOR phase)
- When performance tests fail
- When profiling shows bottleneck

Never optimize based on assumptions.

---

## Minimal Implementation Strategies

### Strategy 1: Fake It

Return a hardcoded value to pass the test.

```python
def test_adds_numbers():
    assert add(2, 3) == 5

# Fake it
def add(a, b):
    return 5  # Hardcoded - will generalize with more tests
```

### Strategy 2: Obvious Implementation

When the solution is clear, implement directly.

```python
def test_adds_numbers():
    assert add(2, 3) == 5

# Obvious implementation
def add(a, b):
    return a + b
```

### Strategy 3: Triangulation

Use multiple tests to drive general solution (see triangulation-examples.md).

---

## Common Mistakes

### Mistake 1: Anticipating Future Tests

```python
# Test only checks positive numbers
def test_sum_positive():
    assert sum_list([1, 2, 3]) == 6

# BAD: Handles cases not yet tested
def sum_list(numbers):
    if not numbers:
        return 0  # No test for empty!
    if any(n < 0 for n in numbers):
        raise ValueError()  # No test for negatives!
    return sum(numbers)
```

### Mistake 2: Adding Error Handling Early

```python
# Test doesn't check errors
def test_divides():
    assert divide(10, 2) == 5

# BAD: Error handling without test
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError()  # No test!
    return a / b
```

**Fix:** Add error handling when a test requires it.

---

## Quick Reference

| Do | Don't |
|----|-------|
| Pass the current test | Anticipate future tests |
| Use simplest solution | Optimize prematurely |
| Hardcode if appropriate | Over-generalize early |
| Wait for tests to drive design | Design without tests |

### GREEN Phase Mantra

```
Does my test pass? → Yes → Stop coding
                  → No  → Write minimal fix
```
