---
title: Lazy Load Feature Modules
impact: CRITICAL
impactDescription: 40-70% initial bundle reduction
tags: lazy-loading, routing, modules
---

## Lazy Load Feature Modules

Lazy loading splits your application into smaller chunks loaded on demand. Use `loadChildren` to lazy load feature modules.

**Incorrect (Eagerly loaded modules):**

```typescript
import { UserModule } from './user/user.module';
import { AdminModule } from './admin/admin.module';

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
    UserModule,   // Loaded immediately
    AdminModule   // Loaded even if user never visits
  ]
})
export class AppRoutingModule {}
```

**Correct (Lazy loaded modules):**

```typescript
const routes: Routes = [
  {
    path: 'users',
    loadChildren: () =>
      import('./user/user.module').then(m => m.UserModule)
  },
  {
    path: 'admin',
    loadChildren: () =>
      import('./admin/admin.module').then(m => m.AdminModule),
    canLoad: [AuthGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

**Why it matters:**
- Initial bundle only includes core code
- Feature modules downloaded on navigation
- `canLoad` prevents loading if not authorized
- Use `forChild` in lazy-loaded routing modules

Reference: [Angular Lazy Loading](https://v16.angular.io/guide/lazy-loading-ngmodules)
