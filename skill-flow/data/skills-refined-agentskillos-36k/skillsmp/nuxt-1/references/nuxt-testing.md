# Nuxt Testing Reference

**Check:** `@nuxt/test-utils` and `vitest` in package.json

Last updated: 2025-12

## Installation

```bash
pnpm add -D @nuxt/test-utils vitest @vue/test-utils happy-dom
```

Register the module in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  modules: ["@nuxt/test-utils/module"],
})
```

## Vitest Configuration

Create `vitest.config.ts` using `defineVitestConfig` (not Vitest's `defineConfig`):

```typescript
import { defineVitestConfig } from "@nuxt/test-utils/config"

export default defineVitestConfig({
  test: {
    environment: "nuxt",
  },
})
```

## Enabling the Nuxt Environment

Three approaches (in order of preference):

### 1. Filename Suffix (Recommended)

Most visible in file explorer:

```
tests/MyComponent.nuxt.test.ts
```

### 2. File-Level Comment

```typescript
// @vitest-environment nuxt
import { describe, it, expect } from "vitest"
```

### 3. Global Config

Set in `vitest.config.ts` (applies to all tests):

```typescript
export default defineVitestConfig({
  test: {
    environment: "nuxt",
  },
})
```

To opt out in specific files: `// @vitest-environment node`

## Test Utilities

### mountSuspended

Mount components with full Nuxt environment (auto-imports, plugins, injections):

```typescript
import { mountSuspended } from "@nuxt/test-utils/runtime"
import MyComponent from "~/components/MyComponent.vue"

it("renders component", async () => {
  const wrapper = await mountSuspended(MyComponent)
  expect(wrapper.text()).toContain("Hello")
})
```

With props:

```typescript
const wrapper = await mountSuspended(MyComponent, {
  props: { title: "Test Title" },
})
```

Test at specific route:

```typescript
import App from "~/app.vue"

const wrapper = await mountSuspended(App, {
  route: "/about",
})
```

### renderSuspended

For `@testing-library/vue` integration:

```typescript
import { renderSuspended } from "@nuxt/test-utils/runtime"
import { screen, fireEvent } from "@testing-library/vue"

it("renders with testing-library", async () => {
  await renderSuspended(MyComponent)
  expect(screen.getByText("Hello")).toBeInTheDocument()
})
```

Requires additional package:

```bash
pnpm add -D @testing-library/vue
```

### mockNuxtImport

Mock auto-imported composables and utilities:

```typescript
import { mockNuxtImport } from "@nuxt/test-utils/runtime"

mockNuxtImport("useAsyncData", () => {
  return () => ({
    data: ref({ id: 1, name: "Test" }),
    status: ref("success"),
    error: ref(null),
  })
})
```

Mock `useFetch`:

```typescript
mockNuxtImport("useFetch", () => {
  return () => ({
    data: ref([{ id: 1 }, { id: 2 }]),
    status: ref("success"),
    error: ref(null),
    refresh: vi.fn(),
  })
})
```

### mockComponent

Mock child components for shallow rendering:

```typescript
import { mockComponent } from "@nuxt/test-utils/runtime"

// Inline mock
mockComponent("ExpensiveChart", {
  props: { data: Array },
  template: "<div>Chart Mock</div>",
})

// External mock file
mockComponent("ExpensiveChart", () => import("./ExpensiveChart.mock.vue"))
```

### registerEndpoint

Mock API endpoints:

```typescript
import { registerEndpoint } from "@nuxt/test-utils/runtime"

registerEndpoint("/api/users", () => [
  { id: 1, name: "Alice" },
  { id: 2, name: "Bob" },
])

registerEndpoint("/api/users/:id", (req) => {
  const id = req.params.id
  return { id, name: `User ${id}` }
})
```

With HTTP methods:

```typescript
registerEndpoint("/api/users", {
  method: "POST",
  handler: (req) => ({ id: 3, ...req.body }),
})
```

## Running Tests

