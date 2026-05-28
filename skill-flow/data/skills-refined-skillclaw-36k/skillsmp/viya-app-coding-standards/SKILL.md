---
name: viya-app-coding-standards
description: Viya-app coding standards for TypeScript, Vue components, and Playwright tests. Use when reviewing, writing, or refactoring code in the viya-app repository.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Viya App Coding Standards

Comprehensive coding standards for the viya-app Vue.js frontend application. These guidelines ensure consistency across TypeScript, Vue components, and Playwright E2E tests.

---

## TypeScript & Vue Code Style

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables/Functions | `camelCase` | `calculateTotal`, `userData` |
| Components | `PascalCase` | `UserProfile.vue`, `RatesTable.vue` |
| Types/Interfaces | `PascalCase` | `RatesData`, `UserProfile` |
| Composables | `camelCase` with `use` prefix | `useRatesCalculator.ts` |
| Stores | `camelCase` with `use` prefix | `useRatesStore.ts` |
| Utilities | `kebab-case` filename | `rates-helpers.ts` |
| Constants | `SCREAMING_SNAKE_CASE` | `MAX_ITEMS`, `API_BASE_URL` |
| CSS classes | `kebab-case` | `user-profile`, `rates-table` |
| Directories | `kebab-case` | `user-profile/`, `rates-tables/` |
| Event names | `kebab-case` | `@update-value`, `@close-modal` |

### Import Rules

- Always use **absolute imports** with `@/` prefix
- Never use relative imports (`../`, `./`)
- Vue files include `.vue` extension
- TypeScript files do NOT include `.ts` extension
- Sort imports: external packages first, then internal `@/` imports

```typescript
// CORRECT
import { SomeComponent } from '@shipitsmarter/viya-ui-warehouse';
import { computed, ref } from 'vue';

import MyComponent from '@/components/feature-name/MyComponent.vue';
import { myHelper } from '@/utils/helpers';

// WRONG - relative imports
import { something } from '../utils/helpers';

// WRONG - .ts extension
import { myHelper } from '@/utils/helpers.ts';
```

### No Magic Numbers/Strings

Always use named constants instead of inline values:

```typescript
// WRONG
if (step.value === 2) { ... }
if (status === 'pending') { ... }

// CORRECT
const PRICES_STEP_INDEX = 2;
const STATUS_PENDING = 'pending';
if (step.value === PRICES_STEP_INDEX) { ... }
if (status === STATUS_PENDING) { ... }
```

### Arrow Functions Preferred

Use arrow functions unless traditional function expressions are necessary for scoping:

```typescript
// CORRECT
const myFunc = () => { ... };
const getData = async () => { ... };

// AVOID unless scoping is needed
function myFunc() { ... }
```

### Type Safety

- Never use `any` - use `unknown` with type guards instead
- Always type props, emits, variables, and functions
- Implement type guards when necessary
- Use optional chaining (`?.`) for nested objects
- Fully type stores, API responses, and component props/emits

### Comment Guidelines

**Prefer self-documenting code over comments:**
- Use descriptive variable/function names that explain *what* and *why*
- Extract complex logic (5-10+ lines) into well-named helper functions

**Comments ARE appropriate for:**
- Non-obvious workarounds (browser quirks, timing issues, API limitations)
- Backend format/protocol explanations that aren't self-evident
- Complex algorithms where intent isn't clear from code structure

**AVOID comments that:**
- Restate what the code already says
- Provide TSDoc for simple/obvious functions
- Give step-by-step explanations (extract to helper functions instead)

```typescript
// WRONG: comment restates the code
// Find the row index by matching the label
const index = data.value.findIndex((row) => row.label === highlightLabel);

// CORRECT: self-explanatory variable name
const matchingRowIndex = data.value.findIndex((row) => row.label === highlightLabel);

// CORRECT: comment explains non-obvious behavior
// setTimeout needed: nextTick waits for Vue reactivity, but TableComponent may still
// be rendering rows. 100ms allows DOM to settle.
setTimeout(() => { ... }, 100);
```

