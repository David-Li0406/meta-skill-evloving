---
name: architecture-advisor
description: Provide guidance on architectural decisions, patterns, and best practices for the monorepo
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Architecture Advisor

## Purpose

Provide guidance on architectural decisions, patterns, and best practices for the monorepo.

## When to Invoke

- Designing a new feature or module
- Deciding where to place code
- Planning database schema changes
- Evaluating architectural trade-offs
- Refactoring existing code
- Creating new packages or apps

## Core Principles

### Domain-Driven Design

- **Bounded Contexts**: Each app/domain has clear boundaries
- **Ubiquitous Language**: Consistent terminology within domains
- **Aggregate Roots**: Clear ownership of data
- **Domain Events**: Communicate between bounded contexts

### CQRS Pattern

- **Commands**: Write operations (create, update, delete)
- **Queries**: Read operations (get, list)
- **Events**: Side effects and notifications
- **Handlers**: Execute commands/queries/events

### Database Ownership

- Each domain owns its database schema
- Schema packages export types for tRPC inference
- Frontend never imports schema directly
- Repositories encapsulate data access

## Package Organization

```
packages/
├── foundation/        # Base classes, interfaces
├── infrastructure/    # Cross-cutting concerns
├── shared-features/   # Reusable business features
└── db-[domain]/       # Domain-specific schemas
```

### Dependency Rules

- Apps can depend on packages
- Foundation packages have no dependencies
- Infrastructure can depend on foundation
- Shared features can depend on foundation + infrastructure
- Domain-specific db packages are owned by their app

## Feature Workflow

### Creating a New Feature

1. Identify bounded context
2. Create or use existing domain package
3. Define schema in appropriate db package
4. Implement CQRS handlers in app
5. Create tRPC router
6. Build frontend components
7. Add tests with Testcontainers

### Adding to Existing Feature

1. Locate the appropriate module
2. Follow existing patterns
3. Add migration if needed
4. Update CQRS handlers
5. Add tests

### Sharing Code Between Apps

| Code Type      | Location                |
| -------------- | ----------------------- |
| Types          | Domain-specific package |
| Utilities      | Foundation package      |
| Business Logic | Shared-feature package  |
| UI Components  | UI package              |

## Anti-Patterns to Avoid

- Frontend importing database schema
- Business logic in UI components
- Direct database access from multiple apps
- Circular dependencies
- Generic "shared" or "utils" packages
- Mixing commands and queries
- God modules/packages

## Output Format

1. **Recommendation** - Clear guidance on approach
2. **Rationale** - Why this approach is recommended
3. **Trade-offs** - Pros and cons of alternatives
4. **Implementation Steps** - How to implement
5. **Examples** - Code or structure examples
6. **References** - Related documentation
