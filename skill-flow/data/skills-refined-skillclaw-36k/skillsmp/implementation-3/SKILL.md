---
name: implementation
description: Systematic approaches to writing high-quality code with contract-first discipline and validation gates
when_to_use: when implementing any backend, frontend, database, or test code
version: 1.0.0
---

# Implementation Skill

## Overview

This skill provides systematic workflows for implementing code across backend APIs, frontend components, databases, and tests. It emphasizes:

1. **Contract-first discipline** - DTOs and interfaces defined and validated before business logic
2. **Validation gates** - Quality checkpoints before considering work complete
3. **Coding standards** - Consistent patterns and best practices
4. **Error handling** - Systematic approach to errors and edge cases
5. **Testing requirements** - Comprehensive test coverage expectations

## When to Use This Skill

**Use this skill when:**
- Implementing backend API endpoints and services
- Building frontend components and UI features
- Creating database schemas and migrations
- Writing tests for any code
- Following a PRP implementation blueprint

**This skill integrates with:**
- `shark-task-management` - Task lifecycle tracking with shark CLI
- `test-driven-development` - TDD methodology for test-first development
- `testing-anti-patterns` - What to avoid when writing tests
- `frontend-design` - UI design patterns and aesthetics
- `architecture` - Design documentation that guides implementation

## Workflow Selection

Choose the appropriate workflow based on what you're implementing:

### Backend Implementation

**API Endpoints** → `workflows/implement-api.md`
- REST/GraphQL endpoint implementation
- Request/response handling
- Authentication and authorization
- API testing

**Backend Services** → `workflows/implement-backend.md`
- Business logic implementation
- Service layer patterns
- Repository patterns
- Backend utilities

**Database Changes** → `workflows/implement-database.md`
- Schema design and migrations
- Database queries and optimization
- Data modeling patterns

### Frontend Implementation

**UI Components** → `workflows/implement-frontend.md`
- Component implementation
- State management
- API integration
- Frontend testing

### Testing

**Test Creation** → `workflows/implement-tests.md`
- Unit test implementation
- Integration test implementation
- Contract test implementation
- E2E test implementation

## Critical Context

Before implementing, always review these context documents:

### Contract-First Discipline
`context/contract-first.md`

**THE GOLDEN RULE:** DTOs are defined in design docs, implemented identically on frontend and backend, and validated BEFORE any business logic is written.

This prevents frontend/backend divergence and enables parallel development.

### Validation Gates
`context/validation-gates.md`

Quality checkpoints that must pass before work is considered complete:
- Linting and formatting
- Type checking
- Unit tests
- Contract tests
- Integration tests

### Coding Standards
`context/coding-standards.md`

Consistent code style, naming conventions, and best practices.

### Error Handling
`context/error-handling.md`

Systematic approach to error handling, logging, and user-facing error messages.

### Testing Requirements
`context/testing-requirements.md`

Test coverage expectations and testing strategies.

## Implementation Process

The standard implementation flow is:

```
1. Read design documentation
   ↓
2. Start task tracking: shark task start <task-id>
   ↓
3. Select appropriate workflow (this SKILL.md)
   ↓
4. Follow contract-first discipline (if applicable)
   ↓
5. Implement code following the workflow
   ↓
6. Apply coding standards
   ↓
7. Implement error handling
   ↓
8. Write/run tests (TDD when applicable)
   ↓
9. Run validation gates
   ↓
10. Document implementation
   ↓
11. Complete task tracking: shark task complete <task-id>
```

## Key Principles

1. **Contracts First** - Define and validate DTOs/interfaces before logic
2. **Test-Driven** - Write tests first when using TDD skill
3. **Incremental** - Implement in small, testable increments
4. **Validated** - Pass all gates before considering work complete
5. **Documented** - Update implementation notes and TODOs

## Anti-Patterns to Avoid

- Implementing business logic before validating contracts
- Skipping validation gates "to save time"
- Diverging DTO/interface names from specification
- Writing code without tests
- Assuming frontend will adapt to backend naming
- Creating database migrations before contracts validated
- Manual testing only (no automated tests)

## Integration with Other Skills

**test-driven-development**
- Use TDD skill for test-first workflow
- Follow RED-GREEN-REFACTOR cycle
- Reference from implement-* workflows

**testing-anti-patterns**
- Consult before writing tests
- Avoid testing mock behavior
- Don't add test-only methods to production

**frontend-design**
- Reference for UI aesthetic guidance
- Complement implement-frontend workflow

**architecture**
- Read architecture docs first
- Implementation follows design decisions

## Success Criteria

Implementation is complete when:
- All contracts validated and synchronized
- All validation gates pass
- Tests provide adequate coverage
- Code follows standards
- Error handling is comprehensive
- Documentation is updated
- No outstanding TODOs in critical paths

---

**Remember:** Quality is built in through systematic workflows, not added later. Follow the discipline, trust the process, and deliver production-ready code.
