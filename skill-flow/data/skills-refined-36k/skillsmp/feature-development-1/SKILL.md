---
name: feature-development
description: >
  Patterns and conventions for implementing complete features following Clean Architecture in GeroCare.
  Trigger: When creating new features, domain entities, repositories, composables, or business logic components.
license: Apache-2.0
metadata:
  author: gero-cloud
  version: "1.0"
  scope: [root]
  auto_invoke: "Creating new features or business logic"
---

## When to Use

Use this skill when creating:
- New business features (medication, care-plans, incidents, shifts, etc.)
- Domain entities and business logic
- Repository interfaces and implementations
- Application composables (use cases)
- Feature-specific Vue components
- Pinia stores for feature state

**Don't use this skill for:**
- Agnostic UI components (use `ui-components` skill)
- Testing (use `testing` skill)
- Infrastructure configuration (Firebase, Docker)

---

## Clean Architecture Structure

All features follow this structure:

```
src/business/{feature-name}/
├── domain/              # Core business logic
│   ├── {Entity}.ts      # Domain entities
│   ├── {Entity}Repository.ts  # Repository interface
│   └── {Entity}Errors.ts      # Error types and factories
├── app/                 # Application layer (use cases)
│   ├── use{Entity}.ts   # Main composable
│   └── use{Entity}Form.ts  # Form-specific composable
├── infrastructure/      # External services
│   ├── Firestore{Entity}Repository.ts  # Firestore implementation
│   ├── index.ts         # Repository factory
│   └── __tests__/       # Infrastructure tests
├── presentation/        # Vue components
│   ├── components/      # Feature-specific components
│   ├── pages/           # Feature pages
│   └── __tests__/       # Component tests
├── store.ts             # Pinia store (optional)
└── routes.ts            # Feature routes
```

---

## Critical Patterns

### 1. Domain Layer

**Entity Pattern:**
```typescript
// domain/{Entity}.ts
export interface Entity {
  id: string
  // Domain properties
  createdAt: Date
  updatedAt: Date
}

// Option 1: Manual validation (legacy)
export function validateEntity(entity: Entity): Result<Entity, string> {
  // Validation logic
  if (!entity.name) {
    return Err('name is required')
  }
  return Ok(entity)
}

// Option 2: Zod validation (recommended) - See `zod` skill
// Use Zod schemas defined in domain/{Entity}.schema.ts or domain/{Entity}.ts
```

**Repository Interface:**
```typescript
// domain/{Entity}Repository.ts
import type { Result } from '@/shared/domain/Result'
import type { EntityError } from './{Entity}Errors'
import type { Entity } from './{Entity}'

export interface EntityRepository {
  create(entity: Omit<Entity, 'id' | 'createdAt' | 'updatedAt'>): Promise<Result<Entity, EntityError>>
  findById(id: string): Promise<Result<Entity | null, EntityError>>
  findAll(): Promise<Result<Entity[], EntityError>>
  update(id: string, updates: Partial<Omit<Entity, 'id' | 'createdAt'>>): Promise<Result<Entity, EntityError>>
  delete(id: string): Promise<Result<void, EntityError>>
}
```

**Error Types:**
```typescript
// domain/{Entity}Errors.ts
export interface EntityError {
  code: string
  message: string
}

export function createEntityNotFoundError(message: string = 'Entity not found'): EntityError {
  return { code: 'ENTITY_NOT_FOUND', message }
}

export function createEntityValidationError(message: string): EntityError {
  return { code: 'ENTITY_VALIDATION_ERROR', message }
}

export function createUnknownEntityError(message: string = 'Unknown error'): EntityError {
  return { code: 'UNKNOWN_ENTITY_ERROR', message }
}
```

### 2. Infrastructure Layer

