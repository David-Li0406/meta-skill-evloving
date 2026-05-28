# Exercise 05: Configuration

**Time:** 15 minutes
**Goal:** Load configuration from environment variables

## The Spring Boot Version

```yaml
# application.yml
server:
  port: ${PORT:8080}

database:
  url: ${DATABASE_URL}
  max-connections: ${DB_MAX_CONN:10}

app:
  api-key: ${API_KEY}
```

```java
@ConfigurationProperties(prefix = "database")
public record DatabaseConfig(String url, int maxConnections) {}
```

## The Go Way

Environment variables are the standard. Use a library like `envconfig` or `viper`:

```go
type Config struct {
    Port         string `envconfig:"PORT" default:"8080"`
    DatabaseURL  string `envconfig:"DATABASE_URL" required:"true"`
    DBMaxConns   int    `envconfig:"DB_MAX_CONN" default:"10"`
    APIKey       string `envconfig:"API_KEY" required:"true"`
}
```

## Your Task

1. Create a Config struct with validation
2. Load config from environment variables
3. Fail fast if required config is missing
4. Use config throughout the application

---

## Step by Step

### 1. Add envconfig dependency (1 min)

```bash
go get github.com/kelseyhightower/envconfig
```

### 2. Create the Config struct (4 min)

Create `internal/config/config.go`:

```go
package config

import (
    "fmt"
    "time"

    "github.com/kelseyhightower/envconfig"
)

type Config struct {
    // server settings
    Port         string        `envconfig:"PORT" default:"8080"`
    ReadTimeout  time.Duration `envconfig:"READ_TIMEOUT" default:"5s"`
    WriteTimeout time.Duration `envconfig:"WRITE_TIMEOUT" default:"10s"`

    // database settings
    DatabaseURL string `envconfig:"DATABASE_URL" required:"true"`
    DBMaxConns  int    `envconfig:"DB_MAX_CONN" default:"10"`

    // application settings
    APIKey   string `envconfig:"API_KEY" required:"true"`
    LogLevel string `envconfig:"LOG_LEVEL" default:"info"`

    // feature flags
    EnableMetrics bool `envconfig:"ENABLE_METRICS" default:"false"`
}

func Load() (*Config, error) {
    var cfg Config
    if err := envconfig.Process("", &cfg); err != nil {
        return nil, fmt.Errorf("loading config: %w", err)
    }
    return &cfg, nil
}

// MustLoad panics if config can't be loaded (use at startup)
func MustLoad() *Config {
    cfg, err := Load()
    if err != nil {
        panic(err)
    }
    return cfg
}
```

### 3. Create a .env file for development (2 min)

Create `.env` in project root:

```bash
PORT=8080
DATABASE_URL=postgres://localhost:5432/myapp
API_KEY=dev-secret-key
LOG_LEVEL=debug
ENABLE_METRICS=true
```

Add to `.gitignore`:
```
.env
```

### 4. Load .env in development (3 min)

Add godotenv for development:

```bash
go get github.com/joho/godotenv
```

Create `cmd/server/main.go`:

```go
package main

import (
    "log"
    "log/slog"
    "net/http"
    "os"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
    "github.com/joho/godotenv"

    "my-first-go-app/internal/config"
    "my-first-go-app/internal/handler"
    intmiddleware "my-first-go-app/internal/middleware"
    "my-first-go-app/internal/repository"
    "my-first-go-app/internal/service"
)

func main() {
    // load .env file if it exists (development only)
    _ = godotenv.Load()

    // load config
    cfg := config.MustLoad()

    // setup logger based on config
    logLevel := slog.LevelInfo
    if cfg.LogLevel == "debug" {
        logLevel = slog.LevelDebug
    }
    logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: logLevel,
    }))

    logger.Info("starting server",
        "port", cfg.Port,
        "log_level", cfg.LogLevel,
        "metrics_enabled", cfg.EnableMetrics,
    )

    // create dependencies
    userRepo := repository.NewUserRepository()
    userService := service.NewUserService(userRepo)
    userHandler := handler.NewUserHandler(userService)

    // setup router
    r := chi.NewRouter()
    r.Use(intmiddleware.RequestID)
    r.Use(intmiddleware.Logging(logger))
    r.Use(middleware.Recoverer)

    // routes
    r.Route("/api", func(r chi.Router) {
        // protected routes
        r.Group(func(r chi.Router) {
            r.Use(intmiddleware.APIKeyAuth(cfg.APIKey))

            r.Route("/users", func(r chi.Router) {
                r.Post("/", userHandler.Create)
                r.Get("/", userHandler.List)
                r.Get("/{id}", userHandler.GetByID)
            })
        })
    })

    // health check (unprotected)
    r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("ok"))
    })

    // start server
    addr := ":" + cfg.Port
    server := &http.Server{
        Addr:         addr,
        Handler:      r,
        ReadTimeout:  cfg.ReadTimeout,
        WriteTimeout: cfg.WriteTimeout,
    }

    logger.Info("server listening", "addr", addr)
    if err := server.ListenAndServe(); err != nil {
        logger.Error("server error", "error", err)
        os.Exit(1)
    }
}
```

### 5. Test it

```bash
# run with .env file
go run ./cmd/server

# or override with environment variables
PORT=9000 go run ./cmd/server

# missing required config fails fast
unset DATABASE_URL && go run ./cmd/server
# panic: loading config: required key DATABASE_URL missing value
```

## Config Patterns

### Nested Config

```go
type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
}

type ServerConfig struct {
    Port    string `envconfig:"PORT" default:"8080"`
    Timeout time.Duration `envconfig:"TIMEOUT" default:"30s"`
}

type DatabaseConfig struct {
    URL      string `envconfig:"DATABASE_URL" required:"true"`
    MaxConns int    `envconfig:"DB_MAX_CONNS" default:"10"`
}
```

### Using Viper for More Features

```go
import "github.com/spf13/viper"

func Load() (*Config, error) {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")
    viper.AutomaticEnv()

    if err := viper.ReadInConfig(); err != nil {
        // config file not found, use env vars only
    }

    var cfg Config
    if err := viper.Unmarshal(&cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}
```

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| application.yml | Environment variables |
| @ConfigurationProperties | Struct with envconfig tags |
| Spring profiles | Different .env files or deployment config |
| @Value injection | Config struct passed as dependency |

## Environment Strategy

| Environment | Config Source |
|-------------|--------------|
| Development | `.env` file (gitignored) |
| Testing | Test fixtures or in-memory |
| Production | Container env vars, secrets manager |

## Checkpoint

- [ ] Config loads from environment variables
- [ ] Missing required config fails at startup
- [ ] Default values work
- [ ] Config is used throughout the app

**Next:** Exercise 06 - CRUD Handler
