---
name: performance-optimization
description: Use this skill to profile applications, identify bottlenecks, and optimize performance for improved response times and resource usage.
---

# Performance Optimization Skill

This skill helps you profile, analyze, and optimize application performance across various components.

## When to Use This Skill

- Investigating slow requests or unresponsive applications
- Optimizing API response times and critical paths
- Reducing Lambda cold starts and improving database query performance
- Enhancing frontend rendering and reducing bundle sizes
- Setting up monitoring and performance budgets

## Optimization Process

1. **Measure** - Profile before optimizing to establish a baseline.
2. **Identify** - Find the biggest bottlenecks affecting performance.
3. **Optimize** - Address the highest-impact issues first.
4. **Verify** - Confirm improvements with metrics.

## Performance Metrics

### Key Performance Indicators

**Backend (API):**
- Response time: < 500ms (p95)
- Cold start: < 2s
- Memory usage: < 512MB
- Error rate: < 1%

**Frontend (Web):**
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1
- TTFB: < 600ms
- FCP: < 1.8s

**Database:**
- Query time: < 100ms
- Connection pool: 80% max
- Cache hit rate: > 80%

## Common Bottlenecks

### Database
- Missing indexes (add indexes on WHERE/JOIN columns)
- N+1 queries (use eager loading)
- Large result sets (implement pagination)

### Memory
- Memory leaks (check event listeners, closures)
- Large objects (stream instead of buffer)
- Cache without TTL (add expiration)

### CPU
- Synchronous operations (make async)
- Complex algorithms (optimize or cache)
- Unnecessary computation (memoize)

### Network
- Too many requests (batch/combine)
- Large payloads (compress, paginate)
- No caching (add CDN, browser cache)

## Profiling Commands

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Python profiling
python -m cProfile -o output.prof script.py
python -m pstats output.prof

# Go profiling
go tool pprof http://localhost:6060/debug/pprof/profile
```

## Performance Testing

### Load Testing with k6

```javascript
// load-test.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "2m", target: 100 },  // Ramp up to 100 users
    { duration: "5m", target: 100 },  // Stay at 100 users
    { duration: "2m", target: 200 },  // Ramp up to 200 users
    { duration: "5m", target: 200 },  // Stay at 200 users
    { duration: "2m", target: 0 },    // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],  // 95% of requests < 500ms
    http_req_failed: ["rate<0.01"],    // < 1% failures
  },
};

export default function () {
  const res = http.get("https://api.example.com/endpoint");

  check(res, {
    "status is 200": (r) => r.status === 200,
    "response time < 500ms": (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

## Performance Budgets

| Metric         | Target |
| -------------- | ------ |
| Load Time (3G) | <3s    |
| Load Time (4G) | <1s    |
| API Response   | <200ms |
| Bundle Size    | <500KB |
| LCP            | <2.5s  |
| FID            | <100ms |
| CLS            | <0.1   |

## Best Practices

1. **Profile First**: Always profile before optimizing.
2. **Monitor Continuously**: Track performance metrics regularly.
3. **Set Budgets**: Define performance budgets and enforce them.
4. **Log Performance**: Automatically log slow operations.
5. **Cache Aggressively**: Implement caching for expensive operations.
6. **Optimize Critical Path**: Focus on user-facing operations.
7. **Load Test**: Test under realistic load conditions.
8. **Memory Awareness**: Monitor memory usage and prevent leaks.

## Troubleshooting

### High Response Times
- Check CloudWatch metrics for Lambda duration and errors.
- Profile locally to identify slow operations.
- Optimize identified bottlenecks.

### Memory Issues
- Monitor memory usage and capture heap snapshots.
- Analyze memory usage with tools like Chrome DevTools.

## References

- Node.js Profiling: https://nodejs.org/en/docs/guides/simple-profiling
- Chrome DevTools: https://developer.chrome.com/docs/devtools/performance
- Lighthouse: https://developer.chrome.com/docs/lighthouse
- k6 Load Testing: https://k6.io/docs