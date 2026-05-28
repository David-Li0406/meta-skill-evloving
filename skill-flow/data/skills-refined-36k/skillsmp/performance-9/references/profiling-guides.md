# Profiling Guides

Tool-specific guides for profiling applications.

## Node.js Profiling

### Chrome DevTools Profiler

```bash
# Start app with inspector
node --inspect app.js

# Or attach to running process
node --inspect=9229 app.js
```

1. Open Chrome and navigate to `chrome://inspect`
2. Click "inspect" under your Node.js target
3. Go to "Performance" tab
4. Click Record, perform actions, stop recording
5. Analyze flame chart for hot paths

### Clinic.js Suite

```bash
# Install
npm install -g clinic

# Doctor - general diagnosis
clinic doctor -- node app.js
# Load test your app, then Ctrl+C
# Opens HTML report with recommendations

# Flame - CPU profiling
clinic flame -- node app.js
# Generates flamegraph showing CPU time

# Bubbleprof - async profiling
clinic bubbleprof -- node app.js
# Visualizes async operations and delays

# HeapProfiler - memory profiling
clinic heapprofiler -- node app.js
```

### 0x Flamegraph

```bash
# Install
npm install -g 0x

# Profile
0x app.js
# Load test, then Ctrl+C
# Opens interactive flamegraph

# With specific settings
0x --output-dir ./profiles --collect-only app.js
```

### Memory Profiling

```javascript
// Check memory usage in code
console.log(process.memoryUsage());
// {
//   rss: 30000000,        // Resident Set Size (total memory)
//   heapTotal: 7000000,   // V8 heap size
//   heapUsed: 5000000,    // V8 heap used
//   external: 1000000     // C++ objects bound to JS
// }

// Force garbage collection (for testing)
// Run with: node --expose-gc app.js
if (global.gc) {
  global.gc();
}

// Take heap snapshot programmatically
const v8 = require('v8');
const fs = require('fs');

const snapshotFile = v8.writeHeapSnapshot();
console.log(`Heap snapshot written to ${snapshotFile}`);
```

## Python Profiling

### cProfile (CPU)

```bash
# Run with profiler
python -m cProfile -o output.prof app.py

# View results
python -m pstats output.prof
# In pstats shell:
# sort cumulative
# stats 20

# Visualize with snakeviz
pip install snakeviz
snakeviz output.prof
```

```python
# Profile specific function
import cProfile
import pstats

def profile(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(20)
        return result
    return wrapper

@profile
def my_function():
    # ...
```

### line_profiler (Line-by-line)

```bash
pip install line_profiler
```

```python
# Decorate functions to profile
@profile
def slow_function():
    result = []
    for i in range(10000):
        result.append(i ** 2)
    return result

# Run with kernprof
# kernprof -l -v script.py
```

### memory_profiler

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_heavy_function():
    data = [i ** 2 for i in range(1000000)]
    return sum(data)

# Run: python -m memory_profiler script.py
```

### py-spy (Sampling Profiler)

```bash
pip install py-spy

# Profile running process
py-spy record -o profile.svg --pid 12345

# Or run new process
py-spy record -o profile.svg -- python app.py

# Top-like live view
py-spy top --pid 12345
```

## Go Profiling

### pprof (Built-in)

```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    // Enable pprof endpoints
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()

    // Your app code
}
```

```bash
# CPU profile (30 seconds)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Memory profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profile
go tool pprof http://localhost:6060/debug/pprof/goroutine

# In pprof interactive mode:
# top20        - show top 20 functions
# list funcName - show source with annotations
# web          - open graph in browser
# png > out.png - save graph
```

### Benchmark Profiling

```go
func BenchmarkMyFunction(b *testing.B) {
    for i := 0; i < b.N; i++ {
        MyFunction()
    }
}
```

```bash
# Run benchmarks with CPU profile
go test -bench=. -cpuprofile=cpu.prof

# Run with memory profile
go test -bench=. -memprofile=mem.prof

# Analyze
go tool pprof cpu.prof

# Compare before/after
go tool pprof -base=before.prof after.prof
```

### Trace

```go
import "runtime/trace"

func main() {
    f, _ := os.Create("trace.out")
    trace.Start(f)
    defer trace.Stop()

    // Your code
}
```

```bash
# View trace
go tool trace trace.out
```

## Frontend Profiling

### Chrome DevTools Performance

1. Open DevTools (F12)
2. Go to Performance tab
3. Click Record
4. Perform actions
5. Stop recording
6. Analyze:
   - **Summary**: Time breakdown (Loading, Scripting, Rendering, Painting)
   - **Bottom-Up**: Functions by self time
   - **Call Tree**: Functions by total time
   - **Event Log**: All events chronologically

### Lighthouse

```bash
# CLI
npm install -g lighthouse
lighthouse https://example.com --output=html --output-path=./report.html

