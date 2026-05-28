---
name: test-coverage-assistant
description: Use this skill when you need to evaluate and improve test completeness using a 7-dimensional framework, ensuring comprehensive test coverage for each feature.
---

# Skill body

## Purpose

This skill utilizes a 7-dimensional framework to help assess and enhance test completeness, ensuring that every feature has thorough test coverage.

## Quick Reference

### 7 Dimensions

```
┌─────────────────────────────────────────────────────────────┐
│              Test Completeness = 7 Dimensions               │
├─────────────────────────────────────────────────────────────┤
│  1. Normal Path        Expected behavior under normal conditions  │
│  2. Boundary Conditions  Minimum/maximum values, limits          │
│  3. Error Handling      Invalid inputs, exceptional situations    │
│  4. Authorization       Role access control                       │
│  5. State Changes       Validation of before and after states    │
│  6. Validation Logic    Format, business rules                    │
│  7. Integration Testing  Real query validation                    │
└─────────────────────────────────────────────────────────────┘
```

### Dimension Summary Table

| # | Dimension       | Test Content                     | Key Questions                     |
|---|----------------|----------------------------------|-----------------------------------|
| 1 | **Normal Path** | Valid input → Expected output    | Does the normal flow work?       |
| 2 | **Boundary**    | Minimum/maximum values, limits    | What happens at the boundaries?  |
| 3 | **Error Handling** | Invalid input, not found data   | How are errors handled?          |
| 4 | **Authorization** | Role permissions                | Who can do what?                 |
| 5 | **State Changes** | Before and after states        | Are states correctly changed?    |
| 6 | **Validation Logic** | Format, business rules       | Is input validated?              |
| 7 | **Integration Testing** | Real DB/API calls         | Are queries really valid?        |

### Required Dimensions by Function Type

| Function Type | Required Dimensions         |
|---------------|-----------------------------|
| CRUD API      | 1, 2, 3, 4, 6, 7            |
| Query/Search  | 1, 2, 3, 4, 7               |
| State Machine  | 1, 3, 4, 5, 6              |
| Validation Logic | 1, 2, 3, 6                |
| Background Job | 1, 3, 5                     |
| External Integration | 1, 3, 7                 |

## Test Design Checklist

Use this checklist for each function:

```
Function: ___________________

□ Normal Path
  □ Valid input produces expected success
  □ Correct data is returned/created
  □ Expected side effects occur

□ Boundary Conditions
  □ Minimum valid value
  □ Maximum valid value
  □ Empty set
  □ Single item set
  □ Large set (if applicable)

□ Error Handling
  □ Invalid input format
  □ Missing required fields
  □ Duplicate/conflict situations
  □ Not found situations
  □ External service failures (if applicable)

□ Authorization
  □ Each allowed role has been tested
  □ Each denied role has been tested
  □ Unauthorized access has been tested
  □ Cross-boundary access has been tested

□ State Changes
  □ Initial state has been validated
  □ Final state has been validated
  □ All valid state transitions have been tested

□ Validation Logic
  □ Format validation (email, phone, etc.)
  □ Business rule validation
  □ Cross-field validation

□ Integration Testing (e.g., using wildcards in UT)
  □ Query predicates have been validated
  □ Entity relationships have been validated
  □ Pagination has been validated
  □ Sorting/filtering has been validated
```

## Detailed Guide

For complete standards, refer to:
- [Test Completeness Dimensions](../../../core/test-completeness-dimensions.md)
- [Testing Standards](../../../core/testing-standards.md)

### AI Optimization Format (Token Saving)

AI assistants can use YAML format files to reduce token usage:
- Basic standards: `ai/standards/test-completeness-dimensions`