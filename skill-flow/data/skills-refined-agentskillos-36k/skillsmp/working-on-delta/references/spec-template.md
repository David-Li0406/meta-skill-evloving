# Delta Specification Template

Use this template when creating delta specifications. Choose the appropriate format based on delta type.

## Template

```markdown
# [FEATURE-ID]: [Feature Name]

## User Story

As a [user type], I want to [action] so that [benefit].

## Behavior

[2-3 sentences in plain English describing the behavior. Focus on WHAT, not HOW.]

## Acceptance Criteria

### Success Cases
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

### Error Cases
- [ ] Given [invalid input/condition], when [action], then [error behavior]
- [ ] Given [edge case], when [action], then [specific handling]

## Requires

Dependencies:
- [FEATURE-ID]: [Why needed]
- Or "None" if no dependencies

---

## Notes

[Optional: Any additional context, constraints, or clarifications]
```

## Guidelines

### User Story

The user story should answer:
- **Who** is the user? (developer, admin, end user, system)
- **What** do they want to do? (specific action)
- **Why** do they want it? (the benefit or value)

Bad: "As a user, I want better performance"
Good: "As a developer, I want hot-reload so that I can see changes without restarting"

### Behavior

Write in plain English, not technical jargon:
- Describe observable behavior from the user's perspective
- Focus on what the user experiences end-to-end
- **Stay layer-agnostic**: No mention of API, UI, database, or implementation choices
- Describe the complete user flow, not individual technical components

Bad: "Implements a WebSocket connection to stream updates"
Good: "Shows real-time updates without requiring page refresh"

Bad: "API endpoint validates credentials and returns JWT token"
Good: "Users can log in with email and password to access their account"

### Acceptance Criteria

Each criterion should be:
- **Testable**: Can verify pass/fail
- **Specific**: Clear inputs and outputs
- **Independent**: Not dependent on other criteria
- **End-to-end**: Describes the complete user flow, not individual layer behaviors

Use Given/When/Then format:
- **Given**: Initial context or state (from user's perspective)
- **When**: The action or trigger (what the user does)
- **Then**: The expected result (what the user sees/experiences)

Include:
- 2-3 success cases (main user scenarios)
- 2-3 error cases (what can go wrong from user's perspective)
- Edge cases if applicable

**Focus on observable user outcomes, not implementation:**
- Bad: "API returns 200 status code"
- Good: "User is redirected to their dashboard"

### Error Cases to Consider

- Invalid input (wrong type, missing required fields)
- Boundary conditions (empty, max length, negative values)
- Resource failures (network, disk, permissions)
- Concurrent access (if relevant)
- Missing dependencies (files, services, data)

### Dependencies

List features that must be complete before this one:
- Only list direct dependencies
- Explain why each is needed
- Framework will validate these exist

---

## Technical Delta Specifications

For technical deltas (tests, refactoring, infrastructure), use this alternative format:

### Template

```markdown
# [DELTA-ID]: [Technical Change Name]

## Technical Story

As a [developer/system/codebase], I need [technical change] so that [quality benefit].

## What It Does

[2-3 sentences describing the technical change and its impact]

## Acceptance Criteria

### Completion Criteria
- [ ] [Measurable outcome - e.g., "Test coverage for auth module reaches 80%"]
- [ ] [Verification step - e.g., "All existing tests continue to pass"]
- [ ] [Quality gate - e.g., "No new linting errors introduced"]

### Scope Boundaries
- [ ] [What IS included]
- [ ] [What is NOT included]

## Requires

Dependencies:
- [DELTA-ID]: [Why needed]
- Or "None" if no dependencies
```

### Guidelines for Technical Deltas

#### Technical Story

The story should answer:
- **Who** benefits? (developer, CI system, codebase quality)
- **What** is the technical change? (specific and bounded)
- **Why** is it needed? (quality, maintainability, reliability benefit)

Bad: "As a developer, I want better tests"
Good: "As a developer, I need unit tests for the auth module so that I can confidently refactor authentication logic"

#### Acceptance Criteria

For technical deltas, criteria should be:
- **Measurable**: Specific numbers or pass/fail conditions
- **Verifiable**: Can be checked automatically or manually
- **Scoped**: Clear boundaries on what's affected

Examples:
- Test coverage: "Coverage for `src/auth/` reaches 80%"
- Refactoring: "All public APIs remain unchanged" + "All tests pass"
- Performance: "Response time for /api/users improves by at least 20%"
- Infrastructure: "CI pipeline completes in under 10 minutes"

Layer-specific terms ARE appropriate for technical deltas (since the delta is about technical concerns).