### File Structure

- Use `index.ts` to export all module contents within a directory
- Keep Vue component files under ~500 lines (split into smaller components)
- Keep helper/utility files under ~1000 lines (split into multiple files)

---

## Vue Component Guidelines

### Component Setup

- Always use `<script setup lang="ts">` for simplicity and performance
- Always type props, emits, variables, and functions
- Follow script, template order (no `<style>` blocks - use Tailwind)

### Strict Script Order (MANDATORY)

All `<script setup>` sections MUST follow this exact order:

```vue
<script setup lang="ts">
// 1. TYPES & INTERFACES (local to this component)
type MyType = { ... };
interface MyInterface { ... }

// 2. COMPOSABLES (external stateful hooks)
const route = useRoute();
const userStore = useUserStore();
const { width, height } = useWindowSize();

// 3. CONSTANTS (static values, never change)
const TABLE_OFFSET = 400;
const DEFAULT_PAGE_SIZE = 50;

// 4. SERVICES (API service instances)
const invoiceService = new InvoiceService();

// 5. PROPS & EMITS (component interface)
const props = defineProps<{ ... }>();
const emit = defineEmits<{ ... }>();

// 6. MODELS (two-way bindings)
const open = defineModel<boolean>('open', { required: true });

// 7. REFS & REACTIVES (local mutable state)
const loading = ref<boolean>(false);
const data = ref<MyType>();
const formState = reactive({ ... });

// 8. COMPUTED (derived state)
const isValid = computed(() => ...);
const filteredItems = computed(() => ...);

// 9. FUNCTIONS (methods, handlers, helpers)
const fetchData = async () => { ... };
const handleClick = () => { ... };

// 10. WATCHERS (reactive side effects)
watch(() => props.id, fetchData, { immediate: true });

// 11. LIFECYCLE HOOKS (always LAST)
onMounted(() => { ... });
onBeforeUnmount(() => { ... });
</script>
```

**Why this order matters:**
- Dependencies flow top-to-bottom (composables before refs that use them)
- Lifecycle hooks are always last because they may depend on anything above
- Watchers come before lifecycle hooks but after functions they may call
- Makes code predictable and easier to navigate

### Template Rules

Use shorthand syntax:
- `@` for `v-on`
- `:` for `v-bind`
- `#` for `v-slot`

```vue
<!-- CORRECT -->
<button @click="handleClick" :disabled="isDisabled" #header>

<!-- WRONG -->
<button v-on:click="handleClick" v-bind:disabled="isDisabled" v-slot:header>
```

No `props.` prefix in template (except `props.class`):
```vue
<!-- CORRECT -->
<span>{{ name }}</span>

<!-- WRONG -->
<span>{{ props.name }}</span>
```

No `()` for event handlers without arguments:
```vue
<!-- CORRECT -->
<button @click="save">

<!-- WRONG -->
<button @click="save()">
```

Never use array index as `:key` in `v-for` loops:
```vue
<!-- WRONG - breaks reactivity when items reorder -->
<div v-for="(item, index) in items" :key="index" />

<!-- CORRECT -->
<div v-for="item in items" :key="item.id" />
```

### Attribute Order (enforced by ESLint)

Bound attributes (`:`) and event handlers (`@`) must come **before** directives:
```vue
<!-- WRONG -->
<MyComponent v-if="show" :data="item" @click="handle" />

<!-- CORRECT -->
<MyComponent :data="item" @click="handle" v-if="show" />
```

### Defensive Rendering

Use `v-if` generously to avoid broken components when data is missing:
```vue
<UserProfile v-if="user" :user="user" />
```

### Styling

**Always use Tailwind CSS classes instead of `<style>` blocks:**
```vue
<!-- CORRECT -->
<input class="text-sm font-medium text-white placeholder:text-white/70" />

<!-- AVOID - scoped CSS -->
<style scoped>
input { font-size: 0.875rem; }
</style>
```

