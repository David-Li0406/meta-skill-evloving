---
name: api-patterns
description: This skill provides API route patterns and conventions for the fitness app. Use when creating or modifying API routes, handling authentication, validating requests, or implementing error handling.
---

# API Route Patterns & Best Practices

This skill provides comprehensive patterns for building API routes in the fitness application using Nuxt server routes.

## Core Principles

**Separation of Concerns**: All database logic MUST be in `/server/database/queries/`. Never use `useDB()` directly in API routes.

**Return Data Directly**: Don't wrap successful responses in `{ success: true, data: ... }`.

**Custom Validation**: Always use validation helpers from `server/utils/bodyValidation.ts` instead of Nuxt's built-in functions.

## API Route Structure

Every API route follows this pattern:

```typescript
import { z } from 'zod'
import { queryUserWorkouts } from '~~/server/database/queries/workouts'
import { validateBody, validateParams, validateQuery } from '~~/server/utils/bodyValidation'

// 1. Define validation schemas locally
const paramsSchema = z.object({
  id: z.uuid(),
})

const bodySchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
})

const querySchema = z.object({
  limit: z.coerce.number().int().min(1).max(100).default(20),
})

// 2. Define event handler
export default defineEventHandler(async (event) => {
  // 3. Authenticate user
  const { user } = await requireUserSession(event)

  // 4. Validate request data
  const { id } = await validateParams(event, paramsSchema)
  const body = await validateBody(event, bodySchema)
  const query = await validateQuery(event, querySchema)

  // 5. Use query functions (never useDB() directly)
  const workouts = await queryUserWorkouts(user.id, query.limit)

  // 6. Return data directly (no wrapper)
  return workouts
})
```

## Authentication

Use `requireUserSession` to get the authenticated user:

```typescript
export default defineEventHandler(async (event) => {
  // Throws 401 if not authenticated
  const { user, session } = await requireUserSession(event)

  // user.id is available for queries
  const workouts = await queryUserWorkouts(user.id)

  return workouts
})
```

**Key points:**
- Automatically throws 401 Unauthorized if no session
- Returns both `user` and `session` objects
- Destructure to get only what you need: `const { user } = await requireUserSession(event)`

## Request Validation

**Always use custom validation helpers** from `server/utils/bodyValidation.ts`:

### validateBody

Validate request body:

```typescript
const bodySchema = z.object({
  name: z.string().min(1).max(100),
  weight: z.coerce.number().positive(),
  sets: z.coerce.number().int().min(1),
})

export default defineEventHandler(async (event) => {
  const body = await validateBody(event, bodySchema)
  // body is typed and validated
})
```

### validateParams

Validate route parameters:

```typescript
// Route: /api/workouts/[id].ts

const paramsSchema = z.object({
  id: z.uuid(),
})

export default defineEventHandler(async (event) => {
  const { id } = await validateParams(event, paramsSchema)
  // id is validated as UUID
})
```

### validateQuery

Validate query parameters:

```typescript
// Route: /api/workouts?status=active&limit=20

const querySchema = z.object({
  status: z.enum(['active', 'completed']).optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  page: z.coerce.number().int().min(1).default(1),
})

export default defineEventHandler(async (event) => {
  const query = await validateQuery(event, querySchema)
  // query.limit and query.page have defaults
})
```

**Important:** Use `z.coerce.number()` for numeric query/body params as they come as strings.

## Response Handling

### Success Responses

Return data directly without wrapping:

```typescript
// ✅ Correct
export default defineEventHandler(async (event) => {
  const workouts = await queryUserWorkouts(userId)
  return workouts // Return array directly
})

// ❌ Wrong: Don't wrap
export default defineEventHandler(async (event) => {
  const workouts = await queryUserWorkouts(userId)
  return { success: true, data: workouts } // Don't do this
})
```

### Error Responses

Use `createError` for error responses:

```typescript
export default defineEventHandler(async (event) => {
  const { id } = await validateParams(event, paramsSchema)

  const workout = await queryWorkoutById(id)

  if (!workout) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Workout not found'
    })
  }

  return workout
})
```

**Common status codes:**
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (not authenticated)
- `403` - Forbidden (authenticated but not authorized)
- `404` - Not Found
- `409` - Conflict (e.g., duplicate resource)
- `422` - Unprocessable Entity (semantic validation errors)
- `500` - Internal Server Error

## Complete CRUD Examples

### POST - Create Resource

```typescript
// server/api/workouts/index.post.ts
import { z } from 'zod'
import { createWorkout } from '~~/server/database/queries/workouts'
import { validateBody } from '~~/server/utils/bodyValidation'

const bodySchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  isPublic: z.boolean().default(false),
  exercises: z.array(z.uuid()).min(1),
})

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const body = await validateBody(event, bodySchema)

  const workout = await createWorkout({
    ...body,
    userId: user.id,
  })

  return workout
})
```

### GET - Read Resource

```typescript
// server/api/workouts/[id].get.ts
import { z } from 'zod'
import { getWorkoutById } from '~~/server/database/queries/workouts'
import { validateParams } from '~~/server/utils/bodyValidation'

const paramsSchema = z.object({
  id: z.uuid(),
})

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const { id } = await validateParams(event, paramsSchema)

  const workout = await getWorkoutById(id, user.id)
  // getWorkoutById throws 404 if not found

  return workout
})
```

