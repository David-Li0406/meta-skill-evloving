---
title: Integration Testing Guidelines
impact: HIGH
impactDescription: End-to-end verification
tags: testing, integration, e2e
---

## Integration Testing Guidelines

Write integration tests to verify component collaboration.

**Test File Naming:**

```
user_test.go          # Unit tests
user_integration_test.go  # Integration tests
```

**Using Build Tags for Isolation:**

```go
//go:build integration

package integration

func TestUserFlow(t *testing.T) {
    // ...
}
```

```bash
# Run only unit tests (default)
go test ./...

# Include integration tests
go test -tags=integration ./...
```

**Test Containers (testcontainers):**

```go
//go:build integration

package integration

import (
    "context"
    "testing"
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/mysql"
)

func TestUserRepository(t *testing.T) {
    ctx := context.Background()

    // Start MySQL container
    mysqlC, err := mysql.RunContainer(ctx,
        testcontainers.WithImage("mysql:8.0"),
        mysql.WithDatabase("testdb"),
        mysql.WithUsername("test"),
        mysql.WithPassword("test"),
    )
    if err != nil {
        t.Fatal(err)
    }
    defer mysqlC.Terminate(ctx)

    // Get connection string
    connStr, err := mysqlC.ConnectionString(ctx)
    if err != nil {
        t.Fatal(err)
    }

    // Initialize database
    db := setupDB(t, connStr)
    repo := NewUserRepository(db)

    // Test
    t.Run("create and find user", func(t *testing.T) {
        user := &User{Name: "John", Email: "john@example.com"}
        err := repo.Save(ctx, user)
        if err != nil {
            t.Fatalf("Save() error = %v", err)
        }

        found, err := repo.FindByID(ctx, user.ID)
        if err != nil {
            t.Fatalf("FindByID() error = %v", err)
        }
        if found.Email != user.Email {
            t.Errorf("Email = %s, want %s", found.Email, user.Email)
        }
    })
}
```

**HTTP API Integration Test:**

```go
func TestAPI(t *testing.T) {
    router := setupRouter()
    server := httptest.NewServer(router)
    defer server.Close()

    t.Run("create user", func(t *testing.T) {
        body := `{"name":"John","email":"john@example.com"}`
        resp, err := http.Post(server.URL+"/api/users", "application/json", strings.NewReader(body))
        if err != nil {
            t.Fatal(err)
        }
        defer resp.Body.Close()

        if resp.StatusCode != http.StatusCreated {
            t.Errorf("status = %d, want %d", resp.StatusCode, http.StatusCreated)
        }
    })
}
```