**Firestore Repository Pattern:**
```typescript
// infrastructure/Firestore{Entity}Repository.ts
import { collection, doc, addDoc, getDoc, updateDoc, deleteDoc, query, where, Timestamp } from 'firebase/firestore'
import type { Firestore } from 'firebase/firestore'
import type { EntityRepository } from '../domain/{Entity}Repository'
import type { Entity } from '../domain/{Entity}'
import type { EntityError } from '../domain/{Entity}Errors'
import { type Result, Ok, Err } from '@/shared/domain/Result'
import { createEntityNotFoundError, createUnknownEntityError } from '../domain/{Entity}Errors'

// Convert Firestore Timestamp to Date
function timestampToDate(timestamp: TimestampLike): Date {
  if (timestamp instanceof Timestamp) return timestamp.toDate()
  if (timestamp instanceof Date) return timestamp
  if (timestamp && typeof timestamp === 'object' && 'toDate' in timestamp) {
    return timestamp.toDate()
  }
  return new Date(timestamp as string)
}

// Convert Date to Firestore Timestamp
function dateToTimestamp(date: Date): Timestamp {
  return Timestamp.fromDate(date)
}

// Convert Firestore document to Entity
function firestoreDocToEntity(docId: string, data: Record<string, unknown>): Entity {
  return {
    id: docId,
    // Map Firestore data to Entity
    createdAt: timestampToDate(data.createdAt as TimestampLike),
    updatedAt: timestampToDate(data.updatedAt as TimestampLike),
  }
}

export function createEntityRepository(db: Firestore): EntityRepository {
  const collectionName = '{entities}'

  async function create(entity: Omit<Entity, 'id' | 'createdAt' | 'updatedAt'>): Promise<Result<Entity, EntityError>> {
    try {
      const now = new Date()
      const entityData = {
        ...entity,
        createdAt: dateToTimestamp(now),
        updatedAt: dateToTimestamp(now),
      }

      const docRef = await addDoc(collection(db, collectionName), entityData)
      const createdEntity: Entity = {
        ...entity,
        id: docRef.id,
        createdAt: now,
        updatedAt: now,
      }

      return Ok(createdEntity)
    } catch (error) {
      return Err(createUnknownEntityError('Failed to create entity'))
    }
  }

  async function findById(id: string): Promise<Result<Entity | null, EntityError>> {
    try {
      const docRef = doc(db, collectionName, id)
      const docSnap = await getDoc(docRef)

      if (!docSnap.exists()) {
        return Ok(null)
      }

      const entity = firestoreDocToEntity(docSnap.id, docSnap.data())
      return Ok(entity)
    } catch (error) {
      return Err(createUnknownEntityError('Failed to find entity'))
    }
  }

  // ... other methods
}
```

**Repository Factory:**
```typescript
// infrastructure/index.ts
import { db } from '@/infrastructure/firebase/firebase.config'
import { createEntityRepository as createFirestoreEntityRepository } from './FirestoreEntityRepository'
import type { EntityRepository } from '../domain/{Entity}Repository'

export function createEntityRepository(): EntityRepository {
  return createFirestoreEntityRepository(db)
}
```

### 3. App Layer (Composables)

**Main Composable Pattern:**
```typescript
// app/use{Entity}.ts
import { ref, computed } from 'vue'
import { createEntityRepository } from '../infrastructure'
import type { Entity } from '../domain/{Entity}'
import type { EntityError } from '../domain/{Entity}Errors'
import { useAuthStore } from '@/business/auth/store'

const repository = createEntityRepository()

export function useEntity() {
  const authStore = useAuthStore()
  const entities = ref<Entity[]>([])
  const entity = ref<Entity | null>(null)
  const isLoading = ref(false)
  const error = ref<EntityError | null>(null)

  const loadEntities = async () => {
    if (!authStore.user) {
      error.value = { code: 'AUTH_ERROR', message: 'User not authenticated' }
      return
    }

    isLoading.value = true
    error.value = null

    try {
      const result = await repository.findAll()
      
      if (result.success) {
        entities.value = result.value
      } else {
        error.value = result.error
      }
    } catch (err) {
      error.value = { code: 'UNKNOWN_ERROR', message: 'Failed to load entities' }
    } finally {
      isLoading.value = false
    }
  }

  const loadEntity = async (id: string) => {
    isLoading.value = true
    error.value = null

    try {
      const result = await repository.findById(id)
      
      if (result.success) {
        entity.value = result.value
      } else {
        error.value = result.error
      }
    } catch (err) {
      error.value = { code: 'UNKNOWN_ERROR', message: 'Failed to load entity' }
    } finally {
      isLoading.value = false
    }
  }

  return {
    entities: computed(() => entities.value),
    entity: computed(() => entity.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    loadEntities,
    loadEntity,
  }
}
```

