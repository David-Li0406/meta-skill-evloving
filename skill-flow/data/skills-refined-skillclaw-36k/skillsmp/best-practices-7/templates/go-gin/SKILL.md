---
name: best-practices
description: Go + Gin performance optimization and idiomatic patterns with mandatory Uber fx DI. Contains 48 rules across 8 categories, prioritized by impact for automated code generation and review.
license: MIT
metadata:
  author: devnogari
  project_type: go-gin
---

# Go + Gin Best Practices

Comprehensive performance optimization and idiomatic patterns guide for Go applications using Gin framework, with mandatory Uber fx dependency injection. Contains 48 rules across 8 categories, prioritized by impact to guide automated code generation and review.

**MANDATORY**: This project uses **Uber fx** for dependency injection. All services MUST use fx.

## When to Apply

Reference these guidelines when:
- Writing new handlers, services, or repositories
- Implementing middleware or error handling
- Optimizing concurrency patterns
- Reviewing or refactoring Go code
- Debugging goroutine or memory issues
- **Creating any new service or component** (must use fx)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Error Handling | CRITICAL | `err-` |
| 2 | Concurrency | CRITICAL | `conc-` |
| 3 | Uber fx DI | CRITICAL | `fx-` |
| 4 | Gin Handlers | HIGH | `gin-` |
| 5 | Performance | HIGH | `perf-` |
| 6 | Testing | MEDIUM | `test-` |
| 7 | Code Style | MEDIUM | `style-` |
| 8 | Advanced Patterns | LOW | `adv-` |

## Quick Reference

### 1. Error Handling (CRITICAL)

- `err-wrap` - Wrap errors with context using fmt.Errorf %w
- `err-once` - Handle errors only once, don't log and return
- `err-types` - Define custom error types for domain errors
- `err-sentinel` - Use sentinel errors for expected conditions
- `err-context` - Add operation context to error messages
- `err-check` - Always check returned errors, never ignore

### 2. Concurrency (CRITICAL)

- `conc-context` - Use context.Context for cancellation propagation
- `conc-goroutine-leak` - Prevent goroutine leaks with proper cleanup
- `conc-channel-close` - Close channels from sender side only
- `conc-mutex` - Prefer sync.Mutex over channels for simple state
- `conc-waitgroup` - Use sync.WaitGroup for goroutine synchronization
- `conc-select` - Use select with default/timeout for non-blocking ops

### 3. Uber fx DI (CRITICAL - MANDATORY)

- `fx-provide` - All dependencies via fx.Provide, no manual instantiation
- `fx-module` - Group related providers into fx.Module per domain
- `fx-lifecycle` - Use fx.Lifecycle for startup/shutdown hooks
- `fx-invoke` - Use fx.Invoke for side effects, not fx.Provide
- `fx-decorate` - Use fx.Decorate for cross-cutting concerns
- `fx-test` - Use fxtest.New() for integration testing

### 4. Gin Handlers (HIGH)

- `gin-binding` - Use ShouldBind with validation tags
- `gin-response` - Consistent response format with wrapper types
- `gin-middleware` - Chain middleware for cross-cutting concerns
- `gin-group` - Use RouterGroup for versioned/grouped routes
- `gin-error` - Centralized error handling middleware
- `gin-context` - Never store gin.Context, copy needed values

### 5. Performance (HIGH)

- `perf-alloc` - Minimize allocations in hot paths
- `perf-pool` - Use sync.Pool for frequently allocated objects
- `perf-slice` - Preallocate slices with known capacity
- `perf-map` - Preallocate maps with known size
- `perf-string` - Use strings.Builder for concatenation
- `perf-interface` - Avoid interface{} in hot paths, use generics

### 6. Testing (MEDIUM)

- `test-table` - Use table-driven tests for coverage
- `test-parallel` - Run independent tests in parallel
- `test-mock` - Use interfaces for mockable dependencies
- `test-fixture` - Use testdata/ for test fixtures
- `test-benchmark` - Write benchmarks for performance-critical code
- `test-golden` - Use golden files for complex output validation

### 7. Code Style (MEDIUM)

