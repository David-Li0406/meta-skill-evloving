---
title: Panic and Recover Usage Guidelines
impact: HIGH
impactDescription: Exception handling strategy
tags: error, panic, recover
---

## Panic and Recover Usage Guidelines

Use panic only for unrecoverable errors, not for normal error handling.

**When to Use Panic:**

```go
// 1. Program initialization failure, cannot continue
func init() {
    if os.Getenv("REQUIRED_VAR") == "" {
        panic("REQUIRED_VAR environment variable is not set")
    }
}

// 2. Programming errors, situations that should never happen
func MustCompile(pattern string) *Regexp {
    re, err := Compile(pattern)
    if err != nil {
        panic(`regexp: Compile(` + quote(pattern) + `): ` + err.Error())
    }
    return re
}

// 3. Unreachable code paths
func unreachable() {
    panic("unreachable")
}
```

**Never Panic in These Situations:**

```go
// Wrong: using panic for normal errors
func GetUser(id int) *User {
    user, err := db.Find(id)
    if err != nil {
        panic(err)  // Wrong! Should return error
    }
    return user
}

// Correct: return error
func GetUser(id int) (*User, error) {
    user, err := db.Find(id)
    if err != nil {
        return nil, fmt.Errorf("get user %d: %w", id, err)
    }
    return user, nil
}
```

**Using Recover to Prevent Service Crashes:**

```go
func (s *Server) handleRequest(w http.ResponseWriter, r *http.Request) {
    defer func() {
        if r := recover(); r != nil {
            log.Printf("panic recovered: %v\n%s", r, debug.Stack())
            http.Error(w, "Internal Server Error", http.StatusInternalServerError)
        }
    }()

    // Handle request...
}
```

**Recover Only Works in Defer:**

```go
func SafeCall(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic: %v", r)
        }
    }()
    fn()
    return nil
}

// Direct recover call is ineffective
func wrong() {
    recover() // Ineffective, not in defer
}
```

**Do Not Expose Panic Across Package Boundaries:**

```go
// Internal panic is OK, but public APIs must return error
// If internal panic can be triggered, recover at package boundary

func (p *Parser) Parse(input string) (result *AST, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("parse error: %v", r)
        }
    }()
    return p.parse(input), nil
}
```
