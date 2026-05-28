---
name: typescript-strict
description: Use this skill when writing any TypeScript code to enforce strict type safety and best practices.
---

# TypeScript Strict Mode

## Core Rules

1. **No `any`** - ever. Use `unknown` if type is truly unknown.
2. **No type assertions** (`as Type`) without justification.
3. **Prefer `type` over `interface`** for data structures.
4. **Reserve `interface`** for behavior contracts only.

---

## Schema Organization

### Organize Schemas by Usage

**Common patterns:**
- Centralized: `src/schemas/` for shared schemas.
- Co-located: Near the modules that use them.
- Layered: Separate by architectural layer (if using layered/hexagonal architecture).

**Key principle:** Avoid duplicating the same validation logic across multiple files.

### Gotcha: Schema Duplication

**Common anti-pattern:**

Defining the same schema in multiple places:
- Validation logic duplicated across endpoints.
- Same business rules defined in multiple adapters.
- Type definitions not shared.

**Why This Is Wrong:**
- ❌ Duplication creates multiple sources of truth.
- ❌ Changes require updating multiple files.
- ❌ Breaks DRY principle at the knowledge level.
- ❌ Domain logic leaks into infrastructure code.

**Solution:**

```typescript
// ✅ CORRECT - Define schema once, import everywhere
// src/schemas/user-requests.ts
import { z } from 'zod';

export const CreateUserRequestSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});

export type CreateUserRequest = z.infer<typeof CreateUserRequestSchema>;
```

```typescript
// Use in multiple places
import { CreateUserRequestSchema } from '../schemas/user-requests.js';

// Express endpoint
app.post('/users', (req, res) => {
  const result = CreateUserRequestSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ error: result.error });
  }
  // Use result.data (validated)
});

// GraphQL resolver
const createUser = (input: unknown) => {
  const validated = CreateUserRequestSchema.parse(input);
  return userService.create(validated);
};
```

**Key Benefits:**
- ✅ Single source of truth for validation.
- ✅ Schema changes propagate everywhere automatically.
- ✅ Type safety maintained across codebase.
- ✅ DRY principle at knowledge level.

**Remember:** If validation logic is duplicated, extract it into a shared schema.

---

## Dependency Injection Pattern

### Inject Dependencies, Don't Create Them

**The Rule:**
- Dependencies are always injected via parameters.
- Never use `new` to create dependencies.