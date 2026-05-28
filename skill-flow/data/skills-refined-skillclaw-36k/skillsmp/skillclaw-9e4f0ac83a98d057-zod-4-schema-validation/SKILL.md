---
name: zod-4-schema-validation
description: Use this skill when creating or updating Zod v4 schemas for validation and parsing, including migration patterns from v3.
---

# Zod 4 Schema Validation Patterns

## Breaking Changes from Zod 3

```typescript
// ❌ Zod 3 (OLD)
z.string().email();
z.string().uuid();
z.string().url();
z.string().nonempty();
z.object({ name: z.string() }).required_error('Required');

// ✅ Zod 4 (NEW)
z.email();
z.uuid();
z.url();
z.string().min(1);
z.object({ name: z.string() }, { error: 'Required' });
```

## Basic Schemas

```typescript
import { z } from 'zod';

// Primitives
const stringSchema = z.string();
const numberSchema = z.number();
const booleanSchema = z.boolean();
const dateSchema = z.date();

// Top-level validators (Zod 4)
const emailSchema = z.email();
const uuidSchema = z.uuid();
const urlSchema = z.url();

// With constraints
const nameSchema = z.string().min(1).max(100);
const ageSchema = z.number().int().positive().max(150);
const priceSchema = z.number().min(0).multipleOf(0.01);
```

## Object Schemas

```typescript
const userSchema = z.object({
  id: z.uuid(),
  email: z.email({ error: 'Invalid email address' }),
  name: z.string().min(1, { error: 'Name is required' }),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'guest']),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

type User = z.infer<typeof userSchema>;

// Parsing
const user = userSchema.parse(data); // Throws on error
const result = userSchema.safeParse(data); // Returns { success, data/error }

if (result.success) {
  console.log(result.data);
} else {
  console.log(result.error.issues);
}
```

## Arrays and Records

```typescript
// Arrays
const tagsSchema = z.array(z.string()).min(1).max(10);
const numbersSchema = z.array(z.number()).nonempty();

// Records (objects with dynamic keys)
const scoresSchema = z.record(z.string(), z.number());
// { [key: string]: number }

// Tuples
const coordinatesSchema = z.tuple([z.number(), z.number()]);
// [number, number]
```

## Unions and Discriminated Unions

```typescript
// Simple union
const stringOrNumber = z.union([z.string(), z.number()]);

// Discriminated union (more efficient)
const resultSchema = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: z.unknown() }),
  z.object({ status: z.literal('error'), error: z.string() }),
]);
```

## Transformations

```typescript
// Transform during parsing
const lowercaseEmail = z.email().transform((val) => val.toLowerCase());
```