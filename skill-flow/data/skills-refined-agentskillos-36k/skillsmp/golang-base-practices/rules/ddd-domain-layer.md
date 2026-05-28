---
title: Domain Layer Design
impact: HIGH
impactDescription: Core business logic
tags: ddd, domain, entity
---

## Domain Layer Design

The domain layer contains core business logic with no dependencies on external frameworks.

**Entity:**

```go
// internal/domain/user/entity.go
package user

import (
    "errors"
    "time"
)

type User struct {
    ID        uint64
    Email     string
    Name      string
    Status    Status
    CreatedAt time.Time
    UpdatedAt time.Time
}

type Status string

const (
    StatusActive   Status = "active"
    StatusInactive Status = "inactive"
    StatusBanned   Status = "banned"
)

// Business rules encapsulated in entity
func (u *User) Activate() error {
    if u.Status == StatusBanned {
        return errors.New("cannot activate banned user")
    }
    u.Status = StatusActive
    return nil
}

func (u *User) CanOrder() bool {
    return u.Status == StatusActive
}
```

**Value Object:**

```go
// internal/domain/user/email.go
package user

import (
    "errors"
    "regexp"
)

type Email string

var emailRegex = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

func NewEmail(s string) (Email, error) {
    if !emailRegex.MatchString(s) {
        return "", errors.New("invalid email format")
    }
    return Email(s), nil
}
```

**Repository Interface (defined in domain layer):**

```go
// internal/domain/user/repository.go
package user

import "context"

type Repository interface {
    FindByID(ctx context.Context, id uint64) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
    Save(ctx context.Context, user *User) error
    Delete(ctx context.Context, id uint64) error
}
```
