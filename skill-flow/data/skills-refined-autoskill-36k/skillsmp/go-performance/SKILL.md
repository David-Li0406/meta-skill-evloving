---
name: go-performance
description: >
  Go performance profiling and optimization. Load when analyzing bottlenecks,
  running benchmarks, profiling CPU/memory, or optimizing hot paths.
  Triggers: pprof, benchmarks, -bench, -memprofile, -cpuprofile, escape analysis,
  sync.Pool, allocation reduction, or performance tuning.
---

# Go Performance Profiling

Performance analysis and optimization patterns for Go applications.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Running benchmarks (`go test -bench`)
- Profiling CPU or memory usage
- Analyzing pprof output
- Optimizing hot paths or reducing allocations
- Escape analysis questions
- Using `sync.Pool` or object reuse
- Memory leak investigation
- Latency optimization

**If you're about to optimize Go code, STOP and use this skill first.**

## Critical Safety Rules

**NEVER:**
- Optimize without benchmarks proving the problem
- Use `sync.Pool` for small objects (overhead exceeds benefit)
- Ignore escape analysis when reducing allocations
- Profile in debug mode (use release builds)
- Assume CPU is the bottleneck (often it's memory/IO)

**ALWAYS:**
- Benchmark before and after optimization
- Use `go test -benchmem` to track allocations
- Profile production-like workloads
- Check escape analysis with `-gcflags="-m"`
- Consider readability vs performance tradeoff

## Quick Reference

| Task | Command |
|------|---------|
| Run benchmarks | `go test -bench=. ./...` |
| With memory stats | `go test -bench=. -benchmem ./...` |
| CPU profile | `go test -bench=. -cpuprofile=cpu.prof` |
| Memory profile | `go test -bench=. -memprofile=mem.prof` |
| Escape analysis | `go build -gcflags="-m" ./...` |
| View profile | `go tool pprof cpu.prof` |
| Compare benchmarks | `benchstat old.txt new.txt` |

---

# Benchmarking

## Writing Benchmarks

```go
func BenchmarkOrderCreation(b *testing.B) {
    // Setup outside the loop
    repo := NewMockRepository()
    svc := NewOrderService(repo)
    
    b.ResetTimer() // Reset after setup
    
    for i := 0; i < b.N; i++ {
        svc.CreateOrder(ctx, testOrder)
    }
}
```

## Benchmark Flags

```bash
# Run all benchmarks
go test -bench=. ./...

# Run specific benchmark
go test -bench=BenchmarkOrderCreation ./...

# With memory allocation stats
go test -bench=. -benchmem ./...

# Run multiple times for statistical significance
go test -bench=. -count=10 ./...

# Set minimum run time
go test -bench=. -benchtime=5s ./...

# Disable CPU profiling overhead
go test -bench=. -cpu=1 ./...
```

## Sub-benchmarks

```go
func BenchmarkProcess(b *testing.B) {
    sizes := []int{10, 100, 1000, 10000}
    
    for _, size := range sizes {
        b.Run(fmt.Sprintf("size=%d", size), func(b *testing.B) {
            data := generateData(size)
            b.ResetTimer()
            
            for i := 0; i < b.N; i++ {
                process(data)
            }
        })
    }
}
```

## Comparing Benchmarks

```bash
# Install benchstat
go install golang.org/x/perf/cmd/benchstat@latest

# Run benchmarks, save results
go test -bench=. -count=10 ./... > old.txt

# Make changes, run again
go test -bench=. -count=10 ./... > new.txt

# Compare
benchstat old.txt new.txt
```

---

# Profiling with pprof

## Generate Profiles

```bash
# CPU profile
go test -bench=. -cpuprofile=cpu.prof ./...

# Memory profile (allocations)
go test -bench=. -memprofile=mem.prof ./...

# Block profile (contention)
go test -bench=. -blockprofile=block.prof ./...

# Mutex profile
go test -bench=. -mutexprofile=mutex.prof ./...
```

## Analyze Profiles

```bash
# Interactive CLI
go tool pprof cpu.prof

# Web UI (recommended)
go tool pprof -http=:8080 cpu.prof

# Top functions by CPU
go tool pprof -top cpu.prof

# Show specific function
go tool pprof -list=ProcessOrder cpu.prof
```

## pprof Commands

| Command | Description |
|---------|-------------|
| `top` | Show top functions by sample count |
| `top -cum` | Show top by cumulative time |
| `list <func>` | Show annotated source |
| `web` | Open call graph in browser |
| `peek <func>` | Show callers and callees |
| `disasm <func>` | Show assembly |

## HTTP pprof (Runtime Profiling)

```go
import _ "net/http/pprof"

func main() {
    // Exposes /debug/pprof/* endpoints
    go http.ListenAndServe(":6060", nil)
    
    // Your application...
}
```

```bash
# Capture 30-second CPU profile from running app
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Memory profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profile
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

---

# Escape Analysis

## Understanding Escape

Variables "escape" to the heap when the compiler cannot prove they're safe on the stack:

```bash
# Show escape analysis decisions
go build -gcflags="-m" ./...

# More verbose
go build -gcflags="-m -m" ./...
```

## Common Escape Causes

| Pattern | Escapes? | Why |
|---------|----------|-----|
| Return pointer to local | Yes | Outlives function |
| Store in interface | Often | Runtime type info needed |
| Closure captures variable | Often | Closure outlives scope |
| Slice grows beyond capacity | Yes | Reallocation |
| Large stack object | Yes | Exceeds stack limit |

## Preventing Escapes

```go
// BAD: Pointer escapes
func NewUser(name string) *User {
    return &User{Name: name}  // Escapes to heap
}

// GOOD: Return value (if struct is small)
func NewUser(name string) User {
    return User{Name: name}  // Stays on stack
}

// BAD: Interface causes escape
func process(v interface{}) { ... }
process(myStruct)  // myStruct escapes

// GOOD: Use generics (Go 1.18+)
func process[T any](v T) { ... }
process(myStruct)  // May stay on stack
```

---

# Reducing Allocations

## Preallocate Slices

```go
// BAD: Multiple allocations as slice grows
var results []Result
for _, item := range items {
    results = append(results, process(item))
}

// GOOD: Single allocation
results := make([]Result, 0, len(items))
for _, item := range items {
    results = append(results, process(item))
}
```

## String Building

```go
// BAD: Multiple allocations
result := ""
for _, s := range strings {
    result += s  // New allocation each iteration
}

// GOOD: Single allocation
var b strings.Builder
b.Grow(totalLen)  // Optional: preallocate
for _, s := range strings {
    b.WriteString(s)
}
result := b.String()
```

## Reuse Buffers

```go
// BAD: New buffer each call
func process(data []byte) []byte {
    buf := make([]byte, 1024)
    // use buf...
    return result
}

// GOOD: Reuse with sync.Pool
var bufPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}

