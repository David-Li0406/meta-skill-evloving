# Exercise 00d: Simplicity and Explicitness

**Time:** 15 minutes
**Goal:** Understand Go's philosophy of simple, explicit code

## The Java Pattern

Spring Boot embraces convention and "magic":

```java
@Service
@Transactional
public class UserService {

    @Autowired
    private UserRepository repo;

    @Cacheable("users")
    @Async
    public CompletableFuture<User> findById(String id) {
        return CompletableFuture.completedFuture(repo.findById(id));
    }
}
```

What's happening?
- `@Service` - registers as bean
- `@Autowired` - injects dependency
- `@Transactional` - wraps in transaction
- `@Cacheable` - adds caching layer
- `@Async` - runs in thread pool

Powerful, but invisible.

## The Go Way

Go prefers explicit, visible code:

```go
type UserService struct {
    repo  UserRepository
    cache *Cache
}

func NewUserService(repo UserRepository, cache *Cache) *UserService {
    return &UserService{repo: repo, cache: cache}
}

func (s *UserService) FindByID(ctx context.Context, id string) (*User, error) {
    // explicit caching
    if user, ok := s.cache.Get(id); ok {
        return user, nil
    }

    // explicit database call
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, err
    }

    // explicit cache update
    s.cache.Set(id, user)
    return user, nil
}
```

More code, but you can read exactly what happens.

## YAGNI: You Aren't Gonna Need It

Java encourages anticipating future needs:

```java
// "we might need multiple payment providers someday"
public interface PaymentProcessor { void process(Payment p); }
public interface PaymentValidator { boolean validate(Payment p); }
public interface PaymentNotifier { void notify(Payment p); }
public class PaymentProcessorFactory { ... }
public class PaymentServiceImpl implements PaymentProcessor { ... }
```

Go encourages building what you need now:

```go
func ProcessPayment(ctx context.Context, payment *Payment) error {
    if payment.Amount <= 0 {
        return errors.New("invalid amount")
    }

    if err := chargeStripe(ctx, payment); err != nil {
        return fmt.Errorf("charging payment: %w", err)
    }

    return nil
}
```

Extract abstractions when you have concrete need, not in anticipation.

## Your Task

Refactor this over-engineered Go code to be simpler:

```go
// over-engineered
type NotificationService interface {
    Send(ctx context.Context, notification *Notification) error
}

type NotificationServiceImpl struct {
    sender NotificationSender
    logger NotificationLogger
    metrics NotificationMetrics
}

func NewNotificationServiceImpl(
    sender NotificationSender,
    logger NotificationLogger,
    metrics NotificationMetrics,
) NotificationService {
    return &NotificationServiceImpl{
        sender: sender,
        logger: logger,
        metrics: metrics,
    }
}

func (s *NotificationServiceImpl) Send(ctx context.Context, n *Notification) error {
    s.logger.LogNotification(n)
    s.metrics.IncrementSent()
    return s.sender.SendNotification(ctx, n)
}
```

---

## Step by Step

### 1. Question the abstractions (3 min)

Ask yourself:
- Do I have multiple NotificationService implementations? (Probably not)
- Do I need separate Logger and Metrics interfaces? (Probably not)
- Is `Impl` suffix adding value? (No)

### 2. Simplify to concrete implementation (5 min)

```go
type NotificationService struct {
    client *http.Client
    apiURL string
    logger *slog.Logger
}

func NewNotificationService(apiURL string, logger *slog.Logger) *NotificationService {
    return &NotificationService{
        client: &http.Client{Timeout: 10 * time.Second},
        apiURL: apiURL,
        logger: logger,
    }
}

func (s *NotificationService) Send(ctx context.Context, n *Notification) error {
    s.logger.Info("sending notification", "to", n.To, "type", n.Type)

    body, err := json.Marshal(n)
    if err != nil {
        return fmt.Errorf("marshaling notification: %w", err)
    }

    req, err := http.NewRequestWithContext(ctx, "POST", s.apiURL, bytes.NewReader(body))
    if err != nil {
        return fmt.Errorf("creating request: %w", err)
    }

    resp, err := s.client.Do(req)
    if err != nil {
        return fmt.Errorf("sending notification: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("notification failed: status %d", resp.StatusCode)
    }

    return nil
}
```

### 3. Add interface only where needed (5 min)

```go
// define interface at the CONSUMER, not provider
// e.g., in the test file or in a package that needs to mock

type NotificationSender interface {
    Send(ctx context.Context, n *Notification) error
}

// NotificationService already satisfies this - no changes needed
```

## Standard Library First

Before adding dependencies, check if stdlib can do it:

| Need | Stdlib Solution |
|------|-----------------|
| HTTP client | `net/http` |
| JSON | `encoding/json` |
| Logging | `log/slog` (Go 1.21+) |
| Testing | `testing` |
| HTTP testing | `net/http/httptest` |
| Context | `context` |
| Time | `time` |
| Crypto | `crypto/*` |
| SQL | `database/sql` |

## Explicit Wiring

Instead of dependency injection frameworks:

```go
func main() {
    // load config
    cfg := loadConfig()

    // create dependencies (explicit, visible)
    db, err := sql.Open("postgres", cfg.DatabaseURL)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

    // wire services
    userRepo := NewUserRepository(db)
    userService := NewUserService(userRepo)
    userHandler := NewUserHandler(userService, logger)

    // setup routes
    r := chi.NewRouter()
    r.Get("/users/{id}", userHandler.GetUser)

    // start server
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

You can see exactly what depends on what.

## The Rule of Three

Don't abstract until you have three concrete examples:

1. First time: just write the code
2. Second time: maybe copy with slight changes
3. Third time: now consider extracting a common pattern

This prevents premature abstraction.

## What Just Happened?

| Java/Spring | Go |
|-------------|-----|
| Convention over configuration | Explicit configuration |
| Framework magic | Visible code |
| Interface for everything | Interface when needed |
| DI container | Manual wiring in main() |
| Anticipate future needs | YAGNI |

## The Mental Shift

**Java thinking:** "I'll create interfaces and abstractions so we can extend later."

**Go thinking:** "I'll write the simplest code that works. I can refactor when I need to."

Less abstraction means:
- Easier to read
- Easier to debug
- Easier for new team members
- Faster to change when requirements actually change

## Checkpoint

- [ ] I can resist the urge to create interfaces "just in case"
- [ ] I understand why explicit code has value
- [ ] I can wire dependencies manually in main()
- [ ] I accept that more code doesn't mean worse code

**Next:** Exercise 01 - First Endpoint