**For deep styling of library components, use Tailwind arbitrary variants:**
```vue
<!-- CORRECT -->
<InputComponent class="[&_input]:text-white [&_input::placeholder]:text-white/70" />

<!-- AVOID -->
<style scoped>
.my-input :deep(input) { color: white; }
</style>
```

### No Buttons/Links Inside RouterLink That Perform Actions

```vue
<!-- WRONG - button with action inside RouterLink -->
<RouterLink :to="{ name: ROUTES.USER_CREATE.name }">
  <ButtonComponent @click="saveUser()" label="Save" />
</RouterLink>

<!-- CORRECT - RouterLink for navigation only -->
<RouterLink :to="{ name: ROUTES.CARRIER_CREATE.name }">
  <ButtonComponent icon="PhPlus" label="Add Carrier" />
</RouterLink>

<!-- CORRECT - button with programmatic navigation -->
<ButtonComponent @click="router.push({ name: ROUTES.FTP_LIST.name })" label="Back" />
```

### Extract Reusable Logic

- Move utility functions and static constants to co-located `-helpers.ts` files
- Keep components focused on reactive state and template rendering
- Never define components inside other components (create separate `.vue` files)

---

## Playwright E2E Test Guidelines

### Import Conventions

```typescript
// CORRECT - Use absolute imports with ~/ prefix (maps to playwright/tests/)
import { expect, test } from '~/helpers/fixtures';
import { fillInput, navigateToConfig } from '~/helpers/functions';
import { PW_ENTITY_PREFIX } from '~/helpers/consts';

// CORRECT - Use ~/ for same-folder imports as well
import { CONTRACT_DATA } from '~/app-tests/rates/mock-data';
import { navigateToRatesOverview } from '~/app-tests/rates/rates-helpers';

// WRONG - Never use relative paths
import { something } from './mock-data';
import { something } from '../../helpers/functions';
```

### Test Structure

```typescript
// Use test.describe.serial for dependent tests
test.describe.serial('Feature Name', () => {
  let sharedState: string;
  let deleted = false;

  // Tests should be FUNCTIONAL, not navigational
  // Each test does ONE complete operation: Create, Update, or Delete
  test('01. Create entity', async ({ adminRolePage }) => { });
  test('02. Update entity', async ({ adminRolePage }) => { });
  test('03. Delete entity', async ({ adminRolePage }) => { });

  // Always include afterAll cleanup
  test.afterAll(async ({ browser }) => {
    if (!deleted) {
      // Cleanup logic
    }
  });
});
```

### Test Naming Conventions

**Test names are converted to directory names by Playwright.** Follow these rules:

```typescript
// CORRECT - Two-digit numbers at START, period and space, short names
test('00. Navigate to overview', async () => { });
test('01. Create entity', async () => { });
test('11. Create second entity', async () => { });

// CORRECT - Keep names SHORT (under ~25 chars after number)
test('11. Create download client', async () => { });

// WRONG - long names, parentheses, brackets, colons, single digits
test('11. Create FTP client - download', async () => { }); // Too long
test('11. Create entity (type)', async () => { }); // Parentheses
test('1. Create entity', async () => { }); // Use '01.'
```

### Fixtures & Naming

```typescript
// Use adminRolePage for authenticated, newRolePage for unauthenticated
test('test name', async ({ adminRolePage }) => {
  const page = adminRolePage.page;
});
```

| Type | Convention | Example |
|------|------------|---------|
| Test files | `kebab-case.spec.ts` | `rates.spec.ts` |
| Helper files | `kebab-case.ts` | `rates-helpers.ts` |
| Functions | `camelCase` | `navigateToRatesOverview` |
| Constants | `SCREAMING_SNAKE_CASE` | `RATES_API`, `CONTRACT_DATA` |
| Test fixtures | Prefix with `PW_ENTITY_PREFIX` | `pwtest-contract-abc123` |

### Element Selection Priority

**Always prefer `data-testid`.** If missing, add it to the Vue component.

