---
name: error-code-guide
description: Use this skill when you need to design consistent error codes following the PREFIX_CATEGORY_NUMBER format for better debugging, monitoring, and user experience.
---

# Error Code Guide

## Purpose

This skill helps design consistent error codes that follow a standard format, enabling better debugging, monitoring, and user experience.

## Quick Reference

### Error Code Format

```
<PREFIX>_<CATEGORY>_<NUMBER>
```

| Element | Description | Example |
|---------|-------------|---------|
| PREFIX  | Application/Service identifier | AUTH, PAY, USR |
| CATEGORY| Error category | VAL, SYS, BIZ |
| NUMBER  | Unique numeric identifier | 001, 100, 404 |

### Examples

```
AUTH_VAL_001    → Authentication validation error
PAY_SYS_503     → Payment system unavailable
USR_BIZ_100     → User business rule violation
API_NET_408     → API network timeout
```

### Error Categories

| Category | Full Name   | Description                     | HTTP Status Code |
|----------|-------------|---------------------------------|-------------------|
| **VAL**  | Validation  | Client input validation failure  | 400               |
| **BIZ**  | Business    | Business rule violation          | 422               |
| **SYS**  | System      | Internal system error            | 500               |
| **NET**  | Network     | Communication error              | 502/503/504       |
| **AUTH** | Auth        | Security-related error           | 401/403           |

### Category Number Ranges

| Range          | Description         | Example                     |
|----------------|---------------------|-----------------------------|
| *_VAL_001-099 | Field validation     | Missing required field      |
| *_VAL_100-199 | Format validation    | Invalid email format        |
| *_VAL_200-299 | Constraint validation| Password too short          |
| *_BIZ_001-099 | Status violation     | Order has been canceled     |
| *_BIZ_100-199 | Rule violation       | Cannot return after 30 days |
| *_BIZ_200-299 | Limit violation      | Exceeded daily limit        |
| *_AUTH_001-099| Authentication       | Incorrect username/password  |
| *_AUTH_100-199| Authorization        | Insufficient permissions     |
| *_AUTH_200-299| Token/Session        | Token has expired           |

## HTTP Status Code Mapping

| Category | HTTP Status Code | Description         |
|----------|------------------|---------------------|
| VAL      | 400              | Bad Request          |
| BIZ      | 422              | Unprocessable Entity  |
| AUTH (001-099) | 401       | Unauthorized         |
| AUTH (100-199) | 403       | Forbidden            |
| SYS      | 500              | Internal Server Error |
| NET      | 502/503/504      | Gateway errors       |

## Detailed Guide

For complete standards, please refer to:
- [Error Code Standards](../../../core/error-code-standards.md)

### AI Optimized Format (Token Saving)

AI assistants can use YAML format files to reduce token usage:
- Basic standard: `ai/standards/error-codes.ai.yaml`

## Error Response Format

### Single Error

```json
{
  "success": false,
  "error": {
    "code": "AUTH_VAL_001",
    "message": "Email is a required field",
    "field": "email",
    "requestId": "req_abc123"
  }
}
```

### Multiple Errors

```json
{
  "success": false,
  "errors": [
    {
      "code": "AUTH_VAL_001",
      "message": "Email is a required field",
      "field": "email"
    },
    {
      "code": "AUTH_VAL_201",
      "message": "Password must be at least 8 characters",
      "field": "password"
    }
  ],
  "requestId": "req_abc123"
}
```

## Internal Error Object

```typescript
// Example TypeScript definition for internal error object
interface InternalError {
  code: string;
  message: string;
  field?: string;
  requestId: string;
}
```