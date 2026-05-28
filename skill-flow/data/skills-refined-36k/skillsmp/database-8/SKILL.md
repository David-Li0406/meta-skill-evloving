---
name: database
description: This skill provides Drizzle ORM patterns and database conventions for the fitness app. Use when creating queries, implementing RLS policies, or working with database schemas.
---

# Database Patterns with Drizzle ORM

This skill provides comprehensive patterns for database operations using Drizzle ORM in the fitness application.

## Core Principles

**Separation of Concerns**: All database logic MUST be in `/server/database/queries/` files. Never use `useDB()` directly in API routes.

**Type Safety**: Let Drizzle infer return types. Do not add explicit `Promise<...>` return types to query functions.

**No Error Handling in Queries**: Never use try/catch in database query functions. Let errors bubble up to the API handler.

**Row Level Security**: Implement and enforce RLS for all user data at the database level.

## Query Naming Conventions

Use consistent naming to indicate behavior:

| Operation | Function | Throws on Not Found? | Returns |
|-----------|----------|---------------------|---------|
| Create | `createX` | N/A | Created record |
| Read | `getX` | Yes (404) | Record |
| Read | `queryX` | No | Record/Array/`null` |
| Update | `updateX` | Yes (404) | Updated record |
| Delete | `deleteX` | Yes (404) | `void`/deleted record |

### queryX() Functions

Return data or `null`/`[]`. Never throw on "not found":

```typescript
// server/database/queries/workouts.ts
export function queryWorkoutById(id: string, userId: string) {
  return useDB().query.workouts.findFirst({
    where: and(
      eq(workouts.id, id),
      eq(workouts.userId, userId)
    ),
  })
  // Returns: Workout | undefined
}

// Usage in API route
const workout = await queryWorkoutById(id, user.id)
if (!workout) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Workout not found'
  })
}
```

### getX() Functions

Return data or throw 404 error if not found:

```typescript
export async function getWorkoutById(id: string, userId: string) {
  const workout = await useDB().query.workouts.findFirst({
    where: and(
      eq(workouts.id, id),
      eq(workouts.userId, userId)
    ),
  })

  if (!workout) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Workout not found'
    })
  }

  return workout
}

// Usage in API route
const workout = await getWorkoutById(id, user.id)
// No null check needed - throws 404 if not found
return workout
```

## Query Patterns

### Use useDB().query for Relations

Prefer `useDB().query.<table>` for most selections, especially with relations:

```typescript
// ✅ Correct: Using query API with relations
export function queryWorkoutWithExercises(id: string, userId: string) {
  return useDB().query.workouts.findFirst({
    where: and(
      eq(workouts.id, id),
      eq(workouts.userId, userId)
    ),
    with: {
      exercises: {
        with: {
          exercise: true
        }
      }
    }
  })
}
```

### Use useDB().select() for Complex Queries

Use `useDB().select().from()` for complex joins or specific columns:

```typescript
// ✅ Correct: Using select for complex queries
export function queryWorkoutStats(userId: string) {
  return useDB()
    .select({
      workoutId: workouts.id,
      workoutName: workouts.name,
      exerciseCount: sql<number>`count(${workoutExercises.id})`,
      totalVolume: sql<number>`sum(${workoutExercises.sets} * ${workoutExercises.reps} * ${workoutExercises.weight})`
    })
    .from(workouts)
    .leftJoin(workoutExercises, eq(workouts.id, workoutExercises.workoutId))
    .where(eq(workouts.userId, userId))
    .groupBy(workouts.id)
}
```

## Type Safety with Drizzle

### Infer Types from Schemas

```typescript
import { type InferSelectModel, type InferInsertModel } from 'drizzle-orm'
import { workouts } from '~~/server/database/schema/workouts'

// ✅ Correct: Infer from schema
type Workout = InferSelectModel<typeof workouts>
type InsertWorkout = InferInsertModel<typeof workouts>

// Query function with inferred return type
export function createWorkout(data: InsertWorkout) {
  return useDB().insert(workouts).values(data).returning()
  // Return type is automatically inferred as Workout[]
}
```

