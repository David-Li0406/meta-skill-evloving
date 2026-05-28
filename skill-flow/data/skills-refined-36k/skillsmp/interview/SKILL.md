---
name: interview
description: Interview the user to build a detailed specification before implementing a feature. Use when requirements are ambiguous or feature has significant complexity.
---

# Interview (Spec-Based Development)

## Description
Interview the user to build a detailed specification before implementing a feature. This ensures requirements are fully understood and edge cases are considered upfront.

## When to Use
- Starting a new feature
- Requirements are ambiguous
- Feature has significant complexity
- Multiple valid implementation approaches exist

## Steps

### 1. Initial Context
- Read any existing spec file (@SPEC.md)
- Review related code areas
- Understand current architecture

### 2. Core Requirements Interview
Ask about using AskUserQuestion:
- What is the primary goal?
- Who are the users?
- What's the happy path?
- What does success look like?

### 3. Technical Deep Dive
Ask non-obvious questions about:
- Data models and storage
- API contracts (if applicable)
- State management
- Performance requirements
- Scalability needs

### 4. Edge Cases & Error Handling
- What happens when X fails?
- How should Y edge case be handled?
- What are the security considerations?
- What are the rollback scenarios?

### 5. UX/UI Details (if applicable)
- User flow and interactions
- Loading and error states
- Responsive behavior
- Accessibility requirements

### 6. Integration Points
- External services involved
- Dependencies on other features
- Backward compatibility needs
- Migration requirements

### 7. Testing Strategy
- What needs unit tests?
- Integration test scenarios
- E2E test cases
- Performance benchmarks

### 8. Write Specification
Compile answers into structured spec:
```markdown
# Feature: [Name]

## Overview
[Summary]

## Requirements
- Functional requirements
- Non-functional requirements

## Technical Design
- Architecture
- Data models
- API contracts

## Edge Cases
- [Case 1]
- [Case 2]

## Testing Plan
- Unit tests
- Integration tests
- E2E tests

## Open Questions
- [Any unresolved items]
```

### 9. Review & Confirm
- Present spec to user
- Get explicit approval
- Note any changes

## Example Usage
```
/interview "Add user authentication"
/interview  # Start fresh interview
```

## Tips
- Ask one focused question at a time
- Don't ask obvious questions
- Challenge assumptions
- Explore tradeoffs explicitly
- Document decisions and rationale
