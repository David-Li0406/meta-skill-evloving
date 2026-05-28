---
name: zod
description: >
  Patterns and conventions for using Zod validation schemas in GeroCare following Clean Architecture.
  Trigger: When creating validation schemas, validating domain entities, form data, or Firestore data.
license: Apache-2.0
metadata:
  author: gero-cloud
  version: "1.0"
  scope: [root]
  auto_invoke: "Creating validation schemas or validating data"
---

## When to Use

Use this skill when:
- Creating validation schemas for domain entities
- Validating form data in application composables
- Validating Firestore data before converting to domain entities
- Replacing manual validation functions with Zod schemas
- Defining schema structures for domain entities

**Don't use this skill for:**
- UI form validation (use component-level validation)
- Simple type guards (use TypeScript types)
- Runtime type checking without validation rules

---

## Clean Architecture: Where Zod Schemas Belong

**Critical Rule**: Zod schemas belong in the **Domain Layer** (`src/business/{feature}/domain/`).

```
src/business/{feature}/
├── domain/
│   ├── {Entity}.ts          # Domain interface
│   └── {Entity}.schema.ts   # Zod schemas (recommended for complex schemas)
└── ...
```

### Decision: Same File vs Separate File

| Scenario | Location | Example |
|----------|----------|---------|
| Simple schema (few fields) | Same file as entity | `Resident.ts` |
| Complex schema (many fields, nested) | Separate file | `Resident.schema.ts` |
| Schema reused across features | Shared domain | `src/shared/domain/*.schema.ts` |

**Recommendation**: Start with the same file, move to separate file if it grows complex.

---

## Critical Patterns

### Pattern 1: Domain Entity Schema

**Always define schemas in the domain layer** alongside the entity interface:

```typescript
// src/business/residents/domain/Resident.schema.ts
import { z } from 'zod'
import type { Resident } from './Resident'

// Base schema (without auto-generated fields)
export const ResidentCreateSchema = z.object({
  firstName: z.string().min(1, 'firstName is required'),
  lastName: z.string().min(1, 'lastName is required'),
  dateOfBirth: z.date(),
  photoURL: z.string().url().optional().or(z.literal('')),
  medicalInfo: z.object({
    allergies: z.array(z.string()).default([]),
    chronicConditions: z.array(z.string()).default([]),
    medications: z.array(z.string()).default([]),
    dietaryRestrictions: z.array(z.string()).default([]),
  }),
  emergencyContacts: z.array(
    z.object({
      name: z.string().min(1, 'name is required'),
      relationship: z.string().min(1, 'relationship is required'),
      phone: z.string().min(1, 'phone is required'),
      email: z.string().email().optional().or(z.literal('')),
    })
  ),
  assignedCaregivers: z.array(z.string()),
})

// Full entity schema (with id and timestamps)
export const ResidentSchema = ResidentCreateSchema.extend({
  id: z.string(),
  createdAt: z.date(),
  updatedAt: z.date(),
})

// Type inference from schema
export type ResidentCreateInput = z.infer<typeof ResidentCreateSchema>
export type ResidentInput = z.infer<typeof ResidentSchema>
```

### Pattern 2: Using Schemas in Domain Layer

**Replace manual validation functions** with Zod schema validation:

```typescript
// src/business/residents/domain/Resident.ts
import { z } from 'zod'
import { type Result, Ok, Err } from '@/shared/domain/Result'
import { ResidentSchema } from './Resident.schema'
import type { ResidentError } from './ResidentErrors'
import { createResidentValidationError } from './ResidentErrors'

export interface Resident {
  // ... entity definition
}

/**
 * Validate a resident entity using Zod
 */
export function validateResident(resident: unknown): Result<Resident, ResidentError> {
  const result = ResidentSchema.safeParse(resident)
  
  if (!result.success) {
    const firstError = result.error.errors[0]
    return Err(createResidentValidationError(firstError.message))
  }
  
  return Ok(result.data)
}
```

### Pattern 3: Using Schemas in Application Layer

**Validate form data** before creating entities:

```typescript
// src/business/residents/app/useResidentForm.ts
import { ref } from 'vue'
import { type Result, Ok, Err } from '@/shared/domain/Result'
import { ResidentCreateSchema } from '../domain/Resident.schema'
import type { ResidentFormData } from './types'

export function useResidentForm() {
  const form = ref<ResidentFormData>({
    // ... form state
  })

  const validate = (): Result<ResidentFormData, string> => {
    // Convert form data to schema-compatible format
    const formData = {
      ...form.value,
      dateOfBirth: form.value.dateOfBirth ? new Date(form.value.dateOfBirth) : undefined,
    }

    const result = ResidentCreateSchema.safeParse(formData)
    
    if (!result.success) {
      const firstError = result.error.errors[0]
      return Err(firstError.message)
    }
    
    return Ok(result.data)
  }

  return {
    form,
    validate,
    // ...
  }
}
```

### Pattern 4: Using Schemas in Infrastructure Layer

**Validate Firestore data** before converting to domain entities:

