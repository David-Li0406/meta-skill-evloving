---
title: Struct Initialization
impact: MEDIUM
impactDescription: Clear construction
tags: idiomatic, struct, init
---

## Struct Initialization

Use field names for initialization to avoid positional dependency.

**Bad Example (Positional Initialization):**

```go
// Depends on field order, breaks when new fields are added
user := User{"John", "john@example.com", 25, true}
```

**Good Example (Named Field Initialization):**

```go
user := User{
    Name:   "John",
    Email:  "john@example.com",
    Age:    25,
    Active: true,
}
```

**Constructor Pattern:**

```go
// Simple constructor
func NewUser(name, email string) *User {
    return &User{
        Name:      name,
        Email:     email,
        CreatedAt: time.Now(),
    }
}

// Constructor with validation
func NewUser(name, email string) (*User, error) {
    if name == "" {
        return nil, errors.New("name is required")
    }
    if !isValidEmail(email) {
        return nil, errors.New("invalid email")
    }
    return &User{Name: name, Email: email}, nil
}
```

**Functional Options Pattern (Multiple Optional Parameters):**

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
server := NewServer(
    WithPort(9000),
    WithTimeout(60*time.Second),
)
```
