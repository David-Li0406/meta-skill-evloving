# Go Error Handling Patterns

## Table of Contents

1. [Error Interface Basics](#error-interface-basics)
2. [Creating Custom Errors](#creating-custom-errors)
3. [Error Wrapping](#error-wrapping)
4. [Sentinel Errors](#sentinel-errors)
5. [Error Types](#error-types)
6. [Panic and Recover](#panic-and-recover)
7. [Defer for Cleanup](#defer-for-cleanup)
8. [Best Practices](#best-practices)

## Error Interface Basics

### The error Interface

```go
// The built-in error interface
type error interface {
    Error() string
}

// Creating errors
err := errors.New("something went wrong")
err := fmt.Errorf("failed to process user %d", userID)
```

### Basic Error Handling

```go
func readFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, err
    }
    return data, nil
}

// Usage
data, err := readFile("config.json")
if err != nil {
    log.Printf("Failed to read file: %v", err)
    return err
}
```

### Multiple Return Values

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Usage
result, err := divide(10, 0)
if err != nil {
    fmt.Printf("Error: %v\n", err)
    return
}
fmt.Printf("Result: %f\n", result)
```

## Creating Custom Errors

### Simple Custom Error

```go
type NotFoundError struct {
    Resource   string
    Identifier string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.Identifier)
}

// Usage
func getUser(id string) (*User, error) {
    user, exists := database[id]
    if !exists {
        return nil, &NotFoundError{
            Resource:   "User",
            Identifier: id,
        }
    }
    return user, nil
}
```

### Custom Error with Context

```go
type ValidationError struct {
    Field   string
    Message string
    Value   interface{}
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}

// Usage
func validateEmail(email string) error {
    if !strings.Contains(email, "@") {
        return &ValidationError{
            Field:   "email",
            Message: "invalid email format",
            Value:   email,
        }
    }
    return nil
}
```

### Error Hierarchy with Type

```go
type ErrorType int

const (
    ErrorTypeValidation ErrorType = iota
    ErrorTypeNotFound
    ErrorTypeDatabase
    ErrorTypeExternal
)

type AppError struct {
    Type    ErrorType
    Message string
    Err     error // underlying error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Constructor functions
func NewValidationError(message string) error {
    return &AppError{
        Type:    ErrorTypeValidation,
        Message: message,
    }
}

func NewNotFoundError(resource, id string) error {
    return &AppError{
        Type:    ErrorTypeNotFound,
        Message: fmt.Sprintf("%s not found: %s", resource, id),
    }
}

func NewDatabaseError(operation string, err error) error {
    return &AppError{
        Type:    ErrorTypeDatabase,
        Message: fmt.Sprintf("database %s failed", operation),
        Err:     err,
    }
}
```

## Error Wrapping

### fmt.Errorf with %w

```go
func readConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        // Wrap error with context
        return nil, fmt.Errorf("failed to read config file %s: %w", path, err)
    }

    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("failed to parse config: %w", err)
    }

    return &config, nil
}
```

### errors.Unwrap, Is, and As

```go
import (
    "errors"
    "io/fs"
)

func processFile(path string) error {
    data, err := readConfig(path)
    if err != nil {
        // Check if error is or wraps a specific error
        if errors.Is(err, fs.ErrNotExist) {
            return fmt.Errorf("config file does not exist")
        }

        // Extract specific error type
        var pathErr *fs.PathError
        if errors.As(err, &pathErr) {
            log.Printf("Path error: %s", pathErr.Path)
        }

        return err
    }

    // Process data...
    return nil
}
```

### Custom Unwrap

```go
type MultiError struct {
    Errors []error
}

func (e *MultiError) Error() string {
    var msgs []string
    for _, err := range e.Errors {
        msgs = append(msgs, err.Error())
    }
    return fmt.Sprintf("multiple errors occurred: %s", strings.Join(msgs, "; "))
}

// Implement Unwrap for multi-error
func (e *MultiError) Unwrap() []error {
    return e.Errors
}

// Usage
func processMultiple(items []string) error {
    var errs []error

    for _, item := range items {
        if err := processItem(item); err != nil {
            errs = append(errs, err)
        }
    }

    if len(errs) > 0 {
        return &MultiError{Errors: errs}
    }

    return nil
}
```

## Sentinel Errors

### Defining Sentinel Errors

```go
var (
    ErrNotFound       = errors.New("not found")
    ErrUnauthorized   = errors.New("unauthorized")
    ErrInvalidInput   = errors.New("invalid input")
    ErrDatabaseClosed = errors.New("database connection closed")
)

// Usage
func getUser(id string) (*User, error) {
    if !isConnected {
        return nil, ErrDatabaseClosed
    }

    user, exists := database[id]
    if !exists {
        return nil, ErrNotFound
    }

    return user, nil
}

// Checking sentinel errors
user, err := getUser("123")
if err != nil {
    if errors.Is(err, ErrNotFound) {
        // Handle not found specifically
        return createDefaultUser()
    }
    // Handle other errors
    return err
}
```

### Sentinel Errors with Context

```go
var ErrValidation = errors.New("validation error")

func validateUser(user *User) error {
    if user.Email == "" {
        return fmt.Errorf("%w: email is required", ErrValidation)
    }

    if user.Age < 18 {
        return fmt.Errorf("%w: age must be at least 18", ErrValidation)
    }

    return nil
}

// Checking
if err := validateUser(user); err != nil {
    if errors.Is(err, ErrValidation) {
        // It's a validation error
        log.Printf("Validation failed: %v", err)
    }
}
```

## Error Types

### Typed Errors for Different Scenarios

```go
// HTTP-related errors
type HTTPError struct {
    StatusCode int
    Message    string
    Err        error
}

func (e *HTTPError) Error() string {
    return fmt.Sprintf("HTTP %d: %s", e.StatusCode, e.Message)
}

func (e *HTTPError) Unwrap() error {
    return e.Err
}

// Database errors
type DBError struct {
    Operation string
    Table     string
    Err       error
}

func (e *DBError) Error() string {
    return fmt.Sprintf("database %s on %s: %v", e.Operation, e.Table, e.Err)
}

func (e *DBError) Unwrap() error {
    return e.Err
}

// Usage with type assertion
func handleError(err error) {
    var httpErr *HTTPError
    if errors.As(err, &httpErr) {
        if httpErr.StatusCode == 404 {
            log.Println("Resource not found")
            return
        }
    }

    var dbErr *DBError
    if errors.As(err, &dbErr) {
        log.Printf("Database operation %s failed", dbErr.Operation)
        return
    }

    log.Printf("Unknown error: %v", err)
}
```

## Panic and Recover

### When to Use Panic

```go
// Panic for unrecoverable errors
func initializeApp() {
    config, err := loadConfig()
    if err != nil {
        panic(fmt.Sprintf("cannot start without config: %v", err))
    }

    db, err := connectDB(config)
    if err != nil {
        panic(fmt.Sprintf("cannot start without database: %v", err))
    }
}

// Panic for programming errors
func getElementAt(slice []string, index int) string {
    if index < 0 || index >= len(slice) {
        panic("index out of bounds")
    }
    return slice[index]
}
```

### Using Recover

```go
func safeExecute(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            // Convert panic to error
            err = fmt.Errorf("panic recovered: %v", r)
        }
    }()

    fn()
    return nil
}

// Usage
err := safeExecute(func() {
    // Code that might panic
    riskyOperation()
})
if err != nil {
    log.Printf("Operation failed: %v", err)
}
```

### Recover in HTTP Handlers

```go
func recoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if r := recover(); r != nil {
                log.Printf("Panic recovered: %v\n%s", r, debug.Stack())

                w.WriteHeader(http.StatusInternalServerError)
                json.NewEncoder(w).Encode(map[string]string{
                    "error": "Internal server error",
                })
            }
        }()

        next.ServeHTTP(w, r)
    })
}
```

## Defer for Cleanup

### Basic Defer Usage

```go
func processFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("failed to open file: %w", err)
    }
    defer file.Close() // Always closes, even if error occurs

    // Process file...
    data, err := io.ReadAll(file)
    if err != nil {
        return fmt.Errorf("failed to read file: %w", err)
    }

    return nil
}
```

### Multiple Defers

```go
func processData(ctx context.Context) error {
    // Defers execute in LIFO order (last in, first out)

    // 1. Context cancellation
    ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
    defer cancel() // Executes third

    // 2. Database transaction
    tx, err := db.Begin()
    if err != nil {
        return err
    }
    defer tx.Rollback() // Executes second (or skipped if Commit succeeds)

    // 3. Lock
    mu.Lock()
    defer mu.Unlock() // Executes first

    // Process with all resources...
    if err := processWithDB(tx); err != nil {
        return err
    }

    return tx.Commit()
}
```

### Defer with Error Handling

```go
func writeData(path string, data []byte) (err error) {
    file, err := os.Create(path)
    if err != nil {
        return fmt.Errorf("failed to create file: %w", err)
    }

    // Defer with error capture
    defer func() {
        if closeErr := file.Close(); closeErr != nil {
            if err == nil {
                err = fmt.Errorf("failed to close file: %w", closeErr)
            } else {
                // Log close error but preserve original error
                log.Printf("Failed to close file: %v", closeErr)
            }
        }
    }()

    if _, err = file.Write(data); err != nil {
        return fmt.Errorf("failed to write data: %w", err)
    }

    return nil
}
```

### Defer for Rollback

```go
func transferFunds(from, to string, amount float64) error {
    tx, err := db.Begin()
    if err != nil {
        return fmt.Errorf("failed to start transaction: %w", err)
    }

    // Defer rollback - will be skipped if Commit succeeds
    defer func() {
        if err := tx.Rollback(); err != nil {
            log.Printf("Rollback failed: %v", err)
        }
    }()

    if err := debit(tx, from, amount); err != nil {
        return fmt.Errorf("failed to debit account: %w", err)
    }

    if err := credit(tx, to, amount); err != nil {
        return fmt.Errorf("failed to credit account: %w", err)
    }

    // Commit transaction - successful commit makes rollback a no-op
    if err := tx.Commit(); err != nil {
        return fmt.Errorf("failed to commit transaction: %w", err)
    }

    return nil
}
```

## Best Practices

### Error Message Guidelines

```go
// ✅ Good: Provide context
return fmt.Errorf("failed to fetch user %s: %w", userID, err)

