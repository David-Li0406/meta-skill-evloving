---
title: Dependency Injection Patterns
impact: HIGH
impactDescription: Testability and decoupling
tags: ddd, dependency-injection, wire
---

## Dependency Injection Patterns

Use dependency injection for decoupling. Google Wire is recommended.

**Install Wire:**

```bash
go install github.com/google/wire/cmd/wire@latest
```

**Provider Definitions:**

```go
// internal/infrastructure/persistence/mysql/provider.go
package mysql

import "github.com/google/wire"

var ProviderSet = wire.NewSet(
    NewUserRepository,
    wire.Bind(new(user.Repository), new(*UserRepository)),
)
```

```go
// internal/application/user/provider.go
package user

import "github.com/google/wire"

var ProviderSet = wire.NewSet(NewHandler)
```

```go
// internal/interfaces/http/handler/provider.go
package handler

import "github.com/google/wire"

var ProviderSet = wire.NewSet(NewUserHandler)
```

**Wire Configuration:**

```go
// cmd/server/wire.go
//go:build wireinject

package main

import (
    "github.com/google/wire"
    "myapp/internal/application/user"
    "myapp/internal/infrastructure/persistence/mysql"
    "myapp/internal/interfaces/http/handler"
)

func InitializeApp(db *gorm.DB) (*App, error) {
    wire.Build(
        mysql.ProviderSet,
        user.ProviderSet,
        handler.ProviderSet,
        NewApp,
    )
    return nil, nil
}
```

**Generate Dependency Injection Code:**

```bash
cd cmd/server && wire
```

**Usage:**

```go
// cmd/server/main.go
func main() {
    db := initDB()
    app, err := InitializeApp(db)
    if err != nil {
        log.Fatal(err)
    }
    app.Run()
}
```
