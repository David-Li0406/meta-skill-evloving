---
name: analyze-test-failures
description: Use this skill when encountering failing tests or when you need to analyze test failures to determine whether they indicate test issues or genuine bugs.
---

# Analyze Test Failures

Analyze failing test cases with a balanced, investigative approach.

## Core Principle

Tests are specifications that define expected behavior. When they fail, it's a critical moment requiring investigation, not automatic dismissal.

## Analysis Process

### 1. Initial Analysis

- Read the failing test carefully, understanding its intent.
- Examine the test's assertions and expected behavior.
- Review the error message and stack trace for context.

### 2. Investigate the Implementation

- Check the actual implementation being tested.
- Trace through the code path that leads to the failure.
- Verify that the implementation matches documented behavior.

### 3. Apply Critical Thinking

For each failing test, consider both possibilities:

| Hypothesis A                    | Hypothesis B             |
| ------------------------------- | ------------------------ |
| Test expectations are incorrect | Implementation has a bug |
| Test is outdated                | Test caught a regression |
| Test has wrong assumptions      | Test found an edge case  |

### 4. Make a Determination

Classify the failure as one of:

| Classification         | Meaning                           |
| ---------------------- | --------------------------------- |
| **Test Bug**           | Test's expectations are incorrect |
| **Implementation Bug** | Code doesn't behave as it should  |
| **Ambiguous**          | Intended behavior is unclear      |

### 5. Document Reasoning

Provide a clear explanation including:

- Evidence supporting the conclusion.
- Specific mismatch between expectation and reality.
- Recommended fix (to test or implementation).

### 6. Learn from the Failure

- What can this teach about the system?
- Should additional tests cover related cases?
- Is there a pattern being missed?

## Red Flags (Dangerous Patterns)

- 🚫 Immediately changing tests to match implementation.
- 🚫 Assuming implementation is always correct.
- 🚫 Bulk-updating tests without individual analysis.
- 🚫 Removing "inconvenient" test cases.

## Example Analyses

### Example 1: Ambiguous Behavior

**Scenario**: Test expects `calculateDiscount(100, 0.2)` to return 20, but it returns 80.

**Analysis**:

- Test assumes function returns discount amount.
- Implementation returns price after discount.
- Function name is ambiguous.

**Determination**: Ambiguous  
**Recommendation**: Check documentation for clarity on expected behavior.