---
name: data-validation
description: Security pattern for input validation and sanitization. Use when implementing input handling, preventing injection attacks (SQL, XSS, command), ensuring data integrity, or processing data from untrusted sources. Addresses "Entity provides unexpected data" problem.
---

# Data Validation Security Pattern

Ensures all incoming data is validated against specifications before processing, preventing injection attacks, data corruption, and unexpected behavior.

## Problem Addressed

**Entity provides unexpected data**: Malicious or malformed input causes:
- Injection attacks (SQL, XSS, command injection)
- System crashes or unexpected behavior
- Data corruption
- Security bypasses

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Entity** | Entity | Sends data to system |
| **Enforcer** | Enforcement Point | Intercepts all incoming data |
| **Validator** | Decision Point | Validates data against specification |
| **Specification Provider** | Information Point | Manages validation rules |
| **System** | Entity | Processes validated data |

### Data Elements

- **data**: Input from entity (raw)
- **canonical_data**: Normalized, validated form
- **specification**: Rules defining valid data
- **type**: Identifier for applicable specification
- **error**: Validation failure message

## Validation Flow

```
Entity → [data] → Enforcer
Enforcer → [data] → Validator
Validator → [get_specification(type)] → Specification Provider
Specification Provider → [specification] → Validator
Validator → [validate, transform to canonical] → Validator
Validator → [canonical_data or error] → Enforcer
Enforcer → [canonical_data] → System (if valid)
        → [error] → Entity (if invalid)
```

1. Enforcer intercepts ALL incoming data
2. Validator retrieves appropriate specification
3. Validator transforms to canonical form
4. Validator checks against specification
5. Valid: canonical data forwarded to System
6. Invalid: error returned to Entity

## Validation Principles

### Validate Everything
- All data from uncontrolled sources
- Parameters, headers, cookies, files
- Data from APIs, databases (defense in depth)

### Canonical Form
Transform data to standardized form:
- Remove/escape special characters
- Decode encoded values
- Normalize Unicode
- Parse structured data to typed objects

**Benefit**: System only processes data in known format.

### Allowlist vs. Blocklist
- **Allowlist (preferred)**: Define what IS allowed
- **Blocklist (risky)**: Define what is NOT allowed

Blocklists fail against unknown attack patterns. Use allowlists.

### Validate Early, Validate Often
- Validate at system boundary (earliest point)
- Re-validate near code that relies on data
- Defense in depth

## Validation Types

### Type Validation
- Ensure data matches expected type
- Integer, string, boolean, date, email, URL

### Range/Length Validation
- Numeric bounds
- String length limits
- Array size limits

### Format Validation
- Regular expressions (carefully!)
- Structural patterns
- Protocol conformance

### Business Logic Validation
- Application-specific rules
- Cross-field validation
- State-dependent validation

## Security Considerations

### Validation ≠ Authorization
- Validation: Is this data well-formed?
- Authorization: Is entity allowed to use this data?

Both are required. Valid data doesn't mean authorized access.

### Error Messages
- Don't reveal validation internals to attackers
- Log detailed errors server-side
- Return generic errors to clients

### Encoding Output
Validation alone doesn't prevent all injection:
- Still encode output for context (HTML, SQL, etc.)
- Use parameterized queries
- Use context-appropriate escaping

### File Uploads
Special validation needed:
- Verify content type (not just extension)
- Scan for malware
- Restrict file sizes
- Store outside web root

### Structured Data (JSON, XML)
- Parse with secure parser
- Disable external entity processing (XXE)
- Validate against schema
- Limit nesting depth

### Regular Expression Safety
- Avoid ReDoS-vulnerable patterns
- Limit input length before regex
- Test regex performance with malicious input

## Common Validation Scenarios

| Input Type | Validations |
|------------|-------------|
| Username | Length, allowed characters, no control chars |
| Email | Format, length, allowlist domains (if applicable) |
| Integer | Type, range, positive/negative |
| URL | Protocol allowlist, format, no javascript: |
| File | Extension, content-type, size, malware scan |
| JSON | Schema validation, depth limits, size limits |

## Implementation Checklist

- [ ] All entry points have validation
- [ ] Canonical form transformation
- [ ] Allowlist-based rules
- [ ] Type checking
- [ ] Length/range limits
- [ ] Business rule validation
- [ ] Secure error handling
- [ ] Output encoding (separate from validation)
- [ ] File upload validation
- [ ] Structured data parsing safely
- [ ] Re-validation near sensitive operations

## Related Patterns

- Authorisation (validation doesn't replace authorization)
- Selective encrypted transmission (protect data in transit)
- Log entity actions (log validation failures)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/04_01_001__data_validation/
- OWASP Input Validation Cheat Sheet
- OWASP XSS Prevention Cheat Sheet
