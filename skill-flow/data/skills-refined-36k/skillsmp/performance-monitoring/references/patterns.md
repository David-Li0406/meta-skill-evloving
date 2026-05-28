# Performance Monitoring - Implementation Patterns

Implementation patterns for monitoring web performance and Core Web Vitals.

## Pattern: Monitor Core Web Vitals

Track LCP, FID, and CLS metrics.

✅ **Good:**
\`\`\`typescript
import { getCLS, getFID, getLCP } from 'web-vitals';

const sendToAnalytics = (metric: Metric) => {
  analytics.track('Web_Vital', {
    metric_name: metric.name,
    metric_value: metric.value,
    metric_id: metric.id,
    metric_rating: metric.rating,
  });
};

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getLCP(sendToAnalytics);
\`\`\`

❌ **Bad:**
\`\`\`typescript
// No performance monitoring
\`\`\`

**Why:** Core Web Vitals:
- User experience metrics
- SEO ranking factor
- Performance insights
- Baseline for optimization

## Pattern: Use Performance Observer

Monitor performance in real-time.

✅ **Good:**
\`\`\`typescript
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(\`\${entry.name}: \${entry.duration}ms\`);
  }
});

observer.observe({ entryTypes: ['measure', 'navigation'] });
\`\`\`

❌ **Bad:**
\`\`\`typescript
// Polling performance data
setInterval(() => {
  const perfData = window.performance.getEntriesByType('navigation');
}, 1000);
\`\`\`

**Why:** Performance Observer:
- Real-time monitoring
- Event-driven
- Better performance
- Standard API

## Pattern: Measure Component Render Time

Track component performance.

✅ **Good:**
\`\`\`typescript
useEffect(() => {
  const start = performance.now();

  return () => {
    const duration = performance.now() - start;
    trackMetric('component_render', duration);
  };
}, []);
\`\`\`

**Why:** Component tracking:
- Identify slow components
- Optimization targets
- Performance regressions

## Summary

**Key Patterns:**
- Monitor Core Web Vitals
- Use Performance Observer
- Track page load times
- Measure component renders
- Send metrics to analytics

**Anti-Patterns to Avoid:**
- No performance monitoring
- Polling instead of observing
- Ignoring Core Web Vitals
