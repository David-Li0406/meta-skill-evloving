# {{PROJECT_NAME}} Conventions

> **Last Updated**: {{DATE}}
> **Maintainer**: {{MAINTAINER}}
>
> This document defines the coding conventions, patterns, and standards for this codebase.

## How to Use This Document

### For Developers

1. **Before coding**: Review relevant sections for the feature you're building
2. **During code review**: Use as a checklist for consistency
3. **When in doubt**: This document is the source of truth for style decisions

### For Spec Authors

Reference these conventions in technical specifications:

```markdown
## Implementation Notes

Follow conventions from [CONVENTIONS.md](./CONVENTIONS.md):
- File structure: Section 1
- Error handling: Section 5
- Testing: Section 7
```

### For PRPs (Product Requirements Prompts)

Include convention references in Claude-facing specifications:

```markdown
## Technical Constraints

This implementation must follow the project's established conventions:
- @see CONVENTIONS.md#error-handling for exception patterns
- @see CONVENTIONS.md#testing for test structure requirements
```

---

## Overview

### Project Summary

<!-- Brief description of what this project does -->

{{PROJECT_DESCRIPTION}}

### Primary Languages

<!-- List the main languages used, in order of prevalence -->

- {{LANGUAGE_1}} (primary)
- {{LANGUAGE_2}}
- {{LANGUAGE_3}}

### Tech Stack

<!-- Key frameworks and tools -->

| Category | Technology |
|----------|------------|
| Backend | {{BACKEND_FRAMEWORK}} |
| Frontend | {{FRONTEND_FRAMEWORK}} |
| Database | {{DATABASE}} |
| Testing | {{TEST_FRAMEWORK}} |
| CI/CD | {{CI_CD}} |

---

## 1. File Organization

### Directory Structure

```
{{PROJECT_NAME}}/
├── src/                    # Source code
│   ├── components/         # UI components (if applicable)
│   ├── services/           # Business logic
│   ├── utils/              # Shared utilities
│   ├── types/              # Type definitions
│   └── config/             # Configuration
├── tests/                  # Test files
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test fixtures
├── docs/                   # Documentation
├── scripts/                # Build and utility scripts
└── config/                 # Configuration files
```

### File Placement Rules

<!-- Define where different types of files should go -->

| File Type | Location | Example |
|-----------|----------|---------|
| React components | `src/components/` | `Button.tsx` |
| API handlers | `src/api/` | `users.ts` |
| Utility functions | `src/utils/` | `formatDate.ts` |
| Type definitions | `src/types/` | `user.types.ts` |
| Unit tests | `tests/unit/` or colocated | `Button.test.tsx` |
| E2E tests | `tests/e2e/` | `login.spec.ts` |

---

## 2. File Naming

### General Conventions

<!-- Define naming patterns for different file types -->

| Pattern | Usage | Example |
|---------|-------|---------|
| `kebab-case` | General files, URLs | `user-profile.ts` |
| `PascalCase` | React components, classes | `UserProfile.tsx` |
| `snake_case` | Python modules | `user_profile.py` |
| `camelCase` | JavaScript utilities | `formatUserName.ts` |

### Specific Patterns

```
Components:       PascalCase.tsx       (UserProfile.tsx)
Hooks:            use*.ts              (useAuth.ts)
Utils:            camelCase.ts         (formatDate.ts)
Types:            *.types.ts           (user.types.ts)
Tests:            *.test.ts            (auth.test.ts)
Test fixtures:    *.fixture.ts         (user.fixture.ts)
Config:           *.config.ts          (jest.config.ts)
```

### Test File Naming

<!-- Consistent test file naming makes tests easy to find -->

- Unit tests: `{{filename}}.test.{{ext}}`
- Integration tests: `{{filename}}.integration.test.{{ext}}`
- E2E tests: `{{filename}}.spec.{{ext}}`

---

## 3. Import Patterns

### Import Order

<!-- Consistent import ordering improves readability -->

```typescript
// 1. External dependencies (node_modules)
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Internal aliases (@/ or ~/)
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';

// 3. Relative imports
import { formatDate } from '../utils/formatDate';
import { UserCard } from './UserCard';

// 4. Type imports (if separated)
import type { User } from '@/types/user.types';

// 5. Style imports
import styles from './Component.module.css';
```

### Path Aliases

<!-- Document your path aliases -->

| Alias | Path | Usage |
|-------|------|-------|
| `@/` | `src/` | All source imports |
| `@components/` | `src/components/` | UI components |
| `@utils/` | `src/utils/` | Utility functions |
| `@tests/` | `tests/` | Test utilities |

### Import Style

<!-- ES Modules vs CommonJS, named vs default exports -->

- **Module system**: ES Modules (`import`/`export`)
- **Prefer**: Named exports over default exports
- **Exception**: React components may use default exports

```typescript
// Preferred: Named exports
export const formatDate = (date: Date) => {...};
export const parseDate = (str: string) => {...};

// Acceptable: Default export for components
export default function UserProfile() {...}
```

