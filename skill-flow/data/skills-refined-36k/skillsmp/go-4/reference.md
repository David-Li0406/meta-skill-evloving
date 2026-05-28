# Go Reference

## Go 1.24+ Features

### Range-Over-Func (Iterators)
Custom iterators using `iter.Seq` and `iter.Seq2`:

```go
import "iter"

// Single-value iterator
func Evens(n int) iter.Seq[int] {
    return func(yield func(int) bool) {
        for i := 0; i < n; i += 2 {
            if !yield(i) {
                return
            }
        }
    }
}

// Key-value iterator
func Enumerate[T any](s []T) iter.Seq2[int, T] {
    return func(yield func(int, T) bool) {
        for i, v := range s {
            if !yield(i, v) {
                return
            }
        }
    }
}

// Usage
for v := range Evens(10) {
    fmt.Println(v)
}
```

### Standard Library Iterators
```go
import (
    "slices"
    "maps"
)

// slices package
slices.All(s)           // iter.Seq2[int, T] - index, value
slices.Values(s)        // iter.Seq[T] - values only
slices.Backward(s)      // iter.Seq2[int, T] - reverse order
slices.Collect(seq)     // Collect iterator into slice

// maps package
maps.All(m)             // iter.Seq2[K, V]
maps.Keys(m)            // iter.Seq[K]
maps.Values(m)          // iter.Seq[V]
maps.Collect(seq)       // Collect iterator into map
```

### Enhanced Generics
```go
// Type inference improvements
func Transform[S ~[]E, E, R any](s S, fn func(E) R) []R {
    result := make([]R, len(s))
    for i, v := range s {
        result[i] = fn(v)
    }
    return result
}

// Constraint unions
type Number interface {
    ~int | ~int64 | ~float64
}
```

## Project Structure

### Standard Layout
```
project/
├── cmd/
│   └── myapp/
│       └── main.go        # Entry point
├── internal/              # Private packages (import restricted)
│   ├── config/
│   ├── handler/
│   └── service/
├── pkg/                   # Public packages (optional)
├── api/                   # API definitions (OpenAPI, proto)
├── web/                   # Web assets
├── scripts/               # Build/dev scripts
├── go.mod
├── go.sum
└── Makefile
```

### Flat Structure (small projects)
```
project/
├── main.go
├── handler.go
├── service.go
├── go.mod
└── go.sum
```

### Key Conventions
- `cmd/` - Each subdirectory is a separate binary
- `internal/` - Compiler-enforced private packages
- `pkg/` - Only for truly reusable public libraries
- Keep `main.go` minimal - delegate to internal packages

## Uber Style Guide Highlights

### Naming
```go
// Unexported: camelCase
var maxRetries = 3

// Exported: PascalCase
var DefaultTimeout = 30 * time.Second

// Acronyms: consistent case
type HTTPClient struct{}  // Not HttpClient
type userID string        // Not userID when unexported

// Interfaces: -er suffix for single method
type Reader interface { Read(p []byte) (n int, err error) }
```

### Error Handling
```go
// Wrap errors with context
if err := doThing(); err != nil {
    return fmt.Errorf("doing thing: %w", err)
}

// Check error types
if errors.Is(err, os.ErrNotExist) { ... }

// Extract error values
var pathErr *os.PathError
if errors.As(err, &pathErr) { ... }

// Sentinel errors are package-level
var ErrNotFound = errors.New("not found")
```

### Prefer Composition
```go
// Embed for delegation, not inheritance
type Server struct {
    http.Handler  // Embed interface
    logger *zap.Logger
}

// Prefer interfaces in function params
func Process(r io.Reader) error { ... }
```

### Initialization
```go
// Prefer var for zero values
var buf bytes.Buffer

// Prefer := for non-zero values
count := 10
names := []string{"a", "b"}

// Use make for slices with known capacity
s := make([]int, 0, 100)
```

## golangci-lint Configuration

### Minimal `.golangci.yml`
```yaml
run:
  timeout: 5m

linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - unused
    - gosimple
    - ineffassign
    - typecheck
    - gofmt
    - goimports
    - misspell
    - unconvert
    - unparam
    - revive

linters-settings:
  revive:
    rules:
      - name: exported
        arguments: [checkPrivateReceivers, disableStutteringCheck]
```

### Recommended Additional Linters
```yaml
linters:
  enable:
    # Error handling
    - errcheck
    - errorlint      # Error wrapping
    - wrapcheck      # Wrap external errors

    # Style
    - gofumpt        # Stricter gofmt
    - godot          # Comments end with period
    - whitespace     # Unnecessary whitespace

    # Performance
    - prealloc       # Preallocate slices
    - bodyclose      # Close HTTP response bodies

    # Security
    - gosec          # Security issues
```

## Module Best Practices

### go.mod Management
```go
// Require specific versions
require (
    github.com/gin-gonic/gin v1.9.1
    go.uber.org/zap v1.27.0
)

// Use replace for local development
replace github.com/myorg/mylib => ../mylib

// Retract broken versions
retract (
    v1.0.0 // Contains critical bug
    [v1.1.0, v1.2.0] // Range retraction
)
```

### Multi-Module Workspaces
```go
// go.work
go 1.24

use (
    ./services/api
    ./services/worker
    ./pkg/shared
)
```

## Repository Routing Table

Query Context7 for these library IDs based on the topic:

| Topic | Library ID | Use For |
|-------|------------|---------|
| **Style & Idioms** | `/uber-go/guide` | Code style, naming, patterns |
| **Linting** | `/golangci/golangci-lint` | Linter config, rules |
| **Testing** | `/stretchr/testify` | Assertions, mocking, suites |
| **Logging** | `/uber-go/zap` | High-performance structured logging |
| **Logging (alt)** | `/rs/zerolog` | Zero-allocation JSON logging |
| **Web/HTTP** | `/gin-gonic/gin` | HTTP framework, middleware |
| **Web/HTTP (alt)** | `/go-chi/chi` | Lightweight router |
| **Web/HTTP (alt)** | `/labstack/echo` | High-performance web framework |
| **CLI** | `/spf13/cobra` | CLI applications, subcommands |
| **CLI (TUI)** | `/charmbracelet/bubbletea` | Terminal UI applications |
| **Config** | `/spf13/viper` | Configuration management |
| **Config (alt)** | `/knadh/koanf` | Lightweight config library |
| **Database/ORM** | `/go-gorm/gorm` | ORM, migrations, associations |
| **Database (SQL)** | `/jmoiron/sqlx` | Extensions to database/sql |
| **Database (Postgres)** | `/jackc/pgx` | PostgreSQL driver |
| **DI** | `/uber-go/fx` | Dependency injection framework |
| **DI (codegen)** | `/google/wire` | Compile-time DI |
| **Validation** | `/go-playground/validator` | Struct validation |
| **HTTP Client** | `/go-resty/resty` | REST client with retries |
| **Concurrency** | `/sourcegraph/conc` | Structured concurrency |
| **Worker Pools** | `/panjf2000/ants` | Goroutine pool |
| **Errors** | `/uber-go/multierr` | Error aggregation |
| **Errors (alt)** | `/samber/oops` | Error handling with context |
| **Generics/Utils** | `/samber/lo` | Lodash-style utilities |
