# Go Idioms: When to Stop Translating from Java

Java-to-Go translation helps you get started. But good Go code isn't "Java translated to Go" - it's idiomatic Go. This reference covers patterns where you should stop thinking in Java.

## 1. Errors Are Values, Not Exceptions

### Java Mindset
```java
public User findById(String id) {
    return repository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
}

// somewhere else, maybe, if someone remembers
try {
    User user = service.findById(id);
} catch (UserNotFoundException e) {
    // handle
}
```

### Bad Go (Java Mentality)
```go
func (s *UserService) FindByID(id string) *User {
    user, err := s.repo.FindByID(id)
    if err != nil {
        panic(err)  // simulating exceptions
    }
    return user
}

// caller hopes nothing panics
user := service.FindByID(id)
```

### Good Go
```go
func (s *UserService) FindByID(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("finding user %s: %w", id, err)
    }
    return user, nil
}

// caller MUST handle
user, err := service.FindByID(ctx, id)
if err != nil {
    if errors.Is(err, ErrNotFound) {
        return nil, ErrUserNotFound
    }
    return nil, err
}
```

**Why:** Errors are explicit, traceable, and can't be ignored. Panic is for truly unrecoverable situations (programming bugs), not business logic.

## 2. No Constructors - Use Factory Functions

### Java Mindset
```java
public class UserService {
    private final UserRepository repo;
    private final Cache cache;

    public UserService(UserRepository repo, Cache cache) {
        this.repo = Objects.requireNonNull(repo);
        this.cache = Objects.requireNonNull(cache);
    }
}
```

### Good Go
```go
type UserService struct {
    repo  UserRepository
    cache *Cache
}

func NewUserService(repo UserRepository, cache *Cache) *UserService {
    if repo == nil {
        panic("repo cannot be nil")  // programmer error, panic is ok
    }
    return &UserService{
        repo:  repo,
        cache: cache,
    }
}
```

**Why:** `NewXxx` is the convention. Return concrete type, accept interfaces. Zero values should be usable when possible.

## 3. Table-Driven Tests

### Java Mindset
```java
@Test
void testAdd_positiveNumbers() {
    assertEquals(5, calculator.add(2, 3));
}

@Test
void testAdd_negativeNumbers() {
    assertEquals(-5, calculator.add(-2, -3));
}

@Test
void testAdd_zero() {
    assertEquals(2, calculator.add(2, 0));
}
```

### Good Go
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"with zero", 2, 0, 2},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

**Why:** Adding test cases is adding data, not code. Each case runs as a subtest with its name.

## 4. Context for Cancellation and Deadlines

### Java Mindset
```java
// pass timeout to each layer
public User findById(String id, Duration timeout) {
    return repo.findById(id, timeout);
}

// or use framework magic
@Timeout(5000)
public User findById(String id) { ... }
```

### Good Go
```go
func (s *UserService) FindByID(ctx context.Context, id string) (*User, error) {
    // ctx carries deadline, cancellation, and request-scoped values
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, err
    }
    return user, nil
}

// caller controls timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

user, err := service.FindByID(ctx, id)
if err != nil {
    if errors.Is(err, context.DeadlineExceeded) {
        // handle timeout
    }
}
```

**Why:** Context is the standard way to propagate cancellation. First parameter by convention. Always pass it through.

## 5. Defer for Cleanup

### Java Mindset
```java
try (var conn = dataSource.getConnection()) {
    // use connection
}  // auto-closed

// or manual
Connection conn = null;
try {
    conn = dataSource.getConnection();
    // use connection
} finally {
    if (conn != null) conn.close();
}
```

### Good Go
```go
conn, err := db.Conn(ctx)
if err != nil {
    return err
}
defer conn.Close()  // runs when function returns

// use connection
```

**Why:** `defer` is cleaner than try-finally, runs in LIFO order, and works for any cleanup (not just AutoCloseable).

## 6. Zero Values Are Useful

### Java Mindset
```java
public class Counter {
    private int count = 0;  // explicit initialization

    public Counter() {
        this.count = 0;  // redundant but "safe"
    }
}
```

