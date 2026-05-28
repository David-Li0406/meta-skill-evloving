# Exercise 00b: Small Interfaces

**Time:** 15 minutes
**Goal:** Understand Go's approach to interface design

## The Java Pattern

Java interfaces often have many methods:

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
}
```

And implementation explicitly declares `implements`:

```java
public class PostgresUserRepository implements UserRepository {
    // must implement all 9 methods
}
```

## The Go Way

Go interfaces are small - often 1-2 methods:

```go
// from standard library
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// compose when needed
type ReadWriter interface {
    Reader
    Writer
}
```

Implementation is **implicit** - no `implements` keyword:

```go
type FileWriter struct {
    path string
}

// FileWriter satisfies Writer by having this method
func (f *FileWriter) Write(p []byte) (int, error) {
    // implementation
    return len(p), nil
}
```

## The io.Reader Principle

Go's `io.Reader` is one method:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

It's implemented by:
- Files
- Network connections
- HTTP response bodies
- Buffers
- Compressed streams
- Encrypted streams

One tiny interface, massive reusability.

## Your Task

Refactor this Java-style interface into Go-style small interfaces:

```go
// this is too big
type UserStore interface {
    FindByID(id string) (*User, error)
    FindAll() ([]*User, error)
    FindByEmail(email string) (*User, error)
    Save(user *User) error
    Delete(id string) error
    Exists(id string) (bool, error)
    Count() (int, error)
}
```

---

## Step by Step

### 1. Identify distinct capabilities (3 min)

What does `UserStore` actually do?
- Find/get users (read operations)
- Save users (write operations)
- Delete users (delete operations)
- Check existence (query operations)

### 2. Split into focused interfaces (5 min)

```go
type UserFinder interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

type UserLister interface {
    FindAll(ctx context.Context) ([]*User, error)
}

type UserSaver interface {
    Save(ctx context.Context, user *User) error
}

type UserDeleter interface {
    Delete(ctx context.Context, id string) error
}
```

### 3. Compose when needed (3 min)

```go
type UserRepository interface {
    UserFinder
    UserSaver
    UserDeleter
}

type ReadOnlyUserStore interface {
    UserFinder
    UserLister
}
```

### 4. Accept minimal interface in functions (4 min)

```go
// only needs to find users
func GetUser(finder UserFinder, id string) (*User, error) {
    return finder.FindByID(context.Background(), id)
}

// only needs to save
func UpdateUser(saver UserSaver, user *User) error {
    return saver.Save(context.Background(), user)
}

// needs both
func CloneUser(finder UserFinder, saver UserSaver, id string) error {
    user, err := finder.FindByID(context.Background(), id)
    if err != nil {
        return err
    }
    user.ID = uuid.New().String()
    return saver.Save(context.Background(), user)
}
```

## Accept Interfaces, Return Structs

**Accept interfaces** - be flexible about what you receive:

```go
func ProcessUser(finder UserFinder, id string) error {
    // accepts any type that can find users
}
```

**Return structs** - be specific about what you provide:

```go
func NewUserRepository(db *sql.DB) *UserRepository {
    // returns concrete type
    return &UserRepository{db: db}
}
```

Why? The caller defines what interface they need. The implementation returns the concrete type so callers know exactly what they get.

## The Empty Interface Trap

Java developers sometimes do this:

```go
// bad: empty interface accepts anything
func Process(data interface{}) {
    // have to type-assert everything
}
```

This loses type safety. Use specific interfaces or generics instead.

## Interface Satisfaction Check

Go's implicit interfaces can be tricky - if you change the interface, implementations silently stop satisfying it.

Add compile-time checks:

```go
// verify PostgresRepo implements UserRepository
var _ UserRepository = (*PostgresRepo)(nil)
```

This fails to compile if `PostgresRepo` doesn't satisfy `UserRepository`.

## What Just Happened?

| Java | Go |
|------|-----|
| Fat interfaces | Tiny interfaces |
| `implements` keyword | Implicit satisfaction |
| Define all methods at once | Compose small interfaces |
| Consumer adapts to interface | Interface adapts to consumer |

## The Mental Shift

**Java thinking:** "I'll create a complete interface for all User operations."

**Go thinking:** "This function only needs to find users. Accept just `UserFinder`."

Define interfaces at the consumer site, not the provider site.

## Stretch Goal

Create a logging decorator using interface embedding:

```go
type LoggingUserFinder struct {
    UserFinder  // embed the interface
    logger *slog.Logger
}

func (l *LoggingUserFinder) FindByID(ctx context.Context, id string) (*User, error) {
    l.logger.Info("finding user", "id", id)
    user, err := l.UserFinder.FindByID(ctx, id)
    if err != nil {
        l.logger.Error("failed to find user", "id", id, "error", err)
    }
    return user, err
}
```

## Checkpoint

- [ ] I can create small, focused interfaces
- [ ] I understand implicit interface satisfaction
- [ ] I know when to compose interfaces
- [ ] I accept that interfaces are defined where they're used

**Next:** Exercise 00c - Error Handling Philosophy