- `style-naming` - Follow Go naming conventions (MixedCaps, not snake_case)
- `style-receiver` - Consistent receiver names, short (1-2 chars)
- `style-interface` - Accept interfaces, return concrete types
- `style-package` - Short, lowercase package names without underscores
- `style-comment` - Document exported symbols with complete sentences
- `style-import` - Group imports: stdlib, external, internal

### 8. Advanced Patterns (LOW)

- `adv-generics` - Use generics for type-safe collections and utilities
- `adv-embed` - Use embedding for composition over inheritance
- `adv-reflect` - Avoid reflect in hot paths, use code generation
- `adv-unsafe` - Avoid unsafe package except for FFI/optimization
- `adv-cgo` - Minimize CGO calls, batch operations when required
- `adv-functional` - Use functional options pattern for config

---

## Detailed Rules

### 1. Error Handling (CRITICAL)

#### `err-wrap` - Wrap Errors with Context

Always wrap errors with additional context using `fmt.Errorf` with `%w` verb.

**Incorrect (loses context):**

```go
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, err  // No context about what operation failed
    }
    return user, nil
}
```

**Correct (adds context):**

```go
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

#### `err-once` - Handle Errors Only Once

Either log OR return an error, never both. This prevents duplicate log entries.

**Incorrect (handles twice):**

```go
func ProcessOrder(order Order) error {
    if err := validate(order); err != nil {
        log.Printf("validation failed: %v", err)  // Logged here
        return fmt.Errorf("process order: %w", err)  // AND returned
    }
    return nil
}
// Caller also logs, creating duplicate entries
```

**Correct (handle once):**

```go
func ProcessOrder(order Order) error {
    if err := validate(order); err != nil {
        return fmt.Errorf("process order: %w", err)  // Return only
    }
    return nil
}

// Top-level handler logs once:
func Handler(c *gin.Context) {
    if err := ProcessOrder(order); err != nil {
        log.Printf("handler error: %v", err)  // Single log point
        c.JSON(500, gin.H{"error": "processing failed"})
    }
}
```

#### `err-types` - Define Custom Error Types

Use custom error types for domain-specific errors that need programmatic handling.

**Correct:**

```go
// Define domain error types
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

// Usage
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err == sql.ErrNoRows {
        return nil, &NotFoundError{Resource: "user", ID: id}
    }
    if err != nil {
        return nil, fmt.Errorf("get user: %w", err)
    }
    return user, nil
}

// Caller can check type
var notFound *NotFoundError
if errors.As(err, &notFound) {
    c.JSON(404, gin.H{"error": notFound.Error()})
}
```

#### `err-sentinel` - Use Sentinel Errors

Define sentinel errors for expected conditions that callers need to check.

**Correct:**

```go
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrConflict     = errors.New("conflict")
)

func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err == sql.ErrNoRows {
        return nil, ErrNotFound
    }
    return user, err
}

// Caller
if errors.Is(err, ErrNotFound) {
    c.JSON(404, gin.H{"error": "user not found"})
    return
}
```

#### `err-context` - Add Operation Context

Include enough context to debug: operation name, relevant IDs, state info.

**Correct:**

```go
func TransferFunds(from, to string, amount decimal.Decimal) error {
    if err := debit(from, amount); err != nil {
        return fmt.Errorf("transfer %s from %s to %s: debit failed: %w",
            amount, from, to, err)
    }
    if err := credit(to, amount); err != nil {
        // Include compensating action info
        return fmt.Errorf("transfer %s from %s to %s: credit failed (debit succeeded, needs reversal): %w",
            amount, from, to, err)
    }
    return nil
}
```

#### `err-check` - Always Check Errors

Never ignore errors. If truly ignorable, document why.

**Incorrect:**

```go
json.Unmarshal(data, &user)  // Error ignored!
file.Close()                  // Error ignored!
_, _ = io.Copy(dst, src)     // Blank identifier abuse
```

**Correct:**

```go
if err := json.Unmarshal(data, &user); err != nil {
    return fmt.Errorf("unmarshal user: %w", err)
}

// For Close, use defer with named return
defer func() {
    if cerr := file.Close(); cerr != nil && err == nil {
        err = fmt.Errorf("close file: %w", cerr)
    }
}()