```bash
# Run all tests
pnpm vitest

# Watch mode
pnpm vitest --watch

# Run specific file
pnpm vitest tests/MyComponent.nuxt.test.ts

# With coverage
pnpm vitest --coverage
```

## Test File Structure

Recommended organization:

```
project/
├── tests/
│   ├── components/
│   │   └── Button.nuxt.test.ts
│   ├── composables/
│   │   └── useCounter.test.ts
│   └── pages/
│       └── index.nuxt.test.ts
├── vitest.config.ts
└── nuxt.config.ts
```

## Component Test Example

```typescript
// tests/components/Counter.nuxt.test.ts
import { mountSuspended } from "@nuxt/test-utils/runtime"
import { describe, it, expect } from "vitest"
import Counter from "~/components/Counter.vue"

describe("Counter", () => {
  it("increments count on click", async () => {
    const wrapper = await mountSuspended(Counter)

    expect(wrapper.text()).toContain("0")

    await wrapper.find("button").trigger("click")

    expect(wrapper.text()).toContain("1")
  })

  it("accepts initial value prop", async () => {
    const wrapper = await mountSuspended(Counter, {
      props: { initialValue: 10 },
    })

    expect(wrapper.text()).toContain("10")
  })
})
```

## Composable Test Example

```typescript
// tests/composables/useCounter.test.ts
// @vitest-environment nuxt
import { describe, it, expect } from "vitest"

describe("useCounter", () => {
  it("increments counter", () => {
    const { count, increment } = useCounter()

    expect(count.value).toBe(0)
    increment()
    expect(count.value).toBe(1)
  })
})
```

## API Route Test Example

```typescript
// tests/api/users.test.ts
import { describe, it, expect } from "vitest"
import { $fetch, setup } from "@nuxt/test-utils/e2e"

describe("API Routes", async () => {
  await setup({
    server: true,
  })

  it("GET /api/users returns users", async () => {
    const users = await $fetch("/api/users")
    expect(users).toBeInstanceOf(Array)
  })
})
```

## Test Environments

- **`nuxt`** - Full Nuxt environment with auto-imports, plugins, app context. Use for components and pages.
- **`happy-dom`** / **`jsdom`** - DOM environment without Nuxt context. Use for simple utility functions.
- **`node`** - No DOM. Use for pure logic, server utilities (but not `server/` directory code).

**Note:** For `server/` directory code, use the `nuxt` environment - the `node` environment knows nothing about Nitro.

## Best Practices

### Use `.nuxt.test.ts` Suffix

Makes test environment visible in file explorer:

```
Button.nuxt.test.ts  # Uses Nuxt environment
utils.test.ts        # Uses default environment
```

### Mock External Dependencies

```typescript
mockNuxtImport("useRuntimeConfig", () => {
  return () => ({
    public: { apiBase: "http://test-api.local" },
  })
})
```

### Test Loading States

```typescript
it("shows loading state", async () => {
  mockNuxtImport("useFetch", () => {
    return () => ({
      data: ref(null),
      status: ref("pending"),
      error: ref(null),
    })
  })

  const wrapper = await mountSuspended(UserList)
  expect(wrapper.text()).toContain("Loading")
})
```

### Test Error States

```typescript
it("shows error state", async () => {
  mockNuxtImport("useFetch", () => {
    return () => ({
      data: ref(null),
      status: ref("error"),
      error: ref(new Error("Network error")),
    })
  })

  const wrapper = await mountSuspended(UserList)
  expect(wrapper.text()).toContain("Error")
})
```

## Common Issues

### Auto-imports Not Working

Ensure you're using the Nuxt environment:

```typescript
// @vitest-environment nuxt
```

Or use `.nuxt.test.ts` filename suffix.

### Component Not Found

Register the test-utils module in `nuxt.config.ts`:

```typescript
modules: ["@nuxt/test-utils/module"]
```

### Async Setup Issues

Always use `mountSuspended` (not `mount`) for components with async setup:

```typescript
// ✓ Correct
const wrapper = await mountSuspended(AsyncComponent)

// ✗ Wrong - will fail with async components
const wrapper = mount(AsyncComponent)
```
