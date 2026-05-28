# Patterns Cookbook

Recipes for common Go design patterns: functional options, dependency injection, error handling, and more.

---

## Functional Options

**Problem**: How to create flexible constructors with optional configuration?

**Solution**:
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
server := NewServer(
    WithHost("0.0.0.0"),
    WithPort(9000),
)
```

**Tip**: Set sensible defaults in the constructor. Options only override what's explicitly set.

---

## Functional Options with Validation

**Problem**: How to validate option values and return configuration errors?

**Solution**:
```go
type Option func(*Config) error

func WithPort(port int) Option {
    return func(c *Config) error {
        if port < 1 || port > 65535 {
            return fmt.Errorf("invalid port: %d", port)
        }
        c.port = port
        return nil
    }
}

func NewConfig(opts ...Option) (*Config, error) {
    c := &Config{port: 8080}
    for _, opt := range opts {
        if err := opt(c); err != nil {
            return nil, err
        }
    }
    return c, nil
}
```

**Tip**: Return errors from options for validation. This catches misconfigurations at startup.

---

## Constructor Injection

**Problem**: How to make code testable by injecting dependencies?

**Solution**:
```go
type UserService struct {
    repo   UserRepository
    logger *slog.Logger
}

func NewUserService(repo UserRepository, logger *slog.Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}

// Interface for testing
type UserRepository interface {
    Get(id string) (*User, error)
    Save(user *User) error
}
```

**Tip**: Accept interfaces, return structs. Interfaces should be defined by the consumer, not the provider.

---

## Dependency Injection with uber-go/fx

**Problem**: How to wire up complex dependency graphs automatically?

**Solution**:
```go
import "go.uber.org/fx"

func main() {
    fx.New(
        fx.Provide(
            NewConfig,
            NewLogger,
            NewDatabase,
            NewUserRepository,
            NewUserService,
            NewHTTPServer,
        ),
        fx.Invoke(func(server *HTTPServer) {
            // Server starts automatically
        }),
    ).Run()
}

// Constructors receive dependencies automatically
func NewUserService(repo *UserRepository, log *zap.Logger) *UserService {
    return &UserService{repo: repo, logger: log}
}
```

**Tip**: fx resolves dependencies by type. Use `fx.Annotate` with tags for multiple implementations of same type.

---

## fx Lifecycle Hooks

**Problem**: How to manage startup and shutdown of resources in fx?

**Solution**:
```go
func NewDatabase(lc fx.Lifecycle) *sql.DB {
    db := connectDB()

    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            return db.PingContext(ctx)
        },
        OnStop: func(ctx context.Context) error {
            return db.Close()
        },
    })

    return db
}
```

**Tip**: OnStart hooks run in dependency order; OnStop hooks run in reverse order.

---

## Error Wrapping

**Problem**: How to add context to errors while preserving the original error?

**Solution**:
```go
func LoadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading config %s: %w", path, err)
    }

    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, fmt.Errorf("parsing config: %w", err)
    }

    return &cfg, nil
}
```

**Tip**: Use `%w` verb to wrap errors. This allows `errors.Is` and `errors.As` to inspect the chain.

---

## Sentinel Errors

**Problem**: How to define and check for specific error conditions?

**Solution**:
```go
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)

func GetUser(id string) (*User, error) {
    user := db.Find(id)
    if user == nil {
        return nil, ErrNotFound
    }
    return user, nil
}

// Check sentinel
if errors.Is(err, ErrNotFound) {
    http.Error(w, "user not found", http.StatusNotFound)
}
```

**Tip**: Sentinel errors are package-level variables. Export them for callers to check against.

---

## Custom Error Types

**Problem**: How to include structured data in errors for programmatic handling?

**Solution**:
```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}

func Validate(u *User) error {
    if u.Email == "" {
        return &ValidationError{Field: "email", Message: "required"}
    }
    return nil
}

// Extract error data
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Printf("field %s: %s\n", valErr.Field, valErr.Message)
}
```

**Tip**: Use `errors.As` to extract typed errors from wrapped chains.

---

## Multiple Errors with multierr

**Problem**: How to collect and return multiple errors from a batch operation?

**Solution**:
```go
import "go.uber.org/multierr"

func validateAll(items []Item) error {
    var errs error
    for _, item := range items {
        if err := validate(item); err != nil {
            errs = multierr.Append(errs, err)
        }
    }
    return errs
}

