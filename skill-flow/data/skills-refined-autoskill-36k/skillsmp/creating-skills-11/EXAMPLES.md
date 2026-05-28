# Skill Examples

Complete, production-ready skill examples you can learn from or adapt.

---

## Example 1: Git Commit Skill

A simple, focused skill for generating commit messages.

```yaml
---
name: git-commit-message
description: Generate conventional commit messages following project standards. Use when committing code, writing commit messages, or asking about commit conventions.
allowed-tools: Bash(git:*), Read, Grep
---

# Git Commit Message Generator

## Overview
Generates conventional commit messages that follow project standards.

## Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

## Process

1. Run `git diff --staged` to see changes
2. Identify the primary change type
3. Determine scope (component/area affected)
4. Write concise subject (imperative mood, <50 chars)
5. Add body if changes need explanation

## Examples

**Simple fix:**
```
fix(auth): resolve token expiration check
```

**Feature with body:**
```
feat(api): add rate limiting to endpoints

Implements sliding window rate limiting with Redis backend.
Default: 100 requests per minute per API key.
```
```

---

## Example 2: Code Review Skill

A read-only analysis skill with tool restrictions.

```yaml
---
name: code-review
description: Review code for bugs, security issues, performance problems, and style violations. Use when reviewing PRs, auditing code, checking for vulnerabilities, or asking for code feedback.
allowed-tools: Read, Grep, Glob
---

# Code Review

## Overview
Provides comprehensive code review without modifying files.

## Review Checklist

### Correctness
- [ ] Logic errors
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] Types correct

### Security
- [ ] Input validation
- [ ] No SQL injection
- [ ] No XSS vulnerabilities
- [ ] Secrets not hardcoded

### Performance
- [ ] No unnecessary loops
- [ ] Efficient algorithms
- [ ] No memory leaks
- [ ] Proper async handling

### Maintainability
- [ ] Clear naming
- [ ] Reasonable complexity
- [ ] No code duplication
- [ ] Tests included

## Review Process

1. **Understand context** - Read related files to understand the change
2. **Check correctness** - Does it do what it claims?
3. **Check security** - Any vulnerabilities?
4. **Check performance** - Any bottlenecks?
5. **Check style** - Follows project conventions?

## Output Format

```markdown
## Code Review: [file/PR name]

### Summary
[1-2 sentence overview]

### Issues Found

#### Critical
- [Issue with file:line reference]

#### Warnings
- [Issue with file:line reference]

#### Suggestions
- [Improvement idea]

### Approval
[Approve / Request Changes / Needs Discussion]
```
```

---

## Example 3: Database Migration Skill

A domain expert skill with detailed knowledge.

```yaml
---
name: postgres-migrations
description: Create PostgreSQL migrations following project conventions. Use when creating tables, modifying schemas, writing migrations, or working with database changes.
---

# PostgreSQL Migrations

## Overview
Creates safe, reversible database migrations for PostgreSQL.

## Conventions

### File Naming
```
YYYYMMDDHHMMSS_description_in_snake_case.sql
```

### Migration Structure
```sql
-- Migration: [description]
-- Created: [timestamp]

-- Up Migration
BEGIN;

[DDL statements]

COMMIT;

-- Down Migration (for rollback)
-- BEGIN;
-- [Reverse DDL statements]
-- COMMIT;
```

## Best Practices

### Always Use TEXT Over VARCHAR
PostgreSQL treats TEXT and VARCHAR identically. VARCHAR(n) adds arbitrary limits that cause silent failures.

```sql
-- Bad
CREATE TABLE users (
  name VARCHAR(100)
);

-- Good
CREATE TABLE users (
  name TEXT NOT NULL
);
```

### Always Include NOT NULL
Explicit nullability prevents ambiguity.

```sql
-- Bad
CREATE TABLE orders (
  status TEXT
);

