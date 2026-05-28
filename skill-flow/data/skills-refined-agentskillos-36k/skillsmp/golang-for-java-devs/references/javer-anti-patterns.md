# Java Developer Anti-Patterns in Go

Code a Java developer would write in Go - and the idiomatic fix.

Each pattern shows: Java instinct -> Bad Go -> Why it's wrong -> Idiomatic Go

---

## 1. Getters and Setters Everywhere

**Your Java instinct:**
```java
public class User {
    private String email;

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

**Bad Go (Java mentality):**
```go
type User struct {
    email string  // private
}

func (u *User) GetEmail() string {
    return u.email
}

func (u *User) SetEmail(email string) {
    u.email = email
}

// usage
user.SetEmail("test@example.com")
fmt.Println(user.GetEmail())
```

**Why it's wrong:** This is pointless indirection. Go doesn't have the JavaBeans spec or frameworks that require getter/setter naming conventions.

**Idiomatic Go:**
```go
type User struct {
    Email string  // exported, direct access
}

// usage
user.Email = "test@example.com"
fmt.Println(user.Email)
```

Only add methods when you need computed values or side effects.

---

## 2. Interface for Everything

**Your Java instinct:**
```java
// always program to interfaces
public interface UserService {
    User findById(String id);
    void save(User user);
}

public class UserServiceImpl implements UserService {
    // implementation
}
```

**Bad Go (Java mentality):**
```go
// create interface for every struct
type UserService interface {
    FindByID(id string) (*User, error)
    Save(user *User) error
}

type UserServiceImpl struct {
    repo *UserRepository
}

func (s *UserServiceImpl) FindByID(id string) (*User, error) {
    // implementation
}
```

**Why it's wrong:** Go interfaces are implicit. Creating interfaces "just in case" adds noise. The `Impl` suffix is a code smell.

**Idiomatic Go:**
```go
// concrete implementation first
type UserService struct {
    repo *UserRepository
}

func (s *UserService) FindByID(ctx context.Context, id string) (*User, error) {
    return s.repo.FindByID(ctx, id)
}

// define interface where you NEED it (consumer side)
// e.g., in test file or another package that needs to mock
type UserFinder interface {
    FindByID(ctx context.Context, id string) (*User, error)
}
```

Interfaces are defined by the consumer, not the provider.

---

## 3. Fighting Error Returns

**Your Java instinct:**
```java
// exceptions bubble up automatically
public User findById(String id) {
    return repo.findById(id)
        .orElseThrow(() -> new NotFoundException(id));
}
```

**Bad Go (fighting the language):**
```go
// try to simulate exceptions
type Result[T any] struct {
    Value T
    Error error
}

func (s *UserService) FindByID(id string) Result[*User] {
    user, err := s.repo.FindByID(id)
    if err != nil {
        return Result[*User]{Error: err}
    }
    return Result[*User]{Value: user}
}

// or worse: panic for control flow
func (s *UserService) FindByID(id string) *User {
    user, err := s.repo.FindByID(id)
    if err != nil {
        panic(err)  // "it's like throwing"
    }
    return user
}
```

**Why it's wrong:** You're writing extra code to avoid Go's error handling, losing stack traces and making code harder to follow.

**Idiomatic Go:**
```go
func (s *UserService) FindByID(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("finding user %s: %w", id, err)
    }
    return user, nil
}

// caller handles explicitly
user, err := service.FindByID(ctx, id)
if err != nil {
    if errors.Is(err, ErrNotFound) {
        // handle not found
    }
    return err
}
```

---

## 4. Factory Classes and Patterns

**Your Java instinct:**
```java
public class UserServiceFactory {
    public static UserService create(Config config) {
        var repo = new UserRepository(config.dbUrl());
        var cache = new Cache(config.cacheUrl());
        return new UserService(repo, cache);
    }
}
```

**Bad Go (Java mentality):**
```go
type UserServiceFactory struct {
    config *Config
}

func NewUserServiceFactory(config *Config) *UserServiceFactory {
    return &UserServiceFactory{config: config}
}

func (f *UserServiceFactory) Create() *UserService {
    repo := NewUserRepository(f.config.DBURL)
    cache := NewCache(f.config.CacheURL)
    return NewUserService(repo, cache)
}
```

**Why it's wrong:** Factory classes add a layer of indirection for no benefit. Go doesn't have static methods, but functions are fine.

**Idiomatic Go:**
```go
// just a function
func NewUserService(cfg *Config) (*UserService, error) {
    repo, err := NewUserRepository(cfg.DBURL)
    if err != nil {
        return nil, err
    }
    cache := NewCache(cfg.CacheURL)
    return &UserService{repo: repo, cache: cache}, nil
}

// or wire in main() directly
func main() {
    repo, _ := NewUserRepository(cfg.DBURL)
    cache := NewCache(cfg.CacheURL)
    service := &UserService{repo: repo, cache: cache}
}
```

---

## 5. Using panic for Control Flow

**Your Java instinct:**
```java
if (user == null) {
    throw new IllegalArgumentException("user cannot be null");
}
```

**Bad Go (Java mentality):**
```go
func ProcessUser(user *User) {
    if user == nil {
        panic("user cannot be nil")  // "it's like throwing"
    }
    // process
}
```

**Why it's wrong:** Panic is for truly unrecoverable situations - bugs in the program, not invalid input. Callers must use recover() to handle panics, which is clunky.

**Idiomatic Go:**
```go
func ProcessUser(user *User) error {
    if user == nil {
        return errors.New("user cannot be nil")
    }
    // process
    return nil
}

