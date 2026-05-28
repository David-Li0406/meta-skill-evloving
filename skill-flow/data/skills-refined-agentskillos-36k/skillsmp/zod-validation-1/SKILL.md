---
name: zod-validation
description: Type-safe schema validation with Zod for runtime data validation, form handling, and API contracts
---

# Zod Validation

This skill covers Zod v3+ patterns for building type-safe validation schemas for forms, APIs, and data parsing.

## Core Concepts

**Zod Benefits:**
- TypeScript-first schema validation
- Runtime type checking
- Type inference from schemas
- Composable and reusable schemas
- Rich error messages
- Zero dependencies

**Key Terms:**
- **Schema**: Validation definition (z.object, z.string, etc.)
- **Parse**: Validate and return typed data
- **SafeParse**: Validate without throwing errors
- **Transform**: Convert data after validation
- **Refine**: Custom validation logic

## Installation

```bash
npm install zod
```

## Basic Types

### Primitives

```typescript
import { z } from "zod";

// String
const nameSchema = z.string();
const emailSchema = z.string().email();
const urlSchema = z.string().url();
const uuidSchema = z.string().uuid();

// Number
const ageSchema = z.number();
const priceSchema = z.number().positive();
const scoreSchema = z.number().min(0).max(100);
const integerSchema = z.number().int();

// Boolean
const agreedSchema = z.boolean();

// Date
const birthDateSchema = z.date();
const futureSchema = z.date().min(new Date());

// BigInt
const bigNumSchema = z.bigint();

// Symbol
const symSchema = z.symbol();

// Undefined, Null, Void
const undefinedSchema = z.undefined();
const nullSchema = z.null();
const voidSchema = z.void();

// Any, Unknown, Never
const anySchema = z.any(); // ⚠️ Avoid if possible
const unknownSchema = z.unknown();
const neverSchema = z.never();
```

### String Validations

```typescript
const schema = z.string()
  .min(3, "Must be at least 3 characters")
  .max(50, "Must be at most 50 characters")
  .email("Invalid email address")
  .url("Invalid URL")
  .uuid("Invalid UUID")
  .regex(/^[a-z0-9_]+$/, "Only lowercase letters, numbers, and underscores")
  .startsWith("https://", "Must start with https://")
  .endsWith(".com", "Must end with .com")
  .includes("@", "Must include @")
  .trim() // Remove whitespace
  .toLowerCase() // Convert to lowercase
  .toUpperCase(); // Convert to uppercase

// Custom error messages
const emailSchema = z.string().email({
  message: "Please enter a valid email address",
});

// Length
const exactLength = z.string().length(5, "Must be exactly 5 characters");

// Date strings
const dateString = z.string().datetime(); // ISO 8601
const dateOnly = z.string().date(); // YYYY-MM-DD
const timeOnly = z.string().time(); // HH:mm:ss

// IP addresses
const ipv4 = z.string().ip({ version: "v4" });
const ipv6 = z.string().ip({ version: "v6" });
```

### Number Validations

```typescript
const schema = z.number()
  .min(0, "Must be at least 0")
  .max(100, "Must be at most 100")
  .positive("Must be positive")
  .negative("Must be negative")
  .nonnegative("Must be 0 or greater")
  .nonpositive("Must be 0 or less")
  .int("Must be an integer")
  .multipleOf(5, "Must be a multiple of 5")
  .finite("Must be finite")
  .safe("Must be a safe integer");

// Coerce string to number
const coercedNumber = z.coerce.number(); // "123" → 123
```

## Object Schemas

### Basic Objects

```typescript
const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  age: z.number().int().min(0).max(120),
  verified: z.boolean(),
  role: z.enum(["ADMIN", "USER", "GUEST"]),
  createdAt: z.date(),
});

// Type inference
type User = z.infer<typeof userSchema>;
// {
//   id: string;
//   email: string;
//   name: string;
//   age: number;
//   verified: boolean;
//   role: "ADMIN" | "USER" | "GUEST";
//   createdAt: Date;
// }
```

### Optional and Nullable

```typescript
const schema = z.object({
  // Optional (can be undefined)
  bio: z.string().optional(),
  
  // Nullable (can be null)
  avatar: z.string().url().nullable(),
  
  // Nullable and optional (can be null or undefined)
  middleName: z.string().nullable().optional(),
  
  // With default value
  role: z.string().default("USER"),
  
  // Default from function
  createdAt: z.date().default(() => new Date()),
});
```

### Nested Objects

```typescript
const addressSchema = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string().length(2),
  zipCode: z.string().regex(/^\d{5}$/),
});

const userSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  address: addressSchema,
  // Or inline
  settings: z.object({
    notifications: z.boolean(),
    theme: z.enum(["light", "dark"]),
  }),
});
```