// If truly ignorable, document why
_ = conn.Close() // Best effort cleanup, connection already invalid
```

---

### 2. Concurrency (CRITICAL)

#### `conc-context` - Use Context for Cancellation

Pass context.Context as first parameter. Respect cancellation in long operations.

**Incorrect (no cancellation):**

```go
func FetchData(url string) ([]byte, error) {
    resp, err := http.Get(url)  // Can't be cancelled
    // ...
}
```

**Correct (respects context):**

```go
func FetchData(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, fmt.Errorf("create request: %w", err)
    }
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("fetch %s: %w", url, err)
    }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}
```

#### `conc-goroutine-leak` - Prevent Goroutine Leaks

Always ensure goroutines can exit. Use context cancellation or done channels.

**Incorrect (goroutine may leak):**

```go
func StartWorker() {
    go func() {
        for {
            result := slowOperation()  // Blocks forever if no work
            process(result)
        }
    }()
}
```

**Correct (respects cancellation):**

```go
func StartWorker(ctx context.Context) {
    go func() {
        for {
            select {
            case <-ctx.Done():
                return  // Clean exit
            default:
                result := slowOperation()
                select {
                case <-ctx.Done():
                    return
                default:
                    process(result)
                }
            }
        }
    }()
}
```

#### `conc-channel-close` - Close Channels from Sender

Only the sender should close a channel. Receivers should never close.

**Incorrect:**

```go
func worker(ch chan int) {
    for v := range ch {
        process(v)
    }
    close(ch)  // Receiver closing - dangerous!
}
```

**Correct:**

```go
func producer(ch chan<- int) {
    defer close(ch)  // Sender closes
    for i := 0; i < 10; i++ {
        ch <- i
    }
}

func consumer(ch <-chan int) {
    for v := range ch {  // Exits when channel closes
        process(v)
    }
}
```

#### `conc-mutex` - Prefer Mutex for Simple State

Use sync.Mutex for simple shared state. Channels are for communication, not synchronization.

**Correct:**

```go
type Counter struct {
    mu    sync.Mutex
    value int64
}

func (c *Counter) Increment() {
    c.mu.Lock()
    c.value++
    c.mu.Unlock()
}

func (c *Counter) Value() int64 {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}

// For high-contention counters, use atomic:
type AtomicCounter struct {
    value atomic.Int64
}

func (c *AtomicCounter) Increment() {
    c.value.Add(1)
}
```

#### `conc-waitgroup` - Use WaitGroup for Synchronization

Use sync.WaitGroup to wait for multiple goroutines to complete.

**Correct:**

```go
func ProcessItems(ctx context.Context, items []Item) error {
    var wg sync.WaitGroup
    errCh := make(chan error, len(items))

    for _, item := range items {
        wg.Add(1)
        go func(item Item) {
            defer wg.Done()
            if err := process(ctx, item); err != nil {
                errCh <- err
            }
        }(item)
    }

    wg.Wait()
    close(errCh)

    // Collect errors
    var errs []error
    for err := range errCh {
        errs = append(errs, err)
    }
    return errors.Join(errs...)
}
```

#### `conc-select` - Use Select for Non-blocking Operations

Use select with default case for non-blocking operations, or timeout for bounded waits.

**Correct:**

```go
// Non-blocking send
select {
case ch <- value:
    // Sent successfully
default:
    // Channel full, handle overflow
    log.Warn("channel full, dropping message")
}

// Timeout pattern
select {
case result := <-resultCh:
    return result, nil
case <-time.After(5 * time.Second):
    return nil, ErrTimeout
case <-ctx.Done():
    return nil, ctx.Err()
}
```

---

### 3. Uber fx DI (CRITICAL - MANDATORY)

#### `fx-provide` - All Dependencies via fx.Provide

**MANDATORY**: No manual instantiation in main(). All dependencies must go through fx.

**Incorrect (manual instantiation - FORBIDDEN):**

```go
func main() {
    cfg := config.Load()
    db := database.New(cfg)
    repo := repository.New(db)
    service := service.New(repo)
    handler := handler.New(service)
    // Manual wiring - forbidden!
}
```

**Correct (fx.Provide):**

```go
func main() {
    fx.New(
        fx.Provide(
            config.Load,
            database.New,
            repository.New,
            service.New,
            handler.New,
        ),
        fx.Invoke(startServer),
    ).Run()
}
```

#### `fx-module` - Group Providers into Modules

Create domain modules to organize related providers.

**Correct:**

```go
// internal/user/module.go
var Module = fx.Options(
    fx.Provide(
        NewRepository,
        NewService,
        NewHandler,
    ),
)