| Priority | Method | Example |
|----------|--------|---------|
| 1 | `data-testid` | `getByTestId('save-btn')` |
| 2 | `getByRole` | `getByRole('button', { name: 'Save' })` |
| 3 | placeholder | `locator('input[placeholder*="name"]')` |
| 4 | `getByText` | `getByText('Success')` |
| Never | CSS selectors | `.card .header .btn` (avoid) |

### Locator Anti-Patterns

**DO NOT use fragile patterns:**

| Anti-Pattern | Example | Problem |
|--------------|---------|---------|
| Index-based column selection | `td.nth(5)`, `input.nth(2)` | Breaks when columns reorder |
| Index-based multiselect | `.multiselect.nth(3)` | Breaks when fields added/removed |
| Generic CSS class filtering | `.flex.flex-col` | Matches unrelated elements |
| Deeply nested CSS paths | `.card .header .btn` | Fragile to DOM restructuring |

**DO use robust patterns:**

```typescript
// CORRECT - data-testid
getByTestId('contract-save-btn')

// CORRECT - Scope to testid first, then internal class
getByTestId('zone-cell').locator('.multiselect')

// CORRECT - Use Radix attributes for popovers
locator('[data-radix-popper-content-wrapper]')

// CORRECT - getByRole with accessible name
getByRole('button', { name: 'Save' })
```

### Entity Cleanup Requirements

**All test entities MUST be cleanable via `entities.teardown.ts`:**

1. **Entity references MUST start with `PW_ENTITY_PREFIX`** (`pwtest-`):
```typescript
import { PW_ENTITY_PREFIX } from '~/helpers/consts';

// CORRECT - uses PW_ENTITY_PREFIX
const fixture = TestId.getFixtureId(8, PW_ENTITY_PREFIX + 'server-');
// Result: "pwtest-server-a1b2c3d4"

// WRONG - custom prefix without pwtest-
const fixture = TestId.getFixtureId(8, 'ftp-server-');
```

2. **Add cleanup section to `entities.teardown.ts`**

3. **Implement `deleteAllTest{Entity}` helper** in feature helpers

### Timeout Strategy

| Operation | Timeout | Notes |
|-----------|---------|-------|
| UI elements | 10-15s | Default expect timeout |
| API responses | **60s** | Firefox can be 2-3x slower |
| Test suite | 120s | Never reduce global timeout |

```typescript
// CRITICAL for Firefox - API wait with explicit timeout
const response = page.waitForResponse(
  (r) => r.url().includes('/api/') && r.request().method() === 'POST',
  { timeout: 60000 }
);
```

### Cross-Browser Requirements

Tests must pass on **both Chromium and Firefox** before committing.

```typescript
// Cross-browser cleanup - only cleanup in last browser
test.afterAll(async ({ browser }, testInfo) => {
  if (testInfo.project.name !== 'firefox') return;
  // ... cleanup code
});

// Cross-browser clipboard handling
try {
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);
} catch { /* Firefox works without */ }
```

### Test Design Principles

**Tests must be FUNCTIONAL, not navigational:**

| CORRECT (Functional) | WRONG (Navigational) |
|---------------------|----------------------|
| `01. Create entity` | `00. Navigate to overview` |
| `02. Update entity` | `00. Check feature enabled` |
| `03. Delete entity` | `02. Verify entity exists` |

Each functional test includes navigation and verification as part of its flow:
- **Create**: navigate -> fill form -> submit -> verify created
- **Update**: navigate -> find entity -> edit -> save -> verify changes
- **Delete**: navigate -> find entity -> delete -> verify removed

**Test count:** 3-6 tests per CRUD feature

### Async/Await Best Practices

```typescript
// Always await page interactions
await page.goto('/path');
await page.getByTestId('button').click();
await expect(page.getByText('Success')).toBeVisible();

// Use waitForURL after navigation
await page.waitForURL(/\/contract\/.*\/edit/);

// Use waitForResponse for API calls
await page.waitForResponse((r) => r.url().includes('/api/'));
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **viya-app-structure** | Understanding project paths and structure |
| **vue-component** | Creating/modifying Vue components |
| **playwright-test** | Writing E2E tests |
| **code-review** | Reviewing code changes |
