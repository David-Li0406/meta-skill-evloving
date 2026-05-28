# Go Philosophy for Java Developers

Go's design philosophy explained for developers coming from Spring Boot's framework-heavy approach.

---

## The Core Difference

**Java/Spring:** Solve complexity with abstraction, frameworks, and patterns.

**Go:** Solve complexity by removing it. Prefer boring, obvious code.

---

## Principle 1: Composition Over Inheritance (For Real This Time)

Java says "favor composition over inheritance." Go enforces it - there's no inheritance.

### Java Pattern

```java
// inheritance hierarchy
public abstract class Animal {
    public abstract void speak();
}

public class Dog extends Animal {
    @Override
    public void speak() { System.out.println("Woof"); }
}

// or composition (the recommended way)
public class Dog {
    private final Speaker speaker;  // has-a, not is-a
}
```

### Go Pattern

```go
// embedding (composition, not inheritance)
type Speaker interface {
    Speak()
}

type Dog struct {
    name string
}

func (d Dog) Speak() { fmt.Println("Woof") }

// embedding for reuse
type LoggingDog struct {
    Dog  // embedded - Dog's methods promoted to LoggingDog
}

func (d LoggingDog) Speak() {
    fmt.Println("About to speak...")
    d.Dog.Speak()  // call embedded method explicitly
}
```

### Why It Matters

- No fragile base class problem
- No deep inheritance hierarchies to understand
- Explicit is better - you always see what's composed

---

## Principle 2: Small Interfaces

Go interfaces are typically 1-2 methods. Java developers create interfaces with 10+ methods by default.

### Java Pattern

```java
public interface UserRepository {
    User findById(String id);
    List<User> findAll();
    List<User> findByEmail(String email);
    List<User> findByStatus(Status status);
    User save(User user);
    void delete(String id);
    void deleteAll();
    boolean exists(String id);
    long count();
    // ... it keeps growing
}
```

### Go Pattern

```go
// small, focused interfaces
type UserFinder interface {
    FindByID(id string) (*User, error)
}

type UserSaver interface {
    Save(user *User) error
}

// compose when needed
type UserRepository interface {
    UserFinder
    UserSaver
}

// accept only what you need
func ProcessUser(finder UserFinder, id string) error {
    user, err := finder.FindByID(id)
    // ...
}
```

### The io.Reader Principle

Go's standard library demonstrates this:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// files, network connections, buffers, HTTP bodies
// all implement these tiny interfaces
```

### Why It Matters

- Easy to implement (one method = one responsibility)
- Easy to mock in tests
- Functions can accept minimal requirements

---

## Principle 3: Accept Interfaces, Return Structs

A key Go idiom that's opposite to some Java patterns.

### Java Pattern

```java
// return interface to hide implementation
public interface UserService {
    User findById(String id);
}

public class UserServiceImpl implements UserService {
    // ...
}

// use interface everywhere
@Autowired
private UserService userService;  // interface type
```

### Go Pattern

```go
// accept interface (for flexibility)
func ProcessUser(finder UserFinder, id string) error {
    user, err := finder.FindByID(id)
    // ...
}

// return concrete type (for clarity)
func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

// users know exactly what they're getting
service := NewUserService(repo)
```

### Why It Matters

- Callers see exact capabilities of returned type
- No hidden implementations
- Interface satisfaction is implicit - let the caller define what they need

---

## Principle 4: Errors Are Values

Not exceptions. Not Optional. Values that you handle explicitly.

### Java Pattern

```java
// exceptions for errors
public User findById(String id) {
    return repository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
}

// caller might catch, might not
try {
    User user = service.findById(id);
} catch (UserNotFoundException e) {
    // handle
}
```

### Go Pattern

```go
// errors are return values
func (s *UserService) FindByID(id string) (*User, error) {
    user, err := s.repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("finding user %s: %w", id, err)
    }
    return user, nil
}

// caller must handle (compiler enforces usage)
user, err := service.FindByID(id)
if err != nil {
    // you MUST handle this
    return err
}
```

### Error Wrapping (Context)

```go
// add context as errors propagate up
user, err := repo.FindByID(id)
if err != nil {
    return nil, fmt.Errorf("user service: %w", err)
}

