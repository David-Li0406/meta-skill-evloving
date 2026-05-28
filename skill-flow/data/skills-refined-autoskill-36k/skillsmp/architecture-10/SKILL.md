---
name: architecture
description: Guidelines for application structure and dependency management.
---

# Architecture

## Hexagonal Architecture
For complex applications (clients, datastore, state), use [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture).

## Dependency Management
- **Initializers**: Create dependencies with sane defaults.
- **Optional Arguments**: Use the **Functional Options Pattern** (variadic args) for optional configuration.

See [Languages](../languages/SKILL.md) for implementation details.
