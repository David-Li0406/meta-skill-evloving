# Error Handling Patterns

## Error Wrapping

```go
import (
    "errors"
    "fmt"
)

// Wrap errors with context
func processUser(id string) error {
    user, err := findUser(id)
    if err != nil {
        return fmt.Errorf("processUser: finding user %s: %w", id, err)
    }
    return nil
}

// Check for specific error
if errors.Is(err, ErrNotFound) {
    // handle not found
}

// Extract error type
var validationErr *ValidationError
if errors.As(err, &validationErr) {
    // handle validation error
}
```

## Custom Errors

```go
// Sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Custom error type
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed: %s - %s", e.Field, e.Message)
}

// Usage
return &ValidationError{Field: "email", Message: "invalid format"}
```

## Error Handling Best Practices

```go
// 1. Handle errors at the appropriate level
func handler(w http.ResponseWriter, r *http.Request) {
    result, err := service.Process(r.Context())
    if err != nil {
        switch {
        case errors.Is(err, ErrNotFound):
            http.Error(w, "Not found", http.StatusNotFound)
        case errors.Is(err, ErrUnauthorized):
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
        default:
            log.Printf("unexpected error: %v", err)
            http.Error(w, "Internal error", http.StatusInternalServerError)
        }
        return
    }
    json.NewEncoder(w).Encode(result)
}

// 2. Don't ignore errors
file, err := os.Open(path)
if err != nil {
    return err  // Don't: _ = os.Open(path)
}
defer file.Close()

// 3. Panic only for unrecoverable errors
if config == nil {
    panic("config is required")  // Startup only
}
```
