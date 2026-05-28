---
title: Use Go-Kratos for Complex Microservices
impact: CRITICAL
impactDescription: Enterprise-grade microservice architecture
tags: framework, kratos, microservice, grpc
---

## Use Go-Kratos for Complex Microservices

For complex microservice systems requiring gRPC and HTTP dual protocols, service discovery, config centers, choose Go-Kratos.

**When to Use:**
- Multi-service collaborative microservice architecture
- Need gRPC + HTTP dual protocols
- Require service discovery, config center
- Team has extensive Go experience

**Correct Example (Kratos project structure):**

```go
// cmd/server/main.go
package main

import (
    "github.com/go-kratos/kratos/v2"
    "github.com/go-kratos/kratos/v2/transport/grpc"
    "github.com/go-kratos/kratos/v2/transport/http"
)

func main() {
    app, cleanup, err := wireApp(conf.Server, conf.Data, logger)
    if err != nil {
        panic(err)
    }
    defer cleanup()

    if err := app.Run(); err != nil {
        panic(err)
    }
}
```

```go
// internal/service/user.go
package service

type UserService struct {
    pb.UnimplementedUserServer
    uc *biz.UserUsecase
}

func NewUserService(uc *biz.UserUsecase) *UserService {
    return &UserService{uc: uc}
}

func (s *UserService) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    user, err := s.uc.GetUser(ctx, req.Id)
    if err != nil {
        return nil, err
    }
    return &pb.User{
        Id:   user.ID,
        Name: user.Name,
    }, nil
}
```

**Kratos Key Features:**
- Protocol Buffers API definition
- Wire dependency injection
- Middleware chain (logging, tracing, circuit breaker)
- Multiple registry support
