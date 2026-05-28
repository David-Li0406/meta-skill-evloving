---
name: coding-style
description: >
  Coding style guide and conventions for GeroCare. Provides decision trees and patterns for writing consistent, maintainable code.
  Trigger: When writing code, refactoring, or making style decisions.
license: Apache-2.0
metadata:
  author: gero-cloud
  version: "1.0"
  scope: [root]
  auto_invoke: "Writing code, refactoring, or making style decisions"
---

## When to Use

Use this skill when:
- Writing new code or functions
- Refactoring existing code
- Making style decisions (ternaries vs if/else, function formatting, etc.)
- Organizing imports or code structure
- Naming variables, functions, types, or files
- Writing Vue components or TypeScript code
- Handling errors or async operations

**Don't use this skill for:**
- Architectural decisions (use `feature-development` skill)
- UI component patterns (use `ui-components` skill)
- Testing patterns (use `testing` skill)

---

## Configuration Reference

### Prettier

```json
{
  "semi": false,
  "singleQuote": true,
  "printWidth": 100
}
```

**Rules:**
- No semicolons
- Single quotes
- Maximum 100 characters per line

### ESLint

**Key Rules:**
- Prohibit relative imports in `src/` (use alias `@/`)
- Auto-sort imports with `simple-import-sort`
- Allow relative imports only in tests and config files

### EditorConfig

**Settings:**
- Indentation: 2 spaces
- Charset: UTF-8
- End of line: LF
- Insert final newline: Yes

---

## Decision Trees

### Ternaries vs If/Else

**Use ternaries when:**
- ✅ Simple expression in return/assignment (1-2 lines)
- ✅ Conditional value assignment (single value)
- ✅ Simple 2-option case

**Use if/else when:**
- ✅ Multi-line logic
- ✅ Side effects (multiple assignments, function calls)
- ✅ Complex conditions with multiple branches
- ✅ Early returns

**Ternary nesting:**
- ✅ Allowed up to 2-3 levels with clear formatting
- ❌ Avoid more than 3 levels (use if/else instead)

**Example - Ternary (correct):**
```typescript
const status = isLoading ? 'loading' : 'ready'

const result = residentId
  ? activeOnly
    ? await repository.findActiveByResident(residentId)
    : await repository.findByResident(residentId)
  : await repository.findAll()
```

**Example - If/Else (correct):**
```typescript
if (result.success) {
  carePlans.value = result.value
  isLoading.value = false
  error.value = null
} else {
  error.value = result.error
  carePlans.value = []
}
```

### Function Parameters Formatting

**Inline format (1-2 simple parameters):**
```typescript
async function fetchCarePlan(id: string) { }
```

**Multiline format (3+ parameters or complex types):**
```typescript
async function updateCarePlan(
  id: string,
  updates: Partial<Omit<CarePlan, 'id' | 'createdAt'>>,
  options?: UpdateOptions
) { }
```

**Optional parameters:**
- Use `?` for optional: `residentId?: string`
- Use defaults when appropriate: `status: 'completed' | 'skipped' = 'completed'`

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| **Files** | PascalCase (Vue), camelCase (TS) | `ResidentForm.vue`, `useResidents.ts` |
| **Functions** | camelCase, descriptive verbs | `loadResidents`, `fetchCarePlan` |
| **Variables** | camelCase, booleans with `is`/`has` | `isLoading`, `carePlans`, `hasError` |
| **Types/Interfaces** | PascalCase, no `I` prefix | `CarePlan`, `ResidentError` |
| **Constants** | UPPER_SNAKE_CASE (global), camelCase (local) | `API_BASE_URL`, `repository` |

---

## Critical Patterns

### 1. Imports Organization

**Order (auto-sorted by ESLint):**
1. Side effect imports (`import 'something'`)
2. Node.js builtins (`import fs from 'node:fs'`)
3. Packages (`import { ref } from 'vue'`)
4. Aliases (`import { useAuthStore } from '@/business/auth/store'`)
5. Parent imports (`import { something } from '../domain'`)
6. Current directory (`import { helper } from './utils'`)
7. Styles (`import './styles.css'`)

**Grouping:**
- Separate imports with blank lines
- Group Vue core, then aliases `@/`, then types

**Example:**
```typescript
import { computed, ref } from 'vue'

import { useAuthStore } from '@/business/auth/store'
import type { Resident } from '@/business/residents/domain/Resident'
import { createResidentRepository } from '@/business/residents/infrastructure'
```

**Type imports:**
- Use `import type` for types-only imports
- Place type imports on separate line after value imports

### 2. Async/Await Pattern

**Always use async/await** (never `.then()` / `.catch()`):

```typescript
// ✅ Correct
async function loadResidents() {
  isLoading.value = true
  try {
    const result = await repository.findAll()
    if (result.success) {
      residents.value = result.value
    }
  } catch {
    error.value = { code: 'UNKNOWN_ERROR', message: 'Failed to load residents' }
  } finally {
    isLoading.value = false
  }
}
```

**Standard pattern:**
1. Set `isLoading.value = true` before try
2. Reset `error.value = null` before try
3. Try block with async operation
4. Check `result.success` if using Result type
5. Catch block for unexpected errors
6. Finally block to set `isLoading.value = false`

### 3. Result Type Pattern

**Always use `Result<T, E>` in repositories:**

```typescript
async function findById(id: string): Promise<Result<CarePlan | null, CarePlanError>> {
  try {
    const result = await repository.findById(id)
    return Ok(carePlan)
  } catch (error) {
    return Err(createUnknownCarePlanError('Failed to find care plan'))
  }
}
```

