---
name: api-feature-module
description: Generate NestJS feature module with CqrsModule, handler registration, and exports. Use when creating new feature modules or configuring CQRS dependencies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Feature Module

## Purpose

Generate a NestJS feature module that imports `CqrsModule`, registers all command/query handlers, event handlers, and exports services and repositories for other modules to use.

## When to Use

- Creating new feature modules
- Setting up module dependencies
- Configuring CQRS module for a feature
- Organizing module providers and exports

## What It Generates

```
apps/api/src/modules/{feature}/{feature}.module.ts
```

## Patterns Enforced

### CqrsModule Import

All feature modules must import `CqrsModule` from `@nestjs/cqrs`:

- Enables CommandBus and QueryBus
- Enables EventBus for domain events
- Required for @CommandHandler, @QueryHandler, @EventsHandler decorators

### Provider Registration

- Command handlers registered as providers
- Query handlers registered as providers
- Event handlers registered as providers
- Services registered as providers
- Repositories registered as providers

### Exports

- Services exported for use by other modules
- Repositories exported for use by other modules
- Guards or interceptors if shared

## Usage Example

```bash
/skill feature-module --name=Users --commands='create,update,delete' --queries='get,list' --events='created,updated,deleted'
```

## Related Files

- [Feature CQRS](../feature-cqrs/SKILL.md) - Complete CQRS feature with module
- [API Controller](../api-controller/SKILL.md) - Generate controller for module
