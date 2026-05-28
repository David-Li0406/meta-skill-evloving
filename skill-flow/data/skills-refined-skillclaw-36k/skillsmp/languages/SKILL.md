---
name: languages
description: Guidelines for Go and Markdown.
---

# Languages

## Go
Follow [Effective Go](https://go.dev/doc/effective_go).

### Functional Options Pattern
Use for object construction.
```go
// Required: host, port. Optional: timeout.
func New(host string, port int, opts ...Option) (*Server, error) {
    s := &Server{host: host, port: port, timeout: 30 * time.Second}
    for _, opt := range opts { ... }
    return s, nil
}
```

### Error Handling
Wrap upstream errors for context. Define common errors at package level.
```go
var ErrUpstreamFailure = errors.New("dependency failed")
return "", fmt.Errorf("%w: %s", ErrUpstreamFailure, err)
```

### Reusable Libraries
Place reusable libraries in `andrewhowdencom/stdlib`.
- **Testable Examples**: Use `Example()` functions in `_test.go` files.
- **Index**: Check `skuills/languages/references/reference-stdlib-index.md` (Note: migrated content).

## Markdown
Break documents at **120 characters**.
