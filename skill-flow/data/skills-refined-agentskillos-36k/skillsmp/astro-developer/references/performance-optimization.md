# Performance Optimization Guide for Astro Projects

This guide covers performance optimization strategies for Astro projects, including build optimization, rendering strategies, and deployment best practices for 2026.

## Table of Contents

1. [Performance Fundamentals](#performance-fundamentals)
2. [Islands Architecture Optimization](#islands-architecture-optimization)
3. [Image & Asset Optimization](#image--asset-optimization)
4. [Code Splitting & Lazy Loading](#code-splitting--lazy-loading)
5. [Build Optimization](#build-optimization)
6. [Server-Side Optimization](#server-side-optimization)
7. [Deployment Strategies](#deployment-strategies)
8. [Monitoring & Measurement](#monitoring--measurement)

## Performance Fundamentals

### Core Web Vitals Targets

- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1
- **TTFB (Time to First Byte)**: < 800ms

### Performance Budgets

```javascript
// astro.config.mjs
export default defineConfig({
  build: {
    // Build optimization options
    inlineStylesheets: 'auto',
  },
  vite: {
    build: {
    // Set chunk size limit
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        output: {
          // Manual chunk splitting
          manualChunks: {
            'vendor': ['react', 'react-dom'],
            'ui': ['@astrojs/react'],
          },
        },
      },
    },
  },
});
```

## Islands Architecture Optimization

### Strategic Client Directive Usage

Choose the right client directive for each component based on its priority and location:

```astro
---
import Header from '@/components/Header.jsx';
import HeroCarousel from '@/components/HeroCarousel.jsx';
import NewsletterForm from '@/components/NewsletterForm.jsx';
import CommentsSection from '@/components/CommentsSection.jsx';
import SocialShare from '@/components/SocialShare.jsx';
import Analytics from '@/components/Analytics.jsx';
---

<!-- IMMEDIATE (client:load) -->
<!-- Use for: Above-fold, critical interactivity -->
<Header client:load />
<MobileMenu client:load media="(max-width: 768px)" />

<!-- VISIBLE (client:visible) -->
<!-- Use for: Below-fold content, carousels, accordions -->
<HeroCarousel client:visible />
<FAQAccordion client:visible />
<TestimonialsCarousel client:visible />

<!-- IDLE (client:idle) -->
<!-- Use for: Secondary features, non-critical UI -->
<NewsletterForm client:idle />
<SocialShare client:idle />
<ThemeToggle client:idle />

<!-- MEDIA (client:load with media query) -->
<!-- Use for: Device-specific features -->
<PrintButton client:load media="print" />
<MobileNavigation client:load media="(max-width: 768px)" />

<!-- DEFER (server:defer) -->
<!-- Use for: Dynamic server-side content -->
<UserProfile server:defer />
<RecommendedPosts server:defer />

<!-- BACKGROUND TASKS -->
<!-- Use for: Analytics, tracking -->
<Analytics client:idle />
```

### Client Directive Selection Guide

| Directive | Use When | Example |
|-----------|----------|---------|
| `client:load` | Above-fold, critical | Header, navigation |
| `client:visible` | Below-fold, expensive | Carousels, heavy widgets |
| `client:idle` | Non-critical, secondary | Newsletter forms, footers |
| `client:media` | Device-specific | Mobile menus, print buttons |
| `server:defer` | Dynamic server data | User profiles, personalized content |

### Minimize JavaScript Payload

```astro
---
// ❌ Wrong: Loading heavy components eagerly
<DatePicker client:load />
<WYSIWYGEditor client:load />
<ChartLibrary client:load />
---

// ✅ Correct: Load only what's needed, when needed
<DatePicker client:visible />
<WYSIWYGEditor client:visible />
<ChartLibrary client:idle />

// ✅ Even better: Use native HTML when possible
<input type="date" />
<textarea />
<svg><!-- Simple chart --></svg>
---
```

## Image & Asset Optimization

### Use Astro's Built-in Image Optimization

```astro
---
import { Image } from 'astro:assets';
import heroImage from '@/images/hero.jpg';
import profilePic from '@/images/profile.png';
---

<!-- ✅ Optimized responsive images -->
<Image
  src={heroImage}
  alt="Hero section background"
  widths={[400, 800, 1200, 1600]}
  sizes="(max-width: 768px) 100vw, 50vw"
  formats={['avif', 'webp', 'jpg']}
  loading="eager"
  decoding="sync"
  priority
/>

<!-- ✅ Lazy loaded below-fold images -->
<Image
  src={profilePic}
  alt="Author profile picture"
  widths={[200, 400]}
  formats={['avif', 'webp', 'png']}
  loading="lazy"
  decoding="async"
/>
```

### Remote Images with Image Service

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sharp from 'sharp';

export default defineConfig({
  image: {
    service: {
      sharp,
    },
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/images/**',
      },
    ],
  },
});
```

```astro
---
// ✅ Optimize remote images
import { Image } from 'astro:assets';

const heroUrl = new URL('https://images.unsplash.com/photo-...');
---

<Image
  src={heroUrl}
  alt="Remote image"
  widths={[600, 1200, 1800]}
  formats={['avif', 'webp']}
  loading="eager"
/>
```

### Font Optimization

```astro
---
// ✅ Use font-display: swap for non-critical fonts
---

<link
  rel="preload"
  href="/fonts/custom.woff2"
  as="font"
  type="font/woff2"
  crossOrigin="anonymous"
/>

<style>
  @font-face {
    font-family: 'CustomFont';
    src: url('/fonts/custom.woff2') format('woff2');
    font-weight: 400;
    font-display: swap; /* Prevents FOIT */
  }
</style>
```

## Code Splitting & Lazy Loading

### Dynamic Component Imports

```jsx
// ReactComponent.jsx
import { lazy, Suspense } from 'react';

// ✅ Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const RichTextEditor = lazy(() => import('./RichTextEditor'));

export default function ReactComponent() {
  return (
    <div>
      {/* Show fallback while loading */}
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>

      <Suspense fallback={<div>Loading editor...</div>}>
        <RichTextEditor />
      </Suspense>
    </div>
  );
}
```

### Route-Based Code Splitting

```astro
---
// ✅ Dynamic imports for heavy routes
const AdminPanel = (await import('@/components/AdminPanel.jsx')).default;
const Dashboard = (await import('@/components/Dashboard.jsx')).default;
---

<!-- Load admin panel only on admin routes -->
{isAdmin && (
  <AdminPanel client:visible />
)}
```

## Build Optimization

### Astro Configuration Best Practices

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  // ✅ Site metadata for SEO
  site: 'https://yoursite.com',
  base: '/',

  // ✅ Integrations
  integrations: [
    react(),
    tailwind({
      applyBaseStyles: false, // Prevent duplicate styles
    }),
    sitemap(),
  ],

  // ✅ Build optimizations
  build: {
    format: 'directory', // Clean URLs (e.g., /about instead of /about.html)
    assets: '_assets',
  },

  // ✅ Vite optimizations
  vite: {
    build: {
      cssMinify: 'lightningcss', // Faster CSS minification
      rollupOptions: {
        output: {
          // Manual chunk splitting for better caching
          manualChunks: (id) => {
            // Vendor chunk for React
            if (id.includes('node_modules/react')) {
              return 'vendor-react';
            }
            // UI library chunk
            if (id.includes('node_modules/@astrojs/react')) {
              return 'vendor-ui';
            }
            // Other node_modules
            if (id.includes('node_modules')) {
              return 'vendor';
            }
          },
        },
      },
    },
    // ✅ Optimize dependencies
    optimizeDeps: {
      include: ['react', 'react-dom'],
      exclude: ['some-large-package'],
    },
  },

  // ✅ Compression
  compress: true,

  // ✅ Prefetching
  prefetch: true,
});
```

### Preconnect to External Origins

```astro
---
// In your layout
---

<html>
  <head>
    <!-- ✅ Preconnect to critical third-party origins -->
    <link rel="preconnect" href="https://api.example.com" />
    <link rel="preconnect" href="https://cdn.example.com" crossOrigin="anonymous" />

    <!-- ✅ DNS prefetch for less critical origins -->
    <link rel="dns-prefetch" href="https://analytics.example.com" />
  </head>
</html>
```

## Server-Side Optimization

### Hybrid Rendering Strategy

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'hybrid', // Mix of static and SSR
});
```

```astro
---
// Static pages (default)
// Most pages - fast, cacheable
---

---
// SSR pages (opt-in)
export const prerender = false;

// Dynamic pages - personalized data
const user = await getUser(Astro.request);
---
```

### Server Islands for Parallel Loading

```astro
---
import UserProfile from '@/components/UserProfile.astro';
import RecommendedPosts from '@/components/RecommendedPosts.astro';
import ShoppingCart from '@/components/ShoppingCart.astro';
---

<!-- Main content loads immediately -->
<main>
  <h1>Welcome to our store</h1>
  <p>Explore our latest products...</p>
</main>

<!-- ✅ Dynamic content loads in parallel without blocking -->
<aside>
  <UserProfile server:defer />
  <RecommendedPosts server:defer />
  <ShoppingCart server:defer />
</aside>
```

### Edge Functions with Middleware

```typescript
// src/middleware.ts
export const onRequest = (context) => {
  // ✅ Route based on location
  const country = context.request.headers.get('cf-ipcountry');

  if (country === 'US') {
    return context.rewrite('/us');
  } else if (country === 'EU') {
    return context.rewrite('/eu');
  }
};
```

### Caching Strategies

```javascript
// API routes with proper caching
export async function GET() {
  const data = await fetch('https://api.example.com/data');

  return Response.json(data, {
    headers: {
      // ✅ Cache at CDN for 1 hour
      'Cache-Control': 'public, max-age=3600, s-maxage=3600',
      // ✅ Stale-while-revalidate
      'Cache-Control': 'public, max-age=60, stale-while-revalidate=3600',
    },
  });
}
```

## Deployment Strategies

### Static Site Deployment (Recommended for Content Sites)

```bash
# Build static site
npm run build

# Deploy to any static host
# - Vercel
# - Netlify
# - Cloudflare Pages
# - GitHub Pages
```

**Best for**:
- Blogs and documentation
- Marketing sites
- Content-heavy sites
- Maximum performance

### Hybrid Deployment (Best of Both Worlds)

```javascript
// astro.config.mjs
import node from '@astrojs/node';

export default defineConfig({
  output: 'hybrid',
  adapter: node({
    mode: 'standalone',
  }),
});
```

**Best for**:
- Sites with some dynamic content
- Personalized experiences
- E-commerce product pages
- Member areas

### Full SSR Deployment

```javascript
// astro.config.mjs
import vercel from '@astrojs/vercel/serverless';
// or
import netlify from '@astrojs/netlify/functions';
// or
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server',
  adapter: vercel(),
});
```

**Best for**:
- Fully dynamic applications
- Real-time features
- Authentication-heavy apps
- APIs

### Edge Deployment (Ultimate Performance)

```javascript
// Deploy to edge for global performance
export default defineConfig({
  output: 'server',
  adapter: cloudflare(),
});
```

## Monitoring & Measurement

### Built-in Performance Analysis

```bash
# Analyze bundle size
npm run build -- --analyze

# Check for unused CSS
npx purgecss --css dist/assets/*.css --content dist/**/*.html
```

### Lighthouse CI Integration

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on: [push, pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            https://yoursite.com
            https://yoursite.com/about
          uploadArtifacts: true
```

### Core Web Vitals Tracking

```jsx
// components/WebVitals.jsx
import { onCLS, onFID, onLCP } from 'web-vitals';

export function WebVitals() {
  useEffect(() => {
    onCLS(console.log);
    onFID(console.log);
    onLCP(console.log);
  }, []);

  return null; // Invisible component
}
```

## Performance Checklist

### Pre-Deployment

- [ ] Set appropriate client directives for all interactive components
- [ ] Optimize all images with `<Image />` component
- [ ] Enable compression in astro.config
- [ ] Configure proper caching headers
- [ ] Minify CSS and JavaScript (automatic in production)
- [ ] Remove unused dependencies
- [ ] Test with Lighthouse (target: 90+ score)
- [ ] Check bundle size (target: < 200KB initial)

### Post-Deployment

- [ ] Monitor Core Web Vitals in production
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure analytics for performance metrics
- [ ] Test on slow 3G connections
- [ ] Verify on mobile devices
- [ ] Check accessibility score

## Performance Optimization Quick Wins

1. **Use `client:visible` for below-fold content** - Instant 20-30% JS reduction
2. **Enable image optimization** - 50-80% image size reduction
3. **Switch to AVIF/WebP** - Additional 20-30% savings
4. **Implement code splitting** - Faster initial page load
5. **Add compression** - 40-60% text size reduction
6. **Use hybrid rendering** - Static speed + dynamic capability
7. **Deploy to edge** - Global latency reduction

## Sources

- [Astro 6 Beta Announcement](https://astro.build/blog/astro-6-beta/)
- [How to Deploy an Astro App in 2026](https://kuberns.com/blogs/post/how-to-deploy-an-astro-app/)
- [Deploying Astro Websites with Hybrid Rendering](https://render.com/articles/deploying-astro-websites-with-hybrid-rendering)
- [Astro Image Optimization](https://docs.astro.build/en/guides/images/)
- [Web.dev Performance Guides](https://web.dev/performance/)
