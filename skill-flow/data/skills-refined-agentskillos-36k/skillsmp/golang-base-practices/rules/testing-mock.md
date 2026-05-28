---
title: Mock and Interface Abstraction
impact: HIGH
impactDescription: Testable design
tags: testing, mock, interface
---

## Mock and Interface Abstraction

Achieve dependency injection and mock testing through interface abstraction.

**Install mockgen:**

```bash
go install go.uber.org/mock/mockgen@latest
```

**Define Interface and Generate Mock:**

```go
// internal/domain/user/repository.go
package user

//go:generate mockgen -source=repository.go -destination=mock_repository.go -package=user

type Repository interface {
    FindByID(ctx context.Context, id uint64) (*User, error)
    Save(ctx context.Context, user *User) error
}
```

```bash
go generate ./...
```

**Using Mock in Tests:**

```go
func TestUserHandler_CreateUser(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := user.NewMockRepository(ctrl)

    // Set expectations
    mockRepo.EXPECT().
        FindByEmail(gomock.Any(), "john@example.com").
        Return(nil, user.ErrUserNotFound)

    mockRepo.EXPECT().
        Save(gomock.Any(), gomock.Any()).
        DoAndReturn(func(ctx context.Context, u *user.User) error {
            u.ID = 1 // Simulate database-generated ID
            return nil
        })

    handler := NewHandler(mockRepo)

    u, err := handler.CreateUser(context.Background(), CreateUserCommand{
        Name:  "John",
        Email: "john@example.com",
    })

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if u.ID != 1 {
        t.Errorf("user.ID = %d, want 1", u.ID)
    }
}
```

**Manual Mock (Simple Scenarios):**

```go
type mockUserRepo struct {
    findByIDFunc func(ctx context.Context, id uint64) (*User, error)
    saveFunc     func(ctx context.Context, user *User) error
}

func (m *mockUserRepo) FindByID(ctx context.Context, id uint64) (*User, error) {
    return m.findByIDFunc(ctx, id)
}

func (m *mockUserRepo) Save(ctx context.Context, user *User) error {
    return m.saveFunc(ctx, user)
}
```