---

## 4. Code Style

### Formatting

<!-- Define formatting rules -->

| Setting | Value |
|---------|-------|
| Indentation | {{INDENT_SIZE}} spaces |
| Max line length | {{MAX_LINE_LENGTH}} characters |
| Quotes | {{QUOTE_STYLE}} |
| Semicolons | {{SEMICOLONS}} |
| Trailing commas | {{TRAILING_COMMAS}} |

### Linting Configuration

<!-- List your linting tools and key rules -->

**Tools**:
- ESLint with `{{ESLINT_CONFIG}}`
- Prettier for formatting

**Key rules**:
```javascript
{
  "no-unused-vars": "error",
  "no-console": "warn",
  "prefer-const": "error",
  // Add your key rules
}
```

### TypeScript Strictness

```json
{
  "strict": true,
  "noImplicitAny": true,
  "strictNullChecks": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true
}
```

### Naming Conventions

<!-- Variable, function, class naming -->

| Entity | Convention | Example |
|--------|------------|---------|
| Variables | camelCase | `userName`, `isActive` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` |
| Functions | camelCase | `getUserById()` |
| Classes | PascalCase | `UserService` |
| Interfaces | PascalCase (no I prefix) | `User`, `ApiResponse` |
| Types | PascalCase | `UserRole`, `Status` |
| Enums | PascalCase | `UserStatus.Active` |

---

## 5. Error Handling

### General Principles

1. **Fail fast**: Validate inputs early
2. **Be specific**: Use custom error types
3. **Preserve context**: Include original error in wrapped errors
4. **Log appropriately**: Log at the boundary, not everywhere

### Error Types

<!-- Define your custom error hierarchy -->

```typescript
// Base application error
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Specific error types
class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401);
  }
}
```

### Try-Catch Patterns

```typescript
// API/Service layer
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError && error.response?.status === 404) {
      throw new NotFoundError('User');
    }
    // Re-throw with context
    throw new AppError(
      `Failed to fetch user: ${error.message}`,
      'FETCH_ERROR'
    );
  }
}

// Component layer
function UserProfile({ userId }: Props) {
  const { data, error } = useQuery(['user', userId], () => fetchUser(userId));

  if (error instanceof NotFoundError) {
    return <NotFoundPage />;
  }

  if (error) {
    return <ErrorBoundary error={error} />;
  }

  return <UserCard user={data} />;
}
```

### Async Error Handling

```typescript
// Use Result type for expected failures
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function parseUserInput(input: string): Promise<Result<User>> {
  try {
    const user = JSON.parse(input);
    return { success: true, data: user };
  } catch {
    return { success: false, error: new ValidationError('Invalid JSON') };
  }
}
```

---

## 6. Logging

### Log Levels

<!-- Define when to use each level -->

| Level | Usage | Example |
|-------|-------|---------|
| `error` | Unrecoverable errors, exceptions | Database connection failed |
| `warn` | Recoverable issues, deprecations | Falling back to default config |
| `info` | Significant events | User logged in, payment processed |
| `debug` | Development details | Function inputs/outputs |

### Logging Format

<!-- Structured logging format -->

```typescript
// Use structured logging
logger.info('User action completed', {
  userId: user.id,
  action: 'purchase',
  amount: order.total,
  duration: performance.now() - start
});

// NOT string concatenation
logger.info(`User ${userId} purchased ${orderId}`); // Avoid
```

### What to Log

**DO log**:
- Application startup/shutdown
- Authentication events (login, logout, failed attempts)
- Business transactions (orders, payments)
- External service calls (API requests, responses)
- Errors with full context

**DON'T log**:
- Sensitive data (passwords, tokens, PII)
- High-frequency operations in loops
- Successful health checks
- Routine database queries

### Logger Setup

```typescript
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  redact: ['password', 'token', 'authorization'],
});
```

---

## 7. Testing

### Test Organization

```
tests/
├── unit/                   # Fast, isolated tests
│   ├── services/
│   └── utils/
├── integration/            # Tests with real dependencies
│   ├── api/
│   └── database/
├── e2e/                    # End-to-end user flows
└── fixtures/               # Shared test data
    ├── users.ts
    └── orders.ts
```

### Test Naming

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {...});
    it('should throw ValidationError for invalid email', async () => {...});
    it('should hash password before saving', async () => {...});
  });
});
```

### Test Patterns

**Arrange-Act-Assert**:
```typescript
it('should calculate order total correctly', () => {
  // Arrange
  const items = [
    { price: 10, quantity: 2 },
    { price: 5, quantity: 3 },
  ];

  // Act
  const total = calculateTotal(items);

  // Assert
  expect(total).toBe(35);
});
```

**Test fixtures**:
```typescript
// fixtures/users.ts
export const testUser = {
  id: 'test-user-1',
  email: 'test@example.com',
  name: 'Test User',
};

export const createTestUser = (overrides = {}) => ({
  ...testUser,
  ...overrides,
});
```

