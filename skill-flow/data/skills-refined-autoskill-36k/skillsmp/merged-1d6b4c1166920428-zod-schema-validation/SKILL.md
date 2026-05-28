---
name: zod-schema-validation
description: Use this skill for TypeScript-first schema validation and type inference with Zod, applicable for form validation, API contracts, and runtime type checking.
---

# Zod Schema Validation

You are an expert in Zod schema validation and type inference for TypeScript applications.

## Core Principles

- Utilize Zod for schema validation and type inference.
- Validate data at system boundaries (API, forms, external data).
- Leverage TypeScript type inference from Zod schemas.
- Implement early returns and guard clauses for validation errors.

## Quick Reference

```typescript
import { z } from "zod";

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date(),
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Validate data
const result = UserSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // Typed as User
} else {
  console.log(result.error.issues);
}
```

## Schema Design

### Basic Schema
```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date(),
});
```

### Best Practices
- Define schemas close to where they're used.
- Use `.infer` to derive TypeScript types.
- Compose schemas using `.extend()`, `.merge()`, `.pick()`, `.omit()`.
- Create reusable base schemas for common patterns.

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

## Form Integration

- Use Zod with react-hook-form via `@hookform/resolvers/zod`.
- Define form schemas that match your form structure.
- Handle validation errors in UI appropriately.
- Use `.partial()` for optional update forms.

## API Validation

- Validate request bodies in API routes.
- Validate query parameters and path params.
- Return structured error responses.
- Use discriminated unions for different response types.

## Error Handling

- Implement custom error messages for better UX.
- Use `.format()` for structured error output.
- Create custom error maps for i18n support.
- Handle nested object errors appropriately.

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
    children: z.array(CategorySchema),
  })
);
```

## Performance

- Precompile schemas that are used frequently.
- Avoid creating schemas inside render functions.
- Use `.passthrough()` or `.strict()` intentionally.
- Consider partial validation for large objects.

## Common Patterns

| Pattern          | Schema                                   |
| ---------------- | ---------------------------------------- |
| Non-empty string | `z.string().min(1)`                      |
| Positive integer | `z.number().int().positive()`            |
| URL string       | `z.string().url()`                       |
| ISO date string  | `z.string().datetime()`                  |
| UUID             | `z.string().uuid()`                      |
| Slug             | `z.string().regex(/^[a-z0-9-]+$/)`       |
| Phone            | `z.string().regex(/^\+?[1-9]\d{1,14}$/)` |
| Hex color        | `z.string().regex(/^#[0-9A-Fa-f]{6}$/)`  |

## Resources

- [Zod Documentation](https://zod.dev)
- [Zod GitHub](https://github.com/colinhacks/zod)
- [react-hook-form + Zod](https://react-hook-form.com/get-started#SchemaValidation)