### Partial, Required, Pick, Omit

```typescript
const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string(),
  bio: z.string().optional(),
});

// Make all fields optional
const partialUser = userSchema.partial();
type PartialUser = z.infer<typeof partialUser>;
// { id?: string; email?: string; name?: string; bio?: string }

// Make all fields required (remove optional)
const requiredUser = userSchema.required();

// Pick specific fields
const userCredentials = userSchema.pick({ email: true, password: true });

// Omit fields
const publicUser = userSchema.omit({ password: true });

// Make specific fields optional
const updateSchema = userSchema.partial({ bio: true });
```

### Extend and Merge

```typescript
const baseSchema = z.object({
  id: z.string(),
  createdAt: z.date(),
});

// Extend (adds fields)
const userSchema = baseSchema.extend({
  email: z.string().email(),
  name: z.string(),
});

// Merge (combines schemas)
const timestampSchema = z.object({
  createdAt: z.date(),
  updatedAt: z.date(),
});

const fullSchema = userSchema.merge(timestampSchema);
```

## Arrays and Tuples

### Arrays

```typescript
// Array of strings
const tagsSchema = z.array(z.string());

// Array with constraints
const schema = z.array(z.string())
  .min(1, "At least one tag required")
  .max(5, "Maximum 5 tags allowed")
  .nonempty("Array cannot be empty");

// Array of objects
const usersSchema = z.array(
  z.object({
    id: z.string(),
    name: z.string(),
  })
);

// Type inference
type Users = z.infer<typeof usersSchema>;
// Array<{ id: string; name: string }>
```

### Tuples

```typescript
// Fixed-length array with specific types
const coordinatesSchema = z.tuple([
  z.number(), // latitude
  z.number(), // longitude
]);

type Coordinates = z.infer<typeof coordinatesSchema>;
// [number, number]

// With rest parameters
const mixedSchema = z.tuple([
  z.string(), // first element is string
  z.number(), // second element is number
]).rest(z.boolean()); // rest are booleans

// ["hello", 42, true, false, true]
```

## Enums and Literals

### Enums

```typescript
// Native enum
const schema = z.enum(["ADMIN", "USER", "GUEST"]);

type Role = z.infer<typeof schema>;
// "ADMIN" | "USER" | "GUEST"

// Access enum values
schema.enum.ADMIN; // "ADMIN"
schema.options; // ["ADMIN", "USER", "GUEST"]

// TypeScript enum
enum UserRole {
  ADMIN = "ADMIN",
  USER = "USER",
  GUEST = "GUEST",
}

const roleSchema = z.nativeEnum(UserRole);
```

### Literals

```typescript
// Single literal value
const trueSchema = z.literal(true);
const adminSchema = z.literal("ADMIN");
const numberSchema = z.literal(42);

// Use with union for multiple values
const statusSchema = z.union([
  z.literal("pending"),
  z.literal("approved"),
  z.literal("rejected"),
]);

// Or use enum
const statusEnum = z.enum(["pending", "approved", "rejected"]);
```

## Unions and Discriminated Unions

### Basic Unions

```typescript
// String or number
const idSchema = z.union([z.string(), z.number()]);

// Null or string
const nullableString = z.union([z.string(), z.null()]);
// Or use .nullable()
const nullableString2 = z.string().nullable();
```

### Discriminated Unions

```typescript
// Better type inference for unions
const eventSchema = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("click"),
    x: z.number(),
    y: z.number(),
  }),
  z.object({
    type: z.literal("keypress"),
    key: z.string(),
  }),
  z.object({
    type: z.literal("focus"),
    element: z.string(),
  }),
]);

type Event = z.infer<typeof eventSchema>;
// { type: "click"; x: number; y: number }
// | { type: "keypress"; key: string }
// | { type: "focus"; element: string }

// TypeScript knows which fields are available based on type
function handleEvent(event: Event) {
  if (event.type === "click") {
    console.log(event.x, event.y); // TypeScript knows x and y exist
  } else if (event.type === "keypress") {
    console.log(event.key); // TypeScript knows key exists
  }
}
```

## Custom Validation

### Refine

```typescript
// Single refinement
const passwordSchema = z
  .string()
  .min(8)
  .refine(
    (password) => /[A-Z]/.test(password),
    { message: "Password must contain an uppercase letter" }
  )
  .refine(
    (password) => /[a-z]/.test(password),
    { message: "Password must contain a lowercase letter" }
  )
  .refine(
    (password) => /[0-9]/.test(password),
    { message: "Password must contain a number" }
  );

// Multi-field refinement
const signupSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .refine(
    (data) => data.password === data.confirmPassword,
    {
      message: "Passwords don't match",
      path: ["confirmPassword"], // Error attached to this field
    }
  );

// Async refinement
const emailSchema = z.string().email().refine(
  async (email) => {
    const user = await db.user.findUnique({ where: { email } });
    return !user; // true if email is available
  },
  { message: "Email already registered" }
);
```

