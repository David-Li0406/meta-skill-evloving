---
title: Interface Design (Small Interfaces First)
impact: HIGH
impactDescription: Flexible decoupling
tags: idiomatic, interface, design
---

## Interface Design (Small Interfaces First)

Define small interfaces and compose as needed.

**Bad Example (Large Interface):**

```go
// Too large, expensive to implement, hard to test
type UserService interface {
    CreateUser(ctx context.Context, req *CreateUserRequest) (*User, error)
    UpdateUser(ctx context.Context, id int, req *UpdateUserRequest) error
    DeleteUser(ctx context.Context, id int) error
    GetUser(ctx context.Context, id int) (*User, error)
    ListUsers(ctx context.Context, filter *Filter) ([]*User, error)
    ActivateUser(ctx context.Context, id int) error
    DeactivateUser(ctx context.Context, id int) error
    ResetPassword(ctx context.Context, id int) error
    // ... more methods
}
```

**Good Example (Small Interfaces):**

```go
// Split by responsibility
type UserReader interface {
    GetUser(ctx context.Context, id int) (*User, error)
}

type UserWriter interface {
    CreateUser(ctx context.Context, req *CreateUserRequest) (*User, error)
    UpdateUser(ctx context.Context, id int, req *UpdateUserRequest) error
    DeleteUser(ctx context.Context, id int) error
}

type UserLister interface {
    ListUsers(ctx context.Context, filter *Filter) ([]*User, error)
}

// Compose as needed
type UserRepository interface {
    UserReader
    UserWriter
    UserLister
}
```

**Interface Definition Location:**

```go
// Interface is defined by the consumer, not the implementer
// internal/application/user/handler.go
package user

// Declare only the methods you need
type userReader interface {
    GetUser(ctx context.Context, id int) (*User, error)
}

type Handler struct {
    reader userReader
}
```

**Implicit Interfaces:**

```go
// Go interfaces are implicitly implemented
// Any type implementing Read method is an io.Reader
type MyReader struct{}

func (r *MyReader) Read(p []byte) (n int, err error) {
    // ...
}

var _ io.Reader = (*MyReader)(nil) // Compile-time check
```
