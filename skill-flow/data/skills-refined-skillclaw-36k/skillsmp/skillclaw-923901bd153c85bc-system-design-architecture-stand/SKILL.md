---
name: system-design-architecture-standards
description: Use this skill when you need to establish universal architectural standards for building robust, scalable, and maintainable systems.
---

# System Design & Architecture Standards

## **Priority: P0 (FOUNDATIONAL)**

## Architectural Principles

- **SoC**: Divide into distinct sections per concern.
- **SSOT**: One source, reference elsewhere.
- **Fail Fast**: Fail visibly when errors occur.
- **Graceful Degradation**: Core functionality remains even if secondary features fail.

## Modularity & Coupling

- **High Cohesion**: Group related functionality within a single module.
- **Loose Coupling**: Utilize interfaces for communication between modules.
- **Dependency Injection (DI)**: Inject dependencies rather than hardcoding them.

## Common Patterns

- **Layered Architecture**: Structure as Presentation → Logic → Data.
- **Event-Driven Architecture**: Enable asynchronous communication between decoupled components.
- **Clean/Hexagonal Architecture**: Keep core logic independent of frameworks.
- **Statelessness**: Favor stateless designs for improved scalability and testing.

## Distributed Systems

- **CAP Theorem**: Understand the trade-offs between Consistency, Availability, and Partition tolerance.
- **Idempotency**: Ensure operations can be repeated without side effects.
- **Circuit Breaker Pattern**: Implement mechanisms to fail fast on failing services.
- **Eventual Consistency**: Design systems for asynchronous data synchronization.

## Documentation & Evolution

- **Design Documentation**: Create specifications before major implementations.
- **Versioning**: Maintain backward compatibility by versioning APIs and schemas.
- **Extensibility**: Use design patterns like Strategy and Factory to accommodate future changes.