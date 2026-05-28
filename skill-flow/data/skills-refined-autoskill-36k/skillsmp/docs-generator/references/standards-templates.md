# Standards Documentation Templates

Templates for generating `docs/standards/` files. Document both **detected** patterns and **recommended** practices.

**Key principle**: Standards should be quick to skim. Focus on clear do/don't examples, not code locations (which go stale).

## General Template Structure

```markdown
# {Standard Category}

## Overview

{1-2 sentences on why this standard matters.}

## Detected Patterns

{What the codebase actually does. Descriptive, not prescriptive.}

### {Pattern Name}

**Pattern**: {Brief description}

**Example**:
```{language}
{illustrative code showing the pattern}
```

## Recommended Practices

{Best practices. Mark status relative to what's detected.}

### {Practice Name}

**Status**: {Already followed / Suggested improvement}

**Do**:
```{language}
{good example}
```

**Don't**:
```{language}
{bad example}
```

**Why**: {One sentence rationale}

## Exceptions

{When the standard doesn't apply.}
```

---

## naming-conventions.md

```markdown
# Naming Conventions

## Overview

Consistent naming improves readability and reduces cognitive load.

## Detected Patterns

### File Naming

**Pattern**: {kebab-case / camelCase / PascalCase / snake_case}

```
user-service.ts
auth-handler.ts
api-routes.ts
```

### Variable Naming

**Pattern**: {camelCase / snake_case}

```{language}
const userAuthToken = getToken();
const isAuthenticated = checkAuth();
```

### Function/Method Naming

**Pattern**: {camelCase / snake_case}

**Conventions**:
- Verbs for actions: `get`, `set`, `create`, `update`, `delete`
- Boolean prefixes: `is`, `has`, `should`, `can`

### Component/Class Naming

**Pattern**: {PascalCase}

```{language}
class UserAuthService { }
interface AuthProvider { }
```

## Recommended Practices

### Descriptive Over Short

**Status**: {Already followed / Suggested improvement}

**Do**:
```{language}
const userAuthenticationToken = getToken();
function calculateTotalOrderPrice(items) {}
```

**Don't**:
```{language}
const uat = getToken();
function calc(i) {}
```

**Why**: Descriptive names are self-documenting.

### Consistent Prefixes

**Status**: {Already followed / Suggested improvement}

| Prefix | Use For | Example |
|--------|---------|---------|
| `is` | Boolean state | `isLoading`, `isValid` |
| `has` | Ownership/presence | `hasPermission`, `hasItems` |
| `on` | Event handler props | `onClick`, `onSubmit` |
| `handle` | Internal handlers | `handleClick`, `handleSubmit` |

## Domain-Specific Conventions

{Project-specific naming patterns.}
```

---

## error-handling.md

```markdown
# Error Handling

## Overview

Consistent error handling ensures predictable behavior and good debugging experience.

## Detected Patterns

### Error Strategy

**Pattern**: {Custom error classes / Error codes / Result types / try-catch}

```{language}
{illustrative error handling pattern}
```

### Custom Error Types

**Pattern**: {Yes/No — describe if yes}

```{language}
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.field = field;
  }
}
```

### Error Boundaries

| Layer | Catches | Transforms To |
|-------|---------|---------------|
| {API layer} | All errors | HTTP response |
| {Service layer} | Domain errors | Custom errors |

## Recommended Practices

### Fail Fast

**Status**: {Already followed / Suggested improvement}

**Do**:
```{language}
function processUser(input) {
  if (!input.id) {
    throw new ValidationError('User ID required');
  }
  // proceed with valid data
}
```

**Don't**:
```{language}
function processUser(input) {
  // silently use default
  const id = input.id || 'unknown';
}
```

**Why**: Catch invalid state early before it propagates.

### Include Error Context

**Status**: {Already followed / Suggested improvement}

**Do**:
```{language}
throw new Error(`Failed to fetch user ${userId}: ${error.message}`);
```

**Don't**:
```{language}
throw new Error('Failed');
```

**Why**: Context accelerates debugging.

### Structured Error Responses

**Status**: {Already followed / Suggested improvement}

**Do**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User-friendly message",
    "details": {}
  }
}
```

## Anti-patterns to Avoid

### Silent Failures

```{language}
// BAD: Error swallowed
try {
  riskyOperation();
} catch (e) {
  // do nothing
}
```

### Overly Broad Catches

```{language}
// BAD: Catches everything, loses context
try {
  multipleOperations();
} catch (e) {
  return null;
}
```
```

---

## testing.md

```markdown
# Testing Standards

## Overview

Testing conventions and patterns for this codebase.

## Detected Patterns

### Test Framework

**Framework**: {Jest / Vitest / pytest / cargo test / etc.}

### Test Naming

**Pattern**: {describe/it / test_ prefix / etc.}

```{language}
describe('UserService', () => {
  it('creates user with valid input', () => {});
  it('throws on invalid email', () => {});
});
```

### Test Organization

**Pattern**: {Colocated with source / Separate `tests/` directory / Both}

### Mocking

**Library**: {jest.fn / vi.fn / unittest.mock / etc.}

## Recommended Practices

### Test Naming

**Status**: {Already followed / Suggested improvement}