// internal/order/module.go
var Module = fx.Options(
    fx.Provide(
        NewRepository,
        NewService,
        NewHandler,
    ),
)

// cmd/server/main.go
func main() {
    fx.New(
        config.Module,
        database.Module,
        user.Module,
        order.Module,
        server.Module,
    ).Run()
}
```

#### `fx-lifecycle` - Use Lifecycle for Startup/Shutdown

Use fx.Lifecycle hooks for resources that need graceful startup/shutdown.

**Correct:**

```go
func NewHTTPServer(lc fx.Lifecycle, handler http.Handler, cfg *Config) *http.Server {
    srv := &http.Server{
        Addr:    cfg.Address,
        Handler: handler,
    }

    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            ln, err := net.Listen("tcp", srv.Addr)
            if err != nil {
                return err
            }
            go srv.Serve(ln)
            return nil
        },
        OnStop: func(ctx context.Context) error {
            return srv.Shutdown(ctx)
        },
    })

    return srv
}
```

#### `fx-invoke` - Use Invoke for Side Effects

Use fx.Invoke for operations that don't return values but need to run at startup.

**Correct:**

```go
func main() {
    fx.New(
        fx.Provide(
            NewConfig,
            NewLogger,
            NewDB,
            NewServer,
        ),
        fx.Invoke(
            RegisterRoutes,  // Side effect: registers routes
            RunMigrations,   // Side effect: runs DB migrations
        ),
    ).Run()
}

func RegisterRoutes(r *gin.Engine, h *Handler) {
    r.GET("/users", h.ListUsers)
    r.POST("/users", h.CreateUser)
}
```

#### `fx-decorate` - Use Decorate for Cross-cutting Concerns

Use fx.Decorate to wrap providers with middleware/logging/metrics.

**Correct:**

```go
var Module = fx.Options(
    fx.Provide(NewRepository),
    fx.Decorate(func(repo Repository, logger *zap.Logger) Repository {
        return &LoggingRepository{
            inner:  repo,
            logger: logger,
        }
    }),
)
```

#### `fx-test` - Use fxtest for Integration Testing

Use fxtest.New() for testing with fx dependency injection.

**Correct:**

```go
func TestUserService(t *testing.T) {
    var svc *UserService

    app := fxtest.New(t,
        fx.Provide(
            NewMockRepository,
            NewUserService,
        ),
        fx.Populate(&svc),
    )
    app.RequireStart()
    defer app.RequireStop()

    // Test service
    user, err := svc.GetUser(context.Background(), "123")
    require.NoError(t, err)
    require.Equal(t, "test", user.Name)
}
```

---

### 4. Gin Handlers (HIGH)

#### `gin-binding` - Use ShouldBind with Validation

Always use ShouldBind methods with validation tags.

**Incorrect (manual parsing):**

```go
func CreateUser(c *gin.Context) {
    var req map[string]interface{}
    json.NewDecoder(c.Request.Body).Decode(&req)
    // No validation, type unsafe
}
```

**Correct (binding with validation):**

```go
type CreateUserRequest struct {
    Email    string `json:"email" binding:"required,email"`
    Name     string `json:"name" binding:"required,min=2,max=100"`
    Age      int    `json:"age" binding:"gte=0,lte=150"`
    Password string `json:"password" binding:"required,min=8"`
}

func (h *Handler) CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, Response{Error: err.Error()})
        return
    }
    // Proceed with validated, typed data
}
```

#### `gin-response` - Consistent Response Format

Define and use consistent response wrapper types.

**Correct:**

```go
type Response struct {
    Success bool        `json:"success"`
    Data    interface{} `json:"data,omitempty"`
    Error   *ErrorInfo  `json:"error,omitempty"`
    Meta    *Meta       `json:"meta,omitempty"`
}

type ErrorInfo struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}

type Meta struct {
    Page       int `json:"page,omitempty"`
    PerPage    int `json:"per_page,omitempty"`
    TotalCount int `json:"total_count,omitempty"`
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, Response{Success: true, Data: data})
}

func SuccessWithMeta(c *gin.Context, data interface{}, meta Meta) {
    c.JSON(http.StatusOK, Response{Success: true, Data: data, Meta: &meta})
}

