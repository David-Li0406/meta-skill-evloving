---
title: Uber fx Dependency Injection
impact: CRITICAL
impactDescription: Mandatory DI framework - ensures clean architecture, testability, and lifecycle management
tags: di, dependency-injection, uber-fx, architecture, mandatory
---

# Uber fx Dependency Injection (MANDATORY)

Uber fx is the **required** dependency injection framework for this project. All services, handlers, and repositories MUST use fx for lifecycle management and dependency wiring.

## Rule 0: fx is MANDATORY - No Exceptions

```go
// ❌ FORBIDDEN - manual instantiation
func main() {
    db := database.New()
    repo := repository.New(db)
    service := service.New(repo)
    handler := handler.New(service)
    // ...
}

// ✅ REQUIRED - use fx.New()
func main() {
    fx.New(
        fx.Provide(
            database.New,
            repository.New,
            service.New,
            handler.New,
        ),
        fx.Invoke(startServer),
    ).Run()
}
```

## Rule 1: Module Organization

**Every domain MUST have an fx module:**

```go
// ❌ INCORRECT - no module organization
// scattered providers across main.go

// ✅ CORRECT - domain module
// internal/user/module.go
package user

import "go.uber.org/fx"

var Module = fx.Options(
    fx.Provide(
        NewRepository,
        NewService,
        NewHandler,
    ),
)

// main.go
func main() {
    fx.New(
        user.Module,
        order.Module,
        payment.Module,
        infrastructure.Module,
    ).Run()
}
```

## Rule 2: Constructor Signatures

**Constructors MUST follow fx conventions:**

```go
// ❌ INCORRECT - returns pointer only
func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

// ✅ CORRECT - returns interface for better testability
func NewUserService(repo UserRepository) UserService {
    return &userServiceImpl{repo: repo}
}

// ✅ CORRECT - with error return when needed
func NewUserService(repo UserRepository, cfg Config) (UserService, error) {
    if cfg.Timeout == 0 {
        return nil, errors.New("timeout required")
    }
    return &userServiceImpl{repo: repo, timeout: cfg.Timeout}, nil
}
```

## Rule 3: Lifecycle Hooks

**Use fx.Lifecycle for startup/shutdown:**

```go
// ❌ INCORRECT - manual lifecycle
func NewServer(handler Handler) *http.Server {
    srv := &http.Server{Handler: handler}
    go srv.ListenAndServe()  // starts immediately, no cleanup
    return srv
}

// ✅ CORRECT - fx lifecycle hooks
func NewServer(lc fx.Lifecycle, handler Handler) *http.Server {
    srv := &http.Server{
        Addr:    ":8080",
        Handler: handler,
    }

    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            go srv.ListenAndServe()
            return nil
        },
        OnStop: func(ctx context.Context) error {
            return srv.Shutdown(ctx)
        },
    })

    return srv
}
```

## Rule 4: Gin Router with fx

**Gin router MUST be provided via fx:**

```go
// ❌ INCORRECT - manual gin setup
func main() {
    r := gin.Default()
    r.GET("/users", userHandler.List)
    r.Run()
}

// ✅ CORRECT - fx-managed gin
// internal/server/module.go
package server

var Module = fx.Options(
    fx.Provide(NewRouter),
    fx.Invoke(RegisterRoutes),
)

func NewRouter() *gin.Engine {
    r := gin.Default()
    r.Use(middleware.Recovery())
    r.Use(middleware.Logger())
    return r
}

type RouteParams struct {
    fx.In
    Router      *gin.Engine
    UserHandler *user.Handler
    OrderHandler *order.Handler
}

func RegisterRoutes(p RouteParams) {
    api := p.Router.Group("/api/v1")
    {
        users := api.Group("/users")
        users.GET("", p.UserHandler.List)
        users.GET("/:id", p.UserHandler.Get)
        users.POST("", p.UserHandler.Create)
    }
    {
        orders := api.Group("/orders")
        orders.GET("", p.OrderHandler.List)
        orders.POST("", p.OrderHandler.Create)
    }
}
```

## Rule 5: fx.In and fx.Out for Multiple Dependencies

**Use fx.In/fx.Out for clean parameter handling:**

```go
// ❌ INCORRECT - too many constructor parameters
func NewHandler(
    userSvc UserService,
    orderSvc OrderService,
    paymentSvc PaymentService,
    logger *zap.Logger,
    cfg Config,
) *Handler {
    // ...
}

// ✅ CORRECT - use fx.In
type HandlerParams struct {
    fx.In
    UserSvc    UserService
    OrderSvc   OrderService
    PaymentSvc PaymentService
    Logger     *zap.Logger
    Config     Config
}

func NewHandler(p HandlerParams) *Handler {
    return &Handler{
        userSvc:    p.UserSvc,
        orderSvc:   p.OrderSvc,
        paymentSvc: p.PaymentSvc,
        logger:     p.Logger,
        cfg:        p.Config,
    }
}
```