// Inspect individual errors
if errs := validateAll(items); errs != nil {
    for _, err := range multierr.Errors(errs) {
        log.Println(err)
    }
}
```

**Tip**: `multierr.Append` returns nil if both arguments are nil - safe for accumulation loops.

---

## Small Interfaces

**Problem**: How to design interfaces that are easy to implement and mock?

**Solution**:
```go
// Good: small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Compose when needed
type ReadWriter interface {
    Reader
    Writer
}
```

**Tip**: The bigger the interface, the weaker the abstraction. Prefer 1-2 methods per interface.

---

## Interface Segregation

**Problem**: How to avoid forcing implementations to provide unused methods?

**Solution**:
```go
// Instead of one large interface
type UserService interface {
    Get(id string) (*User, error)
    Create(u *User) error
    Update(u *User) error
    Delete(id string) error
}

// Split by use case
type UserGetter interface {
    Get(id string) (*User, error)
}

type UserCreator interface {
    Create(u *User) error
}

// Components depend only on what they need
func NewHandler(getter UserGetter) *Handler {
    return &Handler{users: getter}
}
```

**Tip**: Define interfaces where they're used (consumer side), not where they're implemented.

---

## Builder Pattern

**Problem**: How to construct complex objects step-by-step with a fluent API?

**Solution**:
```go
type RequestBuilder struct {
    method  string
    url     string
    headers map[string]string
    body    io.Reader
}

func NewRequest() *RequestBuilder {
    return &RequestBuilder{
        method:  "GET",
        headers: make(map[string]string),
    }
}

func (b *RequestBuilder) Method(m string) *RequestBuilder {
    b.method = m
    return b
}

func (b *RequestBuilder) URL(u string) *RequestBuilder {
    b.url = u
    return b
}

func (b *RequestBuilder) Header(k, v string) *RequestBuilder {
    b.headers[k] = v
    return b
}

func (b *RequestBuilder) Build() (*http.Request, error) {
    req, err := http.NewRequest(b.method, b.url, b.body)
    if err != nil {
        return nil, err
    }
    for k, v := range b.headers {
        req.Header.Set(k, v)
    }
    return req, nil
}

// Usage
req, _ := NewRequest().
    Method("POST").
    URL("https://api.example.com").
    Header("Content-Type", "application/json").
    Build()
```

**Tip**: Return `*Builder` from each method for chaining. Put validation in `Build()`.

---

## Repository Pattern

**Problem**: How to abstract data access behind a clean interface?

**Solution**:
```go
type UserRepository interface {
    Get(ctx context.Context, id string) (*User, error)
    List(ctx context.Context, filter UserFilter) ([]*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
}

type postgresUserRepo struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) UserRepository {
    return &postgresUserRepo{db: db}
}

func (r *postgresUserRepo) Get(ctx context.Context, id string) (*User, error) {
    var user User
    err := r.db.QueryRowContext(ctx,
        "SELECT id, name, email FROM users WHERE id = $1", id,
    ).Scan(&user.ID, &user.Name, &user.Email)
    if err == sql.ErrNoRows {
        return nil, ErrNotFound
    }
    return &user, err
}
```

**Tip**: Always accept `context.Context` as first parameter. Convert DB errors to domain errors.

---

## HTTP Middleware

**Problem**: How to add cross-cutting concerns (logging, auth, recovery) to HTTP handlers?

**Solution**:
```go
type Middleware func(http.Handler) http.Handler

func Logging(logger *slog.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            next.ServeHTTP(w, r)
            logger.Info("request",
                "method", r.Method,
                "path", r.URL.Path,
                "duration", time.Since(start),
            )
        })
    }
}

func Recovery() Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            defer func() {
                if err := recover(); err != nil {
                    w.WriteHeader(http.StatusInternalServerError)
                }
            }()
            next.ServeHTTP(w, r)
        })
    }
}

// Chain middleware
func Chain(h http.Handler, mw ...Middleware) http.Handler {
    for i := len(mw) - 1; i >= 0; i-- {
        h = mw[i](h)
    }
    return h
}

// Usage
handler := Chain(myHandler, Logging(logger), Recovery())
```

**Tip**: Middleware wraps in reverse order - first in list runs first.

---

## Graceful Shutdown

**Problem**: How to stop a server cleanly, finishing in-flight requests?

**Solution**:
```go
func main() {
    server := &http.Server{Addr: ":8080", Handler: router}

    go func() {
        if err := server.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatal(err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Fatal("shutdown error:", err)
    }
    log.Println("server stopped")
}
```

**Tip**: `Shutdown` stops accepting new connections and waits for existing ones to complete.
