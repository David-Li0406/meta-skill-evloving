# Exercise 19: Project Structure

**Time:** 15 minutes
**Goal:** Organize a production Go project following conventions

## The Spring Boot Version

```
src/main/java/
    com/example/myapp/
        MyAppApplication.java
        controller/
            TaskController.java
        service/
            TaskService.java
        repository/
            TaskRepository.java
        entity/
            Task.java
src/main/resources/
    application.yml
```

## The Go Way

```
myapp/
    cmd/
        server/
            main.go
    internal/
        handler/
        service/
        repository/
        model/
    pkg/          # (optional - public library code)
    configs/
    migrations/
```

---

## Standard Go Project Layout

### 1. /cmd - Entry Points

```
cmd/
    server/
        main.go       # HTTP server
    worker/
        main.go       # Background worker
    cli/
        main.go       # CLI tool
```

Each subdirectory is a separate binary. The main package lives here.

### 2. /internal - Private Code

```
internal/
    handler/          # HTTP handlers
    service/          # Business logic
    repository/       # Data access
    model/            # Domain types
    middleware/       # HTTP middleware
    config/           # Configuration
    database/         # DB connection
    apperror/         # Error types
```

**Key:** Code in `/internal` cannot be imported by other projects. This is enforced by Go.

### 3. /pkg - Public Library Code (Optional)

```
pkg/
    validation/       # Reusable validation
    httputil/         # HTTP utilities
```

Use sparingly. Most code should be in `/internal`.

### 4. Supporting Directories

```
configs/              # Configuration files
    config.yaml       # (if using file-based config)

migrations/           # Database migrations
    001_create_tasks.sql
    002_add_users.sql

scripts/              # Build/deploy scripts
    build.sh
    migrate.sh

api/                  # API specifications
    openapi.yaml
```

## Complete Structure Example

```
myapp/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── database/
│   │   └── postgres.go
│   ├── model/
│   │   ├── task.go
│   │   └── user.go
│   ├── repository/
│   │   ├── interface.go
│   │   ├── task_postgres.go
│   │   └── task_memory.go
│   ├── service/
│   │   ├── task.go
│   │   └── task_test.go
│   ├── handler/
│   │   ├── task.go
│   │   ├── task_test.go
│   │   └── response.go
│   ├── middleware/
│   │   ├── logging.go
│   │   ├── auth.go
│   │   └── metrics.go
│   ├── apperror/
│   │   └── errors.go
│   └── testutil/
│       └── postgres.go
├── migrations/
│   └── 001_initial.sql
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

## Package Naming

### Good Names

```go
package user       // singular, clear
package handler
package repository
package config
```

### Avoid

```go
package utils     // too generic
package common    // meaningless
package helpers   // what does it help?
package base      // too abstract
```

## Dependencies Between Packages

```
cmd/server
    └── depends on → internal/*

internal/handler
    └── depends on → internal/service
                   → internal/model
                   → internal/apperror

internal/service
    └── depends on → internal/repository (interface)
                   → internal/model

internal/repository
    └── depends on → internal/model
```

**Rule:** No circular dependencies. Higher layers depend on lower layers.

## main.go Structure

```go
package main

import (
    // stdlib first
    "context"
    "log/slog"
    "os"

    // external packages
    "github.com/go-chi/chi/v5"

    // internal packages
    "myapp/internal/config"
    "myapp/internal/database"
    "myapp/internal/handler"
    "myapp/internal/repository"
    "myapp/internal/service"
)

func main() {
    // 1. load config
    cfg := config.MustLoad()

    // 2. setup logger
    logger := setupLogger(cfg)

    // 3. connect to dependencies
    db := mustConnectDB(cfg, logger)
    defer db.Close()

    // 4. wire dependencies
    taskRepo := repository.NewPostgresTaskRepository(db)
    taskService := service.NewTaskService(taskRepo)
    taskHandler := handler.NewTaskHandler(taskService, logger)

    // 5. setup router
    r := setupRouter(taskHandler, logger)

    // 6. start server
    startServer(cfg, r, logger)
}
```

## Makefile

```makefile
.PHONY: build run test lint

build:
	go build -o bin/server ./cmd/server

run:
	go run ./cmd/server

test:
	go test ./...

test-integration:
	go test -tags=integration ./...

lint:
	golangci-lint run

migrate:
	migrate -path migrations -database $(DATABASE_URL) up
```

## What Spring Devs Might Miss

| Spring | Go Alternative |
|--------|----------------|
| Component scanning | Explicit wiring in main() |
| Configuration profiles | Build tags or env vars |
| Application context | No equivalent - explicit deps |
| Auto-configuration | Manual setup (but simple) |

## Benefits of Go Structure

1. **Explicit dependencies** - main.go shows everything
2. **No magic** - no scanning, no reflection
3. **Fast compilation** - no annotation processing
4. **Easy testing** - inject mocks directly

## Checkpoint

- [ ] Understand cmd/ for entry points
- [ ] Understand internal/ for private code
- [ ] Can structure a new project
- [ ] Know how to wire dependencies

---

Congratulations! You've completed all exercises. You're now ready to write production Go.
