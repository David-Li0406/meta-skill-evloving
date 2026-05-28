---
id: go-project-structure
name: "Go Project Structure"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Go Project Structure

## Overview

Go projects follow conventions established by the community and tools like `go mod`. This methodology covers standard project layouts, package organization, and module management for maintainable Go applications.

## When to Use

- Starting new Go projects
- Microservices and APIs
- CLI tools and utilities
- Libraries and shared packages
- Projects requiring clear dependency management

## Key Principles

1. **Flat by default** - Start simple, add structure as needed
2. **Package by feature** - Group related code together
3. **Internal packages** - Hide implementation details
4. **Minimal dependencies** - Go standard library is comprehensive
5. **Clear public API** - Exported symbols form your contract

## Best Practices

### Standard Project Layout

```
project/
├── cmd/                    # Application entry points
│   ├── api/
│   │   └── main.go
│   └── worker/
│       └── main.go
│
├── internal/               # Private application code
│   ├── config/
│   │   └── config.go
│   ├── database/
│   │   ├── database.go
│   │   └── migrations/
│   ├── handler/
│   │   ├── handler.go
│   │   ├── user.go
│   │   └── order.go
│   ├── middleware/
│   │   ├── auth.go
│   │   └── logging.go
│   ├── model/
│   │   ├── user.go
│   │   └── order.go
│   ├── repository/
│   │   ├── user.go
│   │   └── order.go
│   └── service/
│       ├── user.go
│       └── order.go
│
├── pkg/                    # Public library code
│   └── validation/
│       └── validation.go
│
├── api/                    # API definitions
│   └── openapi.yaml
│
├── scripts/                # Build and deployment scripts
│   └── build.sh
│
├── deployments/            # Docker, K8s configs
│   ├── Dockerfile
│   └── kubernetes/
│
├── docs/                   # Documentation
│   └── architecture.md
│
├── go.mod                  # Module definition
├── go.sum                  # Dependency checksums
├── Makefile                # Build automation
└── README.md
```

### Module Initialization

```bash
# Initialize new module
go mod init github.com/username/project

# Add dependencies
go get github.com/gin-gonic/gin@latest
go get github.com/jmoiron/sqlx

# Tidy dependencies
go mod tidy

# Verify dependencies
go mod verify

# Vendor dependencies (optional)
go mod vendor
```

### Go Module Configuration

```go
// go.mod
module github.com/username/project

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/jmoiron/sqlx v1.3.5
    github.com/lib/pq v1.10.9
    go.uber.org/zap v1.27.0
)

require (
    // indirect dependencies
)
```

### Application Entry Point

```go
// cmd/api/main.go
package main

import (
    "context"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"

    "github.com/username/project/internal/config"
    "github.com/username/project/internal/database"
    "github.com/username/project/internal/handler"
    "github.com/username/project/internal/repository"
    "github.com/username/project/internal/service"
)

func main() {
    // Load configuration
    cfg, err := config.Load()
    if err != nil {
        log.Fatalf("failed to load config: %v", err)
    }

    // Initialize database
    db, err := database.Connect(cfg.DatabaseURL)
    if err != nil {
        log.Fatalf("failed to connect to database: %v", err)
    }
    defer db.Close()

    // Wire dependencies
    userRepo := repository.NewUserRepository(db)
    userService := service.NewUserService(userRepo)
    h := handler.New(userService)

    // Create server
    srv := &http.Server{
        Addr:         ":" + cfg.Port,
        Handler:      h.Routes(),
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    // Start server in goroutine
    go func() {
        log.Printf("server starting on port %s", cfg.Port)
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    // Graceful shutdown
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatalf("server shutdown error: %v", err)
    }

    log.Println("server stopped gracefully")
}
```

### Configuration Management

```go
// internal/config/config.go
package config

import (
    "os"
    "strconv"
)

type Config struct {
    Port        string
    Environment string
    DatabaseURL string
    JWTSecret   string
    LogLevel    string
}

func Load() (*Config, error) {
    return &Config{
        Port:        getEnv("PORT", "8080"),
        Environment: getEnv("ENVIRONMENT", "development"),
        DatabaseURL: getEnv("DATABASE_URL", "postgres://localhost/app"),
        JWTSecret:   getEnv("JWT_SECRET", ""),
        LogLevel:    getEnv("LOG_LEVEL", "info"),
    }, nil
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
    if value := os.Getenv(key); value != "" {
        if i, err := strconv.Atoi(value); err == nil {
            return i
        }
    }
    return defaultValue
}

func (c *Config) IsDevelopment() bool {
    return c.Environment == "development"
}

func (c *Config) IsProduction() bool {
    return c.Environment == "production"
}
```

