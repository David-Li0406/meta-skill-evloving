---
name: api-decorator-custom
description: Generate custom NestJS parameter decorators (user, tenant, actor) and metadata decorators (roles, permissions, public). Use when extracting request context or reducing controller boilerplate.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Custom Decorators

## Purpose

Generate custom NestJS decorators for extracting common request data (user, tenant, actor) and adding metadata (roles, permissions, public).

## When to Use

- Creating reusable parameter decorators
- Adding metadata to routes
- Extracting request context
- Reducing boilerplate in controllers

## What It Generates

### Directory Structure

```
apps/api/src/common/decorators/
├── user.decorator.ts
├── tenant.decorator.ts
├── actor.decorator.ts
├── roles.decorator.ts
├── permissions.decorator.ts
├── public.decorator.ts
└── index.ts
```

## Patterns Enforced

### Parameter Decorators

Use `createParamDecorator` from `@nestjs/common`:

- Extract data from `ExecutionContext`
- Type-safe return values
- Support for WebSockets and GraphQL

### Metadata Decorators

Use `SetMetadata` from `@nestjs/common`:

- Store metadata for guards/interceptors
- Composable decorators
- Default values

## Usage Example

```bash
/skill decorator-custom --types='user,tenant,actor,roles,permissions,public'
```

## Related Files

- [Auth Guards](../auth-guards/SKILL.md) - Guards that use decorators
- [API Controller](../../core/api-controller/SKILL.md) - Controllers with decorators
