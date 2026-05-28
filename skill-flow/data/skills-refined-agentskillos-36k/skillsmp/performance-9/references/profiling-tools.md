# Profiling Tools by Language

Find bottlenecks with language-specific profilers.

## Node.js

### Built-in Profiler

```bash
# Generate V8 profile
node --prof app.js
# Process the log
node --prof-process isolate-*.log > profile.txt
```

### Chrome DevTools

```javascript
// Start debugger
node --inspect app.js
// Open chrome://inspect in Chrome
```

### clinic.js (Recommended)

```bash
npm install -g clinic

# CPU profiling
clinic doctor -- node app.js

# Flame graph
clinic flame -- node app.js

# Memory profiling
clinic heapprofiler -- node app.js
```

## Python

### cProfile (Built-in)

```bash
# Profile script
python -m cProfile -s cumtime script.py

# Save for analysis
python -m cProfile -o profile.pstats script.py
python -c "import pstats; p = pstats.Stats('profile.pstats'); p.sort_stats('cumtime').print_stats(20)"
```

### py-spy (Sampling Profiler)

```bash
pip install py-spy

# Flame graph
py-spy record -o profile.svg -- python script.py

# Live top-like view
py-spy top --pid 12345
```

### memory-profiler

```python
from memory_profiler import profile

@profile
def memory_hungry():
    big_list = [i for i in range(1000000)]
    return big_list

# Run: python -m memory_profiler script.py
```

## Go

### pprof (Built-in)

```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
    // Your application
}
```

```bash
# CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Memory profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Interactive commands
(pprof) top10
(pprof) web  # Opens flame graph in browser
```

### Benchmarking

```go
func BenchmarkFunction(b *testing.B) {
    for i := 0; i < b.N; i++ {
        functionToTest()
    }
}

// Run: go test -bench=. -cpuprofile=cpu.prof -memprofile=mem.prof
```

## Java

### JFR (Java Flight Recorder)

```bash
# Start recording
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr App

# Analyze with JDK Mission Control
jmc recording.jfr
```

### async-profiler

```bash
# Attach to running JVM
./profiler.sh -d 30 -f profile.html <pid>

# Flame graph
./profiler.sh -d 30 -f profile.svg -e cpu <pid>
```

## Browser

### Chrome DevTools Performance

1. Open DevTools (F12)
2. Go to Performance tab
3. Click Record
4. Perform actions
5. Click Stop
6. Analyze flame chart

### Lighthouse

```bash
# CLI
npx lighthouse https://example.com --view

# Programmatic
const lighthouse = require('lighthouse');
const result = await lighthouse(url, {port: 9222});
```

## Database

### PostgreSQL

```sql
-- Enable query logging
ALTER SYSTEM SET log_min_duration_statement = 100;  -- Log queries > 100ms

-- Analyze query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM users WHERE email = 'test@example.com';

-- Check pg_stat_statements
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

### MySQL

```sql
-- Slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- Query analysis
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
SHOW PROFILE FOR QUERY 1;
```

## Quick Reference

| Language | Quick Profile | Flame Graph |
|----------|--------------|-------------|
| Node.js | `clinic doctor` | `clinic flame` |
| Python | `python -m cProfile` | `py-spy record` |
| Go | `go tool pprof` | `pprof -http=:8080` |
| Java | `jcmd <pid> JFR.start` | async-profiler |
| Browser | DevTools Performance | DevTools |
