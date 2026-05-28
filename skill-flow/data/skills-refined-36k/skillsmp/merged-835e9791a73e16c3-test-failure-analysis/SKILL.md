---
name: test-failure-analysis
description: Use this skill when encountering failing tests or when the user asks about "test failure analysis", "debugging tests", or needs to investigate specific test failures.
---

# Test Failure Analysis

Establish a balanced investigative approach for all test failures encountered in this session.

## Core Principle

Tests are specifications - they define expected behavior. When they fail, it's a critical moment requiring balanced investigation, not automatic dismissal.

## Dual Hypothesis Approach

Always consider both possibilities when a test fails:

| Hypothesis A                    | Hypothesis B             |
| ------------------------------- | ------------------------ |
| Test expectations are incorrect | Implementation has a bug |
| Test is outdated                | Test caught a regression |
| Test has wrong assumptions      | Test found an edge case  |

## Investigation Protocol

For EVERY test failure:

### 1. Pause and Read

- Understand what the test is trying to verify.
- Read its name, comments, and assertions carefully.
- Check the test's history (git blame) for context.

### 2. Trace the Implementation

- Follow the code path that leads to the failure.
- Understand actual behavior vs. expected behavior.
- Check if recent changes affected this code path.

### 3. Consider the Context

- Is this testing a documented requirement?
- Would current behavior surprise a user?
- What would be the impact of each possible fix?

### 4. Make a Reasoned Decision

| Situation               | Action                             |
| ----------------------- | ---------------------------------- |
| Implementation is wrong | Fix the bug                        |
| Test is wrong           | Fix test AND document why          |
| Unclear                 | Seek clarification before changing |

### 5. Learn from the Failure

- What can this teach about the system?
- Should additional tests cover related cases?
- Is there a pattern being missed?

## Red Flags (Dangerous Patterns)

- 🚫 Immediately changing tests to match implementation.
- 🚫 Assuming implementation is always correct.
- 🚫 Bulk-updating tests without individual analysis.
- 🚫 Removing "inconvenient" test cases.
- 🚫 Adding mock/stub workarounds instead of fixing root causes.

## Good Practices

- ✅ Treat each test failure as a potential bug discovery.
- ✅ Document analysis in comments when fixing tests.
- ✅ Write clear test names that explain intent.
- ✅ When changing a test, explain why the original was wrong.
- ✅ Consider adding more tests when finding ambiguity.

## Analysis Process

### 1. Initial Analysis

- Read the failing test carefully, understanding its intent.
- Examine the test's assertions and expected behavior.
- Review the error message and stack trace.

### 2. Investigate the Implementation

- Check the actual implementation being tested.
- Trace through the code path that leads to the failure.
- Verify that implementation matches documented behavior.

### 3. Apply Critical Thinking

For each failing test, ask:

- What behavior is the test trying to verify?
- Is this behavior clearly documented or implied by the API design?
- Does the current implementation actually provide this behavior?
- Could this be an edge case the implementation missed?

### 4. Make a Determination

Classify the failure as one of:

| Classification         | Meaning                           |
| ---------------------- | --------------------------------- |
| **Test Bug**           | Test's expectations are incorrect |
| **Implementation Bug** | Code doesn't behave as it should  |
| **Ambiguous**          | Intended behavior is unclear      |

### 5. Document Reasoning

Provide clear explanation including:

- Evidence supporting the conclusion.
- Specific mismatch between expectation and reality.
- Recommended fix (to test or implementation).

## Example Responses

**Good**: "I see test_user_validation is failing. Let me trace through the validation logic to understand if this is catching a real bug or if the test's expectations are incorrect."

**Bad**: "The test is failing so I'll update it to match what the code does."

## Key Principles

- NEVER automatically assume the test is wrong.
- ALWAYS consider that the test might have found a real bug.
- When uncertain, lean toward investigating the implementation.
- A failing test is a gift - it's either catching a bug or clarifying requirements.

## Related Skills

- **comprehensive-test-review**: Full test suite review.