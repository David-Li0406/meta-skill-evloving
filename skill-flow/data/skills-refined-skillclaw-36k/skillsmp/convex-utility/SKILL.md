---
name: convex-utility
description: Skill for standardizing and accelerating Convex backend development with boilerplate generation and pattern enforcement.
---

# Convex Utility Skill

This skill enforces FlyerBoard's backend patterns for Convex mutations and queries.

## Core Patterns

### 1. Authentication Check
All mutations must verify the user's identity.
```typescript
const userId = await getDescopeUserId(ctx);
if (!userId) throw new Error("Must be logged in");
```

### 2. Soft Delete Filter
All queries fetching "active" flyers must filter out deleted records.
```typescript
.filter(q => q.neq(q.field("isDeleted"), true))
```

### 3. Ownership Verification
Modifying a resource requires checking the `userId`.
```typescript
const resource = await ctx.db.get(args.id);
if (resource.userId !== userId) throw new Error("Unauthorized");
```

## Scripts

### `generate-mutation` (via prompt instructions)
When asked to create a new Convex mutation, follow the template in `examples/mutation-template.ts`.

## Examples

### standard-mutation.ts
See `examples/standard-mutation.ts` for a complete implementation of a compliant mutation.

## Quality Standards
- No hard deletes.
- Always use `v.id("tableName")` for ID arguments.
- Return meaningful errors (e.g., "Not found", "Unauthorized").
