# Page Layout Structure

> ⚠️ **CRITICAL: All page components MUST use `class="gl-page-content"` on the root element.**
> Without this class, content (especially tables) may not display correctly!

All page components must use the standard page layout wrapper classes:

```html
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.xxx.page_title')" />
  <div class="content-wrapper">
    <!-- Page content goes here -->
  </div>
</div>
```

## Required Classes

| Class | Purpose |
| ----- | ------- |
| `gl-page-content` | **CRITICAL** - Root wrapper for page content, provides consistent page padding and layout. Tables won't display without this! |
| `content-wrapper` | Inner wrapper for main content area below the title |

---

## Section Titles (gl-title-md)

**CRITICAL**: Use `gl-title-md` class for section titles within forms or content areas.

```html
<!-- ✅ Correct -->
<div class="gl-title-md">{{ t('features.radius.primary_server') }}</div>

<!-- ❌ Wrong - custom class -->
<div class="section-title">{{ t('features.radius.primary_server') }}</div>
```

---

## Key Points

- `*transloco="let t"` should be on the root element for translation scope
- `<one-ui-breadcrumb />` comes first for navigation
- `<mx-page-title>` uses `[title]` input binding (not content projection)
- All main content (tables, forms, etc.) goes inside `content-wrapper`
- ❌ **DO NOT USE `mat-card`** - use `<div class="content-wrapper">` instead

---

## ⚠️ Common Mistake - Using ng-container

```html
<!-- ❌ WRONG: Tables and content won't display properly! -->
<ng-container *transloco="let t">
  <one-ui-breadcrumb />
  <mx-page-title>{{ t('...') }}</mx-page-title>
  <div class="content-wrapper">
    <!-- content here won't display correctly -->
  </div>
</ng-container>

<!-- ✅ CORRECT: Use div with gl-page-content class -->
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('...')" />
  <div class="content-wrapper">
    <!-- content displays correctly -->
  </div>
</div>
```

**Why this happens:** `<ng-container>` doesn't create a DOM element, so the `gl-page-content` styles can't be applied. The page layout CSS requires a real DOM element with this class.

---

## ❌ Don't use mat-card

```html
<!-- ❌ Incorrect: Using mat-card -->
<mat-card>
  <mat-card-content>
    <one-ui-my-table [tableData]="tableData()" />
  </mat-card-content>
</mat-card>

<!-- ✅ Correct: Using content-wrapper -->
<div class="content-wrapper">
  <one-ui-my-table [tableData]="tableData()" />
</div>
```

---

## Example - Page with Form and Table

```html
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.xxx.page_title')" />

  <!-- Form Section -->
  <div class="content-wrapper">
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <!-- form fields -->
    </form>
  </div>

  <!-- Table Section -->
  <div class="content-wrapper">
    <one-ui-my-table [tableData]="tableData()" />
  </div>
</div>
```

## Example - Page with Table

```html
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.account_management.page_title')" />
  <div class="content-wrapper">
    <one-ui-account-table
      [tableData]="tableData()"
      [tableMaxSize]="tableMaxSize()"
      (addAccount)="onAddAccount()"
      (editAccount)="onEditAccount($event)"
      (deleteAccount)="onDeleteAccount($event)"
    />
  </div>
</div>
```

---

## Route Configuration (Breadcrumb)

When adding a new page route in `apps/mxsecurity/mxsecurity/src/app/app.routes.ts`, you **MUST** add the breadcrumb resolver:

```typescript
import { authGuard, createBreadcrumbResolver, menuTreeResolver, ROUTES_ALIASES } from '@one-ui/mxsecurity/shared/domain';

export const appRoutes: Route[] = [
  {
    path: '',
    component: ShellComponent,
    canActivate: [authGuard],
    canActivateChild: [authGuard],
    resolve: {
      menuTree: menuTreeResolver
    },
    children: [
      {
        path: ROUTES_ALIASES['broadcastForwarding'].route,
        loadChildren: () =>
          import('@one-ui/mxsecurity/broadcast-forwarding-page/shell').then((m) => m.createRoutes()),
        // ✅ Required: Add breadcrumb resolver
        resolve: {
          breadcrumb: createBreadcrumbResolver(ROUTES_ALIASES['broadcastForwarding'].id)
        }
      }
    ]
  }
];
```

**Key Points:**

- Import `createBreadcrumbResolver` from `@one-ui/mxsecurity/shared/domain`
- Use `ROUTES_ALIASES['routeKey'].id` as the parameter
- This enables the `<one-ui-breadcrumb />` component to display correct navigation
