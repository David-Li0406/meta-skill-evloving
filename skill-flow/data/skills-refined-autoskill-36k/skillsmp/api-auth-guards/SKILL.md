---
name: api-auth-guards
description: Generate authentication and authorization guards (JWT, API key, roles, permissions) with tenant context validation. Use when protecting API endpoints or implementing RBAC.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Auth Guards

## Purpose

Generate NestJS guards for authentication (JWT, API key) and authorization (roles, permissions) with tenant context validation.

## When to Use

- Protecting API endpoints with authentication
- Implementing role-based access control (RBAC)
- Adding permission checks
- Validating tenant context

## What It Generates

### Directory Structure

```
apps/api/src/common/guards/
├── jwt-auth.guard.ts
├── api-key.guard.ts
├── roles.guard.ts
├── permissions.guard.ts
├── tenant.guard.ts
└── index.ts
```

## Patterns Enforced

### JWT Authentication

Validates JWT tokens from `Authorization` header:

- Extracts and verifies JWT
- Attaches user to request object
- Validates token expiration

### API Key Authentication

Validates API keys from `x-api-key` header:

- Checks key against database
- Attaches organization to request
- Validates key is active

### Role-Based Authorization

Checks user roles from JWT:

- Supports multiple roles per user
- Hierarchical roles (admin > user)
- Custom role metadata

### Permission-Based Authorization

Checks user permissions:

- Fine-grained permissions (e.g., `users:read`, `users:write`)
- Resource-level permissions
- Tenant-scoped permissions

### Tenant Validation

Ensures tenant context is present:

- Validates `x-organization-id` header
- Checks user belongs to tenant
- Prevents cross-tenant access

## Usage Example

```bash
/skill auth-guards --type=jwt,roles,tenant --roles='admin,user,moderator'
```

## Related Files

- [Decorator Custom](../decorator-custom/SKILL.md) - Decorators for guards
- [API Controller](../../core/api-controller/SKILL.md) - Controllers with guards