### Let Drizzle Infer Return Types

```typescript
// ✅ Correct: No explicit return type
export function queryUserWorkouts(userId: string) {
  return useDB().query.workouts.findMany({
    where: eq(workouts.userId, userId),
    with: {
      exercises: true
    }
  })
  // Drizzle infers complex return type automatically
}

// ❌ Wrong: Explicit return type
export function queryUserWorkouts(userId: string): Promise<Workout[]> {
  return useDB().query.workouts.findMany({
    where: eq(workouts.userId, userId),
    with: {
      exercises: true // Type error: exercises not in Workout
    }
  })
}
```

## CRUD Operations

### Create

```typescript
import { workouts } from '~~/server/database/schema/workouts'

export async function createWorkout(data: InsertWorkout) {
  const [workout] = await useDB()
    .insert(workouts)
    .values(data)
    .returning()

  return workout
}
```

### Read (Single)

```typescript
// Query version (returns undefined if not found)
export function queryWorkoutById(id: string, userId: string) {
  return useDB().query.workouts.findFirst({
    where: and(
      eq(workouts.id, id),
      eq(workouts.userId, userId)
    ),
  })
}

// Get version (throws 404 if not found)
export async function getWorkoutById(id: string, userId: string) {
  const workout = await queryWorkoutById(id, userId)

  if (!workout) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Workout not found'
    })
  }

  return workout
}
```

### Read (List)

```typescript
interface QueryOptions {
  limit?: number
  offset?: number
  status?: 'active' | 'completed'
}

export function queryUserWorkouts(
  userId: string,
  options: QueryOptions = {}
) {
  const { limit = 20, offset = 0, status } = options

  return useDB().query.workouts.findMany({
    where: and(
      eq(workouts.userId, userId),
      status ? eq(workouts.status, status) : undefined
    ),
    limit,
    offset,
    orderBy: desc(workouts.createdAt)
  })
}
```

### Update

```typescript
export async function updateWorkout(
  id: string,
  userId: string,
  data: Partial<InsertWorkout>
) {
  const [workout] = await useDB()
    .update(workouts)
    .set({
      ...data,
      updatedAt: new Date()
    })
    .where(and(
      eq(workouts.id, id),
      eq(workouts.userId, userId)
    ))
    .returning()

  if (!workout) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Workout not found'
    })
  }

  return workout
}
```

### Delete

```typescript
export async function deleteWorkout(id: string, userId: string) {
  const [workout] = await useDB()
    .delete(workouts)
    .where(and(
      eq(workouts.id, id),
      eq(workouts.userId, userId)
    ))
    .returning()

  if (!workout) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Workout not found'
    })
  }
}
```

## Row Level Security (RLS)

**Always enforce RLS for user data** by including `userId` in where clauses:

```typescript
// ✅ Correct: Enforces RLS
export function queryUserWorkouts(userId: string) {
  return useDB().query.workouts.findMany({
    where: eq(workouts.userId, userId) // RLS enforcement
  })
}

// ❌ Wrong: No RLS
export function queryAllWorkouts() {
  return useDB().query.workouts.findMany() // Exposes all users' data!
}
```

### RLS for Updates and Deletes

Always verify ownership before modifying:

```typescript
export async function updateWorkout(
  id: string,
  userId: string, // RLS parameter
  data: Partial<InsertWorkout>
) {
  const [workout] = await useDB()
    .update(workouts)
    .set(data)
    .where(and(
      eq(workouts.id, id),
      eq(workouts.userId, userId) // RLS enforcement
    ))
    .returning()

  if (!workout) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Workout not found'
    })
  }

  return workout
}
```

## Query File Organization

Group related queries by domain:

```
server/database/queries/
├── workouts.ts      # Workout-related queries
├── exercises.ts     # Exercise-related queries
├── users.ts         # User-related queries
├── goals.ts         # Goal-related queries
└── notifications.ts # Notification-related queries
```

### Naming to Avoid Conflicts

Use specific function names to avoid conflicts:

```typescript
// ✅ Correct: Specific names
export function deleteWorkoutNotification(id: string) { }
export function deleteProgressNotification(id: string) { }

// ❌ Wrong: Generic name causes conflicts
export function deleteNotification(id: string) { } // Which table?
```

## Relations

Define relations in schema for easy querying:

```typescript
// server/database/schema/workouts.ts
export const workouts = pgTable('workouts', {
  id: uuid('id').primaryKey().defaultRandom(),
  userId: uuid('user_id').notNull().references(() => users.id),
  name: text('name').notNull(),
  // ...
})

export const workoutsRelations = relations(workouts, ({ one, many }) => ({
  user: one(users, {
    fields: [workouts.userId],
    references: [users.id],
  }),
  exercises: many(workoutExercises),
}))
```

Query with relations:

```typescript
export function queryWorkoutWithUser(id: string) {
  return useDB().query.workouts.findFirst({
    where: eq(workouts.id, id),
    with: {
      user: true,
      exercises: {
        with: {
          exercise: true
        }
      }
    }
  })
}
```

## Transactions

Use transactions for atomic operations:

```typescript
export async function createWorkoutWithExercises(
  userId: string,
  workoutData: InsertWorkout,
  exercisesData: InsertWorkoutExercise[]
) {
  return useDB().transaction(async (tx) => {
    // Create workout
    const [workout] = await tx
      .insert(workouts)
      .values({ ...workoutData, userId })
      .returning()

    // Create exercises
    const exercises = await tx
      .insert(workoutExercises)
      .values(
        exercisesData.map(ex => ({
          ...ex,
          workoutId: workout.id
        }))
      )
      .returning()

    return { workout, exercises }
  })
}
```

## Aggregations

Use SQL functions for aggregations:

```typescript
import { sql } from 'drizzle-orm'

export async function queryWorkoutStats(userId: string) {
  const result = await useDB()
    .select({
      totalWorkouts: sql<number>`count(*)`,
      avgDuration: sql<number>`avg(${workouts.duration})`,
      maxWeight: sql<number>`max(${workouts.totalWeight})`,
    })
    .from(workouts)
    .where(eq(workouts.userId, userId))

  return result[0]
}
```

## Counting Records

```typescript
export async function countUserWorkouts(
  userId: string,
  status?: 'active' | 'completed'
) {
  const result = await useDB()
    .select({ count: sql<number>`count(*)` })
    .from(workouts)
    .where(and(
      eq(workouts.userId, userId),
      status ? eq(workouts.status, status) : undefined
    ))

  return result[0].count
}
```

## Pagination

```typescript
interface PaginationOptions {
  page: number
  limit: number
}

export async function queryPaginatedWorkouts(
  userId: string,
  options: PaginationOptions
) {
  const { page, limit } = options
  const offset = (page - 1) * limit

  const [workouts, [{ total }]] = await Promise.all([
    useDB().query.workouts.findMany({
      where: eq(workouts.userId, userId),
      limit,
      offset,
      orderBy: desc(workouts.createdAt)
    }),
    useDB()
      .select({ total: sql<number>`count(*)` })
      .from(workouts)
      .where(eq(workouts.userId, userId))
  ])

  return {
    data: workouts,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  }
}
```

## Critical Rules

### ✅ MUST DO
- Create all database functions in `/server/database/queries/`
- Use naming conventions: `queryX()` vs `getX()`
- Let Drizzle infer return types (no explicit `Promise<...>`)
- Implement RLS for all user data (include `userId` in where clauses)
- Use `useDB().query` for relations
- Use `useDB().select()` for complex queries
- Verify ownership before updates/deletes
- Use transactions for atomic operations

### ❌ NEVER DO
- Use `useDB()` directly in API routes
- Add explicit `Promise<...>` return types to query functions
- Use try/catch in query functions (let errors bubble up)
- Skip RLS policies for user data
- Expose data from all users without filtering
- Create duplicate function names across query files

## Reference Files

For advanced patterns:
- `references/schema-patterns.md` - Schema design patterns
- `references/relations.md` - Working with relations
- `references/transactions.md` - Transaction patterns
- `references/migrations.md` - Migration best practices
