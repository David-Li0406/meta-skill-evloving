---
title: Lazy Load Routes with loadComponent
impact: CRITICAL
impactDescription: 40-70% initial bundle reduction
tags: lazy-loading, routing, bundle-size
---

## Lazy Load Routes with loadComponent

Lazy loading splits your application into smaller chunks loaded on demand. Use `loadComponent` for standalone components to reduce initial bundle size.

**Incorrect (Eagerly loaded routes):**

```typescript
import { DashboardComponent } from './dashboard/dashboard.component';
import { SettingsComponent } from './settings/settings.component';
import { ReportsComponent } from './reports/reports.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'settings', component: SettingsComponent },
  { path: 'reports', component: ReportsComponent }
  // All components loaded upfront, even if never visited
];
```

**Correct (Lazy loaded routes):**

```typescript
export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'settings',
    loadComponent: () =>
      import('./settings/settings.component').then(m => m.SettingsComponent)
  },
  {
    path: 'reports',
    loadChildren: () =>
      import('./reports/reports.routes').then(m => m.REPORTS_ROUTES)
  }
];
```

**Why it matters:**
- Initial bundle only includes code for first route
- Other routes downloaded on navigation
- `loadComponent` for single components
- `loadChildren` for route groups

Reference: [Angular Lazy Loading](https://angular.dev/guide/routing/common-router-tasks#lazy-loading)