**Always check `result.success` before accessing value:**

```typescript
// ✅ Correct
const result = await repository.findById(id)
if (result.success) {
  carePlan.value = result.value // TypeScript knows value exists
} else {
  error.value = result.error // TypeScript knows error exists
}

// ❌ Incorrect - Direct access without check
const result = await repository.findById(id)
carePlan.value = result.value // Error: value may not exist
```

### 4. TypeScript Patterns

**Explicit types:**
- Always for function parameters
- Always for public function returns (when not obvious)
- Use inference for local variables when type is obvious

**Type utilities:**
```typescript
// Omit for removing fields
type CreateInput = Omit<Entity, 'id' | 'createdAt' | 'updatedAt'>

// Partial for updates
updates: Partial<Omit<Entity, 'id' | 'createdAt'>>

// Pick for selecting fields
type Summary = Pick<Entity, 'id' | 'title' | 'status'>
```

**Avoid `any`, use `unknown`:**

```typescript
// ✅ Correct
function validate(data: unknown): Result<Entity, Error> { }

// ❌ Incorrect
function validate(data: any): Entity { }
```

### 5. Vue Component Structure

```vue
<script setup lang="ts">
import { computed, ref } from 'vue'

defineOptions({
  name: 'AppComponentName',
})

interface Props {
  // Props
}

const props = withDefaults(defineProps<Props>(), {
  // Defaults
})

const emit = defineEmits<{
  'event-name': [value: Type]
}>()

// State, computed, methods
</script>

<template>
  <!-- Template -->
</template>

<style scoped>
/* Styles */
</style>
```

**Conventions:**
- Always use `<script setup lang="ts">`
- Use `defineOptions` for component name (`App{ComponentName}`)
- Type props with interfaces
- Type emits with `defineEmits<{...}>()`
- Always use `scoped` styles

### 6. Comments

**Comment when:**
- ✅ Explaining "why" (not "what")
- ✅ Complex business logic requiring context
- ✅ Public API functions (use JSDoc)

**Don't comment:**
- ❌ Obvious code
- ❌ Temporary refactors without context
- ❌ Redundant explanations

**Example:**
```typescript
// ✅ Good - Explains "why"
// Add current user as assigned caregiver if not already included
// (required for proper permission tracking)
const residentWithCaregiver = {
  ...residentData,
  assignedCaregivers: residentData.assignedCaregivers.includes(authStore.user.uid)
    ? residentData.assignedCaregivers
    : [...residentData.assignedCaregivers, authStore.user.uid],
}

// ❌ Bad - Obvious comment
// Set isLoading to true
isLoading.value = true
```

**JSDoc for public APIs:**
```typescript
/**
 * Validates a resident entity using Zod schema
 * @param resident - The resident data to validate (can be unknown)
 * @returns Result containing validated Resident or validation error
 */
export function validateResident(resident: unknown): Result<Resident, ResidentError> {
  // ...
}
```

---

## Common Patterns

### Error Handling Pattern

```typescript
async function fetchCarePlan(id: string) {
  isLoading.value = true
  error.value = null

  try {
    const result = await repository.findById(id)
    if (result.success) {
      currentCarePlan.value = result.value
    } else {
      error.value = result.error
    }
  } catch {
    error.value = { code: 'UNKNOWN_ERROR', message: 'Failed to fetch care plan' }
  } finally {
    isLoading.value = false
  }
}
```

### Loading State Pattern

```typescript
// Before async operation
isLoading.value = true
error.value = null

try {
  // ... async operation
} catch {
  // ... handle error
} finally {
  // Always reset loading state
  isLoading.value = false
}
```

### Early Return Pattern

```typescript
async function loadResidents() {
  // Early return for invalid state
  if (!authStore.user) {
    error.value = { code: 'AUTH_ERROR', message: 'User not authenticated' }
    return
  }

  // ... rest of function
}
```

---

## Spacing and Formatting

### Blank Lines

- After imports (between groups)
- Before return statements
- Between logical blocks

### Line Length

- Maximum 100 characters (enforced by Prettier)
- Break long lines at logical points

### Indentation

- Always 2 spaces (never tabs)
- Consistent indentation for related blocks

---

## Quick Reference

| Pattern | Example |
|---------|---------|
| **Ternary** | `const status = isLoading ? 'loading' : 'ready'` |
| **If/Else** | `if (result.success) { ... } else { ... }` |
| **Function params (simple)** | `function fetch(id: string) { }` |
| **Function params (complex)** | `function update(id: string, updates: Partial<Entity>) { }` |
| **Optional param** | `function fetch(id?: string) { }` |
| **Result type** | `const result = await repo.findById(id); if (result.success) { ... }` |
| **Async/await** | `const result = await repository.findAll()` |
| **Type import** | `import type { Entity } from './Entity'` |
| **Alias import** | `import { useStore } from '@/business/auth/store'` |

---

## Resources

- **Full Style Guide**: `docs/CODING_STYLE.md`
- **Prettier Config**: `.prettierrc.json`
- **ESLint Config**: `eslint.config.ts`
- **EditorConfig**: `.editorconfig`
- **Result Type**: `src/shared/domain/Result.ts`
- **Example Store**: `src/business/care-plans/store.ts`
- **Example Composable**: `src/business/residents/app/useResidents.ts`
- **Example Component**: `src/business/residents/presentation/components/ResidentForm.vue`
