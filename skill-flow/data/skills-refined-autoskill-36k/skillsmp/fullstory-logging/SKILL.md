---
name: fullstory-logging
version: v3
description: Core concepts for Fullstory's Logging API. Platform-agnostic guide covering log levels, message formatting, privacy considerations, and best practices. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
related_skills:
  - fullstory-observe-callbacks
  - fullstory-analytics-events
  - fullstory-async-methods
---

# Fullstory Logging API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's Logging API allows developers to send log messages directly to Fullstory sessions. These logs appear in the session replay, providing valuable context for debugging user issues, tracking application state, and understanding user workflows—without cluttering the device's console or logging systems.

Key use cases:
- **Error Context**: Log errors with stack traces viewable in replay
- **Application State**: Record important state changes
- **Debugging**: Add contextual information during development
- **Audit Trail**: Log significant user actions
- **Support Context**: Add logs that support teams can see in sessions

---

## Core Concepts

### Log Levels

All platforms support the same log levels, though the syntax differs:

| Level | Use For | Severity |
|-------|---------|----------|
| `log` | General information | Lowest |
| `info` | Informational messages | Low |
| `warn` | Warning conditions | Medium |
| `error` | Error conditions | High |
| `debug` | Debug information | Varies |

### Key Behaviors

| Behavior | Description |
|----------|-------------|
| **Session-only** | Logs appear in Fullstory session replay, not device console |
| **Session context** | Logs viewable in session replay timeline |
| **Timestamped** | Automatically timestamped by Fullstory |
| **Searchable** | Can search sessions by log content |
| **String messages** | All platforms require string messages |

### When to Use FS Logging vs Device Console

| Use FS Logging | Use Device Console |
|----------------|-------------------|
| Production errors you want in replay | Development-only debugging |
| State changes for support context | Verbose tracing during development |
| User action audit trails | Performance timing logs |
| Integration errors | Internal debugging |
| Customer-facing error context | CI/CD diagnostics |

---

## Data Privacy

**Never log sensitive data:**
- ❌ Passwords, API keys, tokens
- ❌ Credit card numbers, CVVs
- ❌ Social Security numbers
- ❌ Personal health information
- ❌ Full email addresses (use user IDs instead)

**Safe to log:**
- ✅ User IDs (non-PII identifiers)
- ✅ Action names and types
- ✅ Error messages and codes
- ✅ Application state indicators
- ✅ Timing and performance metrics

---

## Best Practices

### 1. Use Appropriate Log Levels

```
debug   → Development troubleshooting, verbose details
log     → General operational information
info    → Significant but normal events
warn    → Potential issues, degraded functionality
error   → Failures requiring attention
```

### 2. Structure Log Messages Consistently

- Include context: action name, identifiers, state
- Use consistent prefixes for categorization: `[Auth]`, `[Payment]`, `[API]`
- Include relevant IDs for correlation
- Keep messages concise but informative

### 3. Log Strategically

**Good to log:**
- API failures and errors
- Authentication events (login/logout)
- Critical user actions (checkout, form submit)
- State transitions
- Third-party integration events

**Avoid logging:**
- Every mouse movement or scroll
- High-frequency events in loops
- Sensitive/PII data
- Redundant information

### 4. Create Centralized Logging Utilities

Build wrapper functions that:
- Add consistent formatting
- Include timestamps and context
- Check for Fullstory availability
- Sanitize potentially sensitive data

---

## Rate Limits and Constraints

| Constraint | Limit |
|------------|-------|
| Message type | String only (no objects) |
| Rate limiting | Standard API rate limits apply |
| Excessive logging | May be throttled |
| Message length | Keep concise; very long messages may be truncated |

---

## Common Patterns

### Error Logging Pattern

1. Capture error details (message, type, stack)
2. Add context (action, state, identifiers)
3. Format as readable string
4. Send to Fullstory with `error` level
5. Optionally send to other error tracking services

### Audit Trail Pattern

1. Define standard action format
2. Include timestamp, action name, details
3. Use `info` level for normal operations
4. Use `warn` for unusual but valid actions
5. Use `error` for failed operations

### Integration Logging Pattern

1. Log connection attempts
2. Log successful connections
3. Log disconnections with reasons
4. Log errors with operation context
5. Log timeouts with duration

---

## Key Takeaways for Agent

When helping developers implement Fullstory logging:

1. **Always emphasize**:
   - Message format: Always pass strings, not objects or arrays
   - Privacy: Never log PII, passwords, or sensitive data
   - Log levels: Use appropriate severity levels
   - Frequency: Log significant events, not every operation

2. **Common mistakes to watch for**:
   - Logging objects instead of strings
   - Including PII in log messages
   - Excessive logging causing noise
   - Using wrong log levels

3. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Web Logging**: https://developer.fullstory.com/browser/fullcapture/logging/
- **iOS Logging**: https://developer.fullstory.com/mobile/ios/logging/
- **Android Logging**: https://developer.fullstory.com/mobile/android/logging/
- **Help Center - Console Logs**: https://help.fullstory.com/hc/en-us/articles/360020623154