func Error(c *gin.Context, status int, code, message string) {
    c.JSON(status, Response{
        Success: false,
        Error:   &ErrorInfo{Code: code, Message: message},
    })
}
```

#### `gin-middleware` - Chain Middleware for Cross-cutting Concerns

Use middleware for logging, auth, recovery, CORS, etc.

**Correct:**

```go
func NewRouter(h *Handler, auth *AuthMiddleware, logger *LoggerMiddleware) *gin.Engine {
    r := gin.New()

    // Global middleware
    r.Use(gin.Recovery())
    r.Use(logger.Handler())
    r.Use(CORSMiddleware())

    // Public routes
    r.POST("/login", h.Login)
    r.POST("/register", h.Register)

    // Protected routes
    api := r.Group("/api", auth.RequireAuth())
    {
        api.GET("/users", h.ListUsers)
        api.POST("/users", h.CreateUser)
    }

    // Admin routes
    admin := r.Group("/admin", auth.RequireAuth(), auth.RequireRole("admin"))
    {
        admin.DELETE("/users/:id", h.DeleteUser)
    }

    return r
}
```

#### `gin-group` - Use RouterGroup for Organization

Group routes by version, feature, or access level.

**Correct:**

```go
func RegisterRoutes(r *gin.Engine, h *Handler) {
    // API v1
    v1 := r.Group("/api/v1")
    {
        users := v1.Group("/users")
        {
            users.GET("", h.ListUsers)
            users.GET("/:id", h.GetUser)
            users.POST("", h.CreateUser)
        }

        orders := v1.Group("/orders")
        {
            orders.GET("", h.ListOrders)
            orders.POST("", h.CreateOrder)
        }
    }

    // API v2 with breaking changes
    v2 := r.Group("/api/v2")
    {
        v2.GET("/users", h.ListUsersV2)
    }
}
```

#### `gin-error` - Centralized Error Handling

Use middleware for centralized error handling.

**Correct:**

```go
func ErrorHandlerMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err

            var notFound *NotFoundError
            var validation *ValidationError
            var unauthorized *UnauthorizedError

            switch {
            case errors.As(err, &notFound):
                c.JSON(http.StatusNotFound, Response{
                    Error: &ErrorInfo{Code: "NOT_FOUND", Message: err.Error()},
                })
            case errors.As(err, &validation):
                c.JSON(http.StatusBadRequest, Response{
                    Error: &ErrorInfo{Code: "VALIDATION_ERROR", Message: err.Error()},
                })
            case errors.As(err, &unauthorized):
                c.JSON(http.StatusUnauthorized, Response{
                    Error: &ErrorInfo{Code: "UNAUTHORIZED", Message: err.Error()},
                })
            default:
                c.JSON(http.StatusInternalServerError, Response{
                    Error: &ErrorInfo{Code: "INTERNAL_ERROR", Message: "internal server error"},
                })
            }
        }
    }
}
```

#### `gin-context` - Never Store gin.Context

Copy needed values from gin.Context. Don't store or pass it to goroutines.

**Incorrect:**

```go
func (h *Handler) ProcessAsync(c *gin.Context) {
    go func() {
        // DANGEROUS: c may be recycled by gin
        userID := c.GetString("user_id")
        h.process(c.Request.Context(), userID)
    }()
    c.JSON(200, gin.H{"status": "processing"})
}
```

**Correct:**

```go
func (h *Handler) ProcessAsync(c *gin.Context) {
    // Copy values before goroutine
    ctx := c.Request.Context()
    userID := c.GetString("user_id")

    go func() {
        h.process(ctx, userID)
    }()
    c.JSON(200, gin.H{"status": "processing"})
}
```

---

### 5. Performance (HIGH)

#### `perf-alloc` - Minimize Allocations in Hot Paths

Avoid allocations in frequently called code.

**Incorrect:**

```go
func ProcessRequest(data []byte) string {
    return string(data)  // Allocates new string every call
}
```

**Correct:**

```go
// Use unsafe conversion for read-only string (advanced)
func bytesToString(b []byte) string {
    return unsafe.String(unsafe.SliceData(b), len(b))
}

// Or reuse buffers
var bufPool = sync.Pool{
    New: func() interface{} { return new(bytes.Buffer) },
}

