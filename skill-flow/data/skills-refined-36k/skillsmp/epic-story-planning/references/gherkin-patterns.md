---
title: Gherkin Patterns
description: Common patterns for writing effective gherkin acceptance criteria
keywords: gherkin, acceptance criteria, bdd, scenarios
skill: epic-story-planning
---

# Gherkin Patterns

## Scenario Types

| Type | Purpose | Example |
|------|---------|---------|
| Happy Path | Normal successful flow | User logs in successfully |
| Edge Case | Boundary conditions | Empty input, max values |
| Error Case | Expected failures | Invalid credentials |
| Permission | Access control | Admin-only features |

## Given-When-Then Structure

**Given** - Preconditions and context
- System state before action
- User role/permissions
- Existing data

**When** - Action being tested
- Single user action
- System trigger
- API call

**Then** - Expected outcome
- State changes
- User feedback
- Side effects

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Multiple Whens | Tests too much | Split into separate scenarios |
| Implementation details | Brittle tests | Focus on behavior |
| Vague assertions | Hard to verify | Be specific and measurable |
| Duplicate scenarios | Maintenance burden | Use scenario outlines |

## Scenario Outline Pattern

For testing variations:

```gherkin
Scenario Outline: <description>
  Given <precondition>
  When user enters "<input>"
  Then result should be "<expected>"

  Examples:
    | input | expected |
    | valid | success  |
    | empty | error    |
```

## Data Table Pattern

For complex input data:

```gherkin
Scenario: Create user with profile
  Given I am an admin
  When I create user with:
    | field    | value           |
    | name     | John Doe        |
    | email    | john@example.com|
    | role     | editor          |
  Then user should be created
```
