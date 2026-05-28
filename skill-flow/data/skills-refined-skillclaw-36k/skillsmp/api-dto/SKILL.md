---
name: api-dto
description: Generate DTOs with class-validator decorators, transformation logic, partial update DTOs, and response DTOs that exclude sensitive fields. Use when creating request/response DTOs or adding validation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# API DTO

## Purpose

Generate Data Transfer Objects (DTOs) with class-validator decorators, transformation logic, partial DTOs for updates, and response DTOs that exclude sensitive fields.

## When to Use

- Creating request/response DTOs
- Adding validation to inputs
- Type-safe API contracts
- Excluding sensitive fields from responses

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/dto/
├── create-{entity}.dto.ts
├── update-{entity}.dto.ts
├── {entity}-response.dto.ts
├── list-{entities}.dto.ts
└── index.ts
```

## Patterns Enforced

### Validation Decorators

Use `class-validator` decorators:

- `@IsString()`, `@IsEmail()`, `@IsUUID()`, etc.
- `@MinLength()`, `@MaxLength()`, etc.
- Custom validation messages
- `@ValidateNested()` for nested objects

### Transformation

Use `class-transformer`:

- `@Transform()` for trimming strings
- `@Type()` for nested type conversion
- Automatic lowercase for emails

### Partial Updates

Update DTOs extend PartialType from `@nestjs/swagger`:

- All fields optional
- Preserves validation on provided fields

### Response DTOs

- Exclude sensitive fields (passwords, tokens)
- Use `@Expose()` for explicit field control
- Transform dates to ISO strings

## Usage Example

```bash
/skill api-dto --name=User --fields='email:email,password:password,name:string,isActive:boolean'
```

## Related Files

- [API Controller](../api-controller/SKILL.md) - Controllers using DTOs
- [Feature CQRS](../feature-cqrs/SKILL.md) - Commands/queries with DTOs
