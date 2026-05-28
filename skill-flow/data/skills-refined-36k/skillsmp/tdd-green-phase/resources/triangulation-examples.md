# Triangulation Examples
**Version:** {{VERSION}}

How multiple test cases drive general solutions in TDD.

---

## What is Triangulation?

Triangulation uses multiple specific tests to guide toward a general implementation.

**Process:**
1. Write first test → implement with hardcoded value
2. Write second test → hardcoded no longer works
3. Generalize implementation to pass both tests

---

## Example 1: Addition Function

### Step 1: First Test

```python
def test_adds_two_and_three():
    assert add(2, 3) == 5
```

**Fake implementation:**
```python
def add(a, b):
    return 5  # Hardcoded
```

Test passes. But is `add()` really adding?

### Step 2: Second Test (Triangulate)

```python
def test_adds_one_and_one():
    assert add(1, 1) == 2
```

Now hardcoded `5` fails this test.

### Step 3: Generalize

```python
def add(a, b):
    return a + b  # Must generalize
```

Both tests pass. Implementation is correct.

---

## Example 2: FizzBuzz

### Step 1: Plain Number

```python
def test_returns_number_as_string():
    assert fizzbuzz(1) == "1"
```

```python
def fizzbuzz(n):
    return "1"  # Hardcoded
```

### Step 2: Another Plain Number

```python
def test_returns_two_as_string():
    assert fizzbuzz(2) == "2"
```

```python
def fizzbuzz(n):
    return str(n)  # Generalized
```

### Step 3: Divisible by 3

```python
def test_returns_fizz_for_three():
    assert fizzbuzz(3) == "Fizz"
```

```python
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    return str(n)
```

### Step 4: Another Multiple of 3

```python
def test_returns_fizz_for_six():
    assert fizzbuzz(6) == "Fizz"
```

Test passes - implementation already general for multiples of 3.

### Step 5: Continue Pattern

Add tests for Buzz (5), FizzBuzz (15), etc.

---

## Example 3: List Processing

### Step 1: Single Item

```python
def test_sum_single_item():
    assert sum_list([5]) == 5
```

```python
def sum_list(items):
    return 5  # Hardcoded
```

### Step 2: Different Single Item

```python
def test_sum_single_item_seven():
    assert sum_list([7]) == 7
```

```python
def sum_list(items):
    return items[0]  # Return first item
```

### Step 3: Multiple Items

```python
def test_sum_two_items():
    assert sum_list([3, 4]) == 7
```

```python
def sum_list(items):
    return sum(items)  # Generalize to sum all
```

---

## When to Use Triangulation

| Situation | Approach |
|-----------|----------|
| Solution is obvious | Implement directly |
| Solution unclear | Triangulate |
| Complex algorithm | Triangulate step by step |
| Simple utility | Implement directly |

### Signs You Need More Tests

- Implementation feels too specific
- Hardcoded values remain
- Edge cases not covered
- You're "guessing" the algorithm

---

## Triangulation Workflow

```
Test 1 → Fake It (hardcode)
    ↓
Test 2 → Forces generalization
    ↓
Test 3 → Confirms pattern
    ↓
Implementation complete
```

---

## Common Patterns

### Pattern: Edge to Center

1. Test simplest case (empty, zero, one)
2. Test basic case (typical input)
3. Test complex case (multiple items)

### Pattern: Happy to Sad

1. Test success case
2. Test another success case
3. Test error case

---

## Quick Reference

| Tests | Implementation |
|-------|----------------|
| 1 test | Can hardcode |
| 2 tests | Must start generalizing |
| 3+ tests | Should be general |

### Key Insight

> "As tests get more specific, code gets more generic."
> — Robert C. Martin
