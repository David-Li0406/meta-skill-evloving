---
name: requirements-clarification
description: Requirements clarification for TDD. Use BEFORE RED phase to understand WHAT to test. Asks targeted questions to uncover ambiguities, edge cases, and acceptance criteria.
allowed-tools: Read, Grep, Glob
---

# Requirements Clarification for TDD

## Purpose

Before writing tests (RED phase), ensure requirements are understood well enough to:
1. Know WHAT behavior to test
2. Identify edge cases and boundaries
3. Understand acceptance criteria
4. Avoid rework from misunderstood requirements

## When to Use

Initiate clarification when:
- Feature description is less than 2 sentences
- No acceptance criteria provided
- Ambiguous terms like "should handle errors appropriately"
- Business logic without specific rules defined
- No example inputs/outputs given

## When to Skip

Skip clarification when:
- Requirements explicitly define acceptance criteria
- User provides detailed test scenarios
- Simple CRUD with clear schema
- Bug fix with clear reproduction steps
- User requests "skip clarification" or "proceed directly"

## Question Categories

### 1. Functional Requirements

| Question | Purpose |
|----------|---------|
| What is the primary happy path behavior? | Establish main test scenario |
| What inputs does this feature accept? | Define parameter validation tests |
| What outputs/results are expected? | Define assertion expectations |
| What side effects should occur? | Identify integration points |
| Are there any business rules or constraints? | Identify validation logic |

### 2. Edge Cases and Boundaries

| Question | Purpose |
|----------|---------|
| What happens with null/empty input? | Null handling tests |
| What are the boundary values (min/max)? | Boundary condition tests |
| What if required dependencies are unavailable? | Error handling tests |
| Are there concurrency or timing concerns? | Thread safety tests |

### 3. Error Handling

| Question | Purpose |
|----------|---------|
| What exceptions should be thrown and when? | Exception tests |
| How should invalid input be handled? | Validation tests |
| What error messages should users see? | User feedback tests |

### 4. Technical Clarification

| Question | Purpose |
|----------|---------|
| What interfaces/abstractions already exist? | Understand dependencies |
| What existing patterns should be followed? | Consistency with codebase |
| Are there existing tests to follow as examples? | Test style consistency |
| What is the target test scope (unit/integration)? | Test organization |

## Clarification Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLARIFICATION PHASE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Analyze    │───▶│   Identify   │───▶│   Present    │      │
│  │ Requirements │    │    Gaps      │    │  Questions   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                               │                  │
│                    ┌──────────────┐           │                  │
│                    │   Collect    │◀──────────┘                  │
│                    │   Answers    │                              │
│                    └──────────────┘                              │
│                           │                                      │
│                    ┌──────────────┐                              │
│                    │  Sufficient? │                              │
│                    └──────────────┘                              │
│                      │         │                                 │
│                     YES        NO                                │
│                      │         │                                 │
│                      ▼         └──────▶ Ask Follow-up            │
│               ┌──────────────┐                                   │
│               │ Proceed to   │                                   │
│               │  RED Phase   │                                   │
│               └──────────────┘                                   │
│                                                                 │
│  EXIT: Requirements clear enough to define test scenarios        │
└─────────────────────────────────────────────────────────────────┘
```

## Output Template

After clarification, document understanding:

```markdown
## Clarified Requirements for {Feature}

### Understanding Summary
{Brief summary of what the feature should do}

### Inputs and Outputs
- **Inputs**: {List with types}
- **Outputs**: {Expected results}
- **Validation Rules**: {Business rules}

### Identified Test Scenarios
| Scenario Type | Description | Priority |
|---------------|-------------|----------|
| Happy Path | {description} | High |
| Edge Case | {description} | Medium |
| Error Case | {description} | Medium |
| Boundary | {description} | Medium |

### Ready for RED Phase
```

## Minimum Questions (Always Consider)

1. What is the expected behavior for the happy path?
2. What inputs does this accept and what outputs does it produce?
3. How should errors/invalid input be handled?
