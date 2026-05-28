# Performance Monitoring - API Reference

API reference for web performance monitoring including Core Web Vitals, Performance API, and monitoring tools.

## Official Documentation

- **Core Web Vitals**: https://web.dev/vitals/
- **Performance API**: https://developer.mozilla.org/en-US/docs/Web/API/Performance_API
- **Web Vitals Library**: https://github.com/GoogleChrome/web-vitals

## Web Vitals Library

### Install

\`\`\`bash
npm install web-vitals
\`\`\`

### Core Metrics

\`\`\`typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// Largest Contentful Paint (LCP)
getLCP((metric) => {
  console.log('LCP:', metric.value);
});

// First Input Delay (FID)
getFID((metric) => {
  console.log('FID:', metric.value);
});

// Cumulative Layout Shift (CLS)
getCLS((metric) => {
  console.log('CLS:', metric.value);
});

// First Contentful Paint (FCP)
getFCP((metric) => {
  console.log('FCP:', metric.value);
});

// Time to First Byte (TTFB)
getTTFB((metric) => {
  console.log('TTFB:', metric.value);
});
\`\`\`

## Performance API

### Navigation Timing

\`\`\`typescript
const perfData = window.performance.getEntriesByType('navigation')[0];

const pageLoadTime = perfData.loadEventEnd - perfData.fetchStart;
const domContentLoaded = perfData.domContentLoadedEventEnd - perfData.fetchStart;
const serverResponseTime = perfData.responseEnd - perfData.requestStart;
\`\`\`

### Resource Timing

\`\`\`typescript
const resources = window.performance.getEntriesByType('resource');

resources.forEach((resource) => {
  console.log(\`\${resource.name}: \${resource.duration}ms\`);
});
\`\`\`

## Best Practices

1. Monitor Core Web Vitals (LCP, FID, CLS)
2. Track page load times
3. Measure Time to Interactive (TTI)
4. Monitor resource loading
5. Use Performance Observer for real-time monitoring
6. Send metrics to analytics
