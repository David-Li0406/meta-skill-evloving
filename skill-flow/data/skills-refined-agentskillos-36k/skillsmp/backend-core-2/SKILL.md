---
name: backend-core
description: Design and implement backend APIs, services, JPA entities, and security with Java/Spring Boot. Use for API design, controller/service implementation, database modeling, and security patterns.
---

# Backend Core Skill

## When to Use

- Creating or modifying REST API endpoints
- Designing DTOs, entities, or database schema
- Implementing service layer business logic
- Adding security (OTP, rate limiting, audit logging)
- Working with files under `backend/`

---

## CRITICAL: Security Requirements

### OTP Step-up Authentication (MANDATORY)

**Gated Actions:**
- **Redeem** (사용하기): MUST verify OTP session before creating RedeemSession
- (Optional) Profile edit, account recovery

**Implementation:**
- Service layer checks: `OtpSession.isValid()` before critical action
- Session TTL: ~10 min
- Return 403 with `"OTP_REQUIRED"` error code if not verified

**Anti-patterns:**
- NEVER trust client-side "otpVerified" flag
- ALWAYS validate backend-side session

### Rate Limiting & Brute-force Protection
- Phone + name lookup is brute-force risky → add rate limits & cooldown
- Owner-only endpoints must be protected
- Terminal shares owner session in MVP (OK), but log all actions

### Audit Logging
Log issuance/redeem/migration events with:
- walletId, storeId, stampCardId, timestamp, result

---

## Stack

**Default:**
- Java 17
- Spring Boot 3.x
- Spring Web
- Validation (Bean Validation)
- Spring Data JPA
- MySQL

**Optional (only if needed):**
- Spring Security
- Redis (TTL / rate limiting)
- Testcontainers

---

## Architecture

### Package Strategy (Feature-based)

```
com.project.kkookk
  global/
    config/
    security/
    exception/
    response/
    util/
  owner/
    controller/
    service/
    repository/
    domain/
  store/
    controller/
    service/
    repository/
    domain/
  stampcard/
    controller/
    service/
    repository/
    domain/
  wallet/
    controller/
    service/
    repository/
    domain/
  issuance/
    controller/
    service/
    repository/
    domain/
  redeem/
    controller/
    service/
    repository/
    domain/
  migration/
    controller/
    service/
    repository/
    domain/
  qrcode/
    controller/
    service/
    exception/
```

### Layer Responsibilities
- **Controller:** HTTP + DTO mapping + validation
- **Service:** use case orchestration + transactions
- **Domain:** entities, value objects, domain logic (invariants, rules)
- **Repository:** persistence & queries

Keep controllers thin. Put orchestration in services, business rules in domain.

---

## Code Style

**Base:** Google Java Style, with these overrides:
- Indentation: 4 spaces
- Max line length: 120

### Naming Conventions
- Use camelCase for variables/methods/classes
- Avoid unclear names: `Data`, `Info`, `Item`, `Util`, `Common`
- Avoid abbreviations if possible

**Boolean naming:**
- Local boolean variables: prefix with `is...` (e.g., `boolean isValid`)
- Entity boolean fields: **no** `is` prefix (Lombok getter issue). Example: `private boolean active;`

**Find vs Get:**
- `find*`: may not exist → return Optional / empty list
- `get*`: must exist → throw exception when missing

### Lombok Allowed
- `@Getter`, `@Builder`, `@RequiredArgsConstructor`, `@Slf4j`
- JPA Entity: `@NoArgsConstructor(access = PROTECTED)`

### Imports
- No wildcard imports
- Avoid static imports in production (tests can use assert static imports)

### Braces
Never omit braces (`{}`), even for single-line if.

### Complexity Guardrails
- Keep nesting depth around 2
- Prefer early returns and method extraction

---

## API Design (Required Output Format)

Before implementing an API, always output this structure:

### 1) Endpoints
- method + path
- auth
- status codes

### 2) Request/Response DTOs

### 3) DB Model
- tables + main columns
- indexes (only if needed)

### 4) Validation & Exceptions

### 5) Implementation Steps
- Controller → Service → Repository

### 6) Test Cases
- success
- failure

### 7) API Design Checklist (MVP)
- Swagger/OpenAPI disabled (MVP)
- API contracts documented (DTO + status codes + error format)

### MVP Constraints
- Prefer polling over websockets
- Keep TTL & idempotency explicit in spec

---

## Persistence (JPA)

### General
- Use JPA entities for aggregates
- Use `@Transactional` on service layer
- Read-only queries: `@Transactional(readOnly = true)`

### Index Hint
- Index wallet/store IDs for fast lookups

### Idempotency
- Prefer unique constraints (e.g., one active session per reward) to enforce one-time completion

---

## PR Checklist

- [ ] DTO validation exists
- [ ] Error response consistent
- [ ] Transaction boundaries correct
- [ ] Idempotency / TTL considered where needed
- [ ] Tests added (success + failure)
- [ ] No secrets in config
