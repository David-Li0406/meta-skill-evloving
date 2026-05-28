---
name: api-schema-zod
description: Generate Zod validation schemas for reusable API contracts shared between backend and frontend. Use when creating type-safe schemas or sharing validation between projects.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Zod Schemas

## Purpose

Generate Zod validation schemas that can be used both on the backend for validation and shared with the frontend for type-safe API contracts.

## When to Use

- Creating reusable validation schemas
- Sharing schemas between backend and frontend
- Type-safe API contracts
- Runtime validation with TypeScript inference

## What It Generates

### Directory Structure

```
packages/shared-schemas/src/schemas/{feature}/
├── {entity}.schema.ts
├── index.ts
```

## Patterns Enforced

### Schema Reusability

- Common schemas (email, password, UUID) imported from shared
- Schemas composable via `.pick()`, `.omit()`, `.extend()`
- Transformations for data normalization

### Type Inference

- `z.infer<typeof schema>` for TypeScript types
- Types can be exported to frontend

### Error Messages

- Custom validation messages
- User-friendly error descriptions

## Usage Example

```bash
/skill schema-zod --name=User --fields='email:email,password:password,name:string,isActive:boolean'
```

## Related Files

- [API DTO](../../core/api-dto/SKILL.md) - Class-validator DTOs (alternative)
- [API Controller](../../core/api-controller/SKILL.md) - Controllers using schemas
