---
name: schema-validator
description: Use this skill when you need to create and validate Zod schemas for data structures, ensuring type safety and runtime validation.
---

# Schema Validator Skill

## When to Use
- When adding new data structures
- For creating form validation
- To validate API inputs
- When setting up tRPC input validation
- For validating external API data

## What This Skill Does
1. Analyzes data structure requirements.
2. Creates Zod schemas with proper types:
   - Primitives: string, number, boolean
   - Objects: nested structures
   - Arrays: with item validation
   - Unions: for variants
   - Refinements: for complex validations
3. Generates TypeScript types from schemas.
4. Adds custom validation rules and helpful error messages.
5. Implements refined schemas with dependencies.

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
  name: z.string().min(1, 'Name is required'),
  type: z.enum(['run', 'bike', 'swim', 'other']),
  distance: z.number().positive().optional(),
  duration: z.number().int().positive(),
  startTime: z.date(),
  endTime: z.date(),
}).refine(data => data.endTime > data.startTime, {
  message: "End time must be after start time",
  path: ["endTime"],
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

### Form Schema Pattern
```typescript
const createActivitySchema = activitySchema
  .omit({ id: true })
  .extend({
    notes: z.string().max(500).optional(),
    isPrivate: z.boolean().default(false),
  });

// Type for form input
type CreateActivityInput = z.infer<typeof createActivitySchema>;
```

### API Input Validation
```typescript
const activityListInput = z.object({
  limit: z.number().min(1).max(100).default(20),
  offset: z.number().min(0).default(0),
  type: z.enum(['run', 'bike', 'swim', 'other']).optional(),
  search: z.string().optional(),
});
```