// ❌ Bad: No context
return err

// ✅ Good: Lowercase, no punctuation (unless wrapping)
errors.New("failed to connect to database")

// ❌ Bad: Uppercase, punctuation
errors.New("Failed to connect to database.")

// ✅ Good: Chain of context
fmt.Errorf("process user: validate email: %w", err)
```

### Check Errors Immediately

```go
// ✅ Good: Check immediately
data, err := fetchData()
if err != nil {
    return err
}

// ❌ Bad: Check later
data, err := fetchData()
// ... other code ...
if err != nil {
    return err
}
```

### Don't Ignore Errors

```go
// ❌ Bad: Ignoring error
data, _ := fetchData()

// ✅ Good: Handle or log
data, err := fetchData()
if err != nil {
    log.Printf("Failed to fetch data: %v", err)
    return defaultData
}

// ✅ Good: Explicit ignore with comment
data, err := fetchData()
if err != nil {
    // Ignore error - using default data is acceptable here
    return defaultData
}
```

### Error Wrapping Strategy

```go
// Library/package level: Wrap with context
func (r *Repository) GetUser(id string) (*User, error) {
    user, err := r.db.QueryUser(id)
    if err != nil {
        return nil, fmt.Errorf("get user from database: %w", err)
    }
    return user, nil
}