### Coverage Requirements

| Type | Target |
|------|--------|
| Statements | {{COVERAGE_STATEMENTS}}% |
| Branches | {{COVERAGE_BRANCHES}}% |
| Functions | {{COVERAGE_FUNCTIONS}}% |
| Lines | {{COVERAGE_LINES}}% |

### Mocking Guidelines

```typescript
// Mock external dependencies at module boundary
jest.mock('@/services/emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue({ sent: true }),
}));

// Use dependency injection for easier testing
class UserService {
  constructor(private emailService: EmailService) {}

  async createUser(data: UserData) {
    const user = await this.repo.create(data);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}
```

---

## 8. Documentation

### Code Comments

**When to comment**:
- Complex algorithms or business logic
- Non-obvious workarounds
- TODO items with context
- Public API documentation

**When NOT to comment**:
- Obvious code (`// increment counter`)
- Commented-out code (delete it)
- Version history (use git)

### Function Documentation

```typescript
/**
 * Calculates the compound interest for an investment.
 *
 * @param principal - Initial investment amount
 * @param rate - Annual interest rate (as decimal, e.g., 0.05 for 5%)
 * @param years - Investment period in years
 * @param compoundingsPerYear - Number of times interest compounds per year
 * @returns The final amount after interest
 *
 * @example
 * ```typescript
 * // $1000 at 5% for 10 years, compounded monthly
 * const result = calculateCompoundInterest(1000, 0.05, 10, 12);
 * // Returns: 1647.01
 * ```
 */
function calculateCompoundInterest(
  principal: number,
  rate: number,
  years: number,
  compoundingsPerYear: number = 12
): number {
  // Implementation
}
```

### README Requirements

Every project should have:

- [ ] Project description
- [ ] Prerequisites
- [ ] Installation instructions
- [ ] Running locally
- [ ] Running tests
- [ ] Deployment instructions
- [ ] Contributing guidelines
- [ ] License

---

## 9. Security

### Secrets Management

- **NEVER** commit secrets to version control
- Use environment variables for all secrets
- Maintain `.env.example` with placeholder values
- Use secret managers in production

```bash
# .env.example
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=your-api-key-here
JWT_SECRET=your-jwt-secret-here
```

### Input Validation

```typescript
// Validate ALL user input
import { z } from 'zod';

const UserInputSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z.string().min(1).max(100),
});

function createUser(input: unknown) {
  const validated = UserInputSchema.parse(input);
  // Safe to use validated data
}
```

### Authentication Patterns

```typescript
// Always use constant-time comparison for secrets
import { timingSafeEqual } from 'crypto';

function verifyToken(provided: string, expected: string): boolean {
  const a = Buffer.from(provided);
  const b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}
```

### Security Checklist

- [ ] Input validation on all user data
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries to prevent SQL injection
- [ ] HTTPS enforced in production
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Dependencies regularly updated
- [ ] Secrets rotated periodically
- [ ] Logging without sensitive data

---

## 10. Performance

### General Guidelines

1. **Measure first**: Don't optimize without profiling
2. **Lazy loading**: Load resources on demand
3. **Caching**: Cache expensive computations
4. **Batch operations**: Reduce round trips

### Database Patterns

```typescript
// Use selective queries
const user = await db.user.findUnique({
  where: { id },
  select: { id: true, name: true, email: true }, // Only needed fields
});

// Use batch operations
const users = await db.user.createMany({
  data: usersToCreate,
});

// Use indexes appropriately
// See database schema for index definitions
```

### API Patterns

```typescript
// Implement pagination
async function getUsers(page: number, limit: number = 20) {
  return db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });
}

// Use appropriate caching headers
res.setHeader('Cache-Control', 'public, max-age=3600');
```

### Frontend Patterns

```typescript
// Memoize expensive computations
const sortedUsers = useMemo(
  () => users.sort((a, b) => a.name.localeCompare(b.name)),
  [users]
);

// Lazy load components
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

---

## Appendix A: Quick Reference

### Common Commands

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run tests
npm run lint         # Run linter
npm run format       # Format code

# Database
npm run db:migrate   # Run migrations
npm run db:seed      # Seed database
npm run db:reset     # Reset database
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | Yes |
| `API_KEY` | External API key | Yes |
| `LOG_LEVEL` | Logging verbosity | No (default: info) |
| `NODE_ENV` | Environment name | No (default: development) |

---

## Appendix B: Decision Log

<!-- Document significant convention decisions -->

| Date | Decision | Rationale |
|------|----------|-----------|
| {{DATE}} | Use ESLint flat config | Better TypeScript support |
| {{DATE}} | Adopt Zod for validation | Runtime type safety |
| {{DATE}} | Use pnpm over npm | Faster installs, strict deps |

---

## Appendix C: Resources

- [Project Documentation](./docs/)
- [API Reference](./docs/api/)
- [Architecture Decision Records](./docs/adr/)

---

*This document should be reviewed quarterly and updated when conventions change.*
