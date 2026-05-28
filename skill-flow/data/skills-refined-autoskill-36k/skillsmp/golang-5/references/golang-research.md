# golang Research

Research document for the Go language specialist skill. This skill helps developers write idiomatic, performant, and secure Go code.

## Phase 1: Upstream Survey

### VoltAgent golang-pro Subagent

Source: [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-language-specialists/golang-pro.md)

#### Identity
"Expert Go developer specializing in high-performance systems, concurrent programming, and cloud-native microservices."

#### Focus Areas
- Concurrency patterns (goroutines, channels, select)
- Interface design and composition
- Error handling and custom error types
- Performance optimization and pprof profiling
- Testing with table-driven tests and benchmarks
- Module management and vendoring

#### Design Principles
- Simplicity first — clear is better than clever
- Composition over inheritance via interfaces
- Explicit error handling, no hidden magic
- Concurrent by design, safe by default

#### Development Checklist
- [ ] gofmt and golangci-lint compliance
- [ ] Context propagation throughout APIs
- [ ] Error wrapping with context
- [ ] Table-driven tests with subtests
- [ ] Critical path benchmarks
- [ ] Race condition prevention
- [ ] Documentation for exported components

#### Specializations Covered
| Area | Topics |
|------|--------|
| Concurrency | Goroutine lifecycle, channel patterns, context cancellation, worker pools, fan-in/fan-out |
| Error Handling | Wrapped errors, custom types, sentinel errors, recovery strategies |
| Performance | pprof, benchmarks, zero-allocation, sync.Pool, escape analysis |
| Testing | Table-driven, subtests, mocking, fuzzing, race detector |
| Microservices | gRPC, REST, service discovery, circuit breakers, tracing |
| Cloud-Native | Kubernetes operators, service mesh, serverless, event-driven |

#### Delivery Standards
- 80%+ test coverage
- Benchmarks showing performance metrics
- OpenTelemetry/observability integration
- Race condition verification

---

## Phase 2: Research Findings

### 1. Official Go Style Guides

