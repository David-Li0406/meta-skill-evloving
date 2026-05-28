---
name: clean-architecture
description: Clean Architecture principles for maintainable, testable applications. Use when designing application structure or refactoring.
---

# Clean Architecture

## Layer Structure

```
┌─────────────────────────────────────────────┐
│ FRAMEWORKS & DRIVERS (Web, DB, External)    │
│ ┌─────────────────────────────────────────┐ │
│ │ INTERFACE ADAPTERS (Controllers, Repos) │ │
│ │ ┌─────────────────────────────────────┐ │ │
│ │ │ APPLICATION (Use Cases)             │ │ │
│ │ │ ┌─────────────────────────────────┐ │ │ │
│ │ │ │ DOMAIN (Entities)               │ │ │ │
│ │ │ └─────────────────────────────────┘ │ │ │
│ │ └─────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Dependency Rule

**Dependencies point inward only.**

- Domain knows nothing about outer layers
- Use Cases know Domain, nothing else
- Adapters know Use Cases + Domain
- Frameworks know everything

## Layers

### Domain (Entities)
- Business objects with behavior
- Validation rules
- No framework dependencies
- No I/O operations

### Application (Use Cases)
- Orchestrates domain objects
- One use case = one action
- Defines repository interfaces
- Input/Output DTOs

### Interface Adapters
- Controllers: HTTP → Use Case
- Repositories: Use Case → Database
- Presenters: Use Case → Response format

### Frameworks & Drivers
- Web framework (Express, FastAPI, Fiber)
- Database clients
- External APIs
- Configuration

## Folder Structure

```
src/
├── domain/
│   └── entities/
├── application/
│   ├── use-cases/
│   └── interfaces/      # Repository interfaces
├── infrastructure/
│   ├── repositories/    # Interface implementations
│   └── external/        # API clients
└── interfaces/
    ├── http/            # Controllers, routes
    └── cli/             # CLI handlers
```

## Key Patterns

### Dependency Injection
```
UseCase depends on RepositoryInterface (not implementation)
Controller injects concrete Repository into UseCase
```

### Use Case Structure
```
1. Validate input
2. Load entities via repository
3. Execute domain logic
4. Persist via repository
5. Return output DTO
```

### Repository Interface
```
Defined in: application/interfaces/
Implemented in: infrastructure/repositories/
```

## When to Apply

**Use Clean Architecture when:**
- Application will grow/evolve
- Multiple entry points (API, CLI, queue)
- Team needs clear boundaries
- Testing is priority

**Skip for:**
- Simple CRUD apps
- Prototypes/MVPs
- Scripts/tools

## Common Mistakes

- Entities depending on ORM/framework
- Use cases calling HTTP directly
- Business logic in controllers
- Skipping the interface layer
- Over-engineering simple apps

## Testing Strategy

| Layer | Test Type | Mocks |
|-------|-----------|-------|
| Domain | Unit | None |
| Use Cases | Unit | Repositories |
| Adapters | Integration | External services |
| E2E | System | None |