### Transform

```typescript
// Transform after validation
const trimmedString = z.string().transform((str) => str.trim());

const numberFromString = z.string().transform((str) => parseInt(str, 10));

// Or use coerce
const coercedNumber = z.coerce.number(); // "123" → 123

// Complex transformation
const userSchema = z
  .object({
    email: z.string().email(),
    name: z.string(),
  })
  .transform((data) => ({
    ...data,
    email: data.email.toLowerCase(),
    displayName: data.name.toUpperCase(),
  }));

// Async transform
const uploadSchema = z
  .instanceof(File)
  .transform(async (file) => {
    const url = await uploadToS3(file);
    return { url, size: file.size };
  });
```

### Superrefine (Advanced)

```typescript
const schema = z.object({
  age: z.number(),
  hasGuardian: z.boolean(),
  guardianName: z.string().optional(),
}).superRefine((data, ctx) => {
  if (data.age < 18 && !data.hasGuardian) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Guardian required for users under 18",
      path: ["hasGuardian"],
    });
  }
  
  if (data.hasGuardian && !data.guardianName) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Guardian name is required",
      path: ["guardianName"],
    });
  }
});
```

## Parsing and Validation

### Parse (Throws on Error)

```typescript
const userSchema = z.object({
  email: z.string().email(),
  age: z.number(),
});

try {
  const user = userSchema.parse({
    email: "user@example.com",
    age: 25,
  });
  // user is typed as { email: string; age: number }
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error(error.errors);
  }
}
```

### SafeParse (Returns Result Object)

```typescript
const result = userSchema.safeParse({
  email: "invalid",
  age: "not a number",
});

if (result.success) {
  const user = result.data;
  // user is typed correctly
} else {
  const errors = result.error.errors;
  // [
  //   {
  //     code: "invalid_string",
  //     message: "Invalid email",
  //     path: ["email"],
  //   },
  //   {
  //     code: "invalid_type",
  //     message: "Expected number, received string",
  //     path: ["age"],
  //   }
  // ]
}
```

### Async Parsing

```typescript
// For async transforms or refinements
const result = await schema.parseAsync(data);
const result = await schema.safeParseAsync(data);
```

## Error Handling

### Error Structure

```typescript
try {
  userSchema.parse(invalidData);
} catch (error) {
  if (error instanceof z.ZodError) {
    // error.errors is an array of issues
    error.errors.forEach((issue) => {
      console.log(issue.path); // ["email"]
      console.log(issue.message); // "Invalid email"
      console.log(issue.code); // "invalid_string"
    });
    
    // Formatted errors
    const formatted = error.format();
    // {
    //   email: { _errors: ["Invalid email"] },
    //   age: { _errors: ["Expected number, received string"] }
    // }
    
    // Flattened errors
    const flattened = error.flatten();
    // {
    //   formErrors: [],
    //   fieldErrors: {
    //     email: ["Invalid email"],
    //     age: ["Expected number, received string"]
    //   }
    // }
  }
}
```

### Custom Error Messages

```typescript
const schema = z.object({
  email: z.string({
    required_error: "Email is required",
    invalid_type_error: "Email must be a string",
  }).email("Please enter a valid email address"),
  
  age: z.number({
    required_error: "Age is required",
    invalid_type_error: "Age must be a number",
  }).min(18, "Must be at least 18 years old"),
});

// Global error map
z.setErrorMap((issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    if (issue.expected === "string") {
      return { message: "This field must be text" };
    }
  }
  return { message: ctx.defaultError };
});
```

## Reusable Schemas

### Schema Composition

```typescript
// Base schemas
const emailSchema = z.string().email();
const passwordSchema = z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/);
const timestampSchema = z.object({
  createdAt: z.date().default(() => new Date()),
  updatedAt: z.date().default(() => new Date()),
});

// Compose into larger schemas
const loginSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
});

const userSchema = z.object({
  id: z.string().uuid(),
  email: emailSchema,
  name: z.string(),
}).merge(timestampSchema);
```

### Schema Factory

```typescript
// Generic pagination schema
function paginatedSchema<T extends z.ZodTypeAny>(itemSchema: T) {
  return z.object({
    items: z.array(itemSchema),
    total: z.number(),
    page: z.number(),
    pageSize: z.number(),
  });
}

// Usage
const userSchema = z.object({ id: z.string(), name: z.string() });
const paginatedUsers = paginatedSchema(userSchema);

type PaginatedUsers = z.infer<typeof paginatedUsers>;
// {
//   items: Array<{ id: string; name: string }>;
//   total: number;
//   page: number;
//   pageSize: number;
// }
```