// panic is OK for programmer errors during init
func MustCompileRegex(pattern string) *regexp.Regexp {
    re, err := regexp.Compile(pattern)
    if err != nil {
        panic(err)  // programmer error, will be caught immediately
    }
    return re
}
```

---

## 6. Ignoring Errors with _

**Your Java instinct:**
```java
// exceptions are handled... somewhere
userService.save(user);  // might throw, don't care
```

**Bad Go:**
```go
// "I'll handle errors later"
user, _ := service.FindByID(id)
_ = service.Save(user)
```

**Why it's wrong:** You're ignoring errors that could indicate real problems. The code appears to work until it mysteriously fails in production.

**Idiomatic Go:**
```go
user, err := service.FindByID(ctx, id)
if err != nil {
    return nil, err
}

if err := service.Save(ctx, user); err != nil {
    return nil, fmt.Errorf("saving user: %w", err)
}
```

The only acceptable use of `_` for errors is when the function literally cannot fail in your usage, and you've verified this.

---

## 7. Over-Abstracting Too Early

**Your Java instinct:**
```java
// anticipate future needs
public interface PaymentProcessor { void process(Payment p); }
public interface PaymentValidator { void validate(Payment p); }
public interface PaymentNotifier { void notify(Payment p); }
public interface PaymentPersister { void persist(Payment p); }

public class PaymentService {
    // inject all four interfaces
}
```

**Bad Go:**
```go
type PaymentProcessor interface { Process(p *Payment) error }
type PaymentValidator interface { Validate(p *Payment) error }
type PaymentNotifier interface { Notify(p *Payment) error }
type PaymentPersister interface { Persist(p *Payment) error }

type PaymentService struct {
    processor PaymentProcessor
    validator PaymentValidator
    notifier  PaymentNotifier
    persister PaymentPersister
}
```

**Why it's wrong:** You're creating abstraction layers before you need them. YAGNI - You Aren't Gonna Need It.

**Idiomatic Go:**
```go
type PaymentService struct {
    db     *sql.DB
    mailer *Mailer
}

func (s *PaymentService) Process(ctx context.Context, p *Payment) error {
    // validate inline
    if p.Amount <= 0 {
        return errors.New("invalid amount")
    }

    // persist directly
    _, err := s.db.ExecContext(ctx, "INSERT INTO payments ...", p.ID, p.Amount)
    if err != nil {
        return err
    }

    // notify directly
    return s.mailer.Send(ctx, p.CustomerEmail, "Payment received")
}

// extract interfaces only when you have two implementations or need to mock
```

---

## 8. Creating "util" Packages

**Your Java instinct:**
```java
package com.company.util;

public class StringUtils {
    public static String capitalize(String s) { ... }
}

public class DateUtils {
    public static Date parse(String s) { ... }
}
```

**Bad Go:**
```go
package util

func Capitalize(s string) string { ... }
func ParseDate(s string) (time.Time, error) { ... }
func Contains[T comparable](slice []T, item T) bool { ... }
```

**Why it's wrong:** "util" is not a meaningful package name. It becomes a dumping ground. It tells you nothing about what's inside.

**Idiomatic Go:**
```go
// put functions where they're used, or create meaningful packages
package user

func (u *User) DisplayName() string {
    return strings.Title(u.FirstName + " " + u.LastName)
}

// or package by purpose
package str
func Capitalize(s string) string { ... }

// or just use standard library
import "strings"
strings.ToUpper(s[:1]) + s[1:]
```

---

## 9. Dependency Injection Frameworks

**Your Java instinct:**
```java
// Spring wires everything
@Service
public class UserService {
    @Autowired
    private UserRepository repo;
}
```

**Bad Go (seeking the same magic):**
```go
// using wire, dig, or fx for simple projects
// @Inject annotations via struct tags
// complex provider functions
```

**Why it's wrong:** Go's explicit wiring in main() is usually sufficient. DI frameworks add complexity and magic that Go tries to avoid.

**Idiomatic Go:**
```go
func main() {
    // explicit wiring - you can see exactly what's connected
    db, _ := sql.Open("postgres", cfg.DatabaseURL)
    repo := NewUserRepository(db)
    service := NewUserService(repo)
    handler := NewUserHandler(service)

    r := chi.NewRouter()
    r.Get("/users/{id}", handler.GetUser)
    http.ListenAndServe(":8080", r)
}
```

For large projects, wire or fx can help, but start simple.

---

## 10. Not Using defer for Cleanup

**Your Java instinct:**
```java
Connection conn = null;
try {
    conn = dataSource.getConnection();
    // use connection
} finally {
    if (conn != null) {
        conn.close();
    }
}
```

**Bad Go:**
```go
conn, err := db.Conn(ctx)
if err != nil {
    return err
}
// ... lots of code ...
// forget to close, or close in wrong place
conn.Close()
return result
// what if we return early above?
```

**Why it's wrong:** Resources leak when you have multiple return paths.

**Idiomatic Go:**
```go
conn, err := db.Conn(ctx)
if err != nil {
    return err
}
defer conn.Close()  // ALWAYS runs when function returns

// use connection safely
// can return anywhere, conn will be closed
```

---

## The Pattern

Notice the common thread:

| Java Approach | Go Approach |
|--------------|-------------|
| Frameworks do it | You do it explicitly |
| Interfaces first | Concrete first, interfaces when needed |
| Abstractions for extensibility | YAGNI - build what you need |
| Hide complexity | Embrace simplicity |
| Exceptions for errors | Values for errors |
| DI container wiring | Manual wiring in main() |

The instinct to abstract and prepare for change made you a good Java developer. In Go, that instinct often produces worse code. Write simple, explicit code.
