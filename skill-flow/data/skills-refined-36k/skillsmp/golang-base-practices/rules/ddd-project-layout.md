---
title: Standard Project Directory Structure
impact: HIGH
impactDescription: Clear code organization
tags: ddd, project-layout, structure
---

## Standard Project Directory Structure

Follow DDD layered architecture with clear separation of concerns.

**Recommended Project Structure:**

```
myapp/
├── cmd/                    # Application entry points
│   └── server/
│       └── main.go
├── internal/               # Private code
│   ├── domain/             # Domain layer (core business)
│   │   ├── user/
│   │   │   ├── entity.go
│   │   │   ├── repository.go
│   │   │   └── service.go
│   │   └── order/
│   ├── application/        # Application layer (use cases)
│   │   ├── user/
│   │   │   ├── command.go
│   │   │   ├── query.go
│   │   │   └── handler.go
│   │   └── order/
│   ├── infrastructure/     # Infrastructure layer
│   │   ├── persistence/
│   │   │   ├── mysql/
│   │   │   │   ├── user_repo.go
│   │   │   │   └── order_repo.go
│   │   │   └── redis/
│   │   └── external/
│   │       └── payment/
│   └── interfaces/         # Interface layer
│       ├── http/
│       │   ├── handler/
│       │   ├── middleware/
│       │   └── router.go
│       └── grpc/
├── pkg/                    # Public libraries (can be imported externally)
│   ├── errors/
│   └── utils/
├── configs/                # Configuration files
├── migrations/             # Database migrations
├── api/                    # API definitions (proto/openapi)
├── scripts/                # Build and deployment scripts
├── Makefile
└── go.mod
```

**Layer Dependency Rules:**
- interfaces → application → domain
- infrastructure → domain
- Domain layer has no external dependencies
