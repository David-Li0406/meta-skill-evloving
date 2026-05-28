---
name: zod-validation
description: Use this skill for TypeScript-first schema validation, enabling runtime type checking, form validation, and API contract validation with static type inference.
---

# Zod Validation Skill

This skill covers Zod v3+ patterns for building type-safe validation schemas for forms, APIs, and data parsing.

## Core Concepts

**Zod Benefits:**
- TypeScript-first schema validation
- Runtime type checking
- Type inference from schemas
- Composable and reusable schemas
- Rich error messages
- Zero dependencies

## When to Use
- Form validation with type-safe data
- API request/response validation
- Environment variable validation
- Runtime type checking with TypeScript inference
- tRPC procedure inputs/outputs
- Database schema validation (Drizzle, Prisma)

## Quick Start

```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(18).optional(),
  role: z.enum(['user', 'admin']).default('user'),
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Validate data
const result = UserSchema.safeParse(data);
if (result.success) {
  const user: User = result.data;
} else {
  console.error(result.error.format());
}
```

## Schema Primitives

### Basic Types

```typescript
// Strings
const nameSchema = z.string().min(2).max(50).trim();
const urlSchema = z.string().url();
const uuidSchema = z.string().uuid();

// Numbers
const ageSchema = z.number().int().positive().min(0).max(120);
const priceSchema = z.number().positive().multipleOf(0.01); // Currency precision

// Booleans
const isActiveSchema = z.boolean();

// Dates
const createdAtSchema = z.date().min(new Date('2020-01-01')).max(new Date());
```

## Validation Patterns

### Safe Parsing
```typescript
const result = UserSchema.safeParse(data);
if (!result.success) {
  console.error(result.error.format());
  return;
}
// result.data is typed as User
```

### Transform and Refine
```typescript
const schema = z.string()
  .transform((val) => val.trim().toLowerCase())
  .refine((val) => val.length > 0, 'Cannot be empty');
```

## Error Handling

- Implement custom error messages for better UX
- Use `.format()` for structured error output
- Handle nested object errors appropriately

## Advanced Patterns

### Discriminated Unions
```typescript
const ResultSchema = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: UserSchema }),
  z.object({ status: z.literal('error'), message: z.string() }),
]);
```

### Recursive Schemas
```typescript
const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    children: z.array(CategorySchema).optional(),
  })
);
```