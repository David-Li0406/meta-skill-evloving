# Exercise Index

Exercises organized by topic. Each takes ~15 minutes.

## Phase 0: Go Philosophy (Optional)

*Recommended for understanding Go's design. Skip if you want to start coding immediately - you can return later.*

| # | Exercise | You'll Learn |
|---|----------|--------------|
| 00a | [Composition Over Inheritance](00a-composition.md) | Embedding vs extends |
| 00b | [Small Interfaces](00b-interfaces.md) | Accept interfaces, return structs |
| 00c | [Error Handling Philosophy](00c-error-handling.md) | Errors as values, not exceptions |
| 00d | [Simplicity and Explicitness](00d-simplicity.md) | YAGNI, no magic |

**Reference:** [Go Philosophy Quick Reference](../simplicity-foundations.md)

---

## Phase 1: Syntax Survival

| # | Exercise | You'll Learn |
|---|----------|--------------|
| 01 | [First Endpoint](01-first-endpoint.md) | Chi router, JSON handlers, structs |
| 02 | [Validation](02-validation.md) | go-playground/validator, struct tags |
| 03 | [Middleware](03-middleware.md) | Chi middleware, logging, auth |
| 04 | [Dependency Injection](04-dependency-injection.md) | Constructor pattern, manual wiring |
| 05 | [Configuration](05-configuration.md) | Environment variables, envconfig |

## Phase 2: Building APIs

| # | Exercise | You'll Learn |
|---|----------|--------------|
| 06 | [CRUD Handler](06-crud-handler.md) | URL params, request bodies, status codes |
| 07 | [Error Handling](07-error-handling.md) | Custom errors, error middleware |
| 08 | [Testing Handlers](08-testing-handlers.md) | httptest, Chi test helpers |
| 09 | [Testing Services](09-testing-services.md) | Table-driven tests, mocks |

## Phase 3: Data & Concurrency

| # | Exercise | You'll Learn |
|---|----------|--------------|
| 10 | [Database Setup](10-database-setup.md) | database/sql, sqlx |
| 11 | [Repository Layer](11-repository-layer.md) | Interface + implementation |
| 12 | [Goroutines](12-goroutines.md) | go keyword, sync.WaitGroup |
| 13 | [Channels](13-channels.md) | Buffered, unbuffered communication |
| 14 | [Worker Pools](14-worker-pools.md) | Fan-out, fan-in patterns |
| 15 | [Context and Cancellation](15-context-cancellation.md) | Timeouts, deadlines |

## Phase 4: Production Patterns

| # | Exercise | You'll Learn |
|---|----------|--------------|
| 16 | [Observability](16-observability.md) | slog, prometheus metrics |
| 17 | [Graceful Shutdown](17-graceful-shutdown.md) | Signal handling, context |
| 18 | [Integration Testing](18-testing-integration.md) | testcontainers-go |
| 19 | [Project Structure](19-project-structure.md) | cmd/, internal/, pkg/ |

## Project Iterations

After exercises, build the "Task API" service. Iterations are milestones, not requirements.

### Core Path (minimum viable)
Complete these 3 to consider yourself successful:

| Iteration | Focus |
|-----------|-------|
| 1 | Minimal - one endpoint, hardcoded response |
| 2 | Add validation, proper structs, error handling |
| 3 | Add service layer, dependency injection |

### Extended Path (optional)
Continue if you want deeper mastery:

| Iteration | Focus |
|-----------|-------|
| 4 | Add database persistence |
| 5 | Add concurrent processing |
| 6 | Add tests (unit + integration) |
| 7 | Add observability (logging, metrics) |

### Alternative: Switch Projects
After iteration 3, you can build a different service instead of continuing Task API:
- A URL shortener (create short URLs, redirect)
- A file metadata service (upload, list, retrieve)

Variety prevents tedium. The goal is pattern internalization, not Task API completion.

Each iteration can be started fresh to build muscle memory.
