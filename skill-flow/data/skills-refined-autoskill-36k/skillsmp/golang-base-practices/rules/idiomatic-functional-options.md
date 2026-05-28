---
title: Functional Options Pattern
impact: HIGH
impactDescription: Flexible configuration API
tags: idiomatic, functional-options, pattern
---

## Functional Options Pattern

Use the functional options pattern to design flexible configuration APIs.

**Basic Implementation:**

```go
type Server struct {
    host    string
    port    int
    timeout time.Duration
    logger  *log.Logger
}

type Option func(*Server)

func WithHost(host string) Option {
    return func(s *Server) {
        s.host = host
    }
}

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

func WithLogger(l *log.Logger) Option {
    return func(s *Server) {
        s.logger = l
    }
}

func NewServer(opts ...Option) *Server {
    // Set defaults
    s := &Server{
        host:    "localhost",
        port:    8080,
        timeout: 30 * time.Second,
        logger:  log.Default(),
    }

    // Apply options
    for _, opt := range opts {
        opt(s)
    }

    return s
}
```

**Usage Examples:**

```go
// Use default configuration
server := NewServer()

// Custom configuration
server := NewServer(
    WithHost("0.0.0.0"),
    WithPort(9000),
    WithTimeout(60*time.Second),
)

// Partial customization
server := NewServer(
    WithPort(9000),
)
```

**Options with Validation:**

```go
func WithPort(port int) Option {
    return func(s *Server) {
        if port < 1 || port > 65535 {
            // Two approaches:
            // 1. panic (suitable for Must functions)
            panic(fmt.Sprintf("invalid port: %d", port))
            // 2. Return error (see pattern below)
        }
        s.port = port
    }
}
```

**Options with Error Returns:**

```go
type OptionErr func(*Server) error

func NewServerWithErr(opts ...OptionErr) (*Server, error) {
    s := &Server{
        host: "localhost",
        port: 8080,
    }

    for _, opt := range opts {
        if err := opt(s); err != nil {
            return nil, err
        }
    }

    return s, nil
}

func WithPortErr(port int) OptionErr {
    return func(s *Server) error {
        if port < 1 || port > 65535 {
            return fmt.Errorf("invalid port: %d", port)
        }
        s.port = port
        return nil
    }
}
```

**When to Use Functional Options:**

| Scenario | Recommended Approach |
|----------|---------------------|
| Few required parameters | Direct parameters |
| Multiple optional parameters | Functional options |
| Complex configuration structure | Config struct + functional options |
| Most calls don't need options | Functional options (variadic) |
