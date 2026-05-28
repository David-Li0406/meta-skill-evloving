---
title: Sentinel Error Definition
impact: MEDIUM
impactDescription: Error type standardization
tags: error, sentinel, constant
---

## Sentinel Error Definition

Define package-level sentinel errors for callers to check.

**Good Example:**

```go
// pkg/errors/errors.go
package errors

import "errors"

var (
    ErrNotFound      = errors.New("resource not found")
    ErrUnauthorized  = errors.New("unauthorized")
    ErrForbidden     = errors.New("forbidden")
    ErrInvalidInput  = errors.New("invalid input")
    ErrAlreadyExists = errors.New("resource already exists")
)
```

```go
// internal/domain/user/errors.go
package user

import "errors"

var (
    ErrUserNotFound    = errors.New("user not found")
    ErrEmailExists     = errors.New("email already exists")
    ErrInvalidPassword = errors.New("invalid password")
)
```

**Usage:**

```go
func (r *UserRepository) FindByID(ctx context.Context, id uint64) (*User, error) {
    var m userModel
    if err := r.db.WithContext(ctx).First(&m, id).Error; err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, user.ErrUserNotFound
        }
        return nil, fmt.Errorf("find user by id %d: %w", id, err)
    }
    return r.toDomain(&m), nil
}

// Caller
func (h *Handler) GetUser(c *gin.Context) {
    u, err := h.service.GetUser(ctx, id)
    if errors.Is(err, user.ErrUserNotFound) {
        c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
        return
    }
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal error"})
        return
    }
}
```
