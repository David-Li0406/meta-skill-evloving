---
name: nestjs-architecture
description: Use this skill when designing scalable NestJS applications with a focus on modularity and dependency injection patterns.
---

# NestJS Architecture Standards

## **Priority: P0 (FOUNDATIONAL)**

Core architectural patterns and dependency injection standards for scalable NestJS applications.

## Core Principles

1. **Modularity**: Every feature **must** be encapsulated in its own `@Module`.
   - **Do**: `users.module.ts`, `auth.module.ts`.
   - **Don't**: Everything in `app.module.ts`.
2. **Dependency Injection (DI)**: Invert control. Never manually instantiate classes (e.g., `new Service()`).
   - **Use**: Constructor injection `constructor(private readonly service: Service)`.
3. **Scalability**: Use **Feature Modules** for domain logic and **Core/Shared Modules** for reusable utilities.

## Module Configuration

### Dynamic Modules

- **Modern Pattern**: Use `ConfigurableModuleBuilder` class to auto-generate `forRoot`/`register` methods properly.
- **Conventions**:
    - `forRoot`: Global configurations (Db, Config).
    - `register`: Per-instance configurations.
    - `forFeature`: Extending a module with specific providers/entities.

### Circular Dependencies

- **Avoid**: Re-architect to move shared logic to a common module.
- **Constraint**: If unavoidable, use `forwardRef(() => ModuleName)` on **both** sides of the import.

## Advanced Providers

- **Factory Providers**: Use `useFactory` heavily for providers dependent on configuration or async operations.
- **Aliasing**: Use `useExisting` to provide backward compatibility or abstract different implementations.

## Scopes & Lifecycle

- **Default**: **Singleton**. Best performance.
- **Request Scope**: Use `Scope.REQUEST` sparingly.
  - **Performance Warning**: Request scope **bubbles up**. If a Service is request-scoped, every controller injecting it becomes request-scoped, triggering re-instantiation per request (~5-10% latency overhead).
- **Multi-tenancy**: If request-scope is needed (e.g. Tenant ID header), use **Durable Providers** (`durable: true`) with `ContextIdFactory` to reuse DI sub-trees.
- **Shutdown**: `SIGTERM` doesn't trigger cleanup by default.
  - **Mandatory**: Call `app.enableShutdownHooks()` in `main.ts`.

## Structure & Organization

- **Feature Modules**: Domain logic (`ShopModule`, `AuthModule`). Encapsulated.
- **Shared Modules**: Reusable utilities across the application.