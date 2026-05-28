# Rules Directory Guide

Complete documentation for Claude Code's `.claude/rules/` directory system.

## Overview

Rules are modular memory files that load conditionally based on file patterns. They allow focused, context-specific instructions without bloating your main CLAUDE.md.

## Directory Structure

```
.claude/
  rules/
    react-components.md     # React component conventions
    api-routes.md           # API route patterns
    database.md             # Database and migration rules
    testing.md              # Test file conventions
    security.md             # Security-critical patterns
```

## Rule File Anatomy

Every rule file has YAML frontmatter and markdown content:

```markdown
---
globs: ["src/components/**/*.tsx", "src/ui/**/*.tsx"]
description: React component conventions and patterns
alwaysApply: false
---

# React Components

## Naming
- Component files: PascalCase (`UserProfile.tsx`)
- Hook files: camelCase with `use` prefix (`useAuth.ts`)

## Structure
```tsx
// 1. Imports
import { useState } from 'react';
import { Button } from '@/components/ui';

// 2. Types
interface Props {
  userId: string;
}

// 3. Component
export function UserProfile({ userId }: Props) {
  // 4. Hooks
  // 5. Handlers
  // 6. Render
}
```

## Testing
Every component needs a corresponding `.test.tsx` file.
```

## Frontmatter Options

### `globs` (required)

File patterns that trigger this rule:

```yaml
# Single pattern
globs: "src/components/**/*.tsx"

# Multiple patterns (array)
globs:
  - "src/components/**/*.tsx"
  - "src/ui/**/*.tsx"

# Shorthand array
globs: ["**/*.test.ts", "**/*.spec.ts"]
```

### Glob Pattern Syntax

| Pattern | Matches |
|---------|---------|
| `*.ts` | TypeScript files in current directory |
| `**/*.ts` | TypeScript files anywhere |
| `src/**/*` | All files under src/ |
| `src/components/**/*.tsx` | TSX files in components tree |
| `*.{ts,tsx}` | Both .ts and .tsx files |
| `!**/*.test.ts` | Exclude test files |

### `description` (optional)

Brief description of what this rule covers:

```yaml
description: Conventions for React components in this project
```

Used for documentation and debugging.

### `alwaysApply` (optional)

Whether to load this rule regardless of file context:

```yaml
alwaysApply: false   # Only when glob matches (default)
alwaysApply: true    # Always load this rule
```

Use `alwaysApply: true` sparingly - it defeats the purpose of conditional rules.

## When Rules Load

Rules load when Claude is working with files matching the glob patterns:

1. **Reading a file** - Rule loads if file matches glob
2. **Writing a file** - Rule loads if target path matches
3. **Editing a file** - Rule loads if file being edited matches
4. **Discussing a file** - Rule loads if `@file` reference matches

### Example Loading Scenarios

```yaml
# rules/api-routes.md
globs: ["src/routes/**/*.ts", "src/api/**/*.ts"]
```

**Loads when:**
- Reading `src/routes/users.ts`
- Creating `src/api/auth.ts`
- Discussing `@src/routes/products.ts`

**Does NOT load when:**
- Working on `src/components/Button.tsx`
- Editing `package.json`
- General conversation without file context

## Rule Priority

When multiple rules match:

1. **All matching rules load** - Not mutually exclusive
2. **Later files override earlier** - Alphabetical order matters
3. **More specific wins** - Detailed rules override general

### Ordering Strategy

Use numeric prefixes for explicit ordering:

```
.claude/rules/
  00-globals.md        # Loads first (alwaysApply: true)
  10-typescript.md     # General TS rules
  20-react.md          # React-specific (overrides TS where needed)
  30-testing.md        # Test conventions
  90-security.md       # Security overrides everything
```

## Common Rule Patterns

### Component Rules

```markdown
---
globs: ["src/components/**/*.tsx"]
description: React component patterns
---

# Component Conventions

## File Structure
Each component directory contains:
- `ComponentName.tsx` - Main component
- `ComponentName.test.tsx` - Tests
- `index.ts` - Re-export
- `types.ts` - Type definitions (if needed)

## Props
- Use interface for props
- Destructure in function signature
- Document complex props with JSDoc

## State
- Prefer hooks over class state
- Extract complex logic to custom hooks
- Use React Query for server state
```

### API Route Rules

```markdown
---
globs: ["src/routes/**/*.ts", "server/api/**/*.ts"]
description: API route conventions
---

# API Routes

## Structure
```typescript
// Route handler pattern
export async function GET(request: Request) {
  // 1. Auth check
  const user = await requireAuth(request);

  // 2. Validation
  const params = validateParams(request);

  // 3. Business logic (via service)
  const result = await userService.getUser(params.id);

  // 4. Response
  return Response.json(result);
}
```

## Error Handling
Always use `AppError` with appropriate status codes:
```typescript
throw new AppError('User not found', 'USER_NOT_FOUND', 404);
```

## Pagination
Use standard query params: `?page=1&limit=20`
```

### Database Rules