### Shared Validation Schemas

```typescript
// packages/core/src/schemas.ts
export const emailSchema = z.string().email();
export const phoneSchema = z.string().regex(/^\+?[1-9]\d{1,14}$/);
export const uuidSchema = z.string().uuid();

export const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(10),
});

export const userCreateSchema = z.object({
  email: emailSchema,
  name: z.string().min(1).max(100),
  phone: phoneSchema.optional(),
});

export const userUpdateSchema = userCreateSchema.partial();

// Use in multiple packages
// packages/functions/src/user/router.ts
import { userCreateSchema } from "@myapp/core";

export const userRouter = router({
  create: protectedProcedure
    .input(userCreateSchema)
    .mutation(async ({ input }) => {
      // input is typed from schema
    }),
});
```

## Advanced Patterns

### Branded Types

```typescript
// Create nominal types
const userId = z.string().uuid().brand("UserId");
const email = z.string().email().brand("Email");

type UserId = z.infer<typeof userId>; // string & { __brand: "UserId" }
type Email = z.infer<typeof email>; // string & { __brand: "Email" }

// Prevents mixing different string types
function getUser(id: UserId) { /* ... */ }

const validId = userId.parse("550e8400-e29b-41d4-a716-446655440000");
getUser(validId); // ✓ OK

const regularString = "550e8400-e29b-41d4-a716-446655440000";
getUser(regularString); // ✗ Type error
```

### Lazy Schemas (Recursive)

```typescript
// For recursive types
type Category = {
  name: string;
  subcategories: Category[];
};

const categorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(categorySchema),
  })
);
```

### Catch (Fallback Values)

```typescript
// Provide fallback on parse failure
const schema = z.string().catch("default value");

const result = schema.parse(123); // "default value"

// With function
const dateSchema = z.date().catch(() => new Date());
```

### Pipe (Chain Schemas)

```typescript
// Parse then transform
const schema = z.string().pipe(z.coerce.number());

const result = schema.parse("123"); // 123 (number)

// Multi-step validation
const trimmedEmail = z
  .string()
  .transform((s) => s.trim())
  .pipe(z.string().email());
```

## Integration Patterns

### With Conform (Forms)

```typescript
import { parseWithZod } from "@conform-to/zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const submission = parseWithZod(formData, { schema });
  
  if (submission.status !== "success") {
    return json({ submission: submission.reply() });
  }
  
  // submission.value is typed from schema
  await login(submission.value);
  return redirect("/dashboard");
}
```

### With tRPC

```typescript
import { router, publicProcedure } from "./trpc";
import { z } from "zod";

const userRouter = router({
  create: publicProcedure
    .input(
      z.object({
        email: z.string().email(),
        name: z.string().min(1),
      })
    )
    .output(
      z.object({
        id: z.string(),
        email: z.string(),
        name: z.string(),
      })
    )
    .mutation(async ({ input }) => {
      // input is typed
      return await createUser(input);
    }),
});
```

### With Prisma

```typescript
import { Prisma } from "@prisma/client";

// Validate before database operation
const userCreateSchema = z.object({
  email: z.string().email(),
  name: z.string(),
}) satisfies z.ZodType<Prisma.UserCreateInput>;
```

## Best Practices

1. **Reuse schemas**: Create shared schemas in core package
2. **Type from schemas**: Use `z.infer` instead of duplicating types
3. **Composable schemas**: Build complex schemas from simple ones
4. **Async sparingly**: Use async refinements only on server
5. **Custom errors**: Provide helpful, user-friendly error messages
6. **Transform carefully**: Keep transformations simple and predictable
7. **Test schemas**: Unit test complex validation logic
8. **Use safeParse**: Prefer safeParse over parse to avoid exceptions
9. **Branded types**: Use for nominal typing when needed
10. **Document schemas**: Add JSDoc comments to complex schemas

## Common Gotcas

1. **Parse vs safeParse**: parse throws, safeParse returns result
2. **Optional vs nullable**: optional = undefined, nullable = null
3. **Async transforms**: Must use parseAsync/safeParseAsync
4. **Transform order**: Transforms run after validation
5. **Error paths**: Use path in refine for specific field errors
6. **Coerce vs transform**: coerce is simpler for type conversion
7. **Default values**: Apply before validation
8. **Array validation**: Min/max checks array length, not items
9. **Union types**: Discriminated unions have better inference
10. **File validation**: Use z.instanceof(File), not z.object()

## Resources

- [Zod Documentation](https://zod.dev)
- [Zod GitHub](https://github.com/colinhacks/zod)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook)
