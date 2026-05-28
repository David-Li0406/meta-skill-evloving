---
name: bundle-optimization
description: Guide for optimizing bundle size and images. Server Components by default, use image quality caps.
---

# Bundle Optimization Skill

## Purpose

Guide for optimizing bundle size and image performance. Ensure fast page loads and good Core Web Vitals.

## Bundle Analysis Commands

```bash
yarn analyze              # Full bundle analysis (client + server)
yarn analyze:browser      # Browser bundles only
yarn analyze:server       # Server bundles only
yarn analyze:experimental # Next.js 16.1 interactive analyzer (Turbopack-compatible)
```

## Image Optimization

### Quality Caps

External images use quality caps to reduce bandwidth:

| Context      | Quality | Use Case              |
| ------------ | ------- | --------------------- |
| Default      | 50      | Standard images       |
| Priority/LCP | 50      | Above-the-fold images |

> **Note**: LCP quality was reduced from 60 to 50 based on Lighthouse analysis
> showing 159 KiB potential savings. See `utils/image-quality.ts` for details.

### Helper Functions

```typescript
import {
  getOptimalImageQuality,
  getOptimalImageSizes,
} from "@utils/image-quality";

// Get quality based on context (uses options object)
const heroQuality = getOptimalImageQuality({ isPriority: true }); // 50 (LCP external)
const cardQuality = getOptimalImageQuality({ isPriority: false }); // 50 (standard external)

// Get responsive sizes
const sizes = getOptimalImageSizes("card");
// "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
```

### Image Component Usage

```tsx
import Image from "next/image";
import { getOptimalImageQuality, getOptimalImageSizes } from "@utils/image-quality";

// ✅ CORRECT - Using helpers with options object
<Image
  src={event.imageUrl}
  alt={event.title}
  width={400}
  height={300}
  quality={getOptimalImageQuality({ isPriority: false })}
  sizes={getOptimalImageSizes("card")}
  loading="lazy"
/>

// ✅ CORRECT - Priority for LCP images
<Image
  src={event.imageUrl}
  alt={event.title}
  fill
  priority
  quality={getOptimalImageQuality({ isPriority: true })}
  sizes={getOptimalImageSizes("hero")}
/>
```

### Image Retry Logic

For unreliable image sources:

```typescript
import { useImageRetry } from "@hooks/useImageRetry";

function EventImage({ src, alt }) {
  // useImageRetry takes optional maxRetries (default: 2)
  const {
    retryCount,
    hasError,
    imageLoaded,
    showSkeleton,
    handleError,
    getImageKey,
  } = useImageRetry();

  return (
    <Image
      key={getImageKey(src)} // Forces re-render on retry
      src={src}
      alt={alt}
      onError={handleError}
      // Exponential backoff on retry (1s, 2s, 4s...)
    />
  );
}
```

### Preloading Critical Images

```typescript
import { preloadImage } from "@utils/image-preload";

// Preload LCP image
preloadImage(heroImageUrl);
```

**Caution**: `preloadImage` has coupling to internal Next.js `_next/image` URL format. Use sparingly.

## Cache Busting

### Versioned URLs

For static assets that need cache busting, add a version query parameter:

```typescript
// Pattern: Add version param for cache busting
// BUILD_VERSION is available via scripts/generate-sw.mjs
const buildVersion = process.env.BUILD_VERSION || Date.now().toString();

function getVersionedUrl(path: string): string {
  return `${path}?v=${buildVersion}`;
}

// Usage
const url = getVersionedUrl("/static/data.json");
// "/static/data.json?v=1234567890"
```

`BUILD_VERSION` resolves to:

- Development: timestamp
- Production: git SHA (set in CI workflows)

## Code Splitting Best Practices

### Dynamic Imports

```typescript
import dynamic from "next/dynamic";

// ✅ CORRECT - Lazy load heavy components
const HeavyChart = dynamic(() => import("@components/ui/HeavyChart"), {
  loading: () => <ChartSkeleton />,
});

// ❌ WRONG - ssr: false in Server Components
// Don't use ssr: false inside Server Components
// Instead, create a client component wrapper
```

### Server Component Default

Most components should be Server Components (no JS shipped):

```tsx
// ✅ Server Component - Zero JS
export function EventList({ events }) {
  return (
    <ul>
      {events.map((event) => (
        <li key={event.id}>{event.title}</li>
      ))}
    </ul>
  );
}
```

### Client Components - Only When Needed

```tsx
"use client";

// Only add "use client" for:
// - useState, useEffect
// - Event handlers (onClick, etc.)
// - Browser APIs
// - Third-party client-only libraries
```

## Bundle Size Targets

Monitor these in bundle analysis:

| Metric        | Target  | Action if Exceeded   |
| ------------- | ------- | -------------------- |
| First Load JS | < 100kB | Split or lazy load   |
| Shared chunks | < 50kB  | Check for large deps |
| Page-specific | < 30kB  | Review page imports  |

## Common Bundle Bloaters

1. **Large date libraries** → Use native Intl or date-fns (tree-shakeable)
2. **Full icon libraries** → Import specific icons only
3. **Unused dependencies** → Audit with `yarn analyze`
4. **Client-side only code in shared** → Move to client components

## Optimization Checklist

### Images

- [ ] Using quality caps via `getOptimalImageQuality`?
- [ ] Using responsive sizes via `getOptimalImageSizes`?
- [ ] Priority on LCP images only?
- [ ] Lazy loading below-the-fold images?

### Bundles

- [ ] Server Component by default?
- [ ] Dynamic import for heavy components?
- [ ] Running `yarn analyze` for new dependencies?
- [ ] Checking First Load JS size?

### Caching

- [ ] Using `getVersionedUrl` for static assets?
- [ ] Appropriate cache headers on API routes?

## Files to Reference

- [utils/image-quality.ts](../../../utils/image-quality.ts) - Image quality helpers
- [utils/image-preload.ts](../../../utils/image-preload.ts) - Image preloading
- [components/hooks/useImageRetry.ts](../../../components/hooks/useImageRetry.ts) - Retry logic
- [next.config.js](../../../next.config.js) - Image domains, optimization config
- [bundle-size-baseline.json](../../../bundle-size-baseline.json) - Size tracking
