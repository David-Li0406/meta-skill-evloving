# Refine Phase Guide

**Purpose**: Precision - What specifically does "done" look like?

## Key Question

Does every task have acceptance criteria specific enough to test, with documented constraints and explicitly listed edge cases?

## CRITICAL RULE

**No code is written in this phase.** Specifications only.

## Required Outputs

1. **Acceptance Criteria** - Given-When-Then format
2. **Interface Specifications** - Inputs, outputs, error contracts
3. **Edge Cases** - Enumerated by category
4. **Constraints vs Criteria** - How to build vs what to build

## Given-When-Then Format

```gherkin
Given [starting situation/preconditions]
When [action is taken]
Then [expected outcome]
```

Example:
```gherkin
Given a user is logged in
When they click the logout button
Then their session is invalidated
And they are redirected to the login page
```

## Edge Case Categories

For each task, enumerate edge cases in these categories:

| Category | Examples |
|----------|----------|
| Empty/null | Empty string, null input, missing fields |
| Boundary | Min/max values, exactly at limits |
| Invalid | Wrong type, malformed data, out of range |
| Timing | Concurrent requests, timeouts, race conditions |
| Failure | Network errors, service unavailable |
| Concurrent | Simultaneous access, locking issues |

## Constraints vs Criteria

**Criteria** (what to build):
- Functional requirements
- Acceptance tests
- Success conditions

**Constraints** (how to build):
- Technology choices
- Performance requirements
- Security requirements
- Accessibility requirements

## Interface Specification

For each component interface, document:
- **Inputs**: Parameters, types, validation rules
- **Outputs**: Return types, response formats
- **Errors**: Error conditions, error messages, error codes

## Completion Checklist

- [ ] Every task has Given-When-Then criteria
- [ ] Interface specifications documented
- [ ] Edge cases enumerated by category
- [ ] Constraints documented
- [ ] Out-of-scope explicitly listed per task
- [ ] NO CODE WRITTEN

## Common Mistakes

- Writing code before criteria are complete
- Vague acceptance criteria ("works correctly")
- Missing edge cases that cause bugs later
- Confusing constraints with criteria

## Next Phase

When Refine is complete, advance to **Generate** where AI writes code following TDD.