**Do**:
```{language}
// Descriptive names
test('createUser returns user with valid input')
test('createUser throws ValidationError when email missing')

// Or describe/it style
describe('createUser', () => {
  it('returns user with valid input', () => {})
  it('throws ValidationError when email missing', () => {})
})
```

**Don't**:
```{language}
test('test1')
test('works')
```

### Arrange-Act-Assert

**Status**: {Already followed / Suggested improvement}

**Do**:
```{language}
test('example', () => {
  // Arrange
  const input = createTestInput();

  // Act
  const result = functionUnderTest(input);

  // Assert
  expect(result).toEqual(expected);
});
```

**Why**: Clear structure makes tests readable and maintainable.

### Test Isolation

**Status**: {Already followed / Suggested improvement}

- Each test sets up its own state
- No test depends on another test's side effects
- Use factories/fixtures for test data

## Test Categories

| Category | Purpose | Runs When |
|----------|---------|-----------|
| Unit | Single function/component | Every commit |
| Integration | Multiple components | PR/CI |
| E2E | Full user flows | Pre-release |
```

---

## logging.md

```markdown
# Logging Standards

## Overview

Consistent logging enables effective debugging and monitoring.

## Detected Patterns

### Log Library

**Library**: {winston / pino / console / slog / etc.}

### Log Format

**Pattern**: {Structured JSON / Unstructured text}

```{language}
logger.info('User created', { userId: user.id, action: 'create' });
```

### Log Levels

| Level | Used For |
|-------|----------|
| `error` | Failures requiring attention |
| `warn` | Recoverable issues |
| `info` | Significant events |
| `debug` | Detailed debugging |

## Recommended Practices

### Structured Logging

**Status**: {Already followed / Suggested improvement}

**Do**:
```{language}
logger.info('User created', { userId: user.id, email: user.email });
```

**Don't**:
```{language}
logger.info(`User created: ${user.id}, ${user.email}`);
```

**Why**: Structured logs are searchable and parseable.

### Log Level Guidelines

| Level | When to Use |
|-------|-------------|
| `error` | Unexpected failures — DB down, unhandled exception |
| `warn` | Recoverable issues — rate limit approaching, retry |
| `info` | Business events — user signed up, order placed |
| `debug` | Development only — function entry/exit, state dumps |

### Never Log Sensitive Data

**Status**: {Already followed / Needs attention}

Never log:
- Passwords or tokens
- Full credit card numbers
- PII (emails, addresses in debug logs)

**Do**:
```{language}
logger.info('Payment processed', { cardLast4: '1234' });
```

**Don't**:
```{language}
logger.info('Payment', { card: fullCardNumber, user: userObject });
```
```

---

## Subfolder Templates

### backend/api-design.md

```markdown
# API Design Standards

## Overview

Standards for designing APIs in backend services.

## Detected Patterns

### API Style

**Style**: {REST / GraphQL / gRPC / tRPC}

### Endpoint Naming

```
GET  /users/{id}      # Fetch user
POST /users           # Create user
PUT  /users/{id}      # Update user
DELETE /users/{id}    # Delete user
```

### Response Format

**Success**:
```json
{
  "data": {},
  "meta": {}
}
```

**Error**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

## Recommended Practices

### RESTful Conventions

**Status**: {Already followed / Suggested improvement}

| Action | Method | Path | Success | Error |
|--------|--------|------|---------|-------|
| List | GET | `/resources` | 200 | - |
| Get | GET | `/resources/{id}` | 200 | 404 |
| Create | POST | `/resources` | 201 | 400 |
| Update | PUT/PATCH | `/resources/{id}` | 200 | 404 |
| Delete | DELETE | `/resources/{id}` | 204 | 404 |
```

### frontend/react.md

```markdown
# React Standards

## Overview

Conventions for React component development.

## Detected Patterns

### Component Style

**Pattern**: {Functional components / Class components / Mixed}

### State Management

**Library**: {useState / Redux / Zustand / Jotai / etc.}

### Styling

**Approach**: {CSS Modules / Tailwind / styled-components / etc.}

## Recommended Practices

### Component Structure

**Status**: {Already followed / Suggested improvement}

**Do**:
```tsx
// 1. Imports
import { useState } from 'react';

// 2. Types
interface Props {
  title: string;
}

// 3. Component
export function ComponentName({ title }: Props) {
  // 4. Hooks
  const [state, setState] = useState();

  // 5. Handlers
  const handleClick = () => {};

  // 6. Render
  return <div>{title}</div>;
}
```

### Props Conventions

**Status**: {Already followed / Suggested improvement}

- Destructure props in function signature
- Use TypeScript interfaces for prop types
- Prefix: `on` for handler props, `handle` for internal handlers
```

---

## Writing Guidelines

### Keep It Skimmable

- Short sections with clear headers
- Tables for quick reference
- Do/Don't examples side by side
- One-sentence rationale ("Why")

### Detected vs Recommended

- **Detected**: What the code does (descriptive)
- **Recommended**: What it should do (prescriptive)
- Mark status: Already followed / Suggested improvement

### Examples Over Explanations

- Show, don't tell
- Real patterns, simplified for clarity
- Avoid verbatim sensitive code
