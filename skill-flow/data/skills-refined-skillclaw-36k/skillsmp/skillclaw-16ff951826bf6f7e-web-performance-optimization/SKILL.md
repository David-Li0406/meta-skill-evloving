---
name: web-performance-optimization
description: Use this skill when you need to optimize website and web application performance, focusing on loading speed, Core Web Vitals, bundle size, and caching strategies.
---

# Web Performance Optimization Skill

## Overview

This skill helps developers systematically measure, analyze, and improve the performance of websites and web applications to enhance user experience, SEO rankings, and conversion rates.

## When to Use This Skill

- When a website or app is loading slowly
- When optimizing for Core Web Vitals (LCP, FID, CLS)
- When reducing JavaScript bundle size
- When improving Time to Interactive (TTI)
- When optimizing images and assets
- When implementing caching strategies
- When debugging performance bottlenecks
- When preparing for performance audits

## How It Works

### Step 1: Measure Current Performance

1. Run Lighthouse audits to establish baseline metrics.
2. Measure Core Web Vitals (LCP, FID, CLS).
3. Check bundle sizes and analyze network waterfall.
4. Identify performance bottlenecks.

### Step 2: Identify Issues

Analyze performance problems such as:
- Large JavaScript bundles
- Unoptimized images
- Render-blocking resources
- Slow server response times
- Missing caching headers
- Layout shifts
- Long tasks blocking the main thread

### Step 3: Prioritize Optimizations

Focus on high-impact improvements:
- Optimize the critical rendering path
- Implement code splitting and lazy loading
- Optimize images and assets
- Establish effective caching strategies
- Optimize third-party scripts

### Step 4: Implement Optimizations

Apply performance improvements by:
- Optimizing assets (images, fonts, CSS, JS)
- Implementing code splitting
- Adding caching headers
- Lazy loading non-critical resources
- Optimizing the critical rendering path

### Step 5: Verify Improvements

Measure the impact of changes by:
- Re-running Lighthouse audits
- Comparing before/after metrics
- Monitoring real user metrics (RUM)
- Testing on different devices and networks

## Examples

### Example: Optimizing Core Web Vitals

```markdown
## Performance Audit Results

### Current Metrics (Before Optimization)
- **LCP (Largest Contentful Paint):** 4.2s ❌ (should be < 2.5s)
- **FID (First Input Delay):** 180ms ❌ (should be < 100ms)
- **CLS (Cumulative Layout Shift):** 0.25 ❌ (should be < 0.1)
- **Lighthouse Score:** 62/100

### Issues Identified
1. **LCP Issue:** Hero image (2.5MB) loads slowly
2. **FID Issue:** Long tasks blocking main thread
```