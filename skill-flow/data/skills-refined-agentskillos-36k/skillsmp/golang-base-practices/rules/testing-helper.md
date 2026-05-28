---
title: Test Helper Function Guidelines
impact: MEDIUM
impactDescription: Clear test code
tags: testing, helper, t.Helper
---

## Test Helper Function Guidelines

Write test helper functions correctly.

**Use t.Helper():**

```go
// Helper functions must call t.Helper()
func assertEqual(t *testing.T, got, want interface{}) {
    t.Helper()  // Mark as helper function
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}

// When called, error line number points to test code, not helper function
func TestAdd(t *testing.T) {
    result := Add(1, 2)
    assertEqual(t, result, 3)  // Error will point to this line
}
```

**Setup Helper Functions:**

```go
// Return cleanup function
func setupTestDB(t *testing.T) (*sql.DB, func()) {
    t.Helper()

    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("failed to open db: %v", err)
    }

    return db, func() {
        db.Close()
    }
}

func TestUser(t *testing.T) {
    db, cleanup := setupTestDB(t)
    defer cleanup()

    // Test...
}
```

**Using t.Cleanup() (Go 1.14+):**

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()

    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("failed to open db: %v", err)
    }

    t.Cleanup(func() {
        db.Close()
    })

    return db
}

func TestUser(t *testing.T) {
    db := setupTestDB(t)  // No manual cleanup needed
    // Test...
}
```

**Assertion Helper Functions:**

```go
// Keep validation logic in test functions, not helpers
// Wrong: Helper function contains validation logic
func assertUserCreated(t *testing.T, db *sql.DB, email string) {
    t.Helper()
    var count int
    db.QueryRow("SELECT COUNT(*) FROM users WHERE email = ?", email).Scan(&count)
    if count != 1 {
        t.Errorf("expected 1 user with email %s, got %d", email, count)
    }
}

// Correct: Helper only fetches, validation stays in test
func getUserCount(t *testing.T, db *sql.DB, email string) int {
    t.Helper()
    var count int
    if err := db.QueryRow("SELECT COUNT(*) FROM users WHERE email = ?", email).Scan(&count); err != nil {
        t.Fatalf("failed to query: %v", err)
    }
    return count
}

func TestCreateUser(t *testing.T) {
    db := setupTestDB(t)
    createUser(db, "test@example.com")

    count := getUserCount(t, db, "test@example.com")
    if count != 1 {
        t.Errorf("expected 1 user, got %d", count)
    }
}
```

**Avoid Calling t.Fatal in Goroutines:**

```go
// Wrong: Calling t.Fatal in goroutine
func TestConcurrent(t *testing.T) {
    go func() {
        if err := doSomething(); err != nil {
            t.Fatal(err)  // Wrong! Will panic
        }
    }()
}

// Correct: Use channel to pass errors
func TestConcurrent(t *testing.T) {
    errs := make(chan error, 1)
    go func() {
        errs <- doSomething()
    }()

    if err := <-errs; err != nil {
        t.Fatal(err)
    }
}
```
