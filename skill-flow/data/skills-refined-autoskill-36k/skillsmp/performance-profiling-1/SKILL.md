---
name: Performance Profiling
description: Web performance analysis, Core Web Vitals, and optimization
---

# Performance Profiling Skill

## Lighthouse Audits

### CLI Usage
```bash
# Run full audit
lighthouse https://smarter.poker --output=json --output-path=./lighthouse-report.json

# Specific categories
lighthouse https://smarter.poker --only-categories=performance,accessibility

# Mobile emulation
lighthouse https://smarter.poker --preset=perf --emulated-form-factor=mobile
```

### Programmatic
```javascript
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runLighthouse(url) {
  const chrome = await chromeLauncher.launch({chromeFlags: ['--headless']});
  const result = await lighthouse(url, {port: chrome.port});
  await chrome.kill();
  return result.lhr;
}
```

## Core Web Vitals

### Metrics to Track
- **LCP** (Largest Contentful Paint) - < 2.5s
- **FID** (First Input Delay) - < 100ms
- **CLS** (Cumulative Layout Shift) - < 0.1
- **INP** (Interaction to Next Paint) - < 200ms
- **TTFB** (Time to First Byte) - < 800ms

### Measurement Code
```javascript
import { onLCP, onFID, onCLS, onINP, onTTFB } from 'web-vitals';

onLCP(console.log);
onFID(console.log);
onCLS(console.log);
onINP(console.log);
onTTFB(console.log);
```

## Bundle Analysis

### Next.js Bundle Analyzer
```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer({});

// Run: ANALYZE=true npm run build
```

### Webpack Bundle Analyzer
```bash
npx webpack-bundle-analyzer stats.json
```

## Network Performance

### Compression Check
```bash
# Check if gzip/brotli enabled
curl -I -H "Accept-Encoding: gzip, deflate, br" https://smarter.poker | grep -i content-encoding
```

### Resource Timing API
```javascript
const resources = performance.getEntriesByType('resource');
resources.forEach(r => {
  console.log(`${r.name}: ${r.duration}ms`);
});
```

## Memory Profiling

### Chrome DevTools Memory
1. Open DevTools > Memory tab
2. Take heap snapshot
3. Perform actions
4. Take another snapshot
5. Compare for leaks

### Node.js Memory
```bash
# Run with memory tracking
node --inspect --expose-gc app.js

# Check memory usage
process.memoryUsage();
```

## Database Performance

### Query Analysis
```sql
-- Explain query plan
EXPLAIN ANALYZE SELECT * FROM large_table WHERE condition;

-- Check slow queries in Supabase
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

## Optimization Checklist
- [ ] Images optimized (WebP, proper sizing)
- [ ] JavaScript code-split
- [ ] CSS inlined for critical path
- [ ] Fonts preloaded
- [ ] Third-party scripts deferred
- [ ] CDN for static assets
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] Caching headers set
- [ ] Gzip/Brotli compression
- [ ] Database queries indexed
