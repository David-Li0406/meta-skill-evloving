---
name: performance-optimization
description: Use this skill to optimize performance in Next.js applications, focusing on Core Web Vitals, bundle analysis, caching strategies, and rendering optimizations.
---

# Performance Optimization Skill

This skill provides comprehensive strategies for optimizing performance in Next.js applications, including image and font optimization, caching strategies, bundle analysis, and rendering techniques.

## When to Use This Skill

Use this skill when the user requests:

✅ **Primary Use Cases**

- "Improve performance"
- "Fix slow page"
- "Optimize load time"
- "Reduce bundle size"
- "Improve Core Web Vitals"
- "Make it faster"

✅ **Secondary Use Cases**

- "Analyze bundle"
- "Check Lighthouse score"
- "Optimize images"
- "Add caching"
- "Fix layout shift"
- "Reduce LCP"

❌ **Do NOT use when**

- Fixing functional bugs (use debugging)
- Adding new features (use component-development)
- Database schema changes (use neon-database-management)
- Security improvements (use security tools)

---

## Core Web Vitals Targets

| Metric | Target | Good | Needs Work | Poor |
|--------|--------|------|------------|------|
| **LCP** (Largest Contentful Paint) | < 2.0s | ≤ 2.5s | 2.5-4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 100ms | ≤ 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.05 | ≤ 0.1 | 0.1-0.25 | > 0.25 |
| **FCP** (First Contentful Paint) | < 1.0s | ≤ 1.8s | 1.8-3.0s | > 3.0s |
| **TTFB** (Time to First Byte) | < 200ms | ≤ 800ms | 800-1800ms | > 1800ms |

---

## Performance Optimization Techniques

### 1. Image Optimization

```tsx
// Use Next.js Image component
import Image from "next/image";

export function OptimizedImage({ src, alt, width, height }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      priority={true} // For LCP images
      placeholder="blur"
    />
  );
}
```

### 2. Font Optimization

```tsx
// app/layout.tsx
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap", // Prevents Flash of Invisible Text (FOIT)
  preload: true,
});
```

### 3. Caching Strategies

```tsx
// Static generation (cached at build time)
export const dynamic = "force-static";
export const revalidate = 3600; // Revalidate every hour
```

### 4. Bundle Analysis

```bash
# Install analyzer
npm install --save-dev @next/bundle-analyzer

# Update next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // your Next.js config
});
```

### 5. Rendering Optimization

```tsx
import { Suspense } from "react";

export default function Page() {
  return (
    <div>
      <h1>Characters</h1>
      <Suspense fallback={<div>Loading...</div>}>
        <CharacterList />
      </Suspense>
    </div>
  );
}
```

### 6. Database Query Optimization

```typescript
// Optimize queries to avoid N+1 problems
const data = await query(`
  SELECT c.*, json_agg(e.*) as episodes
  FROM characters c
  LEFT JOIN character_episodes ce ON ce.character_id = c.id
  LEFT JOIN episodes e ON e.id = ce.episode_id
  GROUP BY c.id
`);
```

---

## Monitoring & Measurement

### Lighthouse CI

```bash
# Install Lighthouse CI
npm install --save-dev @lhci/cli

# Create config
cat > lighthouserc.js << 'EOF'
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/'],
      startServerCommand: 'npm start',
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
EOF

# Run Lighthouse CI
npm run lhci autorun
```

### Web Vitals Monitoring

```tsx
// app/_components/WebVitals.tsx
"use client";

import { useReportWebVitals } from "next/web-vitals";

export function WebVitals() {
  useReportWebVitals((metric) => {
    // Log to console in development
    if (process.env.NODE_ENV === "development") {
      console.log(metric);
    }
    // Send to analytics in production
    if (process.env.NODE_ENV === "production") {
      fetch("/api/vitals", {
        method: "POST",
        body: JSON.stringify(metric),
        headers: { "Content-Type": "application/json" },
      });
    }
  });

  return null;
}
```

---

## Common Performance Fixes

| Issue | Solution |
|-------|----------|
| High LCP | Add `priority` to LCP image, preload critical resources |
| High CLS | Set explicit dimensions, use skeletons |
| High INP | Reduce JS bundle, use `useDeferredValue` |
| Slow TTFB | Add caching, use edge runtime |
| Large bundle | Dynamic imports, tree shaking |
| Slow images | Use next/image, optimize formats |
| Font flash | Use `display: swap`, preload fonts |

---

## Related Skills

- [webapp-testing](../webapp-testing/SKILL.md) - Performance measurement
- [neon-database-management](../neon-database-management/SKILL.md) - Query optimization
- [component-development](../component-development/SKILL.md) - Efficient components

---

**Last Updated:** January 18, 2026  
**Maintained By:** Development Team  
**Status:** ✅ Production Ready