-- Good
CREATE TABLE orders (
  status TEXT NOT NULL DEFAULT 'pending'
);
```

### Add Indexes for Foreign Keys
PostgreSQL doesn't auto-index foreign keys.

```sql
CREATE TABLE order_items (
  order_id UUID NOT NULL REFERENCES orders(id),
  ...
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

## Common Patterns

### Add Column (Safe)
```sql
ALTER TABLE users ADD COLUMN phone TEXT;
```

### Add NOT NULL Column (Safe)
```sql
-- Step 1: Add nullable
ALTER TABLE users ADD COLUMN status TEXT;

-- Step 2: Backfill
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Step 3: Add constraint
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
```

### Create Enum
```sql
CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'shipped', 'delivered');
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| `VARCHAR(n)` | `TEXT` |
| Add NOT NULL without default | Add nullable, backfill, then constrain |
| Drop column in production | Add deprecated comment, remove in next release |
| Rename column directly | Add new, migrate data, drop old |
```

---

## Example 4: API Endpoint Skill

A code generation skill with templates.

```yaml
---
name: express-endpoint
description: Generate Express.js API endpoints with validation, error handling, and tests. Use when creating API routes, REST endpoints, or HTTP handlers.
---

# Express.js Endpoint Generator

## Overview
Creates production-ready Express endpoints following project patterns.

## Endpoint Structure

```
src/
├── routes/
│   └── [resource].routes.ts
├── handlers/
│   └── [resource].handler.ts
├── validators/
│   └── [resource].validator.ts
└── tests/
    └── [resource].test.ts
```

## Route Template

```typescript
// src/routes/[resource].routes.ts
import { Router } from 'express';
import { validate } from '../middleware/validate.js';
import { [Resource]Handler } from '../handlers/[resource].handler.js';
import { create[Resource]Schema, update[Resource]Schema } from '../validators/[resource].validator.js';

const router = Router();
const handler = new [Resource]Handler();

router.get('/', handler.list);
router.get('/:id', handler.get);
router.post('/', validate(create[Resource]Schema), handler.create);
router.put('/:id', validate(update[Resource]Schema), handler.update);
router.delete('/:id', handler.delete);

export default router;
```

## Handler Template

```typescript
// src/handlers/[resource].handler.ts
import { Request, Response, NextFunction } from 'express';
import { [Resource]Service } from '../services/[resource].service.js';

export class [Resource]Handler {
  private service = new [Resource]Service();

  list = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const items = await this.service.findAll();
      res.json({ data: items });
    } catch (error) {
      next(error);
    }
  };

  get = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const item = await this.service.findById(req.params.id);
      if (!item) {
        return res.status(404).json({ error: 'Not found' });
      }
      res.json({ data: item });
    } catch (error) {
      next(error);
    }
  };

  create = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const item = await this.service.create(req.body);
      res.status(201).json({ data: item });
    } catch (error) {
      next(error);
    }
  };
}
```

## Validator Template

```typescript
// src/validators/[resource].validator.ts
import { z } from 'zod';

export const create[Resource]Schema = z.object({
  name: z.string().min(1).max(255),
  // Add fields
});

export const update[Resource]Schema = create[Resource]Schema.partial();

export type Create[Resource]Input = z.infer<typeof create[Resource]Schema>;
export type Update[Resource]Input = z.infer<typeof update[Resource]Schema>;
```

## Generation Process

1. **Identify resource name** (singular, PascalCase)
2. **Define fields and types**
3. **Generate files** in correct locations
4. **Add route to app** in main router
5. **Create tests**
```

---

## Example 5: Multi-File Skill Structure

Shows how to organize a complex skill with progressive disclosure.

```
testing-skill/
├── SKILL.md              # Overview + quick start (shown below)
├── UNIT-TESTS.md         # Unit testing in detail
├── INTEGRATION-TESTS.md  # Integration testing guide
├── MOCKING.md            # Mocking strategies
├── COVERAGE.md           # Coverage requirements
└── scripts/
    └── run-tests.sh      # Test runner script
```

**SKILL.md:**

```yaml
---
name: testing-guide
description: Write and run tests for TypeScript projects. Use when creating unit tests, integration tests, mocking dependencies, improving coverage, or debugging test failures.
allowed-tools: Read, Bash(pnpm test:*, npx vitest:*)
---

# Testing Guide

## Overview
Comprehensive testing guidance for TypeScript projects using Vitest.

## Quick Start

```bash
# Run all tests
pnpm test

# Run specific file
npx vitest run path/to/file.test.ts

# Run with coverage
pnpm test:coverage
```

## Test File Location

Tests are co-located with source files:
```
src/
├── user.service.ts
├── user.service.test.ts    # <-- Test file
```

## Basic Test Structure

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { UserService } from './user.service.js';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  it('should create user', async () => {
    const user = await service.create({ name: 'Test' });
    expect(user.name).toBe('Test');
  });
});
```

## Detailed Guides

- [Unit Testing](UNIT-TESTS.md) - Testing individual functions/classes
- [Integration Testing](INTEGRATION-TESTS.md) - Testing components together
- [Mocking](MOCKING.md) - Mocking dependencies and external services
- [Coverage](COVERAGE.md) - Coverage requirements and reporting
```

---

## Key Takeaways

1. **Description is critical** - All examples have specific, trigger-rich descriptions
2. **Focused scope** - Each skill does one thing well
3. **Clear structure** - Consistent headings and organization
4. **Practical examples** - Concrete code, not abstract guidance
5. **Progressive disclosure** - Complex skills split into multiple files
6. **Appropriate restrictions** - Read-only skills use `allowed-tools`
