# Go Services

## Patterns


---
  #### **Name**
Error Wrapping with Context
  #### **Description**
Add context to errors without losing the original
  #### **When**
Functions that call other functions, especially across packages
  #### **Example**
    # ERROR WRAPPING:
    
    """
    Go 1.13+ error wrapping - ALWAYS wrap errors with context
    """
    
    import (
        "errors"
        "fmt"
    )
    
    // WRONG: Error loses context
    func getUser(id string) (*User, error) {
        user, err := db.Query(id)
        if err != nil {
            return nil, err  // Where did this happen? Who knows.
        }
        return user, nil
    }
    
    // RIGHT: Error has context chain
    func getUser(id string) (*User, error) {
        user, err := db.Query(id)
        if err != nil {
            return nil, fmt.Errorf("getUser(%s): %w", id, err)
        }
        return user, nil
    }
    
    // Checking wrapped errors
    if errors.Is(err, sql.ErrNoRows) {
        // Handle not found
    }
    
    var dbErr *DatabaseError
    if errors.As(err, &dbErr) {
        // Handle database-specific error
    }
    

---
  #### **Name**
Graceful Shutdown
  #### **Description**
Clean shutdown that finishes in-flight requests
  #### **When**
Any HTTP server or long-running service
  #### **Example**
    # GRACEFUL SHUTDOWN:
    
    """
    Never os.Exit() in production. Always graceful shutdown.
    """
    
    func main() {
        srv := &http.Server{
            Addr:    ":8080",
            Handler: router,
        }
    
        // Start server in goroutine
        go func() {
            if err := srv.ListenAndServe(); err != http.ErrServerClosed {
                log.Fatalf("server error: %v", err)
            }
        }()
    
        // Wait for interrupt signal
        quit := make(chan os.Signal, 1)
        signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
        <-quit
    
        log.Println("Shutting down...")
    
        // Give outstanding requests 30 seconds to complete
        ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()
    
        if err := srv.Shutdown(ctx); err != nil {
            log.Fatalf("forced shutdown: %v", err)
        }
    
        log.Println("Server stopped")
    }
    

---
  #### **Name**
Functional Options Pattern
  #### **Description**
Clean API for configurable constructors
  #### **When**
Types with many optional configuration parameters
  #### **Example**
    # FUNCTIONAL OPTIONS:
    
    """
    Replace NewServer(a, b, c, d, e, f) with clean options
    """
    
    type Server struct {
        host    string
        port    int
        timeout time.Duration
        logger  *slog.Logger
    }
    
    type Option func(*Server)
    
    func WithHost(host string) Option {
        return func(s *Server) {
            s.host = host
        }
    }
    
    func WithPort(port int) Option {
        return func(s *Server) {
            s.port = port
        }
    }
    
    func WithTimeout(d time.Duration) Option {
        return func(s *Server) {
            s.timeout = d
        }
    }
    
    func NewServer(opts ...Option) *Server {
        // Sensible defaults
        s := &Server{
            host:    "localhost",
            port:    8080,
            timeout: 30 * time.Second,
            logger:  slog.Default(),
        }
    
        // Apply options
        for _, opt := range opts {
            opt(s)
        }
    
        return s
    }
    
    // Usage - clean and self-documenting
    srv := NewServer(
        WithHost("0.0.0.0"),
        WithPort(3000),
        WithTimeout(1*time.Minute),
    )
    

---
  #### **Name**
Context-First Function Signatures
  #### **Description**
Always pass context as first parameter
  #### **When**
Any function that does I/O, makes network calls, or could be cancelled
  #### **Example**
    # CONTEXT PROPAGATION:
    
    """
    Context carries deadlines, cancellation, and request-scoped values
    """
    
    // WRONG: No context = can't cancel, no deadlines
    func FetchUser(id string) (*User, error)
    
    // RIGHT: Context enables cancellation and timeouts
    func FetchUser(ctx context.Context, id string) (*User, error) {
        req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
        if err != nil {
            return nil, err
        }
    
        resp, err := client.Do(req)
        if err != nil {
            return nil, err
        }
        // ...
    }
    
    // Using context for timeouts
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    user, err := FetchUser(ctx, "123")
    if errors.Is(err, context.DeadlineExceeded) {
        // Handle timeout
    }
    

---
  #### **Name**
Table-Driven Tests
  #### **Description**
Organize test cases in a slice of structs
  #### **When**