func process(data []byte) []byte {
    buf := bufPool.Get().([]byte)
    defer bufPool.Put(buf)
    // use buf...
    return result
}
```

## Avoid Boxing

```go
// BAD: Interface boxing allocates
func Log(v interface{}) { ... }
Log(42)  // Allocates to box int

// GOOD: Use generics or specific types
func Log[T any](v T) { ... }
Log(42)  // No allocation
```

---

# sync.Pool

## When to Use

- Frequently allocated objects
- Objects are similar size
- Allocation shows up in memory profile
- Object creation is expensive

## When NOT to Use

- Small objects (< 64 bytes)
- Objects with varying sizes
- Objects with complex initialization
- Low allocation rate

## Pattern

```go
var pool = sync.Pool{
    New: func() interface{} {
        return &Buffer{data: make([]byte, 4096)}
    },
}

func process() {
    buf := pool.Get().(*Buffer)
    defer pool.Put(buf)
    
    buf.Reset()  // IMPORTANT: Reset state before use
    // use buf...
}
```

## Gotchas

- Pool is cleared on GC - don't rely on it for caching
- Always reset objects before returning to pool
- Objects may be collected between Put and Get

---

# Memory Optimization

## Struct Field Ordering

```go
// BAD: 24 bytes (padding between fields)
type Bad struct {
    a bool   // 1 byte + 7 padding
    b int64  // 8 bytes
    c bool   // 1 byte + 7 padding
}

