---
title: Use Incremental Hydration for SSR
impact: HIGH
impactDescription: Faster TTI, smaller JavaScript bundles
tags: ssr, hydration, performance
---

## Use Incremental Hydration for SSR

Incremental hydration defers JavaScript loading for below-fold components, reducing initial bundle size and improving Time to Interactive.

**Incorrect (Full hydration of all components):**

```typescript
@Component({
  template: `
    <app-header />
    <app-hero />
    <app-comments [postId]="postId" />      <!-- Heavy, below fold -->
    <app-recommendations />                  <!-- Heavy, below fold -->
    <app-footer />
  `
})
export class PostComponent {
  postId = input.required<string>();
}
```

**Correct (Incremental hydration with @defer):**

```typescript
@Component({
  template: `
    <app-header />
    <app-hero />

    @defer (hydrate on viewport) {
      <app-comments [postId]="postId()" />
    } @placeholder {
      <div class="comments-skeleton">Loading comments...</div>
    }

    @defer (hydrate on idle) {
      <app-recommendations />
    }

    @defer (hydrate never) {
      <app-footer />
    }
  `
})
export class PostComponent {
  postId = input.required<string>();
}
```

**Why it matters:**
- `hydrate on viewport` - Hydrates when scrolled into view
- `hydrate on idle` - Hydrates during browser idle time
- `hydrate on interaction` - Hydrates on user click/focus
- `hydrate never` - Never hydrates (static content only)

Reference: [Angular SSR](https://angular.dev/guide/ssr)
