---
name: web-performance-optimization
description: Optimize web performance using Core Web Vitals, modern patterns, and systematic techniques for fast, responsive experiences.
---

# Web Performance Optimization

Optimize web performance through Core Web Vitals, modern browser APIs, and systematic techniques to improve user experience, SEO rankings, and conversion rates.

## When to Use This Skill

- When website or app is loading slowly
- When optimizing for Core Web Vitals (LCP, FID, CLS, INP)
- When reducing JavaScript bundle size
- When improving Time to Interactive (TTI)
- When optimizing images and assets
- When implementing caching strategies
- When debugging performance bottlenecks
- When preparing for performance audits

## How It Works

### Step 1: Measure Current Performance

Establish baseline metrics:
- Run Lighthouse audits
- Measure Core Web Vitals (LCP, FID, CLS, INP)
- Check bundle sizes
- Analyze network waterfall
- Identify performance bottlenecks

### Step 2: Identify Issues

Analyze performance problems:
- Large JavaScript bundles
- Unoptimized images
- Render-blocking resources
- Slow server response times
- Missing caching headers
- Layout shifts
- Long tasks blocking the main thread

### Step 3: Prioritize Optimizations

Focus on high-impact improvements:
- Critical rendering path optimization
- Code splitting and lazy loading
- Image optimization
- Caching strategies
- Third-party script optimization

### Step 4: Implement Optimizations

Apply performance improvements:
- Optimize assets (images, fonts, CSS, JS)
- Implement code splitting
- Add caching headers
- Lazy load non-critical resources
- Optimize critical rendering path

### Step 5: Verify Improvements

Measure the impact of changes:
- Re-run Lighthouse audits
- Compare before/after metrics
- Monitor real user metrics (RUM)
- Test on different devices and networks

## Core Web Vitals at a Glance

| Metric | Target | Key Optimization |
|--------|--------|------------------|
| **LCP** (Largest Contentful Paint) | <2.5s | Optimize images, preload critical resources |
| **INP** (Interaction to Next Paint) | <200ms | Reduce JavaScript, break up long tasks |
| **CLS** (Cumulative Layout Shift) | <0.1 | Reserve space, optimize fonts |
| **TBT** (Total Blocking Time) | <200ms | Code splitting, defer non-critical JS |
| **FCP** (First Contentful Paint) | <1.8s | Eliminate render-blocking resources |

## Quick Wins

**High-ROI optimizations by time investment:**

**1 Hour Quick Wins:**
- Add `loading="lazy"` to below-fold images
- Enable compression (gzip/brotli)
- Add `rel="preconnect"` for critical origins

**1 Day Investments:**
- Implement code splitting
- Optimize LCP image with `fetchpriority="high"`
- Add basic service worker

**1 Week Comprehensive:**
- Full caching strategy (HTTP headers + service workers)
- Bundle optimization (tree shaking)
- Performance monitoring (Lighthouse CI + RUM)

## Best Practices

### ✅ Do This
- Measure first - Always establish baseline metrics before optimizing
- Optimize images - Use modern formats (WebP, AVIF) and responsive images
- Code split - Break large bundles into smaller chunks
- Lazy load - Defer non-critical resources
- Cache aggressively - Set proper cache headers for static assets

### ❌ Don't Do This
- Don't optimize blindly - Measure first, then optimize
- Don't ignore mobile - Test on real mobile devices and slow networks
- Don't block rendering - Avoid render-blocking CSS and JavaScript

## Common Pitfalls

### Problem: Optimized for Desktop but Slow on Mobile
**Solution:**
- Test on real mobile devices
- Optimize for 3G/4G networks

### Problem: Large JavaScript Bundle
**Solution:**
- Analyze bundle with webpack-bundle-analyzer
- Implement code splitting

### Problem: Images Causing Layout Shifts
**Solution:**
- Always specify width and height
- Use aspect-ratio CSS property

## Performance Tools

### Measurement Tools
- **Lighthouse** - Comprehensive performance audit
- **WebPageTest** - Detailed waterfall analysis
- **Chrome DevTools** - Performance profiling

### Analysis Tools
- **webpack-bundle-analyzer** - Visualize bundle composition
- **source-map-explorer** - Analyze bundle size

### Monitoring Tools
- **Google Analytics** - Track Core Web Vitals
- **Sentry** - Performance monitoring

## Integration with Other Skills

- **nextjs-core** - Next.js Image component, font optimization
- **react** - Component optimization, memoization

---

**Remember:** Performance is a feature, not an afterthought. Every millisecond counts. Start with Quick Wins for immediate impact.