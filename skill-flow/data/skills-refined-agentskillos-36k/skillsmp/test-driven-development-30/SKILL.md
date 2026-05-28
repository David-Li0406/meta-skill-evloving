---
name: test-driven-development
description: Write code by first creating tests that define expected behavior. Use when implementing business logic, algorithms, utilities, or when the user provides test cases, mentions TDD, asks to write tests first, or wants verifiable code generation.
---

# Test-Driven Development

Generate code that passes provided tests, or create tests first then implement.

## Workflow

### When user provides tests

1. **Analyze tests**: Understand expected inputs, outputs, and edge cases
2. **Identify requirements**: Extract implicit requirements from test assertions
3. **Implement solution**: Write minimal code that passes all tests
4. **Verify**: Run tests to confirm implementation
5. **Refactor**: Improve code while keeping tests green

### When user describes behavior

1. **Clarify requirements**: Ask for specific input/output examples
2. **Write tests first**: Create tests covering happy path and edge cases
3. **Present tests**: Show tests to user for confirmation
4. **Implement**: Write code that passes tests
5. **Iterate**: Add tests for additional cases as needed

## Prompting for test cases

When user provides vague requirements, ask:

- What inputs does this function accept?
- What should it return for a typical case?
- What edge cases should be handled? (empty input, null, boundaries)
- What errors should be raised and when?

## Test template

```python
import pytest

class TestCalculateDiscount:
    """Tests for discount calculation logic."""
    
    def test_no_discount_for_small_order(self):
        """Orders under threshold receive no discount."""
        assert calculate_discount(amount=500) == 0
    
    def test_5_percent_discount_over_1000(self):
        """Orders over 1000 receive 5% discount."""
        assert calculate_discount(amount=1500) == 75
    
    def test_10_percent_discount_over_5000(self):
        """Orders over 5000 receive 10% discount."""
        assert calculate_discount(amount=6000) == 600
    
    def test_zero_amount_returns_zero(self):
        """Zero order amount returns zero discount."""
        assert calculate_discount(amount=0) == 0
    
    def test_negative_amount_raises_error(self):
        """Negative amounts are invalid."""
        with pytest.raises(ValueError):
            calculate_discount(amount=-100)
```

## Implementation workflow

Given the tests above, implement step by step:

```python
def calculate_discount(amount: float) -> float:
    """Calculate order discount based on amount thresholds."""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    
    if amount >= 5000:
        return amount * 0.10
    elif amount >= 1000:
        return amount * 0.05
    else:
        return 0
```

## Running tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_discount.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## Best practices

- **One assertion per test** (when practical): Makes failures clear
- **Descriptive test names**: `test_empty_cart_returns_zero_total`
- **Arrange-Act-Assert pattern**: Setup, execute, verify
- **Test edge cases**: Empty, null, boundaries, errors
- **Keep tests independent**: No shared state between tests

## Example interaction

User: "Write a function that validates email addresses"

Response:
1. First, write tests defining valid/invalid emails
2. Show tests: `test_valid_email`, `test_missing_at_symbol`, `test_empty_string`
3. Ask: "Do these test cases cover your requirements?"
4. After confirmation, implement the function
5. Run tests to verify
