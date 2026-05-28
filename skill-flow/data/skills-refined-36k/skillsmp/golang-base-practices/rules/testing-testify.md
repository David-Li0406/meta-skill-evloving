---
title: testify Assertion Library Usage
impact: MEDIUM
impactDescription: Clear assertions
tags: testing, testify, assert
---

## testify Assertion Library Usage

Use testify for clearer assertions.

**Installation:**

```bash
go get github.com/stretchr/testify
```

**assert vs require:**

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestUser(t *testing.T) {
    // assert - continues execution after failure
    assert.Equal(t, "John", user.Name)
    assert.NotNil(t, user.Email)

    // require - stops immediately on failure
    require.NoError(t, err) // Subsequent code depends on err being nil
    require.NotNil(t, user)

    // Subsequent assertions depend on user not being nil
    assert.Equal(t, "john@example.com", user.Email)
}
```

**Common Assertions:**

```go
// Equality
assert.Equal(t, expected, actual)
assert.NotEqual(t, expected, actual)

// Nil checks
assert.Nil(t, obj)
assert.NotNil(t, obj)

// Boolean
assert.True(t, condition)
assert.False(t, condition)

// Errors
assert.NoError(t, err)
assert.Error(t, err)
assert.ErrorIs(t, err, ErrNotFound)
assert.ErrorContains(t, err, "not found")

// Collections
assert.Len(t, slice, 3)
assert.Contains(t, slice, item)
assert.Empty(t, slice)

// Types
assert.IsType(t, &User{}, obj)

// Comparisons
assert.Greater(t, 2, 1)
assert.Less(t, 1, 2)
```

**Custom Messages:**

```go
assert.Equal(t, expected, actual, "user name should match")
assert.Equalf(t, expected, actual, "user %d name should match", userID)
```

**Suite Testing:**

```go
type UserTestSuite struct {
    suite.Suite
    db   *gorm.DB
    repo *UserRepository
}

func (s *UserTestSuite) SetupSuite() {
    s.db = setupTestDB()
    s.repo = NewUserRepository(s.db)
}

func (s *UserTestSuite) TearDownSuite() {
    s.db.Close()
}

func (s *UserTestSuite) TestCreateUser() {
    user := &User{Name: "John"}
    err := s.repo.Save(context.Background(), user)
    s.NoError(err)
    s.NotZero(user.ID)
}

func TestUserSuite(t *testing.T) {
    suite.Run(t, new(UserTestSuite))
}
```