// Service level: Add business context
func (s *UserService) GetActiveUser(id string) (*User, error) {
    user, err := s.repo.GetUser(id)
    if err != nil {
        return nil, fmt.Errorf("get active user %s: %w", id, err)
    }

    if !user.Active {
        return nil, NewValidationError("user is not active")
    }

    return user, nil
}

// HTTP handler: Log and return user-friendly message
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    userID := r.URL.Query().Get("id")

    user, err := h.service.GetActiveUser(userID)
    if err != nil {
        log.Printf("Failed to get user %s: %v", userID, err)

        // Don't expose internal error to user
        http.Error(w, "User not found", http.StatusNotFound)
        return
    }

    json.NewEncoder(w).Encode(user)
}
```

### Retry Pattern

```go
func retryWithBackoff(
    ctx context.Context,
    maxAttempts int,
    baseDelay time.Duration,
    fn func() error,
) error {
    var err error

    for attempt := 0; attempt < maxAttempts; attempt++ {
        err = fn()
        if err == nil {
            return nil
        }

        // Check if context is cancelled
        if ctx.Err() != nil {
            return fmt.Errorf("retry cancelled: %w", ctx.Err())
        }

        if attempt < maxAttempts-1 {
            delay := baseDelay * time.Duration(1<<attempt) // Exponential backoff
            log.Printf("Attempt %d failed, retrying in %v: %v", attempt+1, delay, err)
            time.Sleep(delay)
        }
    }

    return fmt.Errorf("operation failed after %d attempts: %w", maxAttempts, err)
}