**Form Composable Pattern:**
```typescript
// app/use{Entity}Form.ts
import { ref, computed } from 'vue'
import { createEntityRepository } from '../infrastructure'
import type { Entity } from '../domain/{Entity}'
import { useAuthStore } from '@/business/auth/store'

const repository = createEntityRepository()

export function useEntityForm() {
  const authStore = useAuthStore()
  const form = ref<Partial<Entity>>({})
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isFormValid = computed(() => {
    // Validation logic
    return !!form.value.name
  })

  const submit = async () => {
    if (!isFormValid.value || !authStore.user) return

    isLoading.value = true
    error.value = null

    try {
      const entityData = {
        ...form.value,
        // Add required fields
      } as Omit<Entity, 'id' | 'createdAt' | 'updatedAt'>

      const result = await repository.create(entityData)
      
      if (result.success) {
        form.value = {}
        return result.value
      } else {
        error.value = result.error.message
        return null
      }
    } catch (err) {
      error.value = 'Failed to create entity'
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    form,
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    isFormValid,
    submit,
  }
}
```

### 4. Result Type Pattern

Always use Result types for error handling:

```typescript
import { type Result, Ok, Err } from '@/shared/domain/Result'

// In repository methods
async function create(entity: Entity): Promise<Result<Entity, EntityError>> {
  try {
    // ... success logic
    return Ok(createdEntity)
  } catch (error) {
    return Err(createUnknownEntityError('Failed to create entity'))
  }
}

// In composables
const result = await repository.create(entityData)
if (result.success) {
  // Handle success: result.value
} else {
  // Handle error: result.error
}
```

### 5. Firestore Date Conversion

Always convert dates when mapping between Firestore and domain:

```typescript
type TimestampLike = Timestamp | Date | string | { toDate?: () => Date }

function timestampToDate(timestamp: TimestampLike): Date {
  if (timestamp instanceof Timestamp) return timestamp.toDate()
  if (timestamp instanceof Date) return timestamp
  if (timestamp && typeof timestamp === 'object' && 'toDate' in timestamp) {
    return timestamp.toDate()
  }
  return new Date(timestamp as string)
}

function dateToTimestamp(date: Date): Timestamp {
  return Timestamp.fromDate(date)
}
```

### 6. Store vs Composable Decision

| Use Case | Use |
|----------|-----|
| Simple CRUD operations | Composable (`app/use{Entity}.ts`) |
| Complex state management | Store (`store.ts`) |
| Cross-feature state | Store |
| Feature-specific state | Composable (preferred) |

**Prefer composables** for feature-specific state. Use stores only when:
- Multiple features share state
- Complex state management is required
- You need Pinia's devtools/debugging features

---

## Complete Feature Example

### Directory Structure
```
src/business/medication/
├── domain/
│   ├── Medication.ts
│   ├── MedicationRepository.ts
│   └── MedicationErrors.ts
├── app/
│   ├── useMedication.ts
│   └── useMedicationForm.ts
├── infrastructure/
│   ├── FirestoreMedicationRepository.ts
│   └── index.ts
├── presentation/
│   ├── components/
│   │   ├── MedicationList.vue
│   │   └── MedicationForm.vue
│   └── pages/
│       └── MedicationPage.vue
├── store.ts (optional)
└── routes.ts
```

### Step-by-Step Implementation

1. **Domain Layer**: Create entity, repository interface, error types
2. **Infrastructure Layer**: Implement Firestore repository with date conversion
3. **App Layer**: Create composables using repository
4. **Presentation Layer**: Build Vue components using composables
5. **Routes**: Define feature routes in `routes.ts`

---

## Firestore Collection Naming

- Use **plural, lowercase** names: `residents`, `medications`, `incidents`
- Match feature name: `care-plans` → `carePlans` collection
- Always index by `createdAt` or `updatedAt` for queries

---

## Error Handling Best Practices

1. **Always use Result types** in repository methods
2. **Create specific error factories** in `{Entity}Errors.ts`
3. **Handle errors in composables** and expose them to components
4. **Show user-friendly messages** in presentation layer

```typescript
// Domain: Specific error types
export function createEntityNotFoundError(message?: string): EntityError

// Infrastructure: Return Result with error
const result = await repository.findById(id)
if (!result.success) {
  return Err(createEntityNotFoundError('Entity not found'))
}

// App: Handle error in composable
if (!result.success) {
  error.value = result.error
  return
}

// Presentation: Show error to user
<p v-if="error" class="error">{{ error.message }}</p>
```

---

## Resources

- **Result Type**: `src/shared/domain/Result.ts`
- **Firebase Config**: `src/infrastructure/firebase/firebase.config.ts`
- **Zod Validation**: See `zod` skill for validation schema patterns
- **Example Feature**: `src/business/residents/`
- **Example Domain**: `src/business/residents/domain/`
- **Example Infrastructure**: `src/business/residents/infrastructure/`
- **Example App**: `src/business/residents/app/`
- **Example Presentation**: `src/business/residents/presentation/`
