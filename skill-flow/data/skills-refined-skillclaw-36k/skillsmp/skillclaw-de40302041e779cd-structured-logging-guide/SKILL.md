---
name: structured-logging-guide
description: Use this skill when you need to implement consistent, structured, and actionable application logging across all environments.
---

# Skill Body

## Purpose

This skill helps in implementing consistent, structured, and actionable application logging across all environments.

## Quick Reference

### Log Levels

| Level   | Code | Usage Scenario               | Production Environment |
|---------|------|------------------------------|------------------------|
| **TRACE** | 10   | Very detailed debug information | Off                    |
| **DEBUG** | 20   | Detailed debug information    | Off                    |
| **INFO**  | 30   | Normal operational events      | On                     |
| **WARN**  | 40   | Potential issues, recoverable  | On                     |
| **ERROR** | 50   | Errors that need attention     | On                     |
| **FATAL** | 60   | Severe failures                | On                     |

### Level Selection Decision Tree

```
Is it only for debugging?               → DEBUG (Off in production)
Is it a normal operation completion?    → INFO
Is it an unexpected but non-problematic situation? → WARN
Did the operation fail?                  → ERROR
Can the application continue?            → FATAL
```

### Usage Scenarios for Each Level

| Level   | Example                                      |
|---------|----------------------------------------------|
| **TRACE** | Function entry/exit, loop iterations, variable values |
| **DEBUG** | State changes, setting values, query parameters |
| **INFO**  | Application start/stop, user actions, scheduled tasks |
| **WARN**  | Deprecated API, retry attempts, resource nearing limits |
| **ERROR** | Failed operations, caught exceptions, integration failures |
| **FATAL** | Unrecoverable errors, startup failures, loss of critical resources |

## Structured Logging

### Required Fields

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "User logged in successfully",
  "service": "auth-service",
  "environment": "production"
}
```

### Suggested Fields

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "User logged in successfully",
  "service": "auth-service",
  "environment": "production",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "usr_12345",
  "request_id": "req_67890",
  "duration_ms": 150,
  "http_method": "POST",
  "http_path": "/api/v1/login",
  "http_status": 200
}
```

### Field Naming Conventions

Use `snake_case` with domain prefixes:

| Domain | Common Fields                          |
|--------|----------------------------------------|
| HTTP   | http_method, http_path, http_status, http_duration_ms |
| Database | db_query_type, db_table, db_duration_ms, db_rows_affected |
| Queue  | queue_name, queue_message_id, queue_delay_ms |
| User   | user_id, user_role, user_action       |
| Request | request_id, trace_id, span_id         |

## Detailed Guide

For complete standards, refer to:
- [Logging Standards](../../../core/logging-standards.md)

### Sensitive Data Handling

#### Absolutely Do Not Log

- Passwords or secrets
- API keys or tokens
- Credit card numbers
- Identification numbers
- Complete authentication tokens

#### Masking or Redacting

```javascript
// Bad
logger.info('Login attempt', { password: userPassword });

// Good
logger.info('Login attempt', { password: '***REDACTED***' });
```