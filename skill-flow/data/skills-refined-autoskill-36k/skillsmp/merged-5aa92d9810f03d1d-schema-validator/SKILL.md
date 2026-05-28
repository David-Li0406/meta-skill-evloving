---
name: schema-validator
description: Use this skill to create and validate Zod schemas for various data structures, ensuring type safety and runtime validation.
---

# Schema Validator Skill

## When to Use

- User needs to create new data schemas
- User wants to add validation to forms
- User needs to validate API inputs
- User asks to update existing schemas
- User is setting up tRPC input validation
- User is validating external API data

## What This Skill Does

1. Creates Zod schemas with proper validation for various data types:
   - Primitives: string, number, boolean
   - Objects: nested structures
   - Arrays: with item validation
   - Unions: for variants
   - Refinements: for complex validations
2. Infers TypeScript types from schemas
3. Adds custom validation rules and helpful error messages
4. Implements refined schemas with dependencies
5. Creates form-specific sub-schemas
6. Validates input for tRPC queries and mutations

## Basic Schema Patterns

### Primitive Types
```typescript
import { z } from 'zod';

// String with validation
const nameSchema = z.string()
  .min(1, 'Name is required')
  .max(100, 'Name must be less than 100 characters');

// Number with validation
const ageSchema = z.number()
  .int('Must be a whole number')
  .positive('Must be positive')
  .max(120, 'Must be less than 120');

// Boolean
const isActiveSchema = z.boolean();

// Date
const createdAtSchema = z.date();

// UUID
const idSchema = z.string().uuid();

// Email
const emailSchema = z.string().email('Invalid email address');

// URL
const websiteSchema = z.string().url('Invalid URL');
```

### Object Schemas
```typescript
const activitySchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, 'Name required'),
  type: z.enum(['run', 'bike', 'swim', 'other']),
  distance: z.number().positive().optional(),
  duration: z.number().int().positive(),
  startTime: z.date(),
  endTime: z.date(),
}).refine((data) => data.endTime > data.startTime, {
  message: 'End time must be after start time',
  path: ['endTime'],
});

// Infer TypeScript type
type Activity = z.infer<typeof activitySchema>;
```

### Nested Objects
```typescript
const profileSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  settings: z.object({
    notifications: z.boolean(),
    theme: z.enum(['light', 'dark', 'auto']),
    units: z.object({
      distance: z.enum(['km', 'mi']),
      elevation: z.enum(['m', 'ft']),
    }),
  }),
});
```

### Array Schemas
```typescript
// Array of primitives
const tagsSchema = z.array(z.string()).min(1, 'At least one tag required');

// Array of objects
const stepsSchema = z.array(
  z.object({
    id: z.string(),
    name: z.string(),
    duration: z.number(),
  })
).min(1, 'At least one step required');
```

### Enum and Union Types
```typescript
// Enum
const activityTypeSchema = z.enum(['run', 'bike', 'swim', 'other']);

// Union
const resultSchema = z.union([
  z.object({ success: true, data: z.any() }),
  z.object({ success: false, error: z.string() }),
]);
```

### Optional and Nullable
```typescript
// Optional (can be undefined)
const descriptionSchema = z.string().optional();

// Nullable (can be null)
const middleNameSchema = z.string().nullable();
```

## Advanced Patterns

### Refinements (Custom Validation)
```typescript
const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .refine(
    (val) => /[A-Z]/.test(val),
    'Password must contain uppercase letter'
  )
  .refine(
    (val) => /[0-9]/.test(val),
    'Password must contain a number'
  );
```

### Transformations
```typescript
// Transform string to number
const ageSchema = z.string()
  .regex(/^\d+$/, 'Must be a number')
  .transform((val) => parseInt(val, 10));
```

### Conditional Validation
```typescript
const formSchema = z.object({
  type: z.enum(['personal', 'business']),
  email: z.string().email(),
  companyName: z.string().optional(),
}).refine(
  (data) => {
    if (data.type === 'business') {
      return !!data.companyName;
    }
    return true;
  },
  {
    message: 'Company name required for business accounts',
    path: ['companyName'],
  }
);
```

### Extending Schemas
```typescript
// Base schema
const baseActivitySchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  type: z.enum(['run', 'bike', 'swim']),
});

// Extend with additional fields
const detailedActivitySchema = baseActivitySchema.extend({
  distance: z.number(),
  duration: z.number(),
});
```

## Form Validation

### React Hook Form Integration
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const formSchema = z.object({
  name: z.string().min(1, 'Name required'),
  email: z.string().email('Invalid email'),
  age: z.number().int().positive().max(120),
});

type FormData = z.infer<typeof formSchema>;

export function MyForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      age: 0,
    },
  });

  const onSubmit = (data: FormData) => {
    console.log(data); // Validated data
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## Validation at Runtime

### Parse (throw on error)
```typescript
try {
  const activity = activitySchema.parse(unknownData);
  console.log(activity.name);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.log(error.errors);
  }
}
```

### Safe Parse (no throw)
```typescript
const result = activitySchema.safeParse(unknownData);

if (result.success) {
  console.log(result.data.name);
} else {
  console.log(result.error.errors);
}
```

## Error Handling

### Custom Error Messages
```typescript
const schema = z.object({
  email: z.string().email('Please enter a valid email address'),
  age: z.number({
    required_error: 'Age is required',
    invalid_type_error: 'Age must be a number',
  }).positive('Age must be positive'),
});
```

## Schema Location

### Core Package (Shared)
```
packages/core/schemas/
├── activity.ts          # Activity schemas
├── profile.ts           # Profile schemas
└── form-schemas.ts      # Form-specific schemas
```

## Critical Patterns

- ✅ Use meaningful error messages
- ✅ Validate at boundaries (user input, external APIs)
- ✅ Infer types from schemas (single source of truth)
- ✅ Use `.safeParse()` when errors are expected
- ✅ Use `.parse()` when validation failure is exceptional
- ✅ Place shared schemas in core package
- ✅ Test validation logic
- ✅ Document complex refinements

## Example: Complete Activity Schema

```typescript
// packages/core/schemas/activity.ts
import { z } from 'zod';

export const activitySchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  name: z.string().min(1, 'Activity name is required').max(200),
  description: z.string().max(1000).optional(),
  type: z.enum(['run', 'bike', 'swim', 'other'], {
    errorMap: () => ({ message: 'Invalid activity type' }),
  }),
  distance: z.number().nonnegative().optional(),
  duration: z.number().int().positive('Duration must be positive'),
  createdAt: z.date(),
  updatedAt: z.date(),
}).refine(
  (data) => data.endTime > data.startTime,
  {
    message: 'End time must be after start time',
    path: ['endTime'],
  }
);

export type Activity = z.infer<typeof activitySchema>;
```