---
name: zod
description: Zod v4 schema validation. Use for zod, schema, validation, parse, safeParse, infer, coerce, transform, refine, z.object, z.string, z.email, z.url
---

# Zod Schema Validation (v4)

This project uses **Zod v4**. Note the syntax differences from v3.

## Quick Start

```ts
import { z } from 'zod';

const UserSchema = z.object({
  email: z.email(),
  name: z.string().min(1),
  age: z.number().optional(),
});

type User = z.infer<typeof UserSchema>;

const result = UserSchema.safeParse(input);
if (result.success) {
  console.log(result.data);
} else {
  console.log(result.error);
}
```

## Primitives

```ts
z.string();
z.number();
z.boolean();
z.bigint();
z.date();
z.undefined();
z.null();
z.void();
z.any();
z.unknown();
z.never();
```

## String Formats (v4 Top-Level API)

Zod v4 uses top-level functions instead of method chaining:

```ts
// Zod v4 (use these)
z.email();
z.url();
z.uuid();
z.cuid();
z.cuid2();
z.ulid();
z.nanoid();
z.ipv4();
z.ipv6();
z.base64();
z.emoji();

// Deprecated (don't use)
z.string().email();
z.string().url();
z.string().uuid();
```

### ISO Date/Time Formats

```ts
z.iso.date(); // "2024-01-15"
z.iso.time(); // "14:30:00"
z.iso.datetime(); // "2024-01-15T14:30:00Z"
z.iso.duration(); // "P3Y6M4DT12H30M5S"
```

## String Constraints

```ts
z.string().min(1); // Non-empty
z.string().max(100); // Max length
z.string().length(5); // Exact length
z.string().regex(/^[a-z]+$/); // Pattern
z.string().trim(); // Trim whitespace
z.string().toLowerCase(); // Lowercase
z.string().toUpperCase(); // Uppercase
z.string().startsWith('https');
z.string().endsWith('.com');
z.string().includes('@');
```

## Number Constraints

```ts
z.number().min(0);
z.number().max(100);
z.number().int();
z.number().positive();
z.number().negative();
z.number().nonnegative();
z.number().nonpositive();
z.number().multipleOf(5);
z.number().finite();
z.number().safe(); // Safe integer range
```

## Objects

```ts
const User = z.object({
  id: z.string(),
  email: z.email(),
  age: z.number().optional(),
});

type User = z.infer<typeof User>;

// Modifiers
User.partial(); // All optional
User.required(); // All required
User.pick({ id: true, email: true });
User.omit({ age: true });
User.extend({ role: z.string() });
User.merge(OtherSchema);
User.passthrough(); // Allow extra keys
User.strict(); // Reject extra keys
User.strip(); // Remove extra keys
```

## Arrays

```ts
z.array(z.string());
z.array(z.number()).min(1); // Non-empty
z.array(z.number()).max(10);
z.array(z.number()).length(5);
z.array(z.number()).nonempty(); // Non-empty (typed)

// Tuple
z.tuple([z.string(), z.number()]);
z.tuple([z.string(), z.number()]).rest(z.boolean());
```

## Enums & Unions

```ts
// Native enum
z.enum(['admin', 'user', 'guest']);

// Union
z.union([z.string(), z.number()]);
z.string().or(z.number()); // Shorthand

// Discriminated union (better errors)
z.discriminatedUnion('type', [
  z.object({ type: z.literal('email'), email: z.email() }),
  z.object({ type: z.literal('phone'), phone: z.string() }),
]);

// Literal
z.literal('active');
z.literal(42);
z.literal(true);
```

## Records & Maps

```ts
// Record (string keys by default)
z.record(z.number()); // { [key: string]: number }
z.record(z.string(), z.number());

// Enum keys (v4: all keys required)
z.record(z.enum(['a', 'b']), z.number()); // { a: number, b: number }
z.partialRecord(z.enum(['a', 'b']), z.number()); // { a?: number, b?: number }

// Map
z.map(z.string(), z.number());
```

## Optional & Nullable

```ts
z.string().optional(); // string | undefined
z.string().nullable(); // string | null
z.string().nullish(); // string | null | undefined

// Defaults
z.string().default('hello');
z.number().default(0);

// Catch (use default on parse error)
z.string().catch('fallback');
```

## Coercion

```ts
z.coerce.string(); // Converts to string
z.coerce.number(); // Converts to number
z.coerce.boolean(); // Falsy -> false, truthy -> true
z.coerce.date(); // Converts to Date
z.coerce.bigint(); // Converts to BigInt
```

### String to Boolean (v4)

```ts
// Env-style boolean parsing
z.stringbool();

// Recognized values:
// true:  "true", "1", "yes", "on", "y", "enabled"
// false: "false", "0", "no", "off", "n", "disabled"

// Custom values
z.stringbool({
  truthy: ['yes', 'true'],
  falsy: ['no', 'false'],
});
```

## Transforms

```ts
// Transform output type
z.string().transform((val) => val.length); // string -> number
z.string().transform((val) => parseInt(val, 10));

// Overwrite (same type, introspectable)
z.number().overwrite((val) => val * 2);
z.string().overwrite((val) => val.trim());
```

## Refinements

```ts
// Simple refinement
z.string().refine((val) => val.includes('@'), {
  message: 'Must contain @',
});

// Multiple refinements
z.string()
  .refine((val) => val.length > 0, 'Required')
  .refine((val) => val.includes('@'), 'Must contain @');

// SuperRefine (custom errors)
z.string().superRefine((val, ctx) => {
  if (!val.includes('@')) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Must contain @',
    });
  }
});
```

## Parsing

```ts
const schema = z.string();

// Throws on error
schema.parse('hello'); // 'hello'
schema.parse(123); // throws ZodError

// Returns result object
schema.safeParse('hello'); // { success: true, data: 'hello' }
schema.safeParse(123); // { success: false, error: ZodError }

// Async
await schema.parseAsync('hello');
await schema.safeParseAsync('hello');
```

## Type Inference

```ts
const UserSchema = z.object({
  id: z.string(),
  email: z.email(),
});

type User = z.infer<typeof UserSchema>;
// { id: string; email: string }

// Input vs Output types (with transforms)
type UserInput = z.input<typeof UserSchema>;
type UserOutput = z.output<typeof UserSchema>;
```

## Common Patterns

### Form Validation

```ts
const LoginSchema = z.object({
  email: z.email(),
  password: z.string().min(8),
  rememberMe: z.boolean().default(false),
});
```

### API Response

```ts
const ApiResponse = z.object({
  data: z.unknown(),
  error: z.string().nullable(),
  status: z.enum(['success', 'error']),
});
```

### Environment Variables

```ts
const EnvSchema = z.object({
  DATABASE_URL: z.url(),
  PORT: z.coerce.number().default(3000),
  DEBUG: z.stringbool().default(false),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});
```

## Common Mistakes

| Mistake                      | Correct Pattern                    |
| ---------------------------- | ---------------------------------- |
| `z.string().email()`         | `z.email()` (v4 top-level)         |
| `z.string().url()`           | `z.url()` (v4 top-level)           |
| Using `parse` without catch  | Use `safeParse` for error handling |
| Forgetting `.optional()`     | Add when field may be undefined    |
| Using `any` for unknown data | Use `z.unknown()` instead          |

## Delegation

- **Schema design**: Ask user for field requirements
- **Complex validation**: Use `superRefine` for multi-field validation
- **Pattern discovery**: Use `Explore` agent to find existing schemas
