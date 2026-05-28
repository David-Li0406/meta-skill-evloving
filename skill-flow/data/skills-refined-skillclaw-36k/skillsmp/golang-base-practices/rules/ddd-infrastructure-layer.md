---
title: Infrastructure Layer Design
impact: HIGH
impactDescription: Technical implementation details
tags: ddd, infrastructure, repository
---

## Infrastructure Layer Design

The infrastructure layer implements interfaces defined in the domain layer and handles technical details.

**Repository Implementation:**

```go
// internal/infrastructure/persistence/mysql/user_repo.go
package mysql

import (
    "context"
    "errors"
    "myapp/internal/domain/user"
    "gorm.io/gorm"
)

type UserRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *UserRepository {
    return &UserRepository{db: db}
}

// Database model (separate from domain entity)
type userModel struct {
    ID        uint64 `gorm:"primaryKey"`
    Email     string `gorm:"uniqueIndex"`
    Name      string
    Status    string
    CreatedAt time.Time
    UpdatedAt time.Time
}

func (userModel) TableName() string {
    return "users"
}

func (r *UserRepository) FindByID(ctx context.Context, id uint64) (*user.User, error) {
    var m userModel
    if err := r.db.WithContext(ctx).First(&m, id).Error; err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, user.ErrNotFound
        }
        return nil, err
    }
    return r.toDomain(&m), nil
}

func (r *UserRepository) Save(ctx context.Context, u *user.User) error {
    m := r.toModel(u)
    return r.db.WithContext(ctx).Save(m).Error
}

// Model to domain entity conversion
func (r *UserRepository) toDomain(m *userModel) *user.User {
    return &user.User{
        ID:        m.ID,
        Email:     m.Email,
        Name:      m.Name,
        Status:    user.Status(m.Status),
        CreatedAt: m.CreatedAt,
        UpdatedAt: m.UpdatedAt,
    }
}

func (r *UserRepository) toModel(u *user.User) *userModel {
    return &userModel{
        ID:     u.ID,
        Email:  u.Email,
        Name:   u.Name,
        Status: string(u.Status),
    }
}
```

**External Service Adapter:**

```go
// internal/infrastructure/external/payment/client.go
package payment

type Client struct {
    baseURL string
    apiKey  string
}

func NewClient(baseURL, apiKey string) *Client {
    return &Client{baseURL: baseURL, apiKey: apiKey}
}
```
