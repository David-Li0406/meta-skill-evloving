---
name: pinpoint-typescript
description: Use this skill when fixing TypeScript compilation errors, implementing complex types, or when user mentions TypeScript/types/generics.
---

# PinPoint TypeScript Guide

## When to Use This Skill

Use this skill when:
- Fixing TypeScript compilation errors
- Implementing complex types or generics
- Dealing with optional properties and `exactOptionalPropertyTypes`
- Working with Drizzle ORM types
- Handling null/undefined safety
- User mentions: "TypeScript", "type error", "type guard", "optional", "nullable"

## Quick Reference

### Critical TypeScript Rules
1. **Strictest config**: No `any`, no `!`, no unsafe `as`
2. **Explicit return types**: Required for public functions
3. **Path aliases**: Use `~/` instead of relative imports
4. **Optional property assignment**: Use conditional spread, not direct assignment with undefined
5. **Type guards**: Write proper predicates for narrowing

### Common Fixes

**Optional Properties (exactOptionalPropertyTypes)**:
```typescript
// ✅ Correct: Conditional spread
const data = {
  id: uuid(),
  ...(name && { name }),
  ...(description && { description }),
};

// ❌ Wrong: Direct assignment
const data = { name: value }; // Error if value is undefined
```

## Core Safety Patterns

### Null Safety & Optional Chaining

```typescript
// ✅ Safe authentication check
const supabase = await createClient();
const { data: { user } } = await supabase.auth.getUser();

if (!user?.id) {
  throw new Error("Unauthorized");
}
const userId = user.id; // Now safe - TypeScript knows user is not null

// ✅ Safe array access
const firstItem = items[0]?.name ?? "No items";
const lastItem = items.at(-1)?.name ?? "No items";

// ✅ Safe object property access
const machineName = issue.machine?.name ?? "Unknown";
```