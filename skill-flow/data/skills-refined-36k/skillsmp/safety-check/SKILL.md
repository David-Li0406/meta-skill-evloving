---
name: safety-check
description: Audit code for runtime safety and security vulnerabilities. Use when reviewing code, before commits, or performing security assessments.
allowed-tools: ["shell", "read_file"]
metadata:
  short-description: Comprehensive safety audit
---

# Safety Audit

**Read this reference:**
- `~/.config/agent/domain/coding/safety.md` - Complete safety checklist (Part 1: Runtime, Part 2: Security)

## Instructions

Perform comprehensive safety audit covering both runtime and security:

### Part 1: Runtime Safety (9 Categories)

1. **Nil/Null Pointer Dereferences**
   - All pointer dereferences checked
   - Optional/Result types properly unwrapped
   - No assumptions about non-nil values

2. **Race Conditions & Data Races**
   - Shared mutable state properly synchronized
   - Mutex usage correct (defers, no double-locks)
   - No unprotected concurrent access

3. **Resource Leaks**
   - File handles closed (defers)
   - Connections released
   - Memory freed (in manual-memory languages)
   - Contexts cancelled

4. **Buffer Overflows & Bounds Checking**
   - Array/slice access within bounds
   - String operations safe
   - No unchecked buffer writes

5. **Integer Overflow/Underflow**
   - Arithmetic checked for overflow
   - Type conversions validated
   - Size calculations safe

6. **Uninitialized Values**
   - All variables initialized before use
   - No reliance on zero values unless intentional

7. **Error Handling**
   - All errors checked and handled
   - No ignored errors
   - Error context preserved (wrapping)

8. **Panics/Crashes**
   - No panic in library code (return errors)
   - Recover only where appropriate
   - Graceful degradation

9. **Deadlocks**
   - Consistent lock ordering
   - No circular dependencies
   - Timeouts on blocking operations

### Part 2: Security Safety (OWASP Top 10+)

1. **Injection Vulnerabilities**
   - SQL injection (use parameterized queries)
   - Command injection (avoid shell, sanitize input)
   - XSS (escape output, CSP headers)

2. **Authentication & Authorization**
   - Proper credential storage (hashed, salted)
   - Session management secure
   - Authorization checks on all resources

3. **Sensitive Data Exposure**
   - No hardcoded secrets
   - Encryption for data at rest/in transit
   - No secrets in logs

4. **Input Validation**
   - All external input validated
   - Type checking, range checking
   - Sanitization before use

5. **Cryptography**
   - Use standard libraries (no custom crypto)
   - Secure random number generation
   - Proper key management

## Arguments

Target file(s) or package(s): ${ARGUMENTS}