func ProcessRequest(data []byte) {
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)
    }()
    // Use buffer
}
```

#### `perf-pool` - Use sync.Pool for Frequent Allocations

Pool frequently allocated objects to reduce GC pressure.

**Correct:**

```go
var responsePool = sync.Pool{
    New: func() interface{} {
        return &Response{
            Headers: make(map[string]string, 10),
        }
    },
}

func HandleRequest(c *gin.Context) {
    resp := responsePool.Get().(*Response)
    defer func() {
        // Reset before returning to pool
        resp.Status = 0
        resp.Body = nil
        for k := range resp.Headers {
            delete(resp.Headers, k)
        }
        responsePool.Put(resp)
    }()

    // Use resp...
}
```

#### `perf-slice` - Preallocate Slices

Specify capacity when slice size is known or estimatable.

**Incorrect (grows dynamically):**

```go
var users []User
for _, id := range ids {
    user, _ := getUser(id)
    users = append(users, user)  // May reallocate multiple times
}
```

**Correct (preallocated):**

```go
users := make([]User, 0, len(ids))
for _, id := range ids {
    user, _ := getUser(id)
    users = append(users, user)  // No reallocation needed
}
```

#### `perf-map` - Preallocate Maps

Specify initial size for maps when known.

**Correct:**

```go
// Known size
userIndex := make(map[string]*User, len(users))
for _, u := range users {
    userIndex[u.ID] = u
}

// Estimated size
cache := make(map[string]interface{}, 1000)
```

#### `perf-string` - Use strings.Builder for Concatenation

Avoid `+` operator in loops. Use strings.Builder or bytes.Buffer.

**Incorrect:**

```go
var result string
for _, item := range items {
    result += item.Name + ", "  // O(n²) - creates new string each iteration
}
```

**Correct:**

```go
var sb strings.Builder
sb.Grow(len(items) * 20)  // Estimate capacity
for i, item := range items {
    if i > 0 {
        sb.WriteString(", ")
    }
    sb.WriteString(item.Name)
}
result := sb.String()
```

#### `perf-interface` - Avoid interface{} in Hot Paths

Use generics or concrete types. interface{} requires runtime type assertions.

**Incorrect:**

```go
func ProcessItems(items []interface{}) {
    for _, item := range items {
        u := item.(User)  // Runtime assertion, allocation
        process(u)
    }
}
```

**Correct (generics):**

```go
func ProcessItems[T any](items []T, process func(T)) {
    for _, item := range items {
        process(item)  // No type assertion needed
    }
}
```

---

### 6. Testing (MEDIUM)

#### `test-table` - Use Table-Driven Tests

Group related test cases in a table for coverage and maintainability.

**Correct:**

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "user@example.com", false},
        {"valid with subdomain", "user@sub.example.com", false},
        {"missing @", "userexample.com", true},
        {"missing domain", "user@", true},
        {"empty", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail(%q) error = %v, wantErr %v",
                    tt.email, err, tt.wantErr)
            }
        })
    }
}
```

#### `test-parallel` - Run Independent Tests in Parallel

Use t.Parallel() for tests that don't share state.

**Correct:**

```go
func TestUserService(t *testing.T) {
    t.Parallel()  // Mark test as parallel

    tests := []struct {
        name string
        // ...
    }{/*...*/}

    for _, tt := range tests {
        tt := tt  // Capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()  // Each subtest also parallel
            // Test logic
        })
    }
}
```

#### `test-mock` - Use Interfaces for Mockable Dependencies

Define interfaces at the point of use, not implementation.

**Correct:**

```go
// In service package - defines what it needs
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

type UserService struct {
    repo UserRepository
}

// In test
type mockUserRepo struct {
    findByIDFunc func(ctx context.Context, id string) (*User, error)
}

func (m *mockUserRepo) FindByID(ctx context.Context, id string) (*User, error) {
    return m.findByIDFunc(ctx, id)
}

func TestUserService_GetUser(t *testing.T) {
    mock := &mockUserRepo{
        findByIDFunc: func(ctx context.Context, id string) (*User, error) {
            return &User{ID: id, Name: "Test"}, nil
        },
    }
    svc := NewUserService(mock)
    // Test...
}
```

#### `test-fixture` - Use testdata/ for Test Fixtures

