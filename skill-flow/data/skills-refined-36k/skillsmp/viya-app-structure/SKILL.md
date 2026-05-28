---
name: viya-app-structure
description: Understanding viya-app project structure and where to find things. Use when exploring the codebase, finding files, navigating components, or understanding how the Vue.js application is organized.
license: MIT
metadata:
  author: shipitsmarter
  version: "2.0"
---

# Viya App Structure

Guide to understanding and navigating the viya-app project structure.

---

## Project Overview

viya-app is a Vue 3 + TypeScript enterprise Transport Management Application providing:
- Shipment management
- Address books
- Pickup scheduling
- Rate management
- Workflow configuration

---

## Directory Structure

```
viya-app/
├── src/                      # Application source code
│   ├── assets/               # Static assets (images, fonts, SCSS)
│   ├── components/           # Reusable Vue components by feature
│   ├── composables/          # Vue 3 composables (use* pattern)
│   ├── constants/            # Application-wide constants
│   ├── directives/           # Custom Vue directives
│   ├── generated/            # Auto-generated API types (DO NOT EDIT)
│   ├── injection-keys/       # Vue provide/inject keys
│   ├── json-forms/           # JSON Forms integration
│   ├── layout/               # Layout components
│   ├── plugins/              # Vue plugins
│   ├── router/               # Vue Router configuration
│   ├── services/             # API service layer
│   ├── store/                # Pinia stores
│   ├── test-utils/           # Test helper utilities
│   ├── types/                # Shared TypeScript types
│   ├── utils/                # Utility functions
│   └── views/                # Page-level components by feature
├── playwright/               # E2E tests (separate npm project)
├── agents/                   # AI agent documentation
│   ├── plans/                # Feature planning documents
│   └── skills/               # Skill definitions
└── docs/                     # Project documentation
```

---

## Quick Reference

| Looking for... | Location |
|----------------|----------|
| Reusable component | `src/components/<feature>/` |
| Full page | `src/views/<domain>/` |
| API service | `src/services/` |
| API types | `src/generated/<api>/` |
| Global state | `src/store/` |
| Composable | `src/composables/` |
| Utility function | `src/utils/` |
| Route config | `src/router/` |
| Unit test | `src/<path>/__tests__/` |
| E2E test | `playwright/tests/` |
| UI library components | `@shipitsmarter/viya-ui-warehouse` |
| Storybook | https://storybook.viyatest.it/ |

---

## Common Commands

```bash
# Type checking
npm run type-check

# Linting & formatting
npm run lint
npm run lint:fix

# Run dev server
npm run dev:docker:go

# Run unit tests
npm run test:unit
npm run test:unit -- --grep "MyComponent"

# Run Playwright tests
cd playwright
npx playwright test tests/app-tests/{feature}/{feature}.spec.ts --no-deps --project=chromium

# Regenerate API types
npm run generate-api
```

---

## Finding Components

### Reusable components: `src/components/`

Organized by feature area with 36+ directories:

```
src/components/
├── ui/                       # Base UI components (dialog, popover, table)
├── utilities/                # Common utilities (BaseDialog, BaseCard, etc.)
├── docs/                     # In-app documentation system
├── filters/                  # Filter components for list views
├── spotlight/                # Command palette / search
├── condition-builder-new/    # Condition/rule builder
├── shipment/                 # Shipment-specific components
├── upload-download/          # File upload/download components
├── drag-drop/                # Drag-and-drop components
└── ...
```

**Pattern:** `src/components/<feature>/<ComponentName>.vue`

### Page components: `src/views/`

Full pages organized by domain:

```
src/views/
├── shipment/                 # Shipment pages
│   ├── ShipmentOverviewPage.vue
│   ├── create/               # Shipment creation flow
│   └── details/              # Shipment detail views
├── pickup/                   # Pickup scheduling
├── address/                  # Address book
├── freight-settlement/       # Invoicing
├── configuration/            # Settings pages
└── ...
```