### Package Organization

```go
// internal/model/user.go
package model

import "time"

type User struct {
    ID        string    `db:"id" json:"id"`
    Email     string    `db:"email" json:"email"`
    Name      string    `db:"name" json:"name"`
    CreatedAt time.Time `db:"created_at" json:"createdAt"`
    UpdatedAt time.Time `db:"updated_at" json:"updatedAt"`
}

type CreateUserInput struct {
    Email string `json:"email" binding:"required,email"`
    Name  string `json:"name" binding:"required,min=1,max=100"`
}

type UpdateUserInput struct {
    Email *string `json:"email,omitempty" binding:"omitempty,email"`
    Name  *string `json:"name,omitempty" binding:"omitempty,min=1,max=100"`
}

// internal/repository/user.go
package repository

import (
    "context"
    "database/sql"

    "github.com/jmoiron/sqlx"
    "github.com/username/project/internal/model"
)

type UserRepository interface {
    FindByID(ctx context.Context, id string) (*model.User, error)
    FindByEmail(ctx context.Context, email string) (*model.User, error)
    FindAll(ctx context.Context, limit, offset int) ([]model.User, error)
    Create(ctx context.Context, user *model.User) error
    Update(ctx context.Context, user *model.User) error
    Delete(ctx context.Context, id string) error
}

type userRepository struct {
    db *sqlx.DB
}

func NewUserRepository(db *sqlx.DB) UserRepository {
    return &userRepository{db: db}
}

func (r *userRepository) FindByID(ctx context.Context, id string) (*model.User, error) {
    var user model.User
    err := r.db.GetContext(ctx, &user, "SELECT * FROM users WHERE id = $1", id)
    if err == sql.ErrNoRows {
        return nil, nil
    }
    return &user, err
}

func (r *userRepository) Create(ctx context.Context, user *model.User) error {
    query := `
        INSERT INTO users (id, email, name, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5)
    `
    _, err := r.db.ExecContext(ctx, query,
        user.ID, user.Email, user.Name, user.CreatedAt, user.UpdatedAt)
    return err
}
```

### Makefile for Build Automation

```makefile
# Makefile
.PHONY: build run test lint clean

# Variables
BINARY_NAME=api
BUILD_DIR=./build
MAIN_PATH=./cmd/api

# Build
build:
	go build -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)

build-linux:
	GOOS=linux GOARCH=amd64 go build -o $(BUILD_DIR)/$(BINARY_NAME)-linux $(MAIN_PATH)

# Run
run:
	go run $(MAIN_PATH)

dev:
	air -c .air.toml

# Test
test:
	go test -v ./...

test-coverage:
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# Lint
lint:
	golangci-lint run ./...

fmt:
	gofmt -s -w .
	goimports -w .

# Dependencies
tidy:
	go mod tidy
	go mod verify

# Clean
clean:
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html

# Docker
docker-build:
	docker build -t $(BINARY_NAME):latest .

docker-run:
	docker run -p 8080:8080 $(BINARY_NAME):latest
```

### Dockerfile

```dockerfile
# Dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source
COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/api

# Runtime stage
FROM alpine:3.19

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /app

COPY --from=builder /app/server .

EXPOSE 8080

USER nobody:nobody

ENTRYPOINT ["./server"]
```

## Anti-patterns

### Avoid: Cyclic Imports

```go
// BAD - package A imports B, B imports A
// package a
import "project/internal/b"

// package b
import "project/internal/a"

// GOOD - extract shared code to third package
// package shared (no imports from a or b)
// package a imports shared
// package b imports shared
```

### Avoid: Global State

```go
// BAD - global database connection
var DB *sql.DB

func GetUser(id string) (*User, error) {
    return DB.Query(...)
}

// GOOD - dependency injection
type UserRepository struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}

func (r *UserRepository) GetUser(id string) (*User, error) {
    return r.db.Query(...)
}
```

### Avoid: Putting Everything in One Package

```go
// BAD - everything in main package
package main

type User struct{}
type Order struct{}
func CreateUser() {}
func CreateOrder() {}
func HandleUserRequest() {}

// GOOD - separate by responsibility
// internal/model/user.go
// internal/service/user.go
// internal/handler/user.go
```

## References

- [Standard Go Project Layout](https://github.com/golang-standards/project-layout)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
