---
name: spring-boot
description: >
    Spring Boot with WebFlux, R2DBC, and reactive patterns for Kotlin.
    Trigger: When working with controllers, services, repositories, or Spring configuration.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
metadata:
    author: cvix
    version: "2.0"
---

# Spring Boot Skill

Conventions for Spring Boot backend development with WebFlux, R2DBC, and Kotlin.

> **Architecture Note**: This skill covers the **Infrastructure Layer** of our Hexagonal
> Architecture.
> For domain models, use cases, and overall feature organization, see
> the [hexagonal-architecture skill](../hexagonal-architecture/SKILL.md).

## Layer Context

| Layer                           | What Goes Here                                 | Spring Annotations? |
|---------------------------------|------------------------------------------------|---------------------|
| **Domain**                      | Entities, Value Objects, Repository interfaces | NO                  |
| **Application**                 | Commands, Queries, Handlers, Use Case services | NO                  |
| **Infrastructure** (this skill) | Controllers, R2DBC repos, Configs, Adapters    | YES                 |

## When to Use

- Creating REST controllers (HTTP adapters)
- Implementing repository adapters (R2DBC implementations)
- Configuring Spring Security, CORS, caching
- Wiring application services as Spring beans
- Writing integration tests with Testcontainers

## Quick Reference

### Controllers & HTTP Layer

Thin HTTP adapters that delegate to application handlers. No business logic.

- **[Controllers](references/controllers.md)** - `@RestController`, routing, OpenAPI annotations
- **[Request/Response DTOs](references/request-response-dtos.md)** - Jakarta validation, Schema
  annotations
- **[Swagger Standard](references/swagger-standard.md)** - OpenAPI documentation conventions

### Application Layer Wiring

Application services are framework-agnostic; Spring wires them via `@Configuration`.

- **[CQRS Handlers](references/cqrs-handlers.md)** - Command/Query handlers as `@Service` beans

### Persistence Layer

Repository adapters implementing domain ports with R2DBC.

- **[Repositories](references/repositories.md)** - Domain ports, Spring Data interfaces, adapters
- **[Entities & Mappers](references/entities-mappers.md)** - `@Table` entities, mapper components

### Cross-Cutting Concerns

- **[Error Handling](references/error-handling.md)** - `@ControllerAdvice`, ProblemDetail (RFC 7807)
- **[Configuration](references/configuration.md)** - `@ConfigurationProperties`, Security, R2DBC
- **[WebFlux & Coroutines](references/webflux-coroutines.md)** - Reactive patterns, never block

## HTTP Status Codes

| Code                        | When to Use                             |
|-----------------------------|-----------------------------------------|
| `200 OK`                    | Successful GET, PUT                     |
| `201 Created`               | Successful POST that creates resource   |
| `204 No Content`            | Successful DELETE                       |
| `400 Bad Request`           | Invalid input, malformed JSON           |
| `401 Unauthorized`          | Missing or invalid auth                 |
| `403 Forbidden`             | Valid auth but insufficient permissions |
| `404 Not Found`             | Resource doesn't exist                  |
| `409 Conflict`              | State conflict (duplicate email, etc.)  |
| `422 Unprocessable Entity`  | Valid syntax but semantic errors        |
| `500 Internal Server Error` | Unexpected server errors                |

## Application Profiles

| Profile   | Purpose                                               |
|-----------|-------------------------------------------------------|
| `dev`     | Local development, verbose logging, H2/Testcontainers |
| `test`    | Automated tests, mocked external services             |
| `staging` | Production-like, real services                        |
| `prod`    | Production, optimized settings, real databases        |

## Anti-Patterns

| Anti-Pattern                             | Why It's Wrong                                    |
|------------------------------------------|---------------------------------------------------|
| Spring annotations in Application/Domain | Only Infrastructure has Spring dependencies       |
| Business logic in controllers            | Controllers delegate to application handlers      |
| Exposing entities in API                 | Use DTOs (Request/Response classes)               |
| `block()` in WebFlux                     | Use coroutines or reactive operators              |
| Generic exception catching               | Handle specific exceptions with proper responses  |
| Secrets in code                          | Use environment variables or secret managers      |
| Domain ports extending Spring interfaces | Domain ports are pure Kotlin; adapters use Spring |

See [WebFlux & Coroutines](references/webflux-coroutines.md) for reactive anti-patterns.

## Commands

```bash
# Run application
./gradlew bootRun

# Run with profile
SPRING_PROFILES_ACTIVE=dev ./gradlew bootRun

# Run tests
./gradlew test

# Integration tests only
./gradlew test -PincludeTags=integration

# Build JAR
./gradlew bootJar
```

## Resources

### Internal References

- [Controllers](references/controllers.md) - HTTP adapter patterns
- [CQRS Handlers](references/cqrs-handlers.md) - Command/Query handler wiring
- [Repositories](references/repositories.md) - R2DBC repository adapters
- [Entities & Mappers](references/entities-mappers.md) - Persistence entities
- [Configuration](references/configuration.md) - Spring configuration patterns
- [Error Handling](references/error-handling.md) - Exception handling with ProblemDetail
- [WebFlux & Coroutines](references/webflux-coroutines.md) - Reactive patterns
- [Request/Response DTOs](references/request-response-dtos.md) - API contracts
- [Swagger Standard](references/swagger-standard.md) - OpenAPI documentation

### Related Skills

- [hexagonal-architecture](../hexagonal-architecture/SKILL.md) - Domain, Application layers &
  feature organization
- [kotlin](../kotlin/SKILL.md) - Kotlin conventions for all layers

### External Documentation

- [Spring WebFlux](https://docs.spring.io/spring-framework/reference/web/webflux.html)
- [Spring Data R2DBC](https://spring.io/projects/spring-data-r2dbc)
- [Kotlin Coroutines with Spring](https://docs.spring.io/spring-framework/reference/languages/kotlin/coroutines.html)
- [Problem Details RFC 7807](https://www.rfc-editor.org/rfc/rfc7807)
