---
title: Step Writing Guide
description: Best practices for writing effective step prompts that are clear, actionable, and properly scoped for autonomous execution.
keywords: step, prompt, writing, clarity, actionable, scope, bounded, best-practices
skill: creating-sprints
---

# Step Writing Guide

How to write effective step prompts for autonomous sprint execution.

## Core Principles

Good step prompts are:

| Principle | Description |
|-----------|-------------|
| **Clear** | Unambiguous intent, no room for misinterpretation |
| **Actionable** | Concrete deliverable, verifiable outcome |
| **Scoped** | Bounded scope, single responsibility |

## Clarity Guidelines

### Be Specific, Not Vague

| Bad (Vague) | Good (Clear) |
|-------------|--------------|
| "Fix the bug" | "Fix null pointer exception in UserService.login()" |
| "Improve performance" | "Add database index on users.email column" |
| "Update the code" | "Refactor AuthController to use dependency injection" |

### Use Action Verbs

Start steps with clear action verbs:

| Verb | When to Use | Example |
|------|-------------|---------|
| Implement | New functionality | "Implement password reset endpoint" |
| Add | New element to existing | "Add email validation to registration" |
| Create | New file/component | "Create UserRepository interface" |
| Fix | Bug resolution | "Fix session expiration handling" |
| Refactor | Restructure | "Refactor payment logic into PaymentService" |
| Update | Modify existing | "Update login to support OAuth" |
| Remove | Delete | "Remove deprecated v1 API endpoints" |
| Test | Add tests | "Test edge cases for cart calculations" |

### Avoid Ambiguous Terms

| Ambiguous | Specific |
|-----------|----------|
| "Handle errors" | "Return 400 Bad Request for invalid email format" |
| "Make it work" | "Ensure login returns JWT on successful authentication" |
| "Clean up" | "Remove unused imports and dead code in auth module" |

## Actionable Guidelines

### Define Concrete Deliverables

Each step should have a verifiable outcome:

```yaml
# Bad: No clear deliverable
steps:
  - Think about authentication
  - Consider security

# Good: Concrete deliverables
steps:
  - Create AuthService with login() and logout() methods
  - Add JWT middleware that validates tokens on protected routes
```

### Include Success Criteria (When Complex)

For complex steps, embed success criteria:

```yaml
steps:
  - prompt: |
      Implement rate limiting for API endpoints.
      Success criteria:
      - Max 100 requests per minute per IP
      - Return 429 status when exceeded
      - Include retry-after header
```

### Avoid Research-Only Steps

Steps should produce artifacts, not just knowledge:

| Bad (Research Only) | Good (Actionable) |
|---------------------|-------------------|
| "Research JWT libraries" | "Integrate jsonwebtoken library for JWT handling" |
| "Learn about caching" | "Implement Redis caching for user sessions" |
| "Understand the codebase" | "Document current authentication flow in auth.md" |

## Scope Guidelines

### One Task Per Step

Each step should do one thing:

```yaml
# Bad: Multiple tasks
steps:
  - Implement login, add tests, and deploy

# Good: Scoped steps
steps:
  - Implement login endpoint
  - Add unit tests for login
  - Add integration tests for login
```

### Appropriate Granularity

Steps should be completable in a bounded time:

| Too Large | Appropriate | Too Small |
|-----------|-------------|-----------|
| "Build authentication system" | "Implement login endpoint" | "Add import statement" |
| "Create entire API" | "Create user CRUD endpoints" | "Rename variable" |
| "Refactor whole codebase" | "Refactor auth module" | "Change one function name" |

### Define Boundaries

Explicitly state what's in and out of scope if unclear:

```yaml
steps:
  - prompt: |
      Implement user registration endpoint.
      Scope:
      - POST /auth/register
      - Email/password validation
      - Password hashing
      Not in scope:
      - Email verification (separate step)
      - Rate limiting (separate step)
```

## Step Templates

### Feature Implementation

```yaml
- prompt: |
    Implement [feature name].
    Requirements:
    - [Requirement 1]
    - [Requirement 2]
    Location: [file/directory path]
```

### Bug Fix

```yaml
- prompt: |
    Fix [bug description].
    Current behavior: [what happens now]
    Expected behavior: [what should happen]
    Affected file: [path]
```

### Refactoring

```yaml
- prompt: |
    Refactor [component] to [goal].
    Current structure: [description]
    Target structure: [description]
    Preserve: [what must not change]
```

### Testing

```yaml
- prompt: |
    Add tests for [component/feature].
    Test cases:
    - [Case 1]
    - [Case 2]
    - [Edge case]
    Location: [test file path]
```

## Common Mistakes

### Mistake: Compound Steps

```yaml
# Bad
- Implement login and registration and password reset

# Good
- Implement login endpoint
- Implement registration endpoint
- Implement password reset endpoint
```

### Mistake: Vague Outcomes

```yaml
# Bad
- Make the code better

# Good
- Reduce cyclomatic complexity in PaymentService below 10
```

### Mistake: Missing Context

```yaml
# Bad
- Add validation

# Good
- Add email format validation to registration endpoint
```

### Mistake: Implementation-Specific

```yaml
# Bad
- Use lodash.debounce in the search input

# Good
- Add debouncing to search input (300ms delay)
```

## Step Sizing Checklist

Before finalizing a step, verify:

| Check | Question |
|-------|----------|
| Clarity | Would another developer understand exactly what to do? |
| Action | Is there a concrete artifact produced? |
| Scope | Is it completable as a single unit of work? |
| Testable | Can success be verified? |
| Independent | Can it run without human intervention? |

## Examples by Domain

### API Development

```yaml
steps:
  - Create User entity with id, email, password, createdAt fields
  - Implement POST /users endpoint for user creation
  - Implement GET /users/:id endpoint for user retrieval
  - Add request validation using class-validator
  - Add integration tests for user endpoints
```

### UI Development

```yaml
steps:
  - Create LoginForm component with email and password inputs
  - Add form validation with error message display
  - Implement form submission with loading state
  - Connect form to authentication API
  - Add unit tests for LoginForm
```

### Infrastructure

```yaml
steps:
  - Create Dockerfile for Node.js application
  - Add docker-compose.yml with app and database services
  - Configure environment variables for containerized deployment
  - Add health check endpoint for container orchestration
```
