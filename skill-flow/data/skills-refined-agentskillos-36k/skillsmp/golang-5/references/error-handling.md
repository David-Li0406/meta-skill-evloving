# Go Error Handling Patterns

## Core Principles

1. **Errors are values** - treat them as such
2. **Handle errors explicitly** - no hidden control flow
3. **Wrap errors with context** - preserve the chain
4. **Define errors at package level** - for type checking

## Basic Error Handling

### Return and Check

```go
// Always check errors immediately
file, err := os.Open(filename)
if err != nil {
    return fmt.Errorf("opening config: %w", err)
}
defer file.Close()

// Don't ignore errors with _
_, err = io.Copy(dst, src)  // ✅ Check err
_, _ = io.Copy(dst, src)    // ❌ Ignoring error
```

### Sentinel Errors

```go
package user

import "errors"

// Package-level sentinel errors
var (
    ErrNotFound     = errors.New("user not found")
    ErrInvalidEmail = errors.New("invalid email address")
    ErrDuplicate    = errors.New("user already exists")
)

// Usage
func (s *Service) GetByID(id string) (*User, error) {
    user, found := s.cache.Get(id)
    if !found {
        return nil, ErrNotFound
    }
    return user, nil
}

// Checking
if errors.Is(err, user.ErrNotFound) {
    // Handle not found case
}
```

## Error Wrapping (Go 1.13+)

### Using %w Verb

```go
// Wrap with context using %w
func (s *Service) CreateUser(req CreateRequest) (*User, error) {
    if err := req.Validate(); err != nil {
        return nil, fmt.Errorf("validating request: %w", err)
    }

    user, err := s.repo.Insert(req.ToUser())
    if err != nil {
        return nil, fmt.Errorf("inserting user %s: %w", req.Email, err)
    }

    return user, nil
}

// Unwrap chain
if errors.Is(err, sql.ErrNoRows) {
    // Matches even if wrapped multiple times
}
```

### errors.Is vs errors.As

```go
// errors.Is - check for specific error value
if errors.Is(err, os.ErrNotExist) {
    // File doesn't exist
}

// errors.As - check for error type and extract
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Printf("Failed path: %s\n", pathErr.Path)
}

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Printf("Invalid field: %s\n", valErr.Field)
}
```

## Custom Error Types

### Structured Errors

```go
type APIError struct {
    Code       int    `json:"code"`
    Message    string `json:"message"`
    RequestID  string `json:"request_id,omitempty"`
    Underlying error  `json:"-"`
}

func (e *APIError) Error() string {
    if e.Underlying != nil {
        return fmt.Sprintf("[%d] %s: %v", e.Code, e.Message, e.Underlying)
    }
    return fmt.Sprintf("[%d] %s", e.Code, e.Message)
}

func (e *APIError) Unwrap() error {
    return e.Underlying
}

// Factory functions
func NewNotFoundError(resource string, err error) *APIError {
    return &APIError{
        Code:       404,
        Message:    fmt.Sprintf("%s not found", resource),
        Underlying: err,
    }
}
```

### Multi-Error Collection

```go
type MultiError struct {
    Errors []error
}

func (m *MultiError) Error() string {
    if len(m.Errors) == 1 {
        return m.Errors[0].Error()
    }
    return fmt.Sprintf("%d errors occurred", len(m.Errors))
}

func (m *MultiError) Add(err error) {
    if err != nil {
        m.Errors = append(m.Errors, err)
    }
}

func (m *MultiError) HasErrors() bool {
    return len(m.Errors) > 0
}

func (m *MultiError) OrNil() error {
    if m.HasErrors() {
        return m
    }
    return nil
}

// Usage
func ValidateAll(items []Item) error {
    var multi MultiError
    for _, item := range items {
        multi.Add(item.Validate())
    }
    return multi.OrNil()
}
```

## Error Handling Patterns

### Early Return

```go
// ✅ Early return - clear flow
func ProcessFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("opening file: %w", err)
    }
    defer file.Close()

    data, err := io.ReadAll(file)
    if err != nil {
        return fmt.Errorf("reading file: %w", err)
    }

    return processData(data)
}

// ❌ Nested - hard to follow
func ProcessFileBad(path string) error {
    file, err := os.Open(path)
    if err == nil {
        defer file.Close()
        data, err := io.ReadAll(file)
        if err == nil {
            return processData(data)
        }
        return err
    }
    return err
}
```

### Error Transformation at Boundaries

```go
// Internal error
type internalError struct {
    Op  string
    Err error
}

// Transform at API boundary
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, err := h.service.GetUser(r.Context(), userID)
    if err != nil {
        // Transform internal error to HTTP response
        switch {
        case errors.Is(err, ErrNotFound):
            http.Error(w, "User not found", http.StatusNotFound)
        case errors.Is(err, ErrUnauthorized):
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
        default:
            log.Printf("internal error: %v", err)
            http.Error(w, "Internal error", http.StatusInternalServerError)
        }
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

### Deferred Error Handling

```go
func WriteFile(path string, data []byte) (err error) {
    file, err := os.Create(path)
    if err != nil {
        return fmt.Errorf("creating file: %w", err)
    }

    // Named return for deferred error handling
    defer func() {
        closeErr := file.Close()
        if err == nil {
            err = closeErr
        }
    }()

    _, err = file.Write(data)
    if err != nil {
        return fmt.Errorf("writing data: %w", err)
    }

    return nil
}
```

## Panic and Recover

### When to Panic

```go
// ✅ Panic: Unrecoverable programming errors
func MustCompile(pattern string) *regexp.Regexp {
    re, err := regexp.Compile(pattern)
    if err != nil {
        panic(fmt.Sprintf("invalid regex pattern: %s", pattern))
    }
    return re
}

// ✅ Panic: Violated invariants
func NewPositive(n int) Positive {
    if n <= 0 {
        panic("NewPositive called with non-positive value")
    }
    return Positive{n}
}

// ❌ Don't panic: Recoverable errors
func ReadConfig(path string) (*Config, error) {
    // Don't panic if file doesn't exist - return error
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, err
    }
    // ...
}
```

### Recover at Boundaries

```go
// HTTP middleware that recovers from panics
func RecoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                log.Printf("panic recovered: %v\n%s", err, debug.Stack())
                http.Error(w, "Internal Server Error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

## Testing Errors

```go
func TestGetUser_NotFound(t *testing.T) {
    svc := NewService(mockRepo)

    _, err := svc.GetUser(ctx, "nonexistent")

    // Check error type
    if !errors.Is(err, ErrNotFound) {
        t.Errorf("expected ErrNotFound, got %v", err)
    }
}

func TestValidation_Error(t *testing.T) {
    req := CreateRequest{Email: "invalid"}

    err := req.Validate()

    // Check error type with As
    var valErr *ValidationError
    if !errors.As(err, &valErr) {
        t.Fatalf("expected ValidationError, got %T", err)
    }

    if valErr.Field != "email" {
        t.Errorf("expected field 'email', got %s", valErr.Field)
    }
}
```

## Best Practices Summary

| Do | Don't |
|----|-------|
| Return errors, don't panic | Panic for expected failures |
| Wrap with context using `%w` | Return bare errors |
| Use `errors.Is/As` for checking | Use `==` for wrapped errors |
| Define sentinel errors at package level | Create errors inline |
| Handle errors at appropriate level | Log and return same error |
| Use meaningful error messages | Include sensitive data in errors |