**Pattern:** `src/views/<domain>/<PageName>Page.vue`

### UI Component Sources (check in order)

1. `@shipitsmarter/viya-ui-warehouse` - Shared component library
2. `src/components/utilities/` - App-specific utilities (BaseDialog, etc.)
3. `src/components/ui/` - shadcn-based primitives
4. `src/components/{feature}/` - Feature-specific components

**Note:** Use `BaseDialog` from `@/components/utilities/BaseDialog.vue`, NOT `DialogComponent` from warehouse.

---

## Finding Services

### API services: `src/services/`

```
src/services/
├── clients/                  # Base API client setup
├── shipment-service.ts       # Shipment API calls
├── pickup-service.ts         # Pickup API calls
├── address-service.ts        # Address API calls
└── ...
```

**Pattern:** Services use generated types from `@/generated/`

```typescript
import { ShipmentService } from '@/services/shipment-service';
import type { Shipment } from '@/generated/shipping';
```

---

## Finding Generated Types

### Auto-generated from OpenAPI: `src/generated/`

```
src/generated/
├── shipping/                 # Shipment API types
├── rates/                    # Rates API types
├── address/                  # Address API types
├── pickup/                   # Pickup API types
└── ...
```

**Usage:**
```typescript
import type { Shipment, ShipmentStatus } from '@/generated/shipping';
import type { Rate, RateRequest } from '@/generated/rates';
```

---

## Finding Stores

### Pinia stores: `src/store/`

```
src/store/
├── user.ts                   # User/auth state
├── carrier-profile.ts        # Carrier profile state
├── errors.ts                 # Error handling
└── ...
```

**Usage:**
```typescript
import { useUserStore } from '@/store/user';
import { useCarrierProfileStore } from '@/store/carrier-profile';
```

---

## Finding Composables

### Vue composables: `src/composables/`

```
src/composables/
├── useAccess.ts              # Permission checking
├── useIntercom.ts            # Intercom integration
├── useSignedUrl.ts           # Signed URL handling
├── useFormDirtyCheck.ts      # Form dirty state
├── freight-settlement/       # Feature-specific composables
└── ...
```

**Pattern:** `use<Name>.ts` with camelCase

---

## Finding Routes

### Router configuration: `src/router/`

```
src/router/
├── index.ts                  # Main router setup
├── routes.ts                 # Route constants (ROUTES object)
├── shipment.ts               # Shipment routes
├── pickup.ts                 # Pickup routes
└── ...
```

**Route constants:**
```typescript
import { ROUTES } from '@/router/routes';

router.push({ name: ROUTES.SHIPMENT_DETAIL.name, params: { id } });
```

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
import { useMyStore } from '@/store/my-store';
```

**Rules:**
- Always use `@/` prefix (no relative paths like `../../`)
- Include `.vue` extension for Vue components
- Omit `.ts/.js` extension for TypeScript files

---

## Key Files

| File | Purpose |
|------|---------|
| `src/main.ts` | App entry point, plugin setup |
| `src/App.vue` | Root component |
| `src/router/routes.ts` | All route name constants |
| `src/services/clients/index.ts` | API client configuration |
| `vite.config.ts` | Build configuration |
| `tsconfig.json` | TypeScript configuration |
| `.github/copilot-instructions.md` | Coding conventions |

---

## Local Warehouse Development

When testing warehouse changes locally in viya-app:

```bash
# In viya-app - watches warehouse dist folder and syncs to node_modules
npm run watch:lib

# In viya-ui-warehouse - builds on changes
npm run library:watch
```

**Important:** After running `watch:lib`, your `package.json` will have `--local` suffix. Revert before committing:
```bash
git checkout package.json
```

See `docs/local-warehouse-testing.md` for full setup guide.

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **vue-component** | Creating new components |
| **api-integration** | Working with services and API types |
| **unit-testing** | Writing tests |
| **playwright-test** | Writing E2E tests |
| **viya-ui-warehouse-structure** | Working with the shared component library |
