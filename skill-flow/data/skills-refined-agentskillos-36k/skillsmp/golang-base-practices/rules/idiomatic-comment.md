---
title: Comment Guidelines
impact: MEDIUM
impactDescription: Documentation readability
tags: idiomatic, comment, documentation
---

## Comment Guidelines

Write comments and documentation following Go conventions.

**Doc Comments:**

```go
// Package user provides user management functionality.
// It includes operations for creating, updating, and querying users.
package user

// User represents a registered user in the system.
// The zero value is not valid; use NewUser to create instances.
type User struct {
    ID    uint64
    Name  string
    Email string
}

// NewUser creates a new User with the given name and email.
// It returns an error if the email format is invalid.
func NewUser(name, email string) (*User, error) {
    // ...
}

// IsActive reports whether the user account is active.
func (u *User) IsActive() bool {
    return u.Status == StatusActive
}
```

**Comment Rules:**

```go
// Correct: Start with the described item, complete sentence, end with period
// Request represents a client request to the server.
type Request struct{}

// Encode writes the JSON encoding of req to w.
func Encode(w io.Writer, req *Request) error {}

// Wrong: Does not start with the item name
// This struct represents a request...  // Wrong
// A Request is...                       // Should be "Request represents..."
```

**Error Strings:**

```go
// Correct: Start lowercase, no trailing period
return fmt.Errorf("failed to connect: %w", err)
return errors.New("invalid user id")

// Wrong: Starts uppercase or has trailing period
return fmt.Errorf("Failed to connect: %w", err)  // Wrong
return errors.New("Invalid user id.")           // Wrong
```

**Package Comments:**

```go
// Package math provides basic constants and mathematical functions.
//
// This package does not guarantee bit-identical results across architectures.
package math

// Or use a doc.go file
/*
Package template implements data-driven templates for generating textual output.

The template is parsed from a string using Parse or related methods.
*/
package template
```

**Avoid Useless Comments:**

```go
// Wrong: Comment provides no additional information
// GetName returns the name.
func (u *User) GetName() string { return u.Name }

// Correct: Only comment when needed
func (u *User) Name() string { return u.name }
```