**Use fx.Out for multiple return values:**

```go
type InfraResult struct {
    fx.Out
    DB     *sql.DB
    Cache  *redis.Client
    Logger *zap.Logger
}

func NewInfrastructure(cfg Config) (InfraResult, error) {
    db, err := sql.Open("postgres", cfg.DatabaseURL)
    if err != nil {
        return InfraResult{}, err
    }

    cache := redis.NewClient(&redis.Options{Addr: cfg.RedisAddr})
    logger, _ := zap.NewProduction()

    return InfraResult{
        DB:     db,
        Cache:  cache,
        Logger: logger,
    }, nil
}
```

## Rule 6: Named Dependencies

**Use fx.Named for multiple implementations:**

```go
// ❌ INCORRECT - ambiguous dependencies
fx.Provide(
    NewPostgresDB,  // which *sql.DB?
    NewMySQLDB,     // collision!
)

// ✅ CORRECT - named dependencies
fx.Provide(
    fx.Annotate(
        NewPostgresDB,
        fx.ResultTags(`name:"postgres"`),
    ),
    fx.Annotate(
        NewMySQLDB,
        fx.ResultTags(`name:"mysql"`),
    ),
)

// Consumer with named dependency
type RepoParams struct {
    fx.In
    PrimaryDB   *sql.DB `name:"postgres"`
    AnalyticsDB *sql.DB `name:"mysql"`
}
```

## Rule 7: Optional Dependencies

**Use fx.Optional for optional dependencies:**

```go
type ServiceParams struct {
    fx.In
    Repo   Repository
    Cache  Cache    `optional:"true"`  // may not be provided
    Logger *zap.Logger
}

func NewService(p ServiceParams) Service {
    s := &serviceImpl{repo: p.Repo, logger: p.Logger}
    if p.Cache != nil {
        s.cache = p.Cache  // use cache if available
    }
    return s
}
```

## Rule 8: Configuration Loading

**Load config via fx:**

```go
// ✅ CORRECT - config as fx dependency
type Config struct {
    DatabaseURL string `env:"DATABASE_URL,required"`
    RedisAddr   string `env:"REDIS_ADDR" envDefault:"localhost:6379"`
    Port        int    `env:"PORT" envDefault:"8080"`
}

func LoadConfig() (Config, error) {
    var cfg Config
    if err := env.Parse(&cfg); err != nil {
        return Config{}, fmt.Errorf("parse config: %w", err)
    }
    return cfg, nil
}

// main.go
fx.New(
    fx.Provide(LoadConfig),
    // Config is now available to all other constructors
)
```

## Rule 9: Graceful Shutdown

**fx handles shutdown automatically:**

```go
func main() {
    app := fx.New(
        fx.Provide(/* ... */),
        fx.Invoke(startServer),
    )

    // fx.Run() handles:
    // 1. OnStart hooks in dependency order
    // 2. Waits for SIGINT/SIGTERM
    // 3. OnStop hooks in reverse order
    app.Run()
}
```

## Rule 10: Testing with fx

**Use fx.Options for test modules:**

```go
// ✅ CORRECT - test-specific module
func TestUserHandler(t *testing.T) {
    var handler *user.Handler

    app := fxtest.New(t,
        fx.Provide(
            // Use mock repository
            func() user.Repository { return &mockRepo{} },
            user.NewService,
            user.NewHandler,
        ),
        fx.Populate(&handler),
    )
    defer app.RequireStart().RequireStop()

    // Test handler
    req := httptest.NewRequest("GET", "/users", nil)
    rec := httptest.NewRecorder()
    handler.List(rec, req)

    assert.Equal(t, 200, rec.Code)
}
```

## Standard Module Structure

```
internal/
├── user/
│   ├── module.go       # fx.Options for user domain
│   ├── handler.go      # Gin handlers
│   ├── service.go      # Business logic
│   ├── repository.go   # Data access
│   └── model.go        # Domain models
├── order/
│   └── module.go       # fx.Options for order domain
├── infrastructure/
│   ├── module.go       # fx.Options for infra
│   ├── database.go     # DB connection with lifecycle
│   ├── redis.go        # Redis with lifecycle
│   └── logger.go       # Logger setup
└── server/
    ├── module.go       # fx.Options for HTTP server
    └── router.go       # Gin router setup
```

## Compliance Checklist

Before submitting code, verify:

- [ ] All dependencies wired through fx.Provide
- [ ] Each domain has its own fx.Module
- [ ] Lifecycle hooks used for OnStart/OnStop
- [ ] No manual instantiation in main()
- [ ] Named dependencies for multiple implementations
- [ ] fx.In/fx.Out for complex constructors
- [ ] Tests use fxtest for DI
