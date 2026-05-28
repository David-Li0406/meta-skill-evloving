# godoc (Go)

Documentation convention for Go codebases.

## Overview

Go uses a simple convention: comments directly preceding declarations become documentation. No special syntax or tags required—just well-written prose. The `go doc` command and pkg.go.dev extract and display these comments.

## Basic Syntax

```go
// CalculateShipping determines the shipping cost for an order.
//
// It uses tiered pricing based on weight and destination:
// domestic orders under 5kg use standard rates, larger packages
// use dimensional weight pricing, and international orders
// route through carrier-specific rate tables.
//
// Returns 0 if the destination is not serviceable.
func CalculateShipping(order Order, dest Address) (cents int, err error) {
    // ...
}
```

## Key Conventions

| Convention | Example |
|------------|---------|
| Start with the name | `// User represents an authenticated user.` |
| Complete sentences | End with periods, proper capitalization |
| First sentence = summary | Shown in package listings |
| Blank line = new paragraph | For longer explanations |
| Indented block = preformatted | Code examples, ASCII diagrams |
| `//` only, not `/* */` | For doc comments |

## Applying Core Principles

### Start with the Declared Name

Go convention: begin the comment with the name being documented.

```go
// Bad: Doesn't start with the name
// This function creates a new user in the database.
func NewUser(name string) *User

// Good: Starts with the function name
// NewUser creates a user account with default permissions.
//
// The user is created in pending state and must verify their
// email before they can log in. Returns an error if a user
// with the same email already exists.
func NewUser(name, email string) (*User, error)
```

### Use Different Vocabulary

```go
// Bad: Just restates the signature
// GetUserByID gets a user by their ID.
func GetUserByID(id int) *User

// Good: Explains what "getting" means
// GetUserByID retrieves the complete user profile from the database.
//
// The returned User includes loaded associations (orders, preferences).
// Returns nil if no user exists with the given ID.
// Deactivated accounts are excluded; use GetUserByIDAdmin for those.
func GetUserByID(id int) *User
```

### Document Package Purpose

Package comments explain what the package provides:

```go
// Package auth provides user authentication and session management.
//
// It supports multiple authentication methods including OAuth 2.0,
// SAML, and username/password. Sessions are stored in Redis with
// configurable TTL.
//
// Basic usage:
//
//  session, err := auth.Authenticate(credentials)
//  if err != nil {
//      return err
//  }
//  valid := auth.ValidateSession(session.Token)
//
// For more control over session storage, see the Store interface.
package auth
```

## Type Documentation

```go
// ConnectionPool manages a pool of reusable database connections.
//
// Connections are created lazily up to MaxSize, then reused via
// checkout/checkin. Idle connections are validated periodically
// and recycled if stale.
//
// A ConnectionPool is safe for concurrent use by multiple goroutines.
type ConnectionPool struct {
    // MaxSize is the maximum number of connections to maintain.
    // Once reached, Checkout blocks until a connection is available.
    MaxSize int

    // IdleTimeout is how long an unused connection stays in the pool
    // before being closed. Zero means connections never expire.
    IdleTimeout time.Duration

    // unexported fields are not documented
    mu    sync.Mutex
    conns []*Conn
}

// Checkout retrieves a connection from the pool.
//
// If no connections are available and the pool is at capacity,
// Checkout blocks until one becomes available or ctx is cancelled.
func (p *ConnectionPool) Checkout(ctx context.Context) (*Conn, error) {
    // ...
}
```

## Interface Documentation

```go
// Store defines the interface for session storage backends.
//
// Implementations must be safe for concurrent access.
// The default implementation uses Redis; see RedisStore.
type Store interface {
    // Get retrieves a session by its token.
    // Returns nil, nil if the session doesn't exist.
    // Returns nil, error if the storage backend fails.
    Get(ctx context.Context, token string) (*Session, error)

    // Set stores a session with the given TTL.
    // If a session with this token exists, it is overwritten.
    Set(ctx context.Context, session *Session, ttl time.Duration) error

    // Delete removes a session by its token.
    // Returns nil if the session didn't exist.
    Delete(ctx context.Context, token string) error
}
```

## Examples in Documentation

Go has special support for executable examples:

```go
// In example_test.go

func ExampleNewUser() {
    user, err := auth.NewUser("alice", "alice@example.com")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(user.Status)
    // Output: pending
}

func ExampleConnectionPool_Checkout() {
    pool := db.NewConnectionPool(10)
    ctx := context.Background()

    conn, err := pool.Checkout(ctx)
    if err != nil {
        log.Fatal(err)
    }
    defer pool.Checkin(conn)

    // Use conn...
}
```

These examples:
- Appear in documentation
- Are compiled and can be tested
- Output comments are verified by `go test`

## Documenting Constants and Variables

```go
// Default configuration values.
const (
    // DefaultTimeout is the default request timeout in seconds.
    DefaultTimeout = 30

    // MaxRetries is the maximum number of retry attempts
    // for transient failures.
    MaxRetries = 3
)

// Common errors returned by this package.
var (
    // ErrNotFound is returned when the requested resource doesn't exist.
    ErrNotFound = errors.New("not found")

    // ErrUnauthorized is returned when authentication fails.
    ErrUnauthorized = errors.New("unauthorized")
)
```

## Deprecation

```go
// Old creates a widget using the legacy API.
//
// Deprecated: Use New instead, which supports context cancellation.
func Old(name string) *Widget {
    // ...
}
```

## What NOT to Document

Go's philosophy favors minimal documentation:

```go
// Bad: Obvious from the signature
// Close closes the connection.
func (c *Conn) Close() error

// Better: Only if there's something non-obvious
// Close releases the connection back to the pool.
// After Close, the Conn must not be used.
func (c *Conn) Close() error

// Or just let the name speak for itself if truly obvious
func (c *Conn) Close() error {
```

## Tools

- **go doc**: CLI documentation viewer
- **pkg.go.dev**: Official package documentation site
- **godoc**: Local documentation server (`go install golang.org/x/tools/cmd/godoc@latest`)
- **staticcheck**: Includes documentation style checks
