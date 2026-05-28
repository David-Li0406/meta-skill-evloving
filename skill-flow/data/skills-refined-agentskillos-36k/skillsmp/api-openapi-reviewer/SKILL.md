---
name: api-openapi-reviewer
description: Reviews code for OpenAPI documentation completeness, ensuring all API endpoints have proper tags, summaries, descriptions, response codes, and DTO schemas
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
---

## Purpose

Reviews code for OpenAPI documentation completeness, ensuring all API endpoints have proper tags, summaries, descriptions, response codes, and DTO schemas.

## Responsibilities

### Controller Documentation Checks

1. **Required Decorators**
   - Check for `@ApiTags()` on all controllers
   - Check for `@ApiBearerAuth()` when authentication is required
   - Verify `@ApiOperation()` with summary on all endpoints
   - Verify `@ApiResponse()` for all possible status codes

2. **Response Documentation**
   - Success response with type/schema
   - Error responses for all possible error codes
   - Proper error schema examples

3. **DTO Documentation**
   - All DTO fields have `@ApiProperty()`
   - Example values provided
   - Required fields marked
   - Nullable fields marked
   - Array types specified

## Checks Performed

### Controller Level

- [ ] `@ApiTags()` present
- [ ] `@ApiBearerAuth()` present (if auth required)
- [ ] Guard documented

### Endpoint Level

- [ ] `@ApiOperation()` with summary
- [ ] `@ApiResponse()` for success (with type)
- [ ] `@ApiResponse()` for 400 (validation errors)
- [ ] `@ApiResponse()` for 401 (unauthorized)
- [ ] `@ApiResponse()` for 403 (forbidden)
- [ ] `@ApiResponse()` for 404 (not found)
- [ ] `@ApiResponse()` for 409 (conflict)
- [ ] `@ApiResponse()` for other relevant errors

### DTO Level

- [ ] All fields have `@ApiProperty()`
- [ ] Example values provided
- [ ] Required fields marked
- [ ] Nullable/optional fields marked
- [ ] Array types specified with `isArray: true`
- [ ] Enum types specified

## Response Code Reference

| Code | Meaning               | When to Use              |
| ---- | --------------------- | ------------------------ |
| 200  | OK                    | Successful GET, PATCH    |
| 201  | Created               | Successful POST          |
| 204  | No Content            | Successful DELETE        |
| 400  | Bad Request           | Validation errors        |
| 401  | Unauthorized          | Missing/invalid auth     |
| 403  | Forbidden             | Insufficient permissions |
| 404  | Not Found             | Resource not found       |
| 409  | Conflict              | Duplicate/conflict       |
| 422  | Unprocessable Entity  | Business logic error     |
| 429  | Too Many Requests     | Rate limit exceeded      |
| 500  | Internal Server Error | Unexpected error         |