### GET - List Resources

```typescript
// server/api/workouts/index.get.ts
import { z } from 'zod'
import { queryUserWorkouts } from '~~/server/database/queries/workouts'
import { validateQuery } from '~~/server/utils/bodyValidation'

const querySchema = z.object({
  status: z.enum(['active', 'completed']).optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  offset: z.coerce.number().int().min(0).default(0),
})

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const query = await validateQuery(event, querySchema)

  const workouts = await queryUserWorkouts(user.id, query)

  return workouts
})
```

### PATCH - Update Resource

```typescript
// server/api/workouts/[id].patch.ts
import { z } from 'zod'
import { updateWorkout } from '~~/server/database/queries/workouts'
import { validateParams, validateBody } from '~~/server/utils/bodyValidation'

const paramsSchema = z.object({
  id: z.uuid(),
})

const bodySchema = z.object({
  name: z.string().min(1).max(100).optional(),
  description: z.string().max(500).optional(),
  isPublic: z.boolean().optional(),
}).refine(
  data => Object.keys(data).length > 0,
  { message: 'At least one field must be provided' }
)

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const { id } = await validateParams(event, paramsSchema)
  const body = await validateBody(event, bodySchema)

  const workout = await updateWorkout(id, user.id, body)
  // updateWorkout throws 404 if not found

  return workout
})
```

### DELETE - Delete Resource

```typescript
// server/api/workouts/[id].delete.ts
import { z } from 'zod'
import { deleteWorkout } from '~~/server/database/queries/workouts'
import { validateParams } from '~~/server/utils/bodyValidation'

const paramsSchema = z.object({
  id: z.uuid(),
})

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const { id } = await validateParams(event, paramsSchema)

  await deleteWorkout(id, user.id)
  // deleteWorkout throws 404 if not found

  // Return 204 No Content
  setResponseStatus(event, 204)
})
```

## Path Resolution in Server Code

**Critical:** Always use `~~/` for server-side imports:

```typescript
// ✅ Correct: Server imports with ~~/
import { users } from '~~/server/database/schema/users'
import { getUserById } from '~~/server/database/queries/users'
import { validateBody } from '~~/server/utils/bodyValidation'

// ❌ Wrong: Using ~/
import { users } from '~/server/database/schema/users'
// Nitro will look in wrong directory!
```

## Validation Schema Patterns

### Define schemas locally in each route

```typescript
// ✅ Correct: Local schema definition
const paramsSchema = z.object({
  id: z.uuid(),
})

// ❌ Wrong: Importing from shared/
import { idParamsSchema } from '~/shared/schemas/params'
```

**Why?** Keeps schemas close to usage and allows route-specific customization.

### Reuse base schemas

```typescript
// shared/schemas/workout.ts
export const baseWorkoutSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
})

// API route
import { baseWorkoutSchema } from '~/shared/schemas/workout'

const bodySchema = baseWorkoutSchema.extend({
  exercises: z.array(z.uuid()).min(1),
})
```

## Critical Rules

### ✅ MUST DO
- Always use `requireUserSession` for authentication
- Always use validation helpers (`validateBody`, `validateQuery`, `validateParams`)
- Define validation schemas locally in each API route
- Return data directly (no success wrapper)
- Use `createError` for error responses
- Create query functions in `/server/database/queries/`
- Use `~~/` for server-side imports
- Implement Row Level Security (RLS) for user data

### ❌ NEVER DO
- Use `useDB()` directly in API routes
- Use Nuxt's built-in validation functions (`getRouterParam`, `readValidatedBody`, etc.)
- Import parameter schemas from `shared/` directory
- Wrap successful responses in `{ success: true, data: ... }`
- Skip authentication for user data endpoints
- Use `~/` for server-side imports
- Skip RLS policies for user data

## Common Patterns

### Pattern: Paginated List

```typescript
const querySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
})

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const { page, limit } = await validateQuery(event, querySchema)

  const offset = (page - 1) * limit
  const workouts = await queryUserWorkouts(user.id, { limit, offset })
  const total = await countUserWorkouts(user.id)

  return {
    data: workouts,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  }
})
```

### Pattern: Conditional Query Parameters

```typescript
const querySchema = z.object({
  search: z.string().optional(),
  status: z.enum(['active', 'completed']).optional(),
  sortBy: z.enum(['name', 'createdAt']).default('createdAt'),
  order: z.enum(['asc', 'desc']).default('desc'),
})

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const query = await validateQuery(event, querySchema)

  const workouts = await queryUserWorkouts(user.id, query)

  return workouts
})
```

### Pattern: Nested Resources

```typescript
// Route: /api/workouts/[workoutId]/exercises/[exerciseId].ts

const paramsSchema = z.object({
  workoutId: z.uuid(),
  exerciseId: z.uuid(),
})

export default defineEventHandler(async (event) => {
  const { user } = await requireUserSession(event)
  const { workoutId, exerciseId } = await validateParams(event, paramsSchema)

  const exercise = await getWorkoutExercise(workoutId, exerciseId, user.id)

  return exercise
})
```

## Reference Files

- `references/bodyValidation.ts` - File needed to handle all validations
