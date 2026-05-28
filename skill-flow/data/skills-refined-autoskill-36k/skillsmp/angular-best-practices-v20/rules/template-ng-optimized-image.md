---
title: Use NgOptimizedImage for Images
impact: HIGH
impactDescription: LCP improvement, automatic lazy loading
tags: images, performance, lcp
---

## Use NgOptimizedImage for Images

`NgOptimizedImage` enforces image best practices: automatic lazy loading, priority hints for LCP images, and prevents layout shift.

**Incorrect (Native img without optimization):**

```html
<!-- No lazy loading, no priority hints, potential CLS -->
<img src="/assets/hero.jpg" alt="Hero image">

<!-- May cause layout shift without dimensions -->
<img src="{{ user.avatar }}" alt="User avatar">
```

**Correct (NgOptimizedImage with best practices):**

```typescript
@Component({
  imports: [NgOptimizedImage],
  template: `
    <!-- Priority image (above fold, LCP candidate) -->
    <img
      ngSrc="/assets/hero.jpg"
      alt="Hero image"
      width="1200"
      height="600"
      priority
    />

    <!-- Lazy loaded by default (below fold) -->
    <img
      [ngSrc]="user().avatar"
      alt="User avatar"
      width="64"
      height="64"
    />
  `
})
export class ProductComponent {
  user = input.required<User>();
}
```

**Why it matters:**
- `priority` attribute for above-fold images (LCP)
- Automatic lazy loading for below-fold images
- Required `width`/`height` prevents layout shift
- `fill` mode available for dynamic containers

Reference: [Angular Image Optimization](https://angular.dev/guide/image-optimization)