```markdown
---
globs: ["src/db/**/*.ts", "**/*.sql", "drizzle/**/*"]
description: Database and Drizzle ORM conventions
---

# Database Conventions

## Schema Changes
1. Edit schema in `src/db/schema/`
2. Generate migration: `bun db:generate`
3. Review migration SQL
4. Apply: `bun db:migrate`

## Queries
- Use Drizzle query builder, not raw SQL
- Complex queries go in `src/db/queries/`
- Always use transactions for multi-step operations

## Naming
- Tables: snake_case, plural (`user_profiles`)
- Columns: snake_case (`created_at`)
- Indexes: `idx_{table}_{columns}`
```

### Testing Rules

```markdown
---
globs: ["**/*.test.ts", "**/*.test.tsx", "**/*.spec.ts"]
description: Test file conventions
---

# Testing Conventions

## File Organization
Tests live next to source files:
```
UserProfile.tsx
UserProfile.test.tsx
```

## Test Structure
```typescript
describe('ComponentName', () => {
  describe('feature or method', () => {
    it('should do expected behavior', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

## Assertions
- Use Bun's built-in test assertions
- Prefer `expect(x).toBe(y)` over `assert(x === y)`
- One assertion per test when possible

## Mocking
- Never mock database - use test database
- Mock external APIs with MSW
- Use factories for test data
```

### Security Rules

```markdown
---
globs: ["**/*.ts", "**/*.tsx"]
description: Security patterns and requirements
alwaysApply: false
---

# Security Requirements

## Authentication
- All API routes require `requireAuth` middleware
- Never trust client-side auth state
- Session tokens expire after 24 hours

## Authorization
- Check permissions in route handlers
- Use `requireRole('admin')` for admin routes
- Never expose user IDs in URLs without auth

## Data Validation
- Validate ALL input with Zod schemas
- Sanitize before database queries
- Never interpolate strings into SQL

## Sensitive Data
- Never log passwords, tokens, or PII
- Use environment variables for secrets
- Encrypt sensitive fields in database
```

### Migration Rules

```markdown
---
globs: ["drizzle/migrations/**/*.ts", "src/db/migrations/**/*.ts"]
description: Database migration conventions
---

# Migration Conventions

## Naming
`NNNN_description.ts` where NNNN is sequence number

## Structure
```typescript
export async function up(db: Database) {
  // Forward migration
}

export async function down(db: Database) {
  // Rollback migration
}
```

## Rules
1. Always include `down` migration
2. Never modify existing migrations
3. Test migrations on a copy of prod data
4. Keep migrations atomic (one change each)
```

## Organization Strategies

### By Layer

```
.claude/rules/
  frontend/
    components.md
    hooks.md
    pages.md
  backend/
    routes.md
    services.md
    database.md
  shared/
    types.md
    utils.md
```

Note: Only top-level files in `rules/` are read. Subdirectories require flat structure.

### By Concern

```
.claude/rules/
  styling.md         # CSS, Tailwind
  state.md           # State management
  routing.md         # Router patterns
  forms.md           # Form handling
  errors.md          # Error handling
```

### By Tech

```
.claude/rules/
  react.md
  typescript.md
  drizzle.md
  playwright.md
  tailwind.md
```

## Advanced Patterns

### Exclusive Rules

When rules shouldn't combine:

```markdown
---
globs: ["src/legacy/**/*"]
description: Legacy code patterns (different from modern)
---

# Legacy Code

> Note: These patterns ONLY apply to legacy code.
> Modern code in src/ uses different patterns.

## Key Differences
- Uses class components, not hooks
- jQuery for DOM manipulation
- Callback-based async
```

### Inheritance Pattern

Base rule with specific overrides:

```markdown
# rules/00-base-typescript.md
---
globs: ["**/*.ts", "**/*.tsx"]
alwaysApply: false
---

# TypeScript Base

Standard TypeScript conventions...

---

# rules/20-react-typescript.md
---
globs: ["src/components/**/*.tsx"]
---

# React TypeScript

Extends base TypeScript with React-specific patterns...

When this rule loads, both apply (React overrides base where conflicting).
```

### Conditional Patterns

```markdown
---
globs: ["src/features/payments/**/*"]
description: Payment feature - extra security requirements
---

# Payment Feature

## Additional Security
This code handles payments. Extra requirements:

1. Log all payment attempts
2. Require 2FA for amount > $1000
3. Rate limit to 10 attempts per hour
4. Validate card details server-side only
```

## Troubleshooting

### Rule Not Loading

1. **Check glob syntax** - Use correct pattern format
2. **Verify file location** - Must be in `.claude/rules/`
3. **Check frontmatter** - Valid YAML with `---` delimiters
4. **Restart Claude Code** - Rules cached on startup

### Multiple Rules Conflicting

1. **Use numeric prefixes** - Control load order
2. **Be specific** - Narrow globs reduce overlap
3. **Explicit overrides** - State when rule supersedes another

### Rules Too Large

1. **Split by concern** - One topic per rule
2. **Use alwaysApply sparingly** - Avoid global rules
3. **Reference docs** - Link instead of duplicating

## Best Practices

1. **One concern per rule** - Keep focused
2. **Specific globs** - Narrow is better than broad
3. **Descriptive names** - Self-documenting filenames
4. **Regular review** - Update when patterns change
5. **Version control** - Commit rules with code
6. **Team alignment** - Discuss rules in code review
