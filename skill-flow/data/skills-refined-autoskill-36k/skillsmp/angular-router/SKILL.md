---
name: angular-router
description: Angular Router for navigation, routing configuration, route guards, lazy loading, and parameter handling. Use when setting up routes, implementing navigation guards, lazy loading modules, handling route parameters, or implementing breadcrumbs and nested routes in Angular applications.
license: Complete terms in LICENSE.txt
---

# Angular Router

Expert guidance for implementing navigation and routing in Angular applications using the Angular Router module.

## When to Use This Skill

Activate this skill when you need to:
- Configure application routes
- Implement route guards (CanActivate, CanDeactivate, Resolve)
- Set up lazy loading for feature modules
- Handle route parameters and query parameters
- Implement nested and child routes
- Create navigation menus and breadcrumbs
- Handle route transitions and animations
- Implement route redirects and wildcards
- Work with router events and navigation lifecycle

## Basic Setup

```typescript
// app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: '**', component: NotFoundComponent }
];

// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes)
  ]
};
```

## Lazy Loading

```typescript
// Feature module lazy loading
export const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.routes')
      .then(m => m.ADMIN_ROUTES)
  },
  {
    path: 'workspace',
    loadComponent: () => import('./workspace/workspace.component')
      .then(m => m.WorkspaceComponent)
  }
];
```

## Route Guards

```typescript
// Auth guard
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';

export const authGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  
  return router.createUrlTree(['/login']);
};

// Apply guard
{
  path: 'dashboard',
  component: DashboardComponent,
  canActivate: [authGuard]
}
```

## Route Parameters

```typescript
// Route with parameter
{ path: 'user/:id', component: UserDetailComponent }

// Access in component
export class UserDetailComponent {
  private route = inject(ActivatedRoute);
  
  userId = toSignal(
    this.route.params.pipe(map(params => params['id'])),
    { initialValue: null }
  );
}
```

## References

- [Angular Router Documentation](https://angular.dev/guide/routing)
- [Router API Reference](https://angular.dev/api/router)
