---
name: schema-validator
description: Creates and validates Zod schemas for data structures
---

# Schema Validator Skill

## When to Use
- Adding new data structures
- Creating form validation
- Setting up tRPC input validation
- Validating external API data

## What This Skill Does
1. Analyzes data structure requirements
2. Creates Zod schema with proper types:
   - Primitives: string, number, boolean
   - Objects: nested structures
   - Arrays: with item validation
   - Unions: for variants
   - Refinements: for complex validations
3. Adds helpful error messages
4. Generates TypeScript types from schema
5. Adds to core package schemas if shared

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

// Validate array length
const top5Schema = z.array(z.string()).max(5, 'Maximum 5 items');
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

// Discriminated union (better type inference)
const resultSchema = z.discriminatedUnion('success', [
  z.object({ success: z.literal(true), data: z.any() }),
  z.object({ success: z.literal(false), error: z.string() }),
]);
```

### Optional and Nullable
```typescript
// Optional (can be undefined)
const descriptionSchema = z.string().optional();

// Nullable (can be null)
const middleNameSchema = z.string().nullable();

// Optional and nullable
const nicknameSchema = z.string().optional().nullable();

// With default value
const statusSchema = z.string().default('active');
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

// Refine on object
const dateRangeSchema = z.object({
  startDate: z.date(),
  endDate: z.date(),
}).refine(
  (data) => data.endDate > data.startDate,
  {
    message: 'End date must be after start date',
    path: ['endDate'], // Show error on endDate field
  }
);
```

### Transformations
```typescript
// Transform string to number
const ageSchema = z.string()
  .regex(/^\d+$/, 'Must be a number')
  .transform((val) => parseInt(val, 10));

// Transform string to date
const dateSchema = z.string()
  .transform((val) => new Date(val));

// Trim and lowercase
const emailSchema = z.string()
  .email()
  .transform((val) => val.trim().toLowerCase());
```

### Conditional Validation
```typescript
const formSchema = z.object({
  type: z.enum(['personal', 'business']),
  email: z.string().email(),
  companyName: z.string().optional(),
}).refine(
  (data) => {
    // If business type, companyName is required
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
  streams: z.array(z.object({
    type: z.string(),
    data: z.array(z.number()),
  })),
});

// Or use merge
const activityWithProfileSchema = baseActivitySchema.merge(
  z.object({
    profile: profileSchema,
  })
);
```

### Partial and Pick
```typescript
// All fields optional
const partialActivitySchema = activitySchema.partial();

// Specific fields optional
const updateActivitySchema = activitySchema.partial({
  name: true,
  description: true,
});

// Pick specific fields
const activityPreviewSchema = activitySchema.pick({
  id: true,
  name: true,
  type: true,
});

// Omit specific fields
const createActivitySchema = activitySchema.omit({
  id: true,
  createdAt: true,
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

## tRPC Input Validation

### Query Input
```typescript
export const activityRouter = router({
  list: protectedProcedure
    .input(
      z.object({
        limit: z.number().min(1).max(100).default(20),
        offset: z.number().min(0).default(0),
        type: z.enum(['run', 'bike', 'swim', 'other']).optional(),
        search: z.string().optional(),
      })
    )
    .query(async ({ input, ctx }) => {
      // Input is validated automatically
      const { limit, offset, type, search } = input;
      // ...
    }),
});
```

### Mutation Input
```typescript
const createActivitySchema = z.object({
  name: z.string().min(1, 'Name required'),
  type: z.enum(['run', 'bike', 'swim', 'other']),
  distance: z.number().positive().optional(),
  duration: z.number().int().positive(),
});

export const activityRouter = router({
  create: protectedProcedure
    .input(createActivitySchema)
    .mutation(async ({ input, ctx }) => {
      // Input is validated
      // Zod errors automatically converted to TRPC errors
      // ...
    }),
});
```

## Validation at Runtime

### Parse (throw on error)
```typescript
try {
  const activity = activitySchema.parse(unknownData);
  // activity is typed as Activity
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
  // result.data is typed as Activity
  console.log(result.data.name);
} else {
  // result.error is ZodError
  console.log(result.error.errors);
}
```

### Partial Validation
```typescript
// Validate only some fields
const partialResult = activitySchema
  .pick({ name: true, type: true })
  .safeParse(unknownData);
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

### Error Formatting
```typescript
const result = schema.safeParse(data);

if (!result.success) {
  // Get field errors
  const fieldErrors = result.error.flatten().fieldErrors;
  // { email: ['Please enter a valid email'], age: ['Age must be positive'] }

  // Map to form errors
  Object.entries(fieldErrors).forEach(([field, messages]) => {
    form.setError(field, { message: messages?.[0] });
  });
}
```

## Schema Location

### Core Package (Shared)
```
packages/core/schemas/
├── activity.ts          # Activity schemas
├── profile.ts           # Profile schemas
├── activity_plan_v2.ts  # Activity plan schemas
└── form-schemas.ts      # Form-specific schemas
```

### App-Specific
```
apps/mobile/lib/schemas/      # Mobile-only schemas
apps/web/lib/schemas/          # Web-only schemas
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
  elevationGain: z.number().nonnegative().optional(),
  startTime: z.date(),
  endTime: z.date(),
  averageHeartRate: z.number().int().positive().max(220).optional(),
  maxHeartRate: z.number().int().positive().max(220).optional(),
  averagePower: z.number().nonnegative().optional(),
  maxPower: z.number().nonnegative().optional(),
  tss: z.number().nonnegative().optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
}).refine(
  (data) => data.endTime > data.startTime,
  {
    message: 'End time must be after start time',
    path: ['endTime'],
  }
).refine(
  (data) => !data.maxHeartRate || !data.averageHeartRate || data.maxHeartRate >= data.averageHeartRate,
  {
    message: 'Max heart rate must be greater than or equal to average',
    path: ['maxHeartRate'],
  }
);

export type Activity = z.infer<typeof activitySchema>;

// Create variant for input (omit generated fields)
export const createActivitySchema = activitySchema.omit({
  id: true,
  userId: true,
  createdAt: true,
  updatedAt: true,
});

export type CreateActivityInput = z.infer<typeof createActivitySchema>;

// Update variant (all fields optional except id)
export const updateActivitySchema = activitySchema
  .partial()
  .required({ id: true });

export type UpdateActivityInput = z.infer<typeof updateActivitySchema>;
```