# Specific categories
lighthouse https://example.com --only-categories=performance,accessibility

# Emulate mobile
lighthouse https://example.com --emulated-form-factor=mobile
```

### Core Web Vitals Measurement

```javascript
// Using web-vitals library
import { getCLS, getFID, getLCP, getFCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  console.log(metric);
  // Send to your analytics service
}

getCLS(sendToAnalytics);   // Cumulative Layout Shift
getFID(sendToAnalytics);   // First Input Delay
getLCP(sendToAnalytics);   // Largest Contentful Paint
getFCP(sendToAnalytics);   // First Contentful Paint
getTTFB(sendToAnalytics);  // Time to First Byte
```

### Bundle Analysis

```bash
# Webpack
npm install webpack-bundle-analyzer
npx webpack --profile --json > stats.json
npx webpack-bundle-analyzer stats.json

# Vite
npm install rollup-plugin-visualizer
# Add to vite.config.js
import { visualizer } from 'rollup-plugin-visualizer';
export default {
  plugins: [visualizer({ open: true })]
};

# Source map exploration
npm install source-map-explorer
npx source-map-explorer dist/main.js
```

## Database Profiling

### PostgreSQL

```sql
-- Enable query logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = on;
SELECT pg_reload_conf();

-- Explain query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'test@example.com';

-- Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- Table statistics
SELECT relname, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch
FROM pg_stat_user_tables;

-- Index usage
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes;

-- Missing indexes (tables with many seq scans)
SELECT relname, seq_scan, idx_scan,
       CASE WHEN seq_scan > 0
            THEN round(100.0 * idx_scan / (seq_scan + idx_scan), 2)
            ELSE 100 END AS idx_usage_pct
FROM pg_stat_user_tables
WHERE seq_scan > 1000
ORDER BY seq_scan DESC;
```

### MySQL

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- seconds

-- Explain query
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Extended explain
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'test@example.com';

-- Performance schema queries
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;

-- Current running queries
SHOW PROCESSLIST;
```

### Redis

```bash
# Monitor all commands in real-time
redis-cli MONITOR

# Memory usage
redis-cli INFO memory

# Key-space analysis
redis-cli --bigkeys

# Slow log
redis-cli SLOWLOG GET 10
```

## Load Testing

### Apache Bench (ab)

```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:3000/api/users

# With POST data
ab -n 1000 -c 10 -p data.json -T application/json http://localhost:3000/api/users
```

### wrk

```bash
# 12 threads, 400 connections, 30 seconds
wrk -t12 -c400 -d30s http://localhost:3000/api/users

# With Lua script
wrk -t12 -c400 -d30s -s script.lua http://localhost:3000/api/users
```

### k6

```javascript
// script.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp up
    { duration: '1m', target: 20 },    // Stay
    { duration: '10s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
  },
};

export default function () {
  const res = http.get('http://localhost:3000/api/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

```bash
k6 run script.js
```

## Continuous Profiling

### Pyroscope

```yaml
# docker-compose.yml
services:
  pyroscope:
    image: pyroscope/pyroscope:latest
    ports:
      - "4040:4040"

  app:
    build: .
    environment:
      PYROSCOPE_SERVER_ADDRESS: http://pyroscope:4040
```

```javascript
// Node.js integration
const Pyroscope = require('@pyroscope/nodejs');

Pyroscope.init({
  serverAddress: 'http://pyroscope:4040',
  appName: 'my-app',
});

Pyroscope.start();
```

### Grafana Phlare

```yaml
# Production-grade continuous profiling
# Integrates with Grafana for visualization
# Supports Go, Java, Python, Node.js
```

## Performance Monitoring Checklist

### Before Optimization
- [ ] Establish baseline metrics
- [ ] Identify actual bottlenecks (don't guess!)
- [ ] Set performance targets
- [ ] Profile in production-like environment

### During Optimization
- [ ] Make one change at a time
- [ ] Measure impact of each change
- [ ] Document changes and results
- [ ] Avoid premature optimization

### After Optimization
- [ ] Verify targets are met
- [ ] Set up continuous monitoring
- [ ] Create alerts for regressions
- [ ] Document optimizations for team
