---
name: testing
description: >
  Testing strategy and patterns for GeroCare using Vitest, Playwright, and testing utilities.
  Trigger: When creating tests, test helpers, factories, or working with testing infrastructure.
license: Apache-2.0
metadata:
  author: gero-cloud
  version: "1.0"
---

## When to Use

Use this skill when:
- Creating unit tests, integration tests, or E2E tests
- Setting up test helpers, factories, or fixtures
- Mocking Firebase, Vue Router, Pinia, or other dependencies
- Testing Vue components with @vue/test-utils
- Working with testing libraries (@testing-library/vue, @faker-js/faker)
- Preparing tests for Storybook integration

---

## Testing Stack

### Unit & Integration Tests
- **Framework**: Vitest 4.x
- **Vue Testing**: @vue/test-utils
- **Environment**: jsdom (browser simulation)
- **Location**: `src/**/__tests__/**/*.spec.ts`

### E2E Tests
- **Framework**: Playwright
- **Location**: `e2e/**/*.spec.ts`

### Test Helpers
- **Factories**: `src/test/factories/` (ResidentFactory, UserFactory)
- **Helpers**: `src/test/helpers/` (render, router, auth, firestore)
- **Matchers**: `src/test/matchers/` (custom Vitest matchers)
- **Setup**: `src/test/setup.ts` (Firebase emulator, global config)

---

## Critical Patterns

### Pattern 1: Using Factories

**Always use factories** instead of manually creating test data:

```typescript
// ✅ GOOD - Use factory function (recommended)
import { createResidentFactory } from '@/test/factories'

const resident = createResidentFactory()
  .withAge(75)
  .withMedicalInfo({ allergies: ['Peanuts'] })
  .build()

// ✅ ALSO GOOD - Legacy object-style API (still supported)
import { ResidentFactory } from '@/test/factories'

const resident = ResidentFactory.create()
  .withAge(75)
  .withMedicalInfo({ allergies: ['Peanuts'] })
  .build()

// ❌ BAD - Manual object creation
const resident = {
  id: 'test-id',
  firstName: 'Juan',
  // ... many more fields
}
```

**Available Factories**:
- `createResidentFactory()` - Create Resident entities (functional)
- `createUserFactory()` - Create Firebase User objects (functional)
- `ResidentFactory` - Legacy object API (delegates to createResidentFactory)
- `UserFactory` - Legacy object API (delegates to createUserFactory)

### Pattern 2: Testing Vue Components

**Use the render helper** for components that need Pinia/Router:

```typescript
import { renderComponent } from '@/test/helpers/render'
import MyComponent from './MyComponent.vue'

const wrapper = renderComponent(MyComponent, {
  props: { resident },
  router: true,  // Auto-configure router
  pinia: true,   // Auto-configure Pinia
})
```

**For simple components**, use @vue/test-utils directly:

```typescript
import { mount } from '@vue/test-utils'

const wrapper = mount(MyComponent, { props: { data } })
```

### Pattern 3: Mocking Firebase

**Firebase emulator is configured automatically** in `src/test/setup.ts`:

```typescript
import { testDb } from '@/test/setup'
import { createDocument } from '@/test/helpers/firestore'

// Use emulator automatically - no manual mocking needed
const id = await createDocument(testDb, 'residents', residentData)
```

**Mock Firebase Auth** when testing auth-related code:

```typescript
import { vi } from 'vitest'

vi.mock('firebase/auth', () => ({
  signInWithEmailAndPassword: vi.fn(),
  createUserWithEmailAndPassword: vi.fn(),
}))
```

### Pattern 4: Custom Matchers

**Use custom matchers** for domain-specific validations:

```typescript
import { ResidentFactory } from '@/test/factories'

const resident = ResidentFactory.create().withAge(75).build()

expect(resident).toBeValidResident()
expect(resident).toHaveAge(75)
```

---

## Decision Tree

```
Need to test business logic? 
  → Unit test (Vitest)
  → Use factories for test data
  → Mock external dependencies

Need to test Vue component?
  → Component test (Vitest + @vue/test-utils)
  → Use renderComponent() helper if needs Pinia/Router
  → Use mount() directly for simple components

Need to test user interactions/flows?
  → E2E test (Playwright)
  → Test against running app (dev server or preview)

Need to test multiple layers together?
  → Integration test (Vitest)
  → Use Firebase emulator for real Firestore operations
```

---

## Code Examples

### Example 1: Unit Test with Factory

```typescript
import { describe, it, expect } from 'vitest'
import { createResidentFactory } from '@/test/factories'
import { calculateAge } from '@/business/residents/domain/Resident'

describe('calculateAge', () => {
  it('should calculate age correctly', () => {
    const resident = createResidentFactory().withAge(75).build()
    const age = calculateAge(resident.dateOfBirth)
    expect(age).toBe(75)
  })
})
```