Store test data in testdata/ directory (ignored by Go tooling).

**Correct:**

```go
// testdata/users.json
// testdata/golden/response.json

func TestParseUsers(t *testing.T) {
    data, err := os.ReadFile("testdata/users.json")
    require.NoError(t, err)

    users, err := ParseUsers(data)
    require.NoError(t, err)
    require.Len(t, users, 3)
}
```

#### `test-benchmark` - Write Benchmarks for Critical Code

Benchmark performance-critical code with realistic data.

**Correct:**

```go
func BenchmarkParseJSON(b *testing.B) {
    data := []byte(`{"id":"123","name":"Test User","email":"test@example.com"}`)

    b.ResetTimer()
    b.ReportAllocs()

    for i := 0; i < b.N; i++ {
        var user User
        _ = json.Unmarshal(data, &user)
    }
}

// Run: go test -bench=. -benchmem
```

#### `test-golden` - Use Golden Files for Complex Output

Compare output against golden files for complex validation.

**Correct:**

```go
var update = flag.Bool("update", false, "update golden files")

func TestRenderTemplate(t *testing.T) {
    result := RenderTemplate(testData)

    goldenPath := "testdata/golden/template.html"

    if *update {
        os.WriteFile(goldenPath, []byte(result), 0644)
        return
    }

    expected, err := os.ReadFile(goldenPath)
    require.NoError(t, err)
    require.Equal(t, string(expected), result)
}

// Update golden files: go test -update
```

---

### 7. Code Style (MEDIUM)

#### `style-naming` - Follow Go Naming Conventions

Use MixedCaps, not snake_case. Acronyms should be consistent case.

**Correct:**

```go
// Exported names: MixedCaps starting with uppercase
type HTTPClient struct{}  // Not HttpClient
type JSONParser struct{}  // Not JsonParser
var userID string        // Not user_id

// Unexported: mixedCaps starting with lowercase
func parseJSON(data []byte) error {}
var maxRetryCount = 3

// Interfaces ending in -er for single-method
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

#### `style-receiver` - Consistent Receiver Names

Use short, consistent receiver names (1-2 chars). Never use `this` or `self`.

**Correct:**

```go
type UserService struct {
    repo Repository
}

func (s *UserService) GetUser(id string) (*User, error) {
    return s.repo.FindByID(id)
}

func (s *UserService) CreateUser(u *User) error {
    return s.repo.Save(u)
}

// Not: func (this *UserService) GetUser...
// Not: func (self *UserService) GetUser...
// Not: func (userService *UserService) GetUser...
```

#### `style-interface` - Accept Interfaces, Return Concrete

Accept interface parameters for flexibility. Return concrete types for clarity.

**Correct:**

```go
// Accept interface
func ProcessReader(r io.Reader) error {
    // Can accept *os.File, *bytes.Buffer, *strings.Reader, etc.
}

// Return concrete
func NewUserService(repo *UserRepository) *UserService {
    return &UserService{repo: repo}
}

// NOT: func NewUserService(repo Repository) Service
```

#### `style-package` - Short, Lowercase Package Names

Package names should be short, lowercase, no underscores.

**Correct:**

```go
package user     // Not: package userService, user_service
package httputil // Not: package http_util, httpUtil
package config   // Not: package configuration
```

#### `style-comment` - Document Exported Symbols

All exported symbols should have doc comments starting with the name.

**Correct:**

```go
// UserService handles user-related business logic.
type UserService struct {
    repo Repository
}

// GetUser retrieves a user by ID.
// It returns ErrNotFound if the user doesn't exist.
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    // ...
}

// ErrNotFound is returned when a requested resource doesn't exist.
var ErrNotFound = errors.New("not found")
```

#### `style-import` - Group Imports

Group imports: stdlib, external, internal. Use goimports for automatic formatting.

**Correct:**

```go
import (
    // Standard library
    "context"
    "fmt"
    "net/http"

    // External packages
    "github.com/gin-gonic/gin"
    "go.uber.org/fx"
    "go.uber.org/zap"

    // Internal packages
    "myapp/internal/user"
    "myapp/pkg/response"
)
```

---

### 8. Advanced Patterns (LOW)

#### `adv-generics` - Use Generics for Type-Safe Utilities

Use generics for collections, utilities, and type-safe code.

**Correct:**

```go
// Generic slice operations
func Filter[T any](slice []T, predicate func(T) bool) []T {
    result := make([]T, 0, len(slice))
    for _, v := range slice {
        if predicate(v) {
            result = append(result, v)
        }
    }
    return result
}

