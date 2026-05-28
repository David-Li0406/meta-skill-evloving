## Package Design

### Package Scope & Naming

A package should have a single, clear purpose. The name reflects that purpose.

**Naming rules:**

- Lowercase, no underscores or mixedCaps
- Short, clear, singular: `user`, `http`, `io`
- Not overly broad (`common`, `util`, `helpers` are code smells)

```go
// ✓ Good
package user
package http
package middleware

// ✗ Bad
package users          // plural
package httpServer     // mixedCaps
package common         // what does it do?
```

**Signs it's time to split:**

- Multiple unrelated types with separate responsibilities
- File count exceeds 10-15 files
- You struggle to name it without using "and"

**Signs it's too granular:**

- Packages with 1-2 small files
- Heavy cross-package coupling
- Types that always get used together live in separate packages

### Main Package Organization

The `main` package should be small, focused on initialization:

```go
// Good - main.go
package main

func main() {
	ctx := withSignalCancel(context.Background(), os.Interrupt)

    if err := run(ctx); err != nil {
        log.Fatal(err)
    }
}

func run(ctx context.Context) error {
    cfg, err := config.Load()
    if err != nil {
        return fmt.Errorf("load config: %w", err)
    }

    srv := server.New(cfg)
    if err := srv.Start(); err != nil {
        return fmt.Errorf("start server: %w", err)
    }
    return nil
}

func withSignalCancel(ctx context.Context, signals ...os.Signal) context.Context {
	ctx, cancel := context.WithCancelCause(ctx)
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, signals...)

	go func() {
		cancel(fmt.Errorf("interrupted by signal: %v", <-ch))
	}()

	return ctx
}
```

### Multiple Binaries (cmd/)

```
myproject/
├── cmd/
│   ├── server/
│   │   └── main.go
│   ├── worker/
│   │   └── main.go
│   └── cli/
│       └── main.go
├── internal/
└── pkg/
```

Each `cmd/` subdirectory is a separate `package main`. Keep them thin—delegate to internal packages.

### Internal Packages

Use `internal/` to hide implementation details from external consumers:

```
myproject/
├── internal/
│   ├── auth/       # Only importable within myproject
│   └── cache/
├── pkg/
│   └── client/     # Public API, importable by anyone
└── server.go
```

Code in `internal/` cannot be imported by packages outside the parent of `internal/`.

### API Surface

Export minimally. Unexported by default, export only when needed.

```go
// ✓ Minimal exports
type Client struct {
    baseURL string    // unexported - internal detail
    http    *http.Client
}

func New(baseURL string) *Client { ... }  // exported constructor
func (c *Client) Fetch(ctx context.Context, id string) (Item, error) { ... }

// ✗ Over-exported
type Client struct {
    BaseURL string    // why would caller need to read this?
    HTTP    *http.Client  // dangerous to expose
}
```

### Package Documentation

For non-trivial packages, add a `doc.go`:

```go
// Package auth provides authentication and authorization
// for the application's HTTP handlers.
//
// It supports JWT tokens and API keys. Tokens are validated
// against the configured identity provider.
//
// Basic usage:
//
//     middleware := auth.New(auth.Config{...})
//     handler = middleware.Wrap(handler)
package auth
```

### Common Project Layouts

**Small project / library:**

```
mylib/
├── mylib.go
├── mylib_test.go
└── internal/
    └── helper/
```

**Application with one binary:**

```
myapp/
├── main.go
├── internal/
│   ├── server/
│   ├── store/
│   └── domain/
└── migrations/
```

**Large application:**

```
myapp/
├── cmd/
│   ├── api/
│   └── worker/
├── internal/
│   ├── api/
│   ├── worker/
│   ├── domain/
│   └── store/
├── pkg/           # public libraries (use sparingly)
└── migrations/
```

Avoid the `pkg/` directory unless you explicitly intend code to be imported by external projects. For most applications, `internal/` is sufficient.