// GOOD: 16 bytes (fields ordered by size)
type Good struct {
    b int64  // 8 bytes
    a bool   // 1 byte
    c bool   // 1 byte + 6 padding
}
```

```bash
# Check struct sizes
go install golang.org/x/tools/go/analysis/passes/fieldalignment/cmd/fieldalignment@latest
fieldalignment ./...
```

## Slice vs Array

```go
// Array: fixed size, value type, can stay on stack
var arr [100]int

// Slice: dynamic, reference type, backing array may escape
slice := make([]int, 100)
```

## Map Optimization

```go
// Preallocate if size known
m := make(map[string]int, expectedSize)

// Clear map without reallocating
for k := range m {
    delete(m, k)
}
```

---

# CPU Optimization

## Inlining

```go
// Small functions get inlined automatically
// Check with: go build -gcflags="-m"

// Force no inline (for debugging)
//go:noinline
func process() { ... }
```

## Bounds Check Elimination

```go
// BAD: Bounds check each iteration
for i := 0; i < len(slice); i++ {
    _ = slice[i]  // Bounds check
}

// GOOD: Hint to compiler
_ = slice[len(slice)-1]  // Bounds check once
for i := 0; i < len(slice); i++ {
    _ = slice[i]  // No bounds check
}
```

## Loop Optimization

```go
// BAD: Function call in loop condition
for i := 0; i < len(getItems()); i++ { ... }

// GOOD: Cache length
items := getItems()
for i := 0; i < len(items); i++ { ... }

// BEST: Range (idiomatic)
for i, item := range items { ... }
```

---

# Concurrency Performance

## Worker Pool

```go
func processItems(items []Item, workers int) []Result {
    jobs := make(chan Item, len(items))
    results := make(chan Result, len(items))
    
    // Start workers
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range jobs {
                results <- process(item)
            }
        }()
    }
    
    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)
    
    // Wait and collect
    go func() {
        wg.Wait()
        close(results)
    }()
    
    var out []Result
    for r := range results {
        out = append(out, r)
    }
    return out
}
```

## Reduce Lock Contention

```go
// BAD: Single lock for all operations
type Cache struct {
    mu   sync.Mutex
    data map[string]Value
}

// GOOD: Sharded locks
type Cache struct {
    shards [256]struct {
        mu   sync.Mutex
        data map[string]Value
    }
}

func (c *Cache) shard(key string) *shard {
    h := fnv.New32a()
    h.Write([]byte(key))
    return &c.shards[h.Sum32()%256]
}
```

## sync.RWMutex for Read-Heavy Workloads

```go
type Cache struct {
    mu   sync.RWMutex
    data map[string]Value
}

func (c *Cache) Get(key string) (Value, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.data[key]
    return v, ok
}
```

---

# Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| High memory usage | Allocations in hot path | Use sync.Pool, preallocate slices |
| GC pauses | Many small allocations | Reduce allocations, use value types |
| Slow benchmarks | Setup in loop | Move setup before `b.ResetTimer()` |
| Profile shows nothing | Debug build | Use `-gcflags="-N -l"` to disable optimizations for profiling |
| Escape to heap | Pointer return, interface | Return value types, use generics |
| Lock contention | Single mutex | Shard locks, use RWMutex |
| Benchmark variance | External factors | Use `-count=10`, use `benchstat` |

---

# Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Premature optimization | Waste of time | Profile first, prove problem exists |
| Micro-benchmarks only | Miss real bottlenecks | Profile production workloads |
| Optimize allocations blindly | May not be bottleneck | Check if GC is actually a problem |
| Copy large structs | Stack pressure | Pass by pointer |
| Pass small structs by pointer | Extra indirection | Pass by value |
| Global sync.Pool | May not help | Benchmark before and after |

---

# Example Requests

| User Request | Action |
|--------------|--------|
| "Profile this code" | Generate CPU/memory profile with pprof |
| "Why is this slow?" | Run benchmarks, profile, check escape analysis |
| "Reduce allocations" | Use `-benchmem`, check escape, use sync.Pool |
| "Optimize this loop" | Preallocate, bounds check elimination, cache length |
| "Memory leak" | Heap profile, check goroutine leaks, pprof heap |
| "Compare performance" | Use benchstat with multiple runs |
| "This allocates too much" | Escape analysis, preallocate, reuse buffers |
