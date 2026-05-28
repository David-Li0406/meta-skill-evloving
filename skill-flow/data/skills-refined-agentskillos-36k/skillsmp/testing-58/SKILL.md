---
name: testing
description: >
  Testing strategies based on Clean Architecture layers.
  Trigger: Invoke when writing tests to enforce layer-specific mocking strategies (Unit vs Integration)
license: Apache-2.0
metadata:
  author: jmgomezdev
  version: '1.0'
---

## 🧠 Rules by Layer

### 1. Domain Layer (`src/domain`)

- **Type:** Pure Unit Tests.
- **Mocks:** ❌ NONE.
- **Focus:** Test business logic, Zod schema validations (`.parse()`), and utility functions.
- **Example:** `expect(productSchema.parse(invalidData)).toThrow()`.

### 2. Application Layer (`src/application`)

- **Type:** Unit Tests.
- **Mocks:** ✅ Mock **Infrastructure Repositories** and **Zustand Stores**.
- **Focus:**
  - Test `queryOptions` generation keys.
  - Test complex hooks logic (use `renderHook`).
  - Test Zustand actions (state mutations).
- **Tooling:** `vi.spyOn`, `mockZustand`.

### 3. Infrastructure Layer (`src/infrastructure`)

- **Type:** Integration Tests.
- **Mocks:** ✅ Mock **HTTP Network** (use `msw` or `nock`).
- **Focus:**
  - Verify **Repositories** call the correct endpoints.
  - Verify **Mappers** correctly transform API DTOs -> Domain Entities.
  - Verify **DTOs** match expected API shapes.

### 4. Presentation Layer (`src/presentation`)

- **Type:** Component Integration Tests.
- **Mocks:** ✅ Mock **Application Layer Hooks** (e.g., `useProductDetail`).
- **Forbidden:** ❌ NEVER mock `axios`, `fetch`, or `useQuery` directly in components.
- **Focus:**
  - Test UI rendering based on data states (Success, Empty).
  - Test User Interactions (Click, Type) firing handlers.
  - Test Accessibility (`aria-labels`).
- **Tooling:** `render`, `screen`, `userEvent`.

## 📝 Conventions

- **Naming:** `Filename.test.tsx` or `Filename.spec.ts`.
- **Location:** Co-located next to the source file.
- **Async:** Always use `await screen.findBy*` for async elements, never `wait()`.

## Keywords

`vitest`, `react-testing-library`, `rtl`, `user-event`, `msw`, `unit-testing`, `integration-testing`, `mocks`.
