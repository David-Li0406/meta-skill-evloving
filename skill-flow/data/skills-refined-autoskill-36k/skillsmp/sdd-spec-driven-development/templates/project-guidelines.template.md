# Project Guidelines

This file defines project-specific conventions that SDD agents must follow during the design phase. Place this file at `.sdd/project-guidelines.md` in your project root.

---

## Referenced Documentation

List paths to existing project documentation that agents should read and follow. Agents will read these files during the design phase.

- [path/to/error-handling.md or README section]
- [path/to/logging.md]
- [path/to/coding-standards.md]
- [path/to/architecture-decisions.md]

---

## Error Handling

[If not referencing external docs, describe error handling conventions here]

- How should errors be categorized?
- What error types/classes should be used?
- How should errors be propagated?
- What information should errors contain?

---

## Logging

[If not referencing external docs, describe logging conventions here]

- What logging framework/approach is used?
- What log levels should be used and when?
- What context should be included in logs?
- Are there structured logging requirements?

---

## Naming Conventions

[Describe naming patterns for the project]

- File naming patterns
- Class/module naming patterns
- Function/method naming patterns
- Variable naming patterns

---

## Testing Conventions

[Describe testing patterns for the project]

- Test file locations and naming
- Test framework and assertion style
- Mocking/stubbing conventions
- Test data management

---

## Additional Guidelines

[Any other project-specific conventions that should inform design decisions]

---

## Notes for Agents

When reading this file:
1. Read all referenced documentation files listed above
2. Apply these conventions when making architectural decisions
3. Validate that designs align with these guidelines
4. Flag any design decisions that conflict with project conventions