### Example 2: Component Test with Helpers

```typescript
import { describe, it, expect } from 'vitest'
import { renderComponent } from '@/test/helpers/render'
import { createResidentFactory } from '@/test/factories'
import ResidentCard from './ResidentCard.vue'

describe('ResidentCard', () => {
  it('should display resident name', () => {
    const resident = createResidentFactory()
      .withName('Juan', 'Pérez')
      .build()
    
    const wrapper = renderComponent(ResidentCard, {
      props: { resident },
    })
    
    expect(wrapper.text()).toContain('Juan Pérez')
  })
})
```

### Example 3: Integration Test with Firebase

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { testDb } from '@/test/setup'
import { createDocument, getDocumentById } from '@/test/helpers/firestore'
import { createResidentFactory } from '@/test/factories'

describe('Firestore operations', () => {
  beforeEach(async () => {
    // Cleanup handled automatically in setup.ts
  })

  it('should create and retrieve resident', async () => {
    const resident = createResidentFactory().build()
    const id = await createDocument(testDb, 'residents', resident)
    
    const retrieved = await getDocumentById(testDb, 'residents', id)
    expect(retrieved).toMatchObject(resident)
  })
})
```

### Example 4: E2E Test

```typescript
import { test, expect } from '@playwright/test'

test('should navigate to residents list', async ({ page }) => {
  await page.goto('/residents')
  await expect(page.locator('h1')).toContainText('Residents')
})
```

---

## Commands

```bash
# Run all unit tests (watch mode)
npm run test:unit

# Run tests once
npm run test:unit -- --run

# Run tests with coverage
npm run test:unit -- --coverage

# Run specific test file
npm run test:unit -- src/business/residents/__tests__/store.spec.ts

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npm run test:e2e -- --ui

# Run tests in CI mode (no watch)
npm run test:unit -- --run --coverage
```

---

## File Structure

```
src/test/
├── factories/              # Test data factories
│   ├── ResidentFactory.ts
│   ├── UserFactory.ts
│   └── index.ts
├── helpers/               # Test utilities
│   ├── render.ts         # Vue component renderer
│   ├── router.ts         # Router mocks
│   ├── auth.ts           # Auth helpers (legacy, use factories)
│   └── firestore.ts      # Firestore helpers
├── matchers/             # Custom Vitest matchers
│   └── customMatchers.ts
└── setup.ts              # Global test setup (Firebase emulator)

src/**/__tests__/         # Unit and integration tests
e2e/                      # E2E tests
```

---

## Firebase Testing

### Emulator Setup

Firebase emulator is automatically configured in `src/test/setup.ts`:
- **Firestore**: `localhost:8080`
- **Auto-cleanup**: After each test
- **No manual setup needed**: Just import `testDb` from setup

### Helper Functions

Use `src/test/helpers/firestore.ts` for common operations:
- `createDocument()` - Create document in collection
- `getDocumentById()` - Retrieve document by ID
- `updateDocument()` - Update document
- `deleteDocument()` - Delete document
- `queryDocuments()` - Query with filters

---

## Component Testing Best Practices

1. **Use renderComponent()** when component needs Pinia/Router
2. **Use mount()** directly for simple, isolated components
3. **Mock composables** at the module level when possible
4. **Use data-testid** attributes for reliable element selection
5. **Test user interactions**, not implementation details

---

## Storybook Integration

Storybook is planned but not yet configured. When ready:

- Components tested in Storybook should also have unit tests
- Use same factories for story data and tests
- Test interactions with @testing-library/vue in stories
- Reference: `@storybook/test` integration docs

---

## Common Pitfalls

### ❌ Don't create manual test data
```typescript
// BAD
const resident = { id: 'test', firstName: 'Juan', ... }
```

### ✅ Use factories
```typescript
// GOOD
const resident = ResidentFactory.create().build()
```

### ❌ Don't mock Firebase when emulator is available
```typescript
// BAD (unless necessary for specific test)
vi.mock('firebase/firestore')
```

### ✅ Use Firebase emulator
```typescript
// GOOD
import { testDb } from '@/test/setup'
```

### ❌ Don't manually setup Pinia/Router in every test
```typescript
// BAD
const pinia = createPinia()
const router = createRouter(...)
```

### ✅ Use renderComponent() helper
```typescript
// GOOD
const wrapper = renderComponent(MyComponent, { router: true, pinia: true })
```

---

## Resources

- **Factories**: See [src/test/factories/](../src/test/factories/) for ResidentFactory and UserFactory
- **Helpers**: See [src/test/helpers/](../src/test/helpers/) for render, router, and firestore utilities
- **Setup**: See [src/test/setup.ts](../src/test/setup.ts) for Firebase emulator configuration
- **Vitest Docs**: https://vitest.dev/
- **Playwright Docs**: https://playwright.dev/
- **Vue Test Utils**: https://test-utils.vuejs.org/
