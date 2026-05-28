---
title: Table-Driven Tests
impact: HIGH
impactDescription: Maintainable tests
tags: testing, table-driven, pattern
---

## Table-Driven Tests

Use table-driven tests to improve test maintainability.

**Good Example:**

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"mixed numbers", -2, 3, 1},
        {"zeros", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

**With Setup and Teardown:**

```go
func TestUserService(t *testing.T) {
    tests := []struct {
        name      string
        setup     func(*testing.T) *UserService
        input     CreateUserRequest
        wantErr   bool
        wantUser  *User
    }{
        {
            name: "create valid user",
            setup: func(t *testing.T) *UserService {
                repo := &mockRepo{}
                return NewUserService(repo)
            },
            input: CreateUserRequest{
                Name:  "John",
                Email: "john@example.com",
            },
            wantErr: false,
            wantUser: &User{
                Name:  "John",
                Email: "john@example.com",
            },
        },
        {
            name: "invalid email",
            setup: func(t *testing.T) *UserService {
                return NewUserService(&mockRepo{})
            },
            input: CreateUserRequest{
                Name:  "John",
                Email: "invalid",
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := tt.setup(t)
            user, err := svc.CreateUser(context.Background(), tt.input)

            if (err != nil) != tt.wantErr {
                t.Fatalf("CreateUser() error = %v, wantErr %v", err, tt.wantErr)
            }

            if !tt.wantErr && user.Email != tt.wantUser.Email {
                t.Errorf("user.Email = %s, want %s", user.Email, tt.wantUser.Email)
            }
        })
    }
}
```
