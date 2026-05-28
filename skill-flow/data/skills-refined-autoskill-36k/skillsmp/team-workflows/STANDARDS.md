# Establishing Team Standards

Guide for creating and enforcing consistent standards across your team using Claude Code.

## Standards Categories

### 1. Code Style Standards

Create `.claude/rules/code-style.md`:

```yaml
---
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
description: Team code style conventions
alwaysApply: true
---

# Code Style Standards

## Formatting (enforced by Prettier)

| Rule | Value |
|------|-------|
| Indent | 2 spaces |
| Quotes | Single |
| Semicolons | No |
| Line width | 100 |
| Trailing comma | ES5 |

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile.tsx` |
| Hooks | camelCase with use | `useAuth.ts` |
| Utils | camelCase | `formatDate.ts` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Types | PascalCase | `UserResponse` |

## File Organization

```
src/
  components/
    user/
      UserProfile.tsx      # Component
      UserProfile.test.tsx # Tests colocated
      useUserData.ts       # Related hook
      types.ts             # Local types
      index.ts             # Barrel export
```

## Import Order

1. External packages (react, lodash)
2. Internal absolute imports (@/)
3. Relative imports (./)
4. Styles and assets

```typescript
// External
import { useState } from 'react'
import { format } from 'date-fns'

// Internal absolute
import { Button } from '@/components/ui'
import { useAuth } from '@/hooks'

// Relative
import { UserCard } from './UserCard'
import type { UserProps } from './types'
```
```

### 2. Testing Standards

Create `.claude/rules/testing.md`:

```yaml
---
globs: ["**/*.test.ts", "**/*.test.tsx", "**/*.spec.ts", "tests/**/*"]
description: Testing conventions and requirements
alwaysApply: false
---

# Testing Standards

## Test Structure

Follow AAA pattern (Arrange, Act, Assert):

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = { name: 'Test', email: 'test@example.com' }

      // Act
      const result = await userService.createUser(userData)

      // Assert
      expect(result.isOk()).toBe(true)
      expect(result.value.name).toBe('Test')
    })
  })
})
```

## Naming Conventions

- Describe blocks: noun (what you're testing)
- It blocks: should [do something] when [condition]

```typescript
// Good
describe('calculateTax', () => {
  it('should return 0 when amount is negative', () => {})
  it('should apply 10% rate when amount exceeds threshold', () => {})
})

// Avoid
describe('calculateTax tests', () => {
  it('works correctly', () => {})
  it('edge case', () => {})
})
```

## Coverage Requirements

| Type | Minimum | Target |
|------|---------|--------|
| Statements | 80% | 90% |
| Branches | 75% | 85% |
| Functions | 80% | 90% |
| Lines | 80% | 90% |

Critical paths require 100%:
- Authentication flows
- Payment processing
- Data validation
- Security checks

## Mocking Guidelines

```typescript
// Mock external services, not internal logic
const mockPaymentGateway = {
  charge: vi.fn().mockResolvedValue({ success: true })
}

// Use dependency injection for testability
const service = new PaymentService(mockPaymentGateway)

// Reset mocks between tests
beforeEach(() => {
  vi.clearAllMocks()
})
```
```

### 3. API Design Standards

Create `.claude/rules/api-design.md`:

```yaml
---
globs: ["src/routes/**/*", "src/api/**/*", "**/handlers/**/*"]
description: API design conventions
alwaysApply: false
---

# API Design Standards

## RESTful Conventions

| Action | Method | Path | Body |
|--------|--------|------|------|
| List | GET | /users | - |
| Get | GET | /users/:id | - |
| Create | POST | /users | User data |
| Update | PUT | /users/:id | Full user |
| Patch | PATCH | /users/:id | Partial |
| Delete | DELETE | /users/:id | - |

## Response Format

All responses follow this structure:

```typescript
// Success
{
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      { "field": "email", "message": "Must be valid email" }
    ]
  }
}
```

## Status Codes

| Code | Usage |
|------|-------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No content (DELETE) |
| 400 | Validation error |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Not found |
| 409 | Conflict |
| 500 | Server error |

## Validation

Always validate input with Zod:

```typescript
const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['user', 'admin']).default('user')
})

// In handler
const result = createUserSchema.safeParse(body)
if (!result.success) {
  return c.json({ error: formatZodError(result.error) }, 400)
}
```
```

### 4. Security Standards

Create `.claude/rules/security.md`:

