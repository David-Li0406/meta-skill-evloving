---
title: Naming Conventions
impact: MEDIUM
impactDescription: Code readability
tags: idiomatic, naming, convention
---

## Naming Conventions

Follow Go community naming conventions.

**Package Names:**

```go
// Correct: short, lowercase, single word
package user
package http
package json

// Wrong
package userService  // No camelCase
package user_service // No underscores
package util         // Too generic
```

**Variable Names:**

```go
// Short names for local scope
for i := 0; i < len(items); i++ {}
for _, v := range values {}

// Descriptive names for package-level or long scope
var userCount int
var httpClient *http.Client

// Keep abbreviations consistently cased
var userID string  // Not userId
var httpURL string // Not httpUrl
type XMLParser struct{}
```

**Function Names:**

```go
// Start with verb
func GetUser(id int) *User
func CreateOrder(req *OrderRequest) error
func ValidateEmail(email string) bool

// Boolean functions use Is/Has/Can
func IsValid() bool
func HasPermission() bool
func CanDelete() bool

// Private functions start lowercase
func parseConfig() {}
```

**Constants:**

```go
// No ALL_CAPS with underscores
const maxRetries = 3      // Correct
const MAX_RETRIES = 3     // Wrong (C-style)

// Exported constants start uppercase
const DefaultTimeout = 30 * time.Second
```

**Interface Names:**

```go
// Single-method interfaces use method name + er
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Closer interface { Close() error }

// Multi-method interfaces use descriptive names
type UserRepository interface {
    FindByID(ctx context.Context, id int) (*User, error)
    Save(ctx context.Context, user *User) error
}
```