// Usage
err := retryWithBackoff(ctx, 3, time.Second, func() error {
    return fetchFromAPI()
})
```

### Circuit Breaker Pattern

```go
type CircuitBreaker struct {
    maxFailures  int
    resetTimeout time.Duration
    failures     int
    lastFail     time.Time
    state        string // "closed", "open", "half-open"
    mu           sync.Mutex
}

func NewCircuitBreaker(maxFailures int, resetTimeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{
        maxFailures:  maxFailures,
        resetTimeout: resetTimeout,
        state:        "closed",
    }
}

func (cb *CircuitBreaker) Execute(fn func() error) error {
    cb.mu.Lock()

    // Check if we should transition from open to half-open
    if cb.state == "open" && time.Since(cb.lastFail) > cb.resetTimeout {
        cb.state = "half-open"
        cb.failures = 0
    }

    if cb.state == "open" {
        cb.mu.Unlock()
        return errors.New("circuit breaker is open")
    }

    cb.mu.Unlock()

    // Execute function
    err := fn()

    cb.mu.Lock()
    defer cb.mu.Unlock()

    if err != nil {
        cb.failures++
        cb.lastFail = time.Now()

        if cb.failures >= cb.maxFailures {
            cb.state = "open"
            log.Printf("Circuit breaker opened after %d failures", cb.failures)
        }

        return err
    }

    // Success - reset
    if cb.state == "half-open" {
        cb.state = "closed"
        log.Println("Circuit breaker closed")
    }
    cb.failures = 0

    return nil
}
```

## Error Handling Summary

1. **Always check errors**: Never ignore error returns
2. **Provide context**: Wrap errors with `fmt.Errorf` and `%w`
3. **Use sentinel errors**: For well-known error conditions
4. **Create custom types**: For errors needing additional data
5. **Use `errors.Is` and `errors.As`**: For checking wrapped errors
6. **Defer cleanup**: Use defer for resource cleanup
7. **Panic sparingly**: Only for unrecoverable errors
8. **Recover carefully**: Don't recover from panics you can't handle
9. **Log errors**: Log errors with context before returning
10. **Test error paths**: Write tests for all error conditions

## Common Patterns Cheat Sheet

```go
// Check and return
if err != nil {
    return err
}

// Wrap with context
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}

// Check specific error
if errors.Is(err, ErrNotFound) {
    // handle
}

// Check error type
var validationErr *ValidationError
if errors.As(err, &validationErr) {
    // handle
}

// Defer cleanup
defer file.Close()

// Defer with error capture
defer func() {
    if err := resource.Close(); err != nil {
        log.Printf("cleanup failed: %v", err)
    }
}()

// Recover from panic
defer func() {
    if r := recover(); r != nil {
        log.Printf("Recovered: %v", r)
    }
}()
```
