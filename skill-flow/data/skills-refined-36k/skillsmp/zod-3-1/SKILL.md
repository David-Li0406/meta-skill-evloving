---
name: zod-3
description: >
  Zod 3 validation schemas and patterns.
  Trigger: When creating Zod validation schemas for API input validation.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [api]
  auto_invoke: 'Creating Zod schemas'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Basic Schema (REQUIRED)

```typescript
import { z } from 'zod';

export const createClientSchema = z.object({
  companyName: z.string().min(1).max(100),
  contactName: z.string().min(1).max(100),
  email: z.string().email().optional().or(z.literal('')),
  phone: z.string().optional().or(z.literal('')),
  status: z.enum(['active', 'inactive', 'pending']),
  segment: z.string().optional().or(z.literal('')),
  tags: z.array(z.string()).optional(),
  notes: z.string().optional().or(z.literal('')),
});

export type CreateClientInput = z.infer<typeof createClientSchema>;
```

## String Validation

```typescript
z.string();
z.string().min(3); // Minimum length
z.string().max(100); // Maximum length
z.string().length(10); // Exact length
z.string().email(); // Email
z.string().url(); // URL
z.string().uuid(); // UUID
z.string().regex(/^[A-Z]/); // Regex
z.string().trim(); // Trim whitespace
z.string().optional(); // Optional
z.string().nullable(); // Nullable
z.string().default(''); // Default value
```

## Number Validation

```typescript
z.number();
z.number().min(0); // Minimum value
z.number().max(100); // Maximum value
z.number().int(); // Integer
z.number().positive(); // Positive
z.number().nonnegative(); // Non-negative
z.number().optional();
z.number().default(0);
```

## Boolean

```typescript
z.boolean();
z.boolean().optional();
z.boolean().default(false);
```

## Enums

```typescript
z.enum(['active', 'inactive', 'pending']);
z.enum(['active', 'inactive']).default('active');
```

## Arrays

```typescript
z.array(z.string()); // String array
z.array(z.string()).min(1); // Minimum items
z.array(z.string()).max(10); // Maximum items
z.array(z.string()).length(5); // Exact length
z.array(z.string()).optional();
z.array(z.string()).default([]);
```

## Objects

```typescript
z.object({
  name: z.string(),
  age: z.number().optional(),
});
z.object({}).strict(); // No extra fields allowed
z.object({}).passthrough(); // Allow extra fields
```

## Nested Objects

```typescript
z.object({
  user: z.object({
    name: z.string(),
    email: z.string().email(),
  }),
});
```

## Optional vs Nullable

```typescript
z.string().optional(); // undefined allowed
z.string().nullable(); // null allowed
z.string().optional().nullable(); // both allowed
z.string().or(z.literal('')); // empty string allowed
```

## Default Values

```typescript
z.string().default('default value');
z.number().default(0);
z.boolean().default(false);
z.array(z.string()).default([]);
```

## Refinement (Custom Validation)

```typescript
z.string().refine(val => val.length >= 3, 'Must be at least 3 characters');

// With async validation
z.string().refine(async val => await isUniqueEmail(val), 'Email already exists');

// Transform before validation
z.string().transform(val => val.toLowerCase());
```

## Union

```typescript
z.union([z.string(), z.number()]); // string OR number
z.discriminatedUnion('type', [
  z.object({ type: z.literal('a'), value: z.string() }),
  z.object({ type: z.literal('b'), value: z.number() }),
]);
```

## Literals

```typescript
z.literal('active');
z.literal(true);
z.literal(42);
z.array(z.literal('tag1', 'tag2', 'tag3'));
```

## Date Validation

```typescript
z.string().datetime(); // ISO datetime
z.string().date(); // YYYY-MM-DD
z.string().time(); // HH:mm:ss
```

## UUID

```typescript
z.string().uuid();
z.string().uuid().optional();
```

## Email Validation

```typescript
z.string().email();
z.string().email().optional().or(z.literal(''));
```

## Password Validation

```typescript
const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number');
```

## Query Params

```typescript
export const listClientsQuerySchema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(20),
  search: z.string().optional(),
  status: z.enum(['active', 'inactive', 'pending']).optional(),
  sortBy: z.string().default('createdAt'),
  sortOrder: z.enum(['asc', 'desc']).default('desc'),
});

export type ListClientsQuery = z.infer<typeof listClientsQuerySchema>;
```

## Validation in Express

```typescript
export const validateBody = <T>(schema: z.ZodSchema<T>) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        success: false,
        errors: result.error.errors,
      });
    }
    req.body = result.data;
    next();
  };
};

// Usage
router.post('/clients', validateBody(createClientSchema), createHandler);
```

## Parse and Type Inference

```typescript
// Infer type from schema
type CreateClientInput = z.infer<typeof createClientSchema>;

// Parse and get typed result
const result = createClientSchema.parse(req.body);
// result is typed as CreateClientInput

// Safe parse (no throw)
const result = createClientSchema.safeParse(req.body);
if (result.success) {
  const data = result.data;
} else {
  console.log(result.error.errors);
}
```

## Error Format

```typescript
{
  "success": false,
  "errors": [
    {
      "code": "invalid_type",
      "expected": "string",
      "received": "undefined",
      "path": ["companyName"],
      "message": "Required"
    }
  ]
}
```

## Related Skills

- `migestion-api` - API validation patterns
- `typescript` - TypeScript patterns
