---
name: api-feature-cqrs
description: Generate complete CQRS feature module with commands, queries, events, handlers, repository, controller, DTOs, and tests. Use when creating new domain entities or adding CRUD operations with side effects.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Feature CQRS

## Purpose

Generate a complete CQRS-based feature module for NestJS applications. This skill creates the full directory structure with commands, queries, events, handlers, DTOs, controllers, repositories, and tests following enterprise patterns.

## When to Use

- Creating new domain entities (User, Product, Order, etc.)
- Adding CRUD operations to existing features
- Building features with side effects (email notifications, webhooks)
- Implementing multi-tenant features with organization isolation
- Any feature that requires database operations

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/
├── commands/
│   ├── create-{entity}/
│   │   ├── create-{entity}.command.ts
│   │   ├── create-{entity}.handler.ts
│   │   └── index.ts
│   ├── update-{entity}/
│   ├── delete-{entity}/
│   └── index.ts
├── queries/
│   ├── get-{entity}/
│   ├── list-{entities}/
│   └── index.ts
├── events/
│   ├── {entity}-created.event.ts
│   ├── {entity}-updated.event.ts
│   ├── {entity}-deleted.event.ts
│   └── index.ts
├── event-handlers/
│   ├── {event}-handler.ts
│   └── index.ts
├── dto/
│   ├── create-{entity}.dto.ts
│   ├── update-{entity}.dto.ts
│   ├── {entity}-response.dto.ts
│   └── index.ts
├── interfaces/
│   ├── {entity}.repository.interface.ts
│   └── index.ts
├── repositories/
│   ├── {entity}.repository.ts
│   └── index.ts
├── __tests__/
│   ├── fixtures/
│   ├── handlers/
│   └── {feature}.integration.test.ts
├── {feature}.controller.ts
├── {feature}.module.ts
└── index.ts
```

## Patterns Enforced

### CQRS Pattern

All commands implement `ICommand` from `@starter/foundation-cqrs`:

- Include `tenantId` and `actorId` properties (multi-tenancy)
- Use readonly properties
- Include timestamp

All queries implement `IQuery` from `@starter/foundation-cqrs`:

- Include `tenantId` property (multi-tenancy)
- Return typed responses

All events implement `IEvent` from `@starter/foundation-cqrs`:

- Include `tenantId`, `aggregateId`, and `occurredAt`
- Immutable data

### Multi-Tenancy

- All commands/queries include `tenantId` parameter
- All repository methods accept `tenantId`
- Events include `tenantId` for routing

### Event Publishing

- All state changes publish domain events
- Events published after successful database operation
- Events include context for audit logging

### Repository Pattern

- Repositories extend `BaseRepository` from `@starter/foundation-repositories`
- All database operations use transactions for multi-step writes
- Queries scoped to tenant

### OpenAPI Documentation

- Controllers use `@ApiTags()` decorator
- Endpoints use `@ApiOperation()` with summary
- Responses use `@ApiResponse()` decorator
- DTOs use `@ApiProperty()` decorator

## Usage Example

```bash
/skill feature-cqrs --name=Product --fields='name:string,price:number,description:text,isActive:boolean'
```

## Related Files

- [Data Repository](../data-repository/SKILL.md) - Create standalone repository
- [API Controller](../api-controller/SKILL.md) - Generate REST controller
- [API DTO](../api-dto/SKILL.md) - Create DTOs with validation
- [Feature Module](../feature-module/SKILL.md) - Generate NestJS module