#### Effective Go
Source: [go.dev/doc/effective_go](https://go.dev/doc/effective_go)

Core principles:
- Let `gofmt` handle formatting
- Use MixedCaps, not underscores
- Keep interfaces small and focused
- Return concrete types, accept interfaces
- Make zero values useful

> Note: "Effective Go continues to be useful, but the reader should understand it is far from a complete guide."

#### Go Code Review Comments
Source: [go.dev/wiki/CodeReviewComments](https://go.dev/wiki/CodeReviewComments)

Key guidelines:

**Formatting**
```bash
gofmt -s -w .        # Format with simplification
goimports -w .       # Format + manage imports
```

**Naming**
- Package names: short, lowercase, no underscores
- Avoid `util`, `common`, `misc`, `api`, `types`
- Getters: `obj.Name()` not `obj.GetName()`
- Interfaces: single-method `-er` suffix (`Reader`, `Writer`)

**Error Strings**
```go
// Good: lowercase, no punctuation
fmt.Errorf("something bad happened")

// Bad: capitalized, punctuation
fmt.Errorf("Something bad happened.")
```

**Don't Panic**
```go
// Good: return error
func Parse(s string) (Value, error) {
    if s == "" {
        return Value{}, errors.New("empty string")
    }
    // ...
}

// Bad: panic for normal errors
func Parse(s string) Value {
    if s == "" {
        panic("empty string")
    }
    // ...
}
```

#### Google Go Style Guide
Source: [google.github.io/styleguide/go](https://google.github.io/styleguide/go/)

Three documents:
1. **Style Guide** — Foundation/definitive rules
2. **Style Decisions** — Specific style points with reasoning
3. **Best Practices** — Evolved patterns for common problems

#### Uber Go Style Guide
Source: [github.com/uber-go/guide](https://github.com/uber-go/guide/blob/master/style.md)

Practical examples, kept current with recent Go versions.

---

### 2. Go Linters and Tools

#### golangci-lint
Source: [golangci-lint.run](https://golangci-lint.run/)

Meta-linter that runs multiple linters in parallel.

**Default Linters**
| Linter | Purpose |
|--------|---------|
| `errcheck` | Unchecked errors |
| `govet` | Suspicious constructs |
| `ineffassign` | Unused assignments |
| `staticcheck` | Comprehensive static analysis |
| `unused` | Unused code |

**Recommended Configuration**
```yaml
# .golangci.yml
run:
  timeout: 5m

linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - unused
    - gosec
    - bodyclose
    - exhaustive
    - gocritic
    - gocyclo
    - misspell
    - prealloc

linters-settings:
  govet:
    enable-all: true
  gocyclo:
    min-complexity: 15
  gocritic:
    enabled-tags:
      - diagnostic
      - style
      - performance

issues:
  exclude-use-default: false
  max-issues-per-linter: 0
  max-same-issues: 0
```

#### staticcheck
Source: [staticcheck.dev](https://staticcheck.dev/docs/)

State-of-the-art linter finding bugs, performance issues, and style violations.

Check categories:
- `SA*` — Static analysis (bugs)
- `S*` — Simple (simplifications)
- `ST*` — Style (conventions)
- `QF*` — Quick fixes

#### Other Essential Tools

| Tool | Purpose | Command |
|------|---------|---------|
| `gofmt` | Format code | `gofmt -s -w .` |
| `goimports` | Format + imports | `goimports -w .` |
| `go vet` | Find bugs | `go vet ./...` |
| `go mod tidy` | Clean dependencies | `go mod tidy` |
| `govulncheck` | Security vulnerabilities | `govulncheck ./...` |
| `go test -race` | Race detector | `go test -race ./...` |

---

### 3. Common Go Mistakes

Sources: [100go.co](https://100go.co/), [go.dev/wiki/CommonMistakes](https://go.dev/wiki/CommonMistakes)

#### Error Handling

```go
// Bad: handling error multiple times
func process() error {
    err := doSomething()
    if err != nil {
        log.Printf("error: %v", err)  // logged here
        return err                      // and returned
    }
    return nil
}

// Good: handle once
func process() error {
    if err := doSomething(); err != nil {
        return fmt.Errorf("process: %w", err)
    }
    return nil
}
```

#### Slice vs Array

```go
// Arrays are values (copied)
func modify(arr [3]int) {
    arr[0] = 100  // modifies copy
}

// Slices share underlying array
func modify(s []int) {
    s[0] = 100  // modifies original
}

// Be careful with slice capacity
s := make([]int, 0, 10)  // len=0, cap=10
```

#### Map Initialization

```go
// Bad: nil map panic
var m map[string]int
m["key"] = 1  // panic!

// Good: initialize first
m := make(map[string]int)
m["key"] = 1
```

#### Variable Shadowing

```go
// Dangerous shadowing
x := 1
if condition {
    x := 2       // shadows outer x!
    fmt.Println(x)  // prints 2
}
fmt.Println(x)  // prints 1

// Use go vet -shadow to detect
go tool vet -shadow file.go
```

#### Defer in Loops

```go
// Bad: defers accumulate until function returns
func process(files []string) error {
    for _, f := range files {
        file, _ := os.Open(f)
        defer file.Close()  // not closed until function ends!
    }
    return nil
}

// Good: use anonymous function
func process(files []string) error {
    for _, f := range files {
        if err := func() error {
            file, err := os.Open(f)
            if err != nil {
                return err
            }
            defer file.Close()
            // process file
            return nil
        }(); err != nil {
            return err
        }
    }
    return nil
}
```

#### HTTP Response Body

```go
// Bad: not closing body
resp, err := http.Get(url)
if err != nil {
    return err
}
// body never closed = resource leak

// Good: always close body
resp, err := http.Get(url)
if err != nil {
    return err
}
defer resp.Body.Close()
```

#### Goroutine Leaks

```go
// Bad: goroutine never terminates
func leak() {
    ch := make(chan int)
    go func() {
        val := <-ch  // blocks forever if ch never written
        fmt.Println(val)
    }()
    // function returns, goroutine stuck
}

// Good: use context for cancellation
func noLeak(ctx context.Context) {
    ch := make(chan int)
    go func() {
        select {
        case val := <-ch:
            fmt.Println(val)
        case <-ctx.Done():
            return
        }
    }()
}
```

---

### 4. Go Testing

Sources: [go.dev/wiki/TableDrivenTests](https://go.dev/wiki/TableDrivenTests), [go.dev/doc/security/fuzz](https://go.dev/doc/security/fuzz/)

#### Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

#### Parallel Tests

```go
func TestParallel(t *testing.T) {
    tests := []struct {
        name string
        // ...
    }{
        // ...
    }

    for _, tt := range tests {
        tt := tt  // capture range variable (Go < 1.22)
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            // test code
        })
    }
}
```

#### Benchmarks

```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(1, 2)
    }
}

// With setup
func BenchmarkProcess(b *testing.B) {
    data := setupTestData()
    b.ResetTimer()  // exclude setup time

    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

Run benchmarks:
```bash
go test -bench=. -benchmem ./...
```

#### Fuzzing (Go 1.18+)

```go
func FuzzParse(f *testing.F) {
    // Seed corpus
    f.Add("hello")
    f.Add("world")
    f.Add("")

    f.Fuzz(func(t *testing.T, input string) {
        result, err := Parse(input)
        if err != nil {
            return  // invalid input is ok
        }
        // Verify invariants
        if result.IsEmpty() && input != "" {
            t.Errorf("non-empty input produced empty result")
        }
    })
}
```

Run fuzzing:
```bash
go test -fuzz=FuzzParse -fuzztime=30s ./...
```

---

### 5. Go Idioms and Patterns

#### Accept Interfaces, Return Structs

```go
// Good: accept interface
func Process(r io.Reader) error {
    // works with any Reader
}

// Good: return concrete type
func NewService() *Service {
    return &Service{}
}
```

#### Functional Options

```go
type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) {
        s.port = port
    }
}

func WithTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(opts ...Option) *Server {
    s := &Server{
        port:    8080,
        timeout: 30 * time.Second,
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
srv := NewServer(
    WithPort(9000),
    WithTimeout(time.Minute),
)
```

#### Context Propagation

```go
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    result, err := doWork(ctx)
    if err != nil {
        // handle error
    }
}

func doWork(ctx context.Context) (Result, error) {
    select {
    case <-ctx.Done():
        return Result{}, ctx.Err()
    default:
        // do work
    }
}
```

#### Error Wrapping

```go
import "fmt"

func readConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read config %s: %w", path, err)
    }

    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, fmt.Errorf("parse config: %w", err)
    }

    return &cfg, nil
}

// Check wrapped errors
if errors.Is(err, os.ErrNotExist) {
    // handle missing file
}
```

---

## Audit Checklist Summary

### Critical (Must Have)
- [ ] Code passes `gofmt` / `goimports`
- [ ] No `go vet` warnings
- [ ] All errors handled (not discarded with `_`)
- [ ] No data races (`go test -race`)
- [ ] Context propagated through call chains

### Important (Should Have)
- [ ] golangci-lint configured and passing
- [ ] Table-driven tests for core logic
- [ ] Exported functions documented
- [ ] Error messages lowercase, no punctuation
- [ ] govulncheck shows no vulnerabilities
- [ ] Interfaces small and focused

### Recommended (Nice to Have)
- [ ] Benchmarks for performance-critical paths
- [ ] Fuzz tests for parsers/validators
- [ ] 80%+ test coverage
- [ ] Functional options for complex configs
- [ ] Graceful shutdown handling
- [ ] OpenTelemetry/observability integration

---

## Sources

### Official Documentation
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Wiki: Common Mistakes](https://go.dev/wiki/CommonMistakes)
- [Go Wiki: Table Driven Tests](https://go.dev/wiki/TableDrivenTests)
- [Go Fuzzing](https://go.dev/doc/security/fuzz/)

### Style Guides
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)

### Tools
- [golangci-lint](https://golangci-lint.run/)
- [staticcheck](https://staticcheck.dev/docs/)

### Books & Resources
- [100 Go Mistakes and How to Avoid Them](https://100go.co/)
- [50 Shades of Go](https://golang50shades.com/)

### Upstream
- [VoltAgent golang-pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-language-specialists/golang-pro.md)