### Good Go
```go
type Counter struct {
    count int  // zero value is 0
}

// no constructor needed for default state
var c Counter  // c.count is 0, ready to use
c.count++
```

**Why:** Go's zero values are intentional defaults. `int` is 0, `string` is "", `bool` is false, pointers/slices/maps are nil. Design types to be useful at zero value.

## 7. Accept Interfaces, Return Structs

### Java Mindset
```java
// return interfaces to hide implementation
public interface UserService {
    User findById(String id);
}

public class UserServiceImpl implements UserService {
    // ...
}
```

### Good Go
```go
// accept interface (what you need)
type UserFinder interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

func ProcessUser(finder UserFinder, id string) error {
    user, err := finder.FindByID(context.Background(), id)
    // ...
}

// return concrete type (what you provide)
func NewUserService(repo *UserRepository) *UserService {
    return &UserService{repo: repo}
}
```

**Why:** Callers define the interfaces they need. Implementations return concrete types so callers know exactly what they get.

## 8. Don't Use Getters and Setters

### Java Mindset
```java
public class User {
    private String email;

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

### Good Go
```go
type User struct {
    Email string  // direct access
}

user.Email = "test@example.com"
fmt.Println(user.Email)
```

**Why:** If the field is exported (capitalized), access it directly. Getters/setters are only for computed values or when you need side effects.

## 9. Embed for Composition, Not Inheritance

### Java Mindset
```java
public class LoggingUserService extends UserService {
    @Override
    public User findById(String id) {
        log.info("Finding user {}", id);
        return super.findById(id);
    }
}
```

### Good Go
```go
type LoggingUserService struct {
    *UserService  // embedded
    logger *slog.Logger
}

func (s *LoggingUserService) FindByID(ctx context.Context, id string) (*User, error) {
    s.logger.Info("finding user", "id", id)
    return s.UserService.FindByID(ctx, id)  // delegate
}
```

**Why:** Embedding promotes methods to the outer type. It's composition, not inheritance - the embedded type doesn't know it's embedded.

## 10. Use Channels for Communication, Mutexes for State

### Java Mindset
```java
// use synchronized/locks everywhere
private final Lock lock = new ReentrantLock();

public void process() {
    lock.lock();
    try {
        // do work
    } finally {
        lock.unlock();
    }
}
```

### Good Go
```go
// for shared state, mutex is fine
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

// for communication between goroutines, use channels
func worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        results <- process(job)
    }
}
```

**Why:** "Don't communicate by sharing memory; share memory by communicating." Channels make concurrent code clearer.

## 11. Package by Feature, Not Layer

### Java Mindset
```
com.company.app/
    controller/
        UserController.java
        OrderController.java
    service/
        UserService.java
        OrderService.java
    repository/
        UserRepository.java
        OrderRepository.java
```

### Good Go
```
app/
    user/
        handler.go
        service.go
        repository.go
    order/
        handler.go
        service.go
        repository.go
    internal/
        database/
            postgres.go
```

**Why:** Related code lives together. Changing user logic touches one directory. Internal packages hide implementation details.

## 12. Functional Options for Optional Configuration

### Java Mindset
```java
// builder pattern
Server server = Server.builder()
    .port(8080)
    .timeout(Duration.ofSeconds(30))
    .maxConnections(100)
    .build();
```

### Good Go
```go
type Option func(*Server)

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
    s := &Server{
        port:    8080,  // defaults
        timeout: 30 * time.Second,
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// usage
server := NewServer(
    WithPort(9000),
    WithTimeout(time.Minute),
)
```

**Why:** Functional options allow extensible, readable configuration without a separate builder type.

---

## The Mindset Shift

**Phase 1 (Understanding):** "How would I do this in Java? What's the Go equivalent?"

**Phase 2 (Fluency):** "What's the idiomatic Go way to solve this?"

**Phase 3 (Mastery):** You stop thinking about Java at all when writing Go.

The goal isn't to like Go more than Java. It's to write good Go when you need to write Go.
