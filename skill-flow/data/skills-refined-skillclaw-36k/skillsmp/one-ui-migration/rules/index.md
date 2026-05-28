# One-UI Migration Rules

> Angular 16 (f2e-networking) → Angular 20 (one-ui)

## Core Principle

```
MIGRATE, DON'T INNOVATE
```

100% behavior parity with Legacy. No improvements, no optimizations, no new features.

---

## What do you need? → Check this

### Tool Reference

| I need to... | Check this tool |
|--------------|-----------------|
| Add form validation | [tools/one-validators.md](./tools/one-validators.md) ⭐ |
| Create a form | [tools/form-builder.md](./tools/form-builder.md) ⭐ |
| Use shared helpers | [tools/shared-helpers.md](./tools/shared-helpers.md) 🆕 |
| Manage state | [tools/signal-store.md](./tools/signal-store.md) |
| Handle loading states | [tools/loading-states.md](./tools/loading-states.md) |
| Create a table | [tools/common-table.md](./tools/common-table.md) |
| Create a dialog | [tools/ui/dialogs.md](./tools/ui/dialogs.md) |
| Use MX components | [tools/mx-components.md](./tools/mx-components.md) |
| Page structure | [tools/ui/page-layout.md](./tools/ui/page-layout.md) |
| Configure routes | [tools/routing.md](./tools/routing.md) |
| Translate text | [tools/transloco.md](./tools/transloco.md) |
| Handle authentication | [tools/auth.md](./tools/auth.md) |

⭐ = Enhanced with new patterns | 🆕 = New documentation

### Integration Guides

| I need to... | Check this guide |
|--------------|------------------|
| Create a complete page | [guides/create-page.md](./guides/create-page.md) |
| Create a dialog | [guides/create-dialog.md](./guides/create-dialog.md) |
| Create a table | [guides/create-table.md](./guides/create-table.md) |

### Reference

| I need to... | Check this |
|--------------|------------|
| DDD layer rules | [reference/ddd-architecture.md](./reference/ddd-architecture.md) ⭐ |
| Common migration mistakes | [reference/pitfalls.md](./reference/pitfalls.md) 🆕 |
| Angular 20 syntax transforms | [reference/angular-20-syntax.md](./reference/angular-20-syntax.md) |
| Pre-PR checklist | [reference/checklist.md](./reference/checklist.md) ⭐ |

⭐ = Enhanced with new patterns | 🆕 = New documentation

---

## Import Paths

```typescript
// Domain - API & State
import { MxRestService } from '@one-ui/mxsecurity/shared/domain';
import { queryMethod, mutationMethod, LoadingState, loadingInitialState } from '@one-ui/shared/domain';

// Domain - Validators
import { OneValidators } from '@one-ui/shared/domain';

// Features - Dialog
import { mediumDialogConfig, CONFIRM_DIALOG_CONFIG } from '@one-ui/shared/domain';
import { ConfirmDialogComponent } from '@one-ui/shared/ui';

// UI - Table
import { CommonTableComponent, SELECT_COLUMN_KEY, EDIT_COLUMN_KEY } from '@one-ui/shared/ui';

// UI - Form
import { OneUiFormErrorDirective } from '@one-ui/shared/ui/form';
import { MxLabelDirective } from '@moxa/formoxa/mx-label';
import { MxLoadingButtonDirective } from '@moxa/formoxa/mx-button';
import { MxStatusComponent } from '@moxa/formoxa/mx-status';

// UI - Page Layout
import { BreadcrumbComponent } from '@one-ui/shared/ui';
import { MxPageTitleComponent } from '@moxa/formoxa/mx-page-title';

// Routing - Breadcrumb
import { createBreadcrumbResolver, ROUTES_ALIASES } from '@one-ui/mxsecurity/shared/domain';
```