```yaml
---
globs: ["**/*.ts", "**/*.tsx"]
description: Security requirements and patterns
alwaysApply: true
---

# Security Standards

## NEVER

- Commit secrets, API keys, or credentials
- Log sensitive data (passwords, tokens, PII)
- Use `eval()` or `Function()` constructors
- Trust user input without validation
- Use string concatenation for SQL queries

## ALWAYS

- Use environment variables for secrets
- Validate and sanitize all user input
- Use parameterized queries for SQL
- Hash passwords with bcrypt/argon2
- Implement rate limiting on auth endpoints

## Input Validation

```typescript
// Always validate before processing
const schema = z.object({
  id: z.string().uuid(),
  amount: z.number().positive().max(10000)
})

const validated = schema.parse(input) // Throws if invalid
```

## SQL Queries

```typescript
// Good - Parameterized
const user = await db.query.users.findFirst({
  where: eq(users.id, userId)
})

// NEVER - String concatenation
const user = await db.execute(`SELECT * FROM users WHERE id = '${userId}'`)
```

## Authentication Checks

```typescript
// Every protected route must check auth
export async function protectedHandler(c: Context) {
  const session = await getSession(c)
  if (!session) {
    return c.json({ error: 'Unauthorized' }, 401)
  }

  // Check authorization too
  if (!hasPermission(session.user, 'read:resource')) {
    return c.json({ error: 'Forbidden' }, 403)
  }

  // ... handler logic
}
```

## Secrets Handling

```bash
# Good - Environment variables
DATABASE_URL=postgres://...
API_KEY=${API_KEY}

# NEVER - Hardcoded
DATABASE_URL=postgres://user:password123@host/db
```
```

### 5. Documentation Standards

Create `.claude/rules/documentation.md`:

```yaml
---
globs: ["**/*.md", "docs/**/*"]
description: Documentation conventions
alwaysApply: false
---

# Documentation Standards

## Required Documentation

Every feature needs:
- [ ] API endpoint documentation
- [ ] Type definitions
- [ ] Usage examples
- [ ] Error handling details

## JSDoc Format

```typescript
/**
 * Creates a new user account.
 *
 * @param data - User creation data
 * @returns Created user or error result
 * @throws {ValidationError} When data is invalid
 *
 * @example
 * const result = await createUser({
 *   name: 'John',
 *   email: 'john@example.com'
 * })
 */
export async function createUser(data: CreateUserInput): Promise<Result<User>> {
  // ...
}
```

## README Structure

```markdown
# Feature Name

Brief description.

## Installation
## Usage
## API Reference
## Examples
## Contributing
```

## Changelog Format

```markdown
## [1.2.0] - 2025-01-08

### Added
- New user profile endpoint

### Changed
- Improved error messages

### Fixed
- Race condition in auth flow

### Security
- Updated dependencies with vulnerabilities
```
```

## Enforcing Standards

### Pre-commit Hooks

Configure hooks to enforce standards:

```bash
# .husky/pre-commit
bun run lint
bun run typecheck
bun test --run
```

### CI/CD Checks

Add to your CI pipeline:

```yaml
# .github/workflows/ci.yml
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun lint
      - run: bun typecheck
      - run: bun test
```

### Code Review Checklist

Create `.claude/rules/review.md`:

```yaml
---
globs: ["**/*"]
description: Code review checklist
alwaysApply: false
---

# Code Review Checklist

## Before Approving

- [ ] Code follows style standards
- [ ] Tests are present and passing
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Documentation is updated
- [ ] Breaking changes are noted
```

## Gradual Adoption

### Phase 1: Document

1. Create CLAUDE.md with basic conventions
2. Add essential rules (code style, testing)
3. Share with team for feedback

### Phase 2: Automate

1. Add linting with auto-fix
2. Configure pre-commit hooks
3. Set up CI checks

### Phase 3: Enforce

1. Block merges on check failures
2. Require code review
3. Track metrics (coverage, lint errors)

### Phase 4: Iterate

1. Review standards quarterly
2. Add patterns from code review feedback
3. Remove obsolete rules

## Standards Template

Use this template for new standards:

```yaml
---
globs: ["relevant/file/patterns/**/*"]
description: What these standards cover
alwaysApply: true|false
---

# [Standard Name]

## Overview
Brief description of why these standards exist.

## Rules

### Rule 1
- Description
- Examples

### Rule 2
- Description
- Examples

## Examples

### Good
```code
Example of correct implementation
```

### Avoid
```code
Example of what NOT to do
```

## Exceptions
When these rules can be broken (if ever).
```
