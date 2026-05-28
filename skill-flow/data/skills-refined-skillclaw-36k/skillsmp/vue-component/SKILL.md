---
name: vue-component
description: Creating Vue 3 components following project conventions and script order. Use when building new components, refactoring existing ones, or reviewing component code for convention compliance.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.2"
---

# Vue Component Skill

Guidelines for creating Vue 3 components in this project.

> **IMPORTANT:** All code must follow the **Frontend Guidelines** in `docs/frontend-guidelines/frontend-guidelines.md`. This is the authoritative source.

> **Detailed conventions**: See [reference/conventions.md](reference/conventions.md) for script order, lessons learned, and patterns.

---

## Quick Reference

### Common Commands
```bash
npm run type-check    # Type checking
npm run lint          # Linting
npm run lint:fix      # Auto-fix lint issues
npm run dev:docker:go # Run dev server
npm run test:unit     # Run unit tests
npm run test:unit -- --grep "MyComponent"  # Run specific test
```

### Key Paths
| Path | Purpose |
|------|----------|
| `src/views/{feature}/` | Feature page components |
| `src/components/{feature}/` | Reusable feature components |
| `src/components/utilities/` | Common utility components (BaseDialog, BaseCard, etc.) |
| `src/composables/` | Stateful reusable logic |
| `src/utils/` | Stateless pure functions |
| `src/services/` | API service classes |
| `src/store/` | Pinia stores |
| `src/types/` | TypeScript type definitions |

### Development Workflow (8 Steps)
1. **Understand** → 2. **PLAN.md** → 3. **Types** → 4. **Implementation** → 5. **Lint & Format** → 6. **Type Check** → 7. **Test Decision** → 8. **Unit/E2E Tests**

---

## Development Workflow (Detailed)

| Step | Action | Output |
|------|--------|--------|
| **1. Understand** | Read existing code, routes, services, types, API endpoints | Understanding of feature context |
| **2. Create PLAN.md** | Document implementation plan with steps, file changes, decisions | `PLAN.md` in feature directory |
| **3. Define Types** | Create/update TypeScript interfaces and types | Type definitions |
| **4. Implement** | Write Vue components, composables, services following code standards | Working feature code |
| **5. Lint & Format** | Run `npm run lint:fix` to auto-fix formatting issues | Clean, formatted code |
| **6. Type Check** | Run `npm run typecheck` and fix all errors | Zero type errors |
| **7. Test Decision** | Evaluate if E2E tests are needed (see Test Decision Framework) | Decision documented in PLAN.md |
| **8. Write Tests** | Write unit tests and/or E2E tests as appropriate | Test coverage |

**Critical:** Do NOT skip steps. Steps 5-6 are mandatory before any PR.

---

## Script Order (MANDATORY)

All Vue components MUST follow this exact order in `<script setup>`:

1. **TYPES & INTERFACES** - local to this component
2. **COMPOSABLES** - external stateful hooks
3. **CONSTANTS** - static values
4. **SERVICES** - API service instances
5. **PROPS & EMITS** - component interface
6. **MODELS** - two-way bindings
7. **REFS & REACTIVES** - local mutable state
8. **COMPUTED** - derived state
9. **FUNCTIONS** - methods, handlers, helpers
10. **WATCHERS** - reactive side effects
11. **LIFECYCLE HOOKS** - always LAST

See [reference/conventions.md](reference/conventions.md) for full example with code.

---

## Import Conventions

```typescript
// External packages first
import { SomeComponent } from '@shipitsmarter/viya-ui-warehouse';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';

// Internal imports second (with @/ prefix)
import MyComponent from '@/components/my/MyComponent.vue';
import { SomeType } from '@/generated/shipping';
import { myService } from '@/services/my-service';
```

**Rules:**
- Always use `@/` prefix (no relative paths like `../../`)
- Include `.vue` extension for Vue components
- Omit `.ts/.js` extension for TypeScript files

---

## Props and Emits

```typescript
// Props - always typed with interface
interface Props {
  shipmentId: string;
  readonly?: boolean;
  status?: 'pending' | 'active' | 'completed';
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false,
  status: 'pending',
});

// Emits - always typed
interface Emits {
  (e: 'update', value: string): void;
  (e: 'close'): void;
}

const emit = defineEmits<Emits>();
```

---

## Template Conventions

- Bound attributes (`:`) and event handlers (`@`) before directives
- Use shorthands: `@` for events, `:` for props, `#` for slots
- Avoid `props.` prefix in templates (except for `props.class`)
- Don't use `()` for method bindings unless passing arguments
- Never use array index as `:key` - use `item.id`

---

## Styling with Tailwind CSS

**Always use Tailwind CSS classes instead of `<style>` blocks:**

```vue
<!-- Correct: Use Tailwind classes -->
<input class="text-sm font-medium text-white placeholder:text-white/70" />

<!-- For deep styling of library components -->
<InputComponent class="[&_input]:text-white [&_input::placeholder]:text-white/70" />
```

---

## UI Library Components

**Before creating a new component**, check if it already exists:

- **Storybook**: https://storybook.viyatest.it/
- **Package**: `@shipitsmarter/viya-ui-warehouse`

```typescript
import {
  ButtonComponent,
  InputComponent,
  DialogComponent,
  TableComponent,
} from '@shipitsmarter/viya-ui-warehouse';
```

---

## Test Decision Framework

```
Should I write an E2E test?
│
├─ Critical business workflow? (shipments, rates, bookings) → YES
├─ Crosses multiple pages/routes? → YES
├─ Area has recurring bugs? → YES
├─ Manual testing time-consuming? → YES
├─ Can unit tests cover it adequately? → Skip E2E
└─ Default → Skip E2E (start with unit tests)
```

When E2E tests are needed, use the **playwright-test** skill.

---

## Component Checklist

Before submitting:
- [ ] Script follows the mandatory order
- [ ] All props and emits are typed
- [ ] Uses `@/` absolute imports
- [ ] Template uses v-if for defensive rendering
- [ ] No `any` types
- [ ] Uses Tailwind classes (no `<style>` blocks unless necessary)
- [ ] Checked Storybook for existing UI components
- [ ] Helper functions extracted to `-helpers.ts`
- [ ] Barrel export in `index.ts`
- [ ] Unit test in `__tests__/` directory

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **api-integration** | Using services in components |
| **pr-review** | Component structure verification during review |
| **playwright-test** | Adding data-testid for E2E testing |