```typescript
// src/business/residents/infrastructure/FirestoreResidentRepository.ts
import { Timestamp } from 'firebase/firestore'
import { ResidentSchema } from '../domain/Resident.schema'
import type { Resident } from '../domain/Resident'
import type { ResidentError } from '../domain/ResidentErrors'
import { type Result, Ok, Err } from '@/shared/domain/Result'
import { createUnknownResidentError } from '../domain/ResidentErrors'

// Convert Firestore document to domain entity
function firestoreDocToResident(docId: string, data: Record<string, unknown>): Result<Resident, ResidentError> {
  try {
    // Convert Firestore Timestamp to Date
    const residentData = {
      id: docId,
      ...data,
      dateOfBirth: data.dateOfBirth instanceof Timestamp ? data.dateOfBirth.toDate() : data.dateOfBirth,
      createdAt: data.createdAt instanceof Timestamp ? data.createdAt.toDate() : data.createdAt,
      updatedAt: data.updatedAt instanceof Timestamp ? data.updatedAt.toDate() : data.updatedAt,
    }

    // Validate with Zod schema
    const result = ResidentSchema.safeParse(residentData)
    
    if (!result.success) {
      return Err(createUnknownResidentError('Invalid resident data from Firestore'))
    }
    
    return Ok(result.data)
  } catch (error) {
    return Err(createUnknownResidentError('Failed to convert Firestore document to Resident'))
  }
}
```

### Pattern 5: Date Handling with Zod

**Always handle Date conversions explicitly** before validation:

```typescript
import { z } from 'zod'

// Option 1: Use z.coerce.date() for string inputs
const DateSchema = z.coerce.date()

// Option 2: Use z.preprocess() for complex conversions
const DateFromTimestampSchema = z.preprocess(
  (val) => val instanceof Timestamp ? val.toDate() : val,
  z.date()
)

// Option 3: Manual conversion before validation
const formData = {
  ...form.value,
  dateOfBirth: form.value.dateOfBirth ? new Date(form.value.dateOfBirth) : undefined,
}
const result = ResidentCreateSchema.safeParse(formData)
```

### Pattern 6: Combining Result Type with Zod

**Convert Zod validation errors** to domain Result types:

```typescript
import { z } from 'zod'
import { type Result, Ok, Err } from '@/shared/domain/Result'
import type { EntityError } from '../domain/EntityErrors'
import { createEntityValidationError } from '../domain/EntityErrors'

function validateWithSchema<T extends z.ZodTypeAny>(
  schema: T,
  data: unknown,
  createError: (message: string) => EntityError
): Result<z.infer<T>, EntityError> {
  const result = schema.safeParse(data)
  
  if (!result.success) {
    const firstError = result.error.errors[0]
    return Err(createError(firstError.message))
  }
  
  return Ok(result.data)
}

// Usage
const result = validateWithSchema(ResidentSchema, resident, createResidentValidationError)
```

---

## Schema Naming Conventions

| Schema Type | Naming Pattern | Example |
|-------------|---------------|---------|
| Create schema (without id, timestamps) | `{Entity}CreateSchema` | `ResidentCreateSchema` |
| Full entity schema | `{Entity}Schema` | `ResidentSchema` |
| Update schema (partial) | `{Entity}UpdateSchema` | `ResidentUpdateSchema` |
| Form data schema | `{Entity}FormSchema` | `ResidentFormSchema` |
| Type inference | `{Entity}Input` | `ResidentInput` |

---

## Migration from Manual Validation

When migrating existing manual validation to Zod:

1. **Create Zod schema** in domain layer (same or separate file)
2. **Keep existing function** temporarily for backward compatibility
3. **Replace manual validation** with Zod validation:
   ```typescript
   // OLD: Manual validation
   export function validateResident(resident: Resident): Result<Resident, string> {
     if (!resident.firstName || resident.firstName.trim() === '') {
       return Err('firstName is required')
     }
     // ... more manual checks
   }
   
   // NEW: Zod validation
   export function validateResident(resident: unknown): Result<Resident, ResidentError> {
     const result = ResidentSchema.safeParse(resident)
     if (!result.success) {
       return Err(createResidentValidationError(result.error.errors[0].message))
     }
     return Ok(result.data)
   }
   ```
4. **Update usages** in application and infrastructure layers
5. **Remove old manual validation** once all usages are migrated

---

## Common Zod Patterns

### Optional Fields with Empty String Handling

```typescript
// Handle empty strings as undefined for optional fields
photoURL: z.string().url().optional().or(z.literal('')),
email: z.string().email().optional().or(z.literal('')),
```

### Array Fields with Defaults

```typescript
// Provide default empty array
allergies: z.array(z.string()).default([]),
assignedCaregivers: z.array(z.string()).default([]),
```

### Nested Objects

```typescript
medicalInfo: z.object({
  allergies: z.array(z.string()).default([]),
  chronicConditions: z.array(z.string()).default([]),
}),
```

### Date Validation

```typescript
// Validate date is not in the future
dateOfBirth: z.date().refine(
  (date) => date <= new Date(),
  { message: 'dateOfBirth cannot be in the future' }
),
```

---

## Best Practices

1. **Always define schemas in domain layer** - Keep validation logic close to entities
2. **Use safeParse() instead of parse()** - Handle errors gracefully with Result types
3. **Convert Zod errors to domain errors** - Maintain consistent error handling
4. **Handle date conversions explicitly** - Convert Firestore Timestamps and string dates before validation
5. **Infer types from schemas** - Use `z.infer<typeof Schema>` for type safety
6. **Start with same file, separate if complex** - Keep simple schemas with entities, complex ones separate

---

## Resources

- **Zod Documentation**: https://zod.dev/
- **Domain Layer**: `src/business/{feature}/domain/`
- **Result Type**: `src/shared/domain/Result.ts`
- **Feature Development Skill**: See `feature-development` skill for Clean Architecture patterns
