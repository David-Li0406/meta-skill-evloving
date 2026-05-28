# Routing

## What is this?

One-UI routing configuration with breadcrumb resolver and route aliases.

## When to use

When adding new page routes to the application.

## Import

```typescript
import { createBreadcrumbResolver, ROUTES_ALIASES } from '@one-ui/mxsecurity/shared/domain';
```

---

## Route Configuration

### Basic Route with Breadcrumb

```typescript
// app.routes.ts
import { createBreadcrumbResolver, ROUTES_ALIASES } from '@one-ui/mxsecurity/shared/domain';

export const routes: Route[] = [
  {
    path: ROUTES_ALIASES['myFeature'].route,
    loadChildren: () => import('@one-ui/mxsecurity/my-feature/shell').then((m) => m.createRoutes()),
    resolve: {
      breadcrumb: createBreadcrumbResolver(ROUTES_ALIASES['myFeature'].id)
    }
  }
];
```

### ROUTES_ALIASES Structure

```typescript
// Each feature has an alias entry
ROUTES_ALIASES['myFeature'] = {
  id: 'my-feature',        // Breadcrumb translation key
  route: 'my-feature'      // URL path segment
};
```

---

## Feature Routes (Shell Layer)

```typescript
// libs/{scope}/{feature}/shell/src/lib/{feature}.routes.ts
import { Route } from '@angular/router';
import { FeaturePageComponent } from '@one-ui/{scope}/{feature}/features';
import { FeatureStore, FeatureApiService } from '@one-ui/{scope}/{feature}/domain';

const loadDataResolver = (store = inject(FeatureStore)) => {
  store.loadItems();
  return true;
};

export const createRoutes = (): Route[] => [
  {
    path: '',
    component: FeaturePageComponent,
    providers: [FeatureStore, FeatureApiService],
    resolve: {
      data: () => loadDataResolver()
    }
  }
];
```

---

## Nested Routes

```typescript
// For features with sub-pages
export const createRoutes = (): Route[] => [
  {
    path: '',
    component: FeaturePageComponent,
    providers: [FeatureStore, FeatureApiService],
    resolve: { data: () => loadDataResolver() }
  },
  {
    path: ':id',
    component: FeatureDetailComponent,
    resolve: { data: () => loadDetailResolver() }
  }
];
```

---

## Breadcrumb Display

The `<one-ui-breadcrumb />` component automatically reads the resolved breadcrumb data:

```html
<!-- In page template -->
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.xxx.page_title')" />
  <!-- ... -->
</div>
```

---

## Common Mistakes

```typescript
// ❌ WRONG: Missing breadcrumb resolver
{
  path: 'my-feature',
  loadChildren: () => import('./my-feature/shell').then((m) => m.createRoutes())
  // Breadcrumb won't display correctly
}

// ✅ CORRECT: Include breadcrumb resolver
{
  path: ROUTES_ALIASES['myFeature'].route,
  loadChildren: () => import('./my-feature/shell').then((m) => m.createRoutes()),
  resolve: {
    breadcrumb: createBreadcrumbResolver(ROUTES_ALIASES['myFeature'].id)
  }
}
```

```typescript
// ❌ WRONG: Hardcoded route path
{
  path: 'my-feature',  // Don't hardcode
  ...
}

// ✅ CORRECT: Use ROUTES_ALIASES
{
  path: ROUTES_ALIASES['myFeature'].route,
  ...
}
```

---

## Related Tools

- [page-layout.md](./ui/page-layout.md) - Page structure with breadcrumb
- [signal-store.md](./signal-store.md) - Store used in resolvers
