---
name: bug-fix-testing
description: Patterns for creating tests that verify bug fixes and prevent regressions. Use when writing tests for bug fixes, creating regression tests, or verifying fix effectiveness.
---

# Bug Fix Testing

This skill provides testing patterns specifically designed for bug fix verification.

## When to Use

- Creating regression tests for a specific bug fix
- Writing tests that prove a bug is fixed
- Verifying fix effectiveness
- Adding edge case coverage related to a bug

## Test Types Required for Bug Fixes

### 1. Regression Test (Required)

Proves the specific bug is fixed and prevents recurrence:

```typescript
describe('[TICKET-ID]: Brief bug description', () => {
  it('should not exhibit the bug behavior', () => {
    // Arrange: Set up the exact condition that triggered the bug
    // Use steps from bug-context.md "Steps to Reproduce"
    
    // Act: Trigger the scenario that caused the bug
    
    // Assert: Verify correct behavior (not bug behavior)
  });
});
```

**Key Principle**: This test should FAIL on the old code and PASS with the fix.

### 2. Edge Case Tests (Recommended)

Cover related scenarios identified in the RCA:

```typescript
it('should handle [edge case from RCA]', () => {
  // Test boundary conditions and related scenarios
});
```

### 3. Integration Test (If Applicable)

Verify the fix works in realistic context:

```typescript
it('should work correctly in [real-world scenario]', () => {
  // End-to-end verification
});
```

## Test Naming Convention

Format: `[TICKET-ID]_[Component]_[Scenario]_[ExpectedBehavior]`

**Examples:**
- `EMS1234_UserAuth_ExpiredToken_ShouldRedirectToLogin`
- `TMSPROV567_DataSync_ConcurrentUpdates_ShouldNotLoseData`
- `TEST001_PromptStructure_MixedPatterns_ShouldBeConsistent`

## Verification Approach

### Proving Test Effectiveness

Since we cannot automatically run tests on old code:

1. **With fix**: Run the test → Should PASS ✅
2. **Optional verification**: 
   - Temporarily revert the fix
   - Run the test → Should FAIL ❌
   - Re-apply the fix

### Test Quality Checklist

- [ ] Test uses exact scenario from bug report
- [ ] Test would fail without the fix
- [ ] Test is deterministic (no flakiness)
- [ ] Test is isolated (no external dependencies)
- [ ] Test has clear assertion messages
- [ ] Test covers the root cause, not just symptoms

## Language-Specific Templates

### TypeScript/JavaScript (Jest/Vitest)

```typescript
import { describe, it, expect, beforeEach } from 'vitest'; // or 'jest'

describe('[TICKET-ID]: [Bug title]', () => {
  // Setup that recreates bug conditions
  beforeEach(() => {
    // Reset state
  });

  it('should not [bug behavior]', () => {
    // Arrange
    const input = /* condition that triggered bug */;
    
    // Act
    const result = functionUnderTest(input);
    
    // Assert
    expect(result).not.toBe(/* bug behavior */);
    expect(result).toBe(/* correct behavior */);
  });

  it('should handle [edge case]', () => {
    // Additional coverage
  });
});
```

### Python (pytest)

```python
import pytest

class TestTicketID:
    """Tests for bug fix: [TICKET-ID] - [Bug title]"""
    
    def test_should_not_exhibit_bug_behavior(self):
        """Regression test: ensures bug does not recur."""
        # Arrange
        input_data = ...  # condition that triggered bug
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result != "bug behavior"
        assert result == "correct behavior"
    
    def test_should_handle_edge_case(self):
        """Edge case from RCA analysis."""
        # Additional coverage
        pass
```

### C# (xUnit/NUnit)

```csharp
public class TicketIdTests
{
    /// <summary>
    /// Regression test for TICKET-ID: Bug title
    /// </summary>
    [Fact]
    public void ShouldNotExhibitBugBehavior()
    {
        // Arrange
        var input = /* condition that triggered bug */;
        
        // Act
        var result = _sut.MethodUnderTest(input);
        
        // Assert
        Assert.NotEqual(/* bug behavior */, result);
        Assert.Equal(/* correct behavior */, result);
    }
}
```

## Common Anti-Patterns to Avoid

### ❌ Testing the fix, not the bug
```typescript
// BAD: Tests that the fix exists
it('should call the new validation method', () => {
  expect(newValidationMethod).toHaveBeenCalled();
});

// GOOD: Tests that the bug behavior doesn't occur
it('should reject invalid input', () => {
  expect(() => process(invalidInput)).toThrow('Validation error');
});
```

### ❌ Vague assertions
```typescript
// BAD
expect(result).toBeTruthy();

// GOOD
expect(result.status).toBe('success');
expect(result.errors).toHaveLength(0);
```

### ❌ Testing too much
```typescript
// BAD: Unrelated assertions
it('should fix the bug', () => {
  // Tests 10 different behaviors
});

// GOOD: Focused on specific behavior
it('should not allow null values', () => {
  // Tests only null handling
});
```

## References

- Bug context: Use `bug-context.md` for exact reproduction steps
- Root cause: Use `verified-rca.md` for edge cases to cover
- Existing tests: Check `research/codebase-research.md` for test patterns in this repo
