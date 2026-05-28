---
name: mutation-testing
description: Use this skill when you want to evaluate the quality of your Python test suite by introducing code mutations and verifying that tests catch them, ensuring your tests are effective and comprehensive.
---

# Mutation Testing with mutmut

Mutation testing assesses test suite quality by introducing small changes (mutations) to source code and verifying that tests fail. If tests don't catch a mutation, it indicates gaps in test coverage or quality.

## Key Concepts

- **Mutant**: Modified version of code with small change
- **Killed**: Test fails when mutation introduced (good)
- **Survived**: Test passes despite mutation (test gap)
- **Mutation Score**: Percentage of mutants killed

## When to Use This Skill

Use mutation testing analysis when:
- Reviewing code changes on a branch
- Verifying test effectiveness after Test-Driven Development (TDD)
- Identifying weak tests that appear to have coverage
- Finding missing edge case tests
- Validating that refactoring didn't weaken the test suite

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
dict_synonyms=Struct, NamedStruct
```

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

Categorize findings based on the effectiveness of your tests against the mutants generated.

## Example: Weak vs Strong Tests

```python
# src/validators.py
def is_valid_order(order: dict) -> bool:
    if not order:
        return False
    if not order.get("items"):
        return False
    if order.get("total", 0) <= 0:
        return False
    return True

def calculate_discount(total: float, tier: str) -> float:
    if tier == "gold":
        return total * 0.2
    elif tier == "silver":
        return total * 0.1
    return 0.0
```

```python
# ❌ Weak tests - mutations survive
def test_order_basic():
    order = {"items": ["a"], "total": 10}
    assert is_valid_order(order) == True  # Only tests happy path

# ✅ Strong tests - kill mutations
def test_order_null():
    assert is_valid_order(None) == False
    assert is_valid_order({}) == False

def test_order_empty_items():
    assert is_valid_order({"items": [], "total": 10}) == False

def test_order_zero_total():
    assert is_valid_order({"items": ["a"], "total": 0}) == False

def test_order_negative_total():
    assert is_valid_order({"items": ["a"], "total": -5}) == False

def test_order_valid():
    assert is_valid_order({"items": ["a"], "total": 10}) == True

def test_discount_gold():
    assert calculate_discount(100, "gold") == 20.0

def test_discount_silver():
    assert calculate_discount(100, "silver") == 10.0
```