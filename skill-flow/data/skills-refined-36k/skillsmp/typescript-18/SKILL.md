---
name: typescript
description: This skill provides TypeScript best practices and conventions for the fitness app. Use when writing TypeScript code, defining types, working with interfaces, or ensuring type safety.
---

# TypeScript Best Practices

This skill provides strict TypeScript conventions for the fitness application.

## Core Principles

**Strict TypeScript**: All code must be strictly typed. The project uses strict mode with no exceptions.

**Prefer Interfaces**: Use interfaces over type aliases for better extendability and declaration merging.

**No Enums**: Avoid TypeScript enums. Use const objects (maps) for better type safety and flexibility.

## Type Safety Rules

### ✅ MUST DO

**1. Explicit typing for all code:**
```typescript
// ✅ Correct: Explicitly typed
function calculateBMI(weight: number, height: number): number {
  return weight / (height * height)
}

// ✅ Correct: Typed parameters
const users: User[] = []
const count: number = users.length
```

**2. Type component props and emits:**
```vue
<script setup lang="ts">
interface Props {
  workout: Workout
  isActive?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  update: [workout: Workout]
  delete: [id: string]
}>()
</script>
```

**3. Use `unknown` instead of `any`:**
```typescript
// ✅ Correct: Use unknown for type-safe handling
function processData(data: unknown) {
  if (typeof data === 'string') {
    return data.toUpperCase()
  }
  throw new Error('Invalid data type')
}

// ❌ Wrong: Using any
function processData(data: any) {
  return data.toUpperCase() // Unsafe
}
```

**4. Implement type guards:**
```typescript
interface Workout {
  id: string
  name: string
}

function isWorkout(value: unknown): value is Workout {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    typeof (value as Workout).id === 'string' &&
    typeof (value as Workout).name === 'string'
  )
}

// Usage
function processData(data: unknown) {
  if (isWorkout(data)) {
    // TypeScript knows data is Workout here
    console.log(data.name)
  }
}
```

### ❌ NEVER DO

**1. Never use `any`:**
```typescript
// ❌ Wrong
function process(data: any) {
  return data.property // Unsafe
}

// ✅ Correct
function process(data: unknown) {
  if (isValidData(data)) {
    return data.property // Type-safe
  }
}
```

**2. Never use `@ts-ignore`:**
```typescript
// ❌ Wrong: Ignoring TypeScript errors
// @ts-ignore
const value = dangerousOperation()

// ✅ Correct: Fix the underlying issue or use proper type assertion
const value = dangerousOperation() as ExpectedType
```

**3. Never use TypeScript enums:**
```typescript
// ❌ Wrong: TypeScript enum
enum WorkoutType {
  Strength = 'strength',
  Cardio = 'cardio',
}

// ✅ Correct: Const object
const WORKOUT_TYPE = {
  STRENGTH: 'strength',
  CARDIO: 'cardio',
} as const

type WorkoutType = typeof WORKOUT_TYPE[keyof typeof WORKOUT_TYPE]
```

## Interfaces vs Types

### Prefer Interfaces

Interfaces are preferred for object shapes because they:
- Support declaration merging
- Provide better error messages
- Are more extensible

```typescript
// ✅ Correct: Interface for object shapes
interface User {
  id: string
  name: string
  email: string
}

interface AdminUser extends User {
  permissions: string[]
}

// Declaration merging works with interfaces
interface User {
  createdAt: Date
}
```

### When to Use Types

Use type aliases for:
- Unions
- Intersections
- Primitives
- Mapped types
- Conditional types

```typescript
// ✅ Correct: Type for unions
type Status = 'active' | 'inactive' | 'pending'

// ✅ Correct: Type for intersections
type TimestampedUser = User & {
  createdAt: Date
  updatedAt: Date
}

// ✅ Correct: Mapped type
type ReadonlyUser = {
  readonly [K in keyof User]: User[K]
}
```

## Database-First Types

**Derive all types from Drizzle DB schemas:**

```typescript
// ✅ Correct: Derive from DB schema
import { type InferSelectModel, type InferInsertModel } from 'drizzle-orm'
import { workouts } from '~~/server/database/schema/workouts'

type Workout = InferSelectModel<typeof workouts>
type InsertWorkout = InferInsertModel<typeof workouts>

// ✅ Correct: Extend DB types for specific use cases
interface WorkoutWithExercises extends Workout {
  exercises: Exercise[]
}

// ❌ Wrong: Manually defining types that mirror DB schemas
interface Workout {
  id: string
  name: string
  createdAt: Date
  // ... duplicating schema
}
```

## Error Types

Use proper, specific error types:

```typescript
// ✅ Correct: Specific error types
class NotFoundError extends Error {
  statusCode = 404
  constructor(message: string) {
    super(message)
    this.name = 'NotFoundError'
  }
}

class ValidationError extends Error {
  statusCode = 400
  constructor(
    message: string,
    public field: string
  ) {
    super(message)
    this.name = 'ValidationError'
  }
}

// Usage
function getWorkout(id: string): Workout {
  const workout = findWorkout(id)
  if (!workout) {
    throw new NotFoundError(`Workout ${id} not found`)
  }
  return workout
}
```

## Const Assertions

Use `as const` for immutable values:

```typescript
// ✅ Correct: Const assertion for literal types
const WORKOUT_TYPES = {
  STRENGTH: 'strength',
  CARDIO: 'cardio',
  FLEXIBILITY: 'flexibility',
} as const

type WorkoutType = typeof WORKOUT_TYPES[keyof typeof WORKOUT_TYPES]
// Type: 'strength' | 'cardio' | 'flexibility'

// ✅ Correct: Const assertion for arrays
const DIFFICULTY_LEVELS = ['beginner', 'intermediate', 'advanced'] as const
type DifficultyLevel = typeof DIFFICULTY_LEVELS[number]
// Type: 'beginner' | 'intermediate' | 'advanced'
```

## Generic Types

Use generics for reusable, type-safe functions:

```typescript
// ✅ Correct: Generic type for API responses
interface ApiResponse<T> {
  data: T
  meta: {
    page: number
    total: number
  }
}

function fetchList<T>(endpoint: string): Promise<ApiResponse<T>> {
  return $fetch<ApiResponse<T>>(endpoint)
}

// Usage with type inference
const workouts = await fetchList<Workout>('/api/workouts')
// workouts.data is Workout[]
```

## Utility Types

Leverage TypeScript utility types:

```typescript
// Partial - make all properties optional
type UpdateWorkout = Partial<Workout>

// Pick - select specific properties
type WorkoutSummary = Pick<Workout, 'id' | 'name' | 'createdAt'>

// Omit - exclude specific properties
type WorkoutWithoutTimestamps = Omit<Workout, 'createdAt' | 'updatedAt'>

// Required - make all properties required
type RequiredUser = Required<User>

// Record - create object type with specific keys
type WorkoutMap = Record<string, Workout>

// ReturnType - extract return type of function
function getWorkout() {
  return { id: '1', name: 'Test' }
}
type WorkoutReturn = ReturnType<typeof getWorkout>
```

## Discriminated Unions

Use discriminated unions for type-safe state handling:

```typescript
// ✅ Correct: Discriminated union
type LoadingState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }

function renderWorkout(state: LoadingState<Workout>) {
  switch (state.status) {
    case 'idle':
      return 'Not loaded'
    case 'loading':
      return 'Loading...'
    case 'success':
      return state.data.name // TypeScript knows data exists
    case 'error':
      return state.error.message // TypeScript knows error exists
  }
}
```

## Zod Integration

Use Zod for runtime validation with TypeScript inference:

```typescript
import { z } from 'zod'

// ✅ Correct: Define Zod schema
const createWorkoutSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  exercises: z.array(z.uuid()).min(1),
})

// Infer TypeScript type from Zod schema
type CreateWorkout = z.infer<typeof createWorkoutSchema>

// Use in validation
function validateWorkout(data: unknown): CreateWorkout {
  return createWorkoutSchema.parse(data)
}
```

## Function Types

Type function parameters and return values:

```typescript
// ✅ Correct: Explicitly typed function
function calculateVolume(
  sets: number,
  reps: number,
  weight: number
): number {
  return sets * reps * weight
}

// ✅ Correct: Typed arrow function
const calculateCalories = (
  duration: number,
  intensity: number
): number => {
  return duration * intensity * 3.5
}

// ✅ Correct: Function type
type MathOperation = (a: number, b: number) => number

const add: MathOperation = (a, b) => a + b
const subtract: MathOperation = (a, b) => a - b
```

## Async Function Types

Always type async functions:

```typescript
// ✅ Correct: Typed async function
async function fetchWorkout(id: string): Promise<Workout> {
  const workout = await $fetch<Workout>(`/api/workouts/${id}`)
  return workout
}

// ✅ Correct: Async function with error handling
async function createWorkout(
  data: InsertWorkout
): Promise<Workout | null> {
  try {
    return await $fetch<Workout>('/api/workouts', {
      method: 'POST',
      body: data
    })
  } catch {
    return null
  }
}
```

## Branded Types

Use branded types for type-safe IDs:

```typescript
// ✅ Correct: Branded type for IDs
type WorkoutId = string & { readonly __brand: 'WorkoutId' }
type UserId = string & { readonly __brand: 'UserId' }

function createWorkoutId(id: string): WorkoutId {
  return id as WorkoutId
}

function getWorkout(id: WorkoutId): Workout {
  // ...
}

// Type safety prevents mixing IDs
const workoutId = createWorkoutId('workout-123')
const userId = createUserId('user-456')

getWorkout(workoutId) // ✅ OK
getWorkout(userId) // ❌ Type error
```

## Type Narrowing

Use type narrowing for safe type handling:

```typescript
function processValue(value: string | number | null) {
  // Type narrowing with typeof
  if (typeof value === 'string') {
    return value.toUpperCase() // value is string
  }

  if (typeof value === 'number') {
    return value.toFixed(2) // value is number
  }

  // value is null here
  return 'No value'
}

// Type narrowing with in operator
interface Workout {
  name: string
}

interface Exercise {
  title: string
}

function getName(item: Workout | Exercise): string {
  if ('name' in item) {
    return item.name // item is Workout
  }
  return item.title // item is Exercise
}
```

## Summary: TypeScript Rules

### Type Safety
- ✅ Use strict TypeScript everywhere
- ✅ Prefer interfaces for object shapes
- ✅ Use type aliases for unions and intersections
- ✅ Implement type guards for runtime validation
- ✅ Use `unknown` instead of `any`
- ❌ Never use `any`
- ❌ Never use `@ts-ignore`
- ❌ Never use TypeScript enums

### Database Types
- ✅ Derive types from Drizzle schemas
- ✅ Use `InferSelectModel` and `InferInsertModel`
- ❌ Don't manually define types that mirror DB schemas

### Best Practices
- ✅ Type all function parameters and returns
- ✅ Type component props and emits
- ✅ Use const assertions for literal types
- ✅ Leverage utility types (Partial, Pick, Omit, etc.)
- ✅ Use discriminated unions for state
- ✅ Integrate Zod for runtime validation

## Reference Files

For advanced patterns:
- `references/advanced-types.md` - Advanced TypeScript patterns
- `references/zod-integration.md` - Zod and TypeScript integration
