---
title: Application Layer Design
impact: HIGH
impactDescription: Use case orchestration
tags: ddd, application, usecase
---

## Application Layer Design

The application layer orchestrates use cases, coordinating domain objects to complete business processes.

**Command Query Separation (CQRS):**

```go
// internal/application/user/command.go
package user

type CreateUserCommand struct {
    Email string
    Name  string
}

type UpdateUserCommand struct {
    ID   uint64
    Name string
}
```

```go
// internal/application/user/query.go
package user

type GetUserQuery struct {
    ID uint64
}

type ListUsersQuery struct {
    Page     int
    PageSize int
    Status   string
}
```

**Handler (use case implementation):**

```go
// internal/application/user/handler.go
package user

import (
    "context"
    "myapp/internal/domain/user"
)

type Handler struct {
    repo user.Repository
}

func NewHandler(repo user.Repository) *Handler {
    return &Handler{repo: repo}
}

func (h *Handler) CreateUser(ctx context.Context, cmd CreateUserCommand) (*user.User, error) {
    // Validate email format
    email, err := user.NewEmail(cmd.Email)
    if err != nil {
        return nil, err
    }

    // Check if email already exists
    existing, err := h.repo.FindByEmail(ctx, string(email))
    if err == nil && existing != nil {
        return nil, errors.New("email already exists")
    }

    // Create user
    u := &user.User{
        Email:  string(email),
        Name:   cmd.Name,
        Status: user.StatusActive,
    }

    if err := h.repo.Save(ctx, u); err != nil {
        return nil, err
    }

    return u, nil
}

func (h *Handler) GetUser(ctx context.Context, q GetUserQuery) (*user.User, error) {
    return h.repo.FindByID(ctx, q.ID)
}
```