// unwrap to check specific errors
if errors.Is(err, ErrNotFound) {
    return nil, ErrUserNotFound
}
```

### Why It Matters

- Errors can't be silently ignored
- Error path is explicit and visible
- No unexpected exceptions from deep call stacks

---

## Principle 5: No Magic (Explicit Over Implicit)

Spring Boot's annotations do a lot behind the scenes. Go does very little.

### Java Pattern

```java
@Service
@Transactional
public class OrderService {
    @Autowired  // magic injection
    private OrderRepository repo;

    @Cacheable("orders")  // magic caching
    @Async  // magic threading
    public CompletableFuture<Order> findById(String id) {
        return repo.findById(id);  // magic persistence
    }
}
```

### Go Pattern

```go
type OrderService struct {
    repo  OrderRepository
    cache *Cache
}

// explicit construction
func NewOrderService(repo OrderRepository, cache *Cache) *OrderService {
    return &OrderService{repo: repo, cache: cache}
}

// explicit caching
func (s *OrderService) FindByID(ctx context.Context, id string) (*Order, error) {
    // check cache explicitly
    if order, ok := s.cache.Get(id); ok {
        return order, nil
    }

    // fetch from repo explicitly
    order, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, err
    }

    // cache explicitly
    s.cache.Set(id, order)
    return order, nil
}
```

### Why It Matters

- You can read the code and understand what it does
- No proxy behavior surprises (@Async not working when called internally)
- Debugging is straightforward

---

## Principle 6: Standard Library First

Go's standard library is comprehensive. Use it before reaching for frameworks.

### Java Pattern

```java
// need HTTP? use Spring Web
// need JSON? use Jackson
// need validation? use Hibernate Validator
// need config? use Spring Config
// need testing? use Spring Test + Mockito
```

### Go Pattern

```go
// need HTTP? use net/http (or chi for routing)
// need JSON? use encoding/json
// need validation? manual or go-playground/validator
// need config? use os.Getenv or envconfig
// need testing? use testing package

import (
    "encoding/json"
    "net/http"
    "testing"
)
```

### Why It Matters

- Fewer dependencies = fewer security updates
- Standard library is stable and well-documented
- Code is portable across Go projects

---

## Principle 7: Minimal Abstraction

Add abstraction only when you have concrete need, not in anticipation.

### Java Pattern (Anticipatory)

```java
public interface PaymentProcessor {
    void process(Payment payment);
}

public class StripePaymentProcessor implements PaymentProcessor {
    // implementation
}

public class PaymentProcessorFactory {
    public PaymentProcessor create(String type) {
        // factory logic
    }
}

// all this, even if there's only one payment provider
```

### Go Pattern (Pragmatic)

```go
// start with concrete implementation
func ProcessStripePayment(ctx context.Context, payment *Payment) error {
    // direct implementation
}

// extract interface only when you have two implementations
// or when you need to mock in tests
type PaymentProcessor interface {
    Process(ctx context.Context, payment *Payment) error
}
```

### YAGNI (You Aren't Gonna Need It)

- Don't create interfaces until you have two implementations
- Don't create factories until you need runtime selection
- Don't create abstractions until concrete code is duplicated

---

## Summary: The Mental Shift

| Java/Spring Mindset | Go Mindset |
|--------------------|------------|
| Hide complexity behind abstractions | Remove complexity |
| Framework does it for me | I write explicit code |
| Design for extensibility | Design for clarity |
| Prevent errors with types | Handle errors explicitly |
| Annotations configure behavior | Code IS the configuration |
| Rich interfaces | Tiny interfaces |
| Inheritance hierarchies | Composition of small parts |

---

## The Payoff

Go codebases tend to be:
- Easier to read (explicit > implicit)
- Easier to debug (no proxy magic)
- Easier to onboard (less framework knowledge needed)
- Faster to build and test

The cost is more boilerplate. The benefit is more understanding.