Testing functions with multiple input/output combinations
  #### **Example**
    # TABLE-DRIVEN TESTS:
    
    """
    Go idiom for comprehensive, readable tests
    """
    
    func TestParseEmail(t *testing.T) {
        tests := []struct {
            name    string
            input   string
            want    string
            wantErr bool
        }{
            {
                name:  "valid email",
                input: "user@example.com",
                want:  "user@example.com",
            },
            {
                name:    "missing @",
                input:   "userexample.com",
                wantErr: true,
            },
            {
                name:    "empty string",
                input:   "",
                wantErr: true,
            },
            {
                name:  "with plus addressing",
                input: "user+tag@example.com",
                want:  "user+tag@example.com",
            },
        }
    
        for _, tt := range tests {
            t.Run(tt.name, func(t *testing.T) {
                got, err := ParseEmail(tt.input)
    
                if tt.wantErr {
                    if err == nil {
                        t.Errorf("ParseEmail(%q) expected error", tt.input)
                    }
                    return
                }
    
                if err != nil {
                    t.Errorf("ParseEmail(%q) unexpected error: %v", tt.input, err)
                }
    
                if got != tt.want {
                    t.Errorf("ParseEmail(%q) = %q, want %q", tt.input, got, tt.want)
                }
            })
        }
    }
    

---
  #### **Name**
Accept Interfaces, Return Structs
  #### **Description**
Depend on behavior, provide concrete types
  #### **When**
Designing package APIs and function signatures
  #### **Example**
    # INTERFACE DESIGN:
    
    """
    Accept the smallest interface you need.
    Return concrete types - let callers decide the interface.
    """
    
    // WRONG: Accepting concrete type limits flexibility
    func Process(file *os.File) error
    
    // RIGHT: Accept interface - works with any io.Reader
    func Process(r io.Reader) error {
        data, err := io.ReadAll(r)
        // ...
    }
    
    // WRONG: Returning interface hides useful methods
    func NewUserService() UserServiceInterface
    
    // RIGHT: Return struct - caller can use interface if needed
    func NewUserService() *UserService
    
    // Small interfaces are powerful
    type Writer interface {
        Write([]byte) (int, error)
    }
    
    type Reader interface {
        Read([]byte) (int, error)
    }
    
    // Compose interfaces when needed
    type ReadWriter interface {
        Reader
        Writer
    }
    

## Anti-Patterns


---
  #### **Name**
Empty Error Check
  #### **Description**
Checking error but doing nothing with it
  #### **Why**
    Ignored errors lead to silent failures. The bug that takes you
    three days to find is always a swallowed error. Go makes errors
    explicit for a reason - don't undermine it.
    
  #### **Instead**
    Handle every error. If you truly don't care (rare), use blank
    identifier with a comment explaining why:
    
    // Deliberately ignoring close error - best effort cleanup
    _ = file.Close()
    

---
  #### **Name**
Naked Returns in Long Functions
  #### **Description**
Using named return values without explicit returns
  #### **Why**
    Named returns are useful for documentation and defer patterns, but
    naked returns (just "return" with no values) in long functions make
    code hard to follow. You have to scan the whole function to know
    what's being returned.
    
  #### **Instead**
    Use naked returns only in short functions (< 10 lines) or for
    defer error handling. In long functions, return explicitly:
    
    return result, nil  // Clear what's returned
    

---
  #### **Name**
Package-Level Variables for Dependencies
  #### **Description**
Using global variables for database connections, clients, etc.
  #### **Why**
    Makes testing impossible without complex setup. Creates hidden
    dependencies. Race conditions if accessed from multiple goroutines.
    
  #### **Instead**
    Inject dependencies through constructors or methods:
    
    type UserService struct {
        db *sql.DB
        cache *redis.Client
    }
    
    func NewUserService(db *sql.DB, cache *redis.Client) *UserService {
        return &UserService{db: db, cache: cache}
    }
    

---
  #### **Name**
Overusing Channels
  #### **Description**
Using channels when mutex or atomic would be simpler
  #### **Why**
    Channels have overhead. Not every concurrency problem needs channels.
    A simple mutex is often clearer and faster for protecting shared state.
    
  #### **Instead**
    Use channels for: communication, signaling, pipelines
    Use mutex for: protecting shared state
    Use atomic for: counters, flags
    
    // Simple counter - use atomic
    var count atomic.Int64
    count.Add(1)
    
    // Shared map - use mutex
    var mu sync.RWMutex
    mu.Lock()
    cache[key] = value
    mu.Unlock()
    

---
  #### **Name**
Giant Interfaces
  #### **Description**
Interfaces with 10+ methods
  #### **Why**
    Large interfaces can't be satisfied easily. Hard to mock for tests.
    Forces implementations to provide everything even if they don't need it.
    The bigger the interface, the weaker the abstraction.
    
  #### **Instead**
    Small interfaces that describe behavior:
    
    // WRONG
    type UserManager interface {
        Create(u User) error
        Update(u User) error
        Delete(id string) error
        Get(id string) (*User, error)
        List() ([]User, error)
        // ... 15 more methods
    }
    
    // RIGHT - one method interfaces composed as needed
    type UserReader interface {
        GetUser(id string) (*User, error)
    }
    
    type UserWriter interface {
        SaveUser(u User) error
    }
    