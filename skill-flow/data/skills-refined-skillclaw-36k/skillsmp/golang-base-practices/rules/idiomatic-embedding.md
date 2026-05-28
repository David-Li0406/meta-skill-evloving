---
title: Type Embedding
impact: MEDIUM
impactDescription: Composition over inheritance
tags: idiomatic, embedding, composition
---

## Type Embedding

Use embedding for code reuse, but handle with care.

**Correct Use of Embedding:**

```go
// Embed interfaces to gain methods
type ReadWriter interface {
    io.Reader
    io.Writer
}

// Embed structs to reuse implementation
type Logger struct {
    *log.Logger
}

func NewLogger() *Logger {
    return &Logger{
        Logger: log.New(os.Stdout, "", log.LstdFlags),
    }
}

// Can directly call embedded type's methods
logger := NewLogger()
logger.Println("hello") // Calls log.Logger.Println
```

**Internal Implementation Embedding (Recommended):**

```go
// Embedding for internal implementation, not exposed externally
type Server struct {
    config Config

    // Embed mutex for internal synchronization
    mu sync.Mutex
}

// But don't embed in exported structs to expose to users
```

**Avoid Embedding in Public APIs (Uber Style):**

```go
// Wrong: Embedding in public API leaks implementation details
type Client struct {
    http.Client  // Exposes all http.Client methods
}

// Correct: Use explicit field and delegation
type Client struct {
    client *http.Client
}

func (c *Client) Do(req *http.Request) (*http.Response, error) {
    return c.client.Do(req)
}
```

**Name Collision Handling:**

```go
type A struct {
    Name string
}

type B struct {
    Name string
}

type C struct {
    A
    B
}

// c.Name will error: ambiguous selector
// Must specify explicitly: c.A.Name or c.B.Name

type D struct {
    A
    Name string // Outer field shadows inner
}
// d.Name uses D.Name, d.A.Name uses embedded field
```

**Compile-Time Interface Check:**

```go
// Verify type implements interface
var _ io.Reader = (*MyReader)(nil)
var _ json.Marshaler = (*MyType)(nil)
```
