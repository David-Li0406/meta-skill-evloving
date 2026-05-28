---
name: compile-time-dependency-injection
description: Use this skill for implementing compile-time dependency injection in both Go and Java applications.
---

# Compile-Time Dependency Injection Standards

## Go: Wire Dependency Injection

### Basic Setup

```go
// wire.go
//go:build wireinject
// +build wireinject

package main

import "github.com/google/wire"

func InitializeApp() (*App, error) {
    wire.Build(
        NewDatabase,
        NewUserRepository,
        NewUserService,
        NewApp,
    )
    return nil, nil
}
```

```bash
# Generate wire_gen.go
wire ./...
```

### Providers

```go
// Providers are constructors
func NewDatabase(cfg *Config) (*sql.DB, error) {
    return sql.Open("postgres", cfg.DatabaseURL)
}

func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}

func NewUserService(repo *UserRepository) *UserService {
    return &UserService{repo: repo}
}

func NewApp(svc *UserService) *App {
    return &App{userService: svc}
}
```

### Provider Sets

```go
// Group related providers
var DatabaseSet = wire.NewSet(
    NewDatabase,
    NewUserRepository,
)

var ServiceSet = wire.NewSet(
    NewUserService,
)

// Use sets in injector
func InitializeApp(cfg *Config) (*App, error) {
    wire.Build(
        DatabaseSet,
        ServiceSet,
        NewApp,
    )
    return nil, nil
}
```

### Interface Binding

```go
type UserRepository interface {
    FindByID(id int) (*User, error)
}

type userRepository struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) *userRepository {
    return &userRepository{db: db}
}

// Bind implementation to interface
var RepositorySet = wire.NewSet(
    NewUserRepository,
    wire.Bind(new(UserRepository), new(*userRepository)),
)
```

### Cleanup Functions

```go
func NewDatabase(cfg *Config) (*sql.DB, func(), error) {
    db, err := sql.Open("postgres", cfg.DatabaseURL)
    if err != nil {
        return nil, nil, err
    }

    cleanup := func() {
        db.Close()
    }

    return db, cleanup, nil
}

// Injector returns cleanup
func InitializeApp(cfg *Config) (*App, func(), error) {
    wire.Build(
        NewDatabase,
        NewApp,
    )
    return nil, nil, nil
}

// Usage
app, cleanup, err := InitializeApp(cfg)
if err != nil {
    log.Fatal(err)
}
defer cleanup()
```

## Java: Micronaut Core

### Compile-Time DI

```java
@Singleton
public class UserService {

    private final UserRepository repository;
    private final EventPublisher eventPublisher;

    // Constructor injection (preferred)
    public UserService(UserRepository repository, EventPublisher eventPublisher) {
        this.repository = repository;
        this.eventPublisher = eventPublisher;
    }
}

// Factory beans
@Factory
public class ClientFactory {

    @Singleton
    @Named("primary")
    public HttpClient primaryClient() {
        return HttpClient.create(URI.create("https://api.primary.com"));
    }

    @Singleton
    @Named("fallback")
    public HttpClient fallbackClient() {
        return HttpClient.create(URI.create("https://api.fallback.com"));
    }
}
```

### Configuration

```java
@ConfigurationProperties("app")
public record AppConfig(
    String name,
    int maxConnections,
    DatabaseConfig database
) {
    public record DatabaseConfig(
        String url,
        String username
    ) {}
}
```

```yaml
app:
  name: MyMicronautApp
  max-connections: 100
  database:
    url: jdbc:postgresql://localhost/db
    username: admin
```

### Controllers

```java
@Controller("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @Get("/{id}")
    public User findById(Long id) {
        return userService.findById(id);
    }

    @Post
    @Status(HttpStatus.CREATED)
    public User create(@Valid @Body CreateUserRequest request) {
        return userService.create(request);
    }
}
```

## Best Practices

1. **Provider sets**: Group related providers.
2. **Interfaces**: Use binding for testability.
3. **Cleanup**: Return cleanup functions for resources.
4. **Build tags**: Use appropriate build tags for Go.
5. **Regenerate**: Run necessary commands after changes.