func Map[T, R any](slice []T, mapper func(T) R) []R {
    result := make([]R, len(slice))
    for i, v := range slice {
        result[i] = mapper(v)
    }
    return result
}

// Usage
adults := Filter(users, func(u User) bool { return u.Age >= 18 })
names := Map(users, func(u User) string { return u.Name })
```

#### `adv-embed` - Use Embedding for Composition

Prefer embedding over inheritance for code reuse.

**Correct:**

```go
type BaseRepository struct {
    db *sql.DB
}

func (r *BaseRepository) ExecContext(ctx context.Context, query string, args ...any) (sql.Result, error) {
    return r.db.ExecContext(ctx, query, args...)
}

// Embed BaseRepository
type UserRepository struct {
    BaseRepository  // Embedded - inherits all methods
}

func (r *UserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    // Can use r.ExecContext directly
}
```

#### `adv-reflect` - Avoid Reflect in Hot Paths

Reflect is slow. Use code generation or generics instead.

**Incorrect:**

```go
func SetField(obj interface{}, name string, value interface{}) {
    v := reflect.ValueOf(obj).Elem()
    f := v.FieldByName(name)
    f.Set(reflect.ValueOf(value))  // Slow!
}
```

**Correct:**

```go
// Use code generation (go generate) for struct operations
//go:generate go run gen.go

// Or use generics for type-safe operations
func SetField[T any](obj *T, setter func(*T, string)) {
    setter(obj, "value")
}
```

#### `adv-unsafe` - Avoid unsafe Except for FFI

Only use unsafe for FFI or proven optimizations with benchmarks.

**Acceptable use:**

```go
// Zero-allocation string to bytes (read-only)
func stringToBytes(s string) []byte {
    return unsafe.Slice(unsafe.StringData(s), len(s))
}

// Only use when benchmarks prove significant improvement
// and you understand the safety implications
```

#### `adv-cgo` - Minimize CGO Calls

CGO has significant overhead. Batch operations when possible.

**Correct:**

```go
// Bad: Many small CGO calls
for _, item := range items {
    C.process_item(item)  // CGO overhead per call
}

// Better: Batch into single CGO call
C.process_items((*C.Item)(unsafe.Pointer(&items[0])), C.int(len(items)))
```

#### `adv-functional` - Use Functional Options Pattern

Use functional options for flexible, extensible configuration.

**Correct:**

```go
type Server struct {
    host    string
    port    int
    timeout time.Duration
}

type Option func(*Server)

func WithHost(host string) Option {
    return func(s *Server) { s.host = host }
}

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(opts ...Option) *Server {
    s := &Server{
        host:    "localhost",
        port:    8080,
        timeout: 30 * time.Second,
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
srv := NewServer(
    WithHost("0.0.0.0"),
    WithPort(9000),
    WithTimeout(time.Minute),
)
```

---

## How to Use

Use rule prefixes for quick reference (e.g., `err-wrap`, `conc-context`, `fx-provide`).
All 48 rules are documented inline above with detailed code examples.

## fx Compliance Checklist

Before submitting any Go code:

- [ ] All dependencies wired through `fx.Provide`
- [ ] Each domain has its own `fx.Module` (var Module = fx.Options(...))
- [ ] `fx.Lifecycle` hooks used for OnStart/OnStop
- [ ] No manual instantiation in `main()`
- [ ] Tests use `fxtest.New()` for DI

## Integration Workflow

1. **New Service**: Create fx module → Add providers → Wire in main.go
2. **New Handler**: Add to existing module → Register routes via fx.Invoke
3. **Testing**: Use fxtest.New() → Provide mocks → Populate dependencies
4. **Code Review**: Run `go vet`, `staticcheck`, verify fx compliance

## References

- [Uber Go Style Guide](https://github.com/uber-go/guide)
- [Effective Go](https://go.dev/doc/effective_go)
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
- [Uber fx Documentation](https://uber-go.github.io/fx/)
- [Gin Web Framework](https://gin-gonic.com/docs/)
