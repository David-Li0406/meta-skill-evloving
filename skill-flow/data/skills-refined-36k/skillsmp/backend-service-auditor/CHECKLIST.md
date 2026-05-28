# Backend Service Audit Checklist

Complete checklist for auditing backend services. Work through each section systematically.

---

## Security

### Authentication & Authorization

- [ ] **AuthN correctness** - Verify authentication flows cannot be bypassed
- [ ] **AuthZ correctness** - Confirm authorization checks on all protected endpoints
- [ ] **Tenant isolation** - Multi-tenant data properly scoped to tenant
- [ ] **IDOR vulnerabilities** - Object references validated against user permissions
- [ ] **Privilege escalation** - Role changes and admin functions properly protected
- [ ] **Session management** - Secure session handling, proper expiration
- [ ] **JWT pitfalls** - Algorithm confusion, missing expiry, weak secrets
- [ ] **API key security** - Keys properly scoped, rotatable, revocable

### Input Validation & Injection

- [ ] **Input validation** - All user input validated and sanitized
- [ ] **SQL injection** - Parameterized queries, no string concatenation
- [ ] **Command injection** - No shell execution with user input
- [ ] **SSRF vulnerabilities** - URL inputs validated, allowlists enforced
- [ ] **Path traversal** - File paths sanitized, no `../` exploitation
- [ ] **Deserialization** - Safe deserialization, no arbitrary object instantiation
- [ ] **XML/XXE** - External entity processing disabled
- [ ] **Template injection** - User input not in template expressions

### Secrets & Sensitive Data

- [ ] **Secrets in code** - No hardcoded credentials, API keys, or tokens
- [ ] **Secrets in logs** - No PII, tokens, or passwords logged
- [ ] **Environment variables** - Secrets loaded from env/vault, not config files
- [ ] **Key rotation readiness** - Can rotate secrets without downtime
- [ ] **Token storage** - Tokens stored securely (httpOnly cookies, encrypted)
- [ ] **Data encryption** - Sensitive data encrypted at rest and in transit

### Dependencies & Configuration

- [ ] **Vulnerable packages** - No known CVEs in dependencies
- [ ] **Outdated dependencies** - Dependencies reasonably up to date
- [ ] **Unsafe defaults** - Security-relevant config explicitly set
- [ ] **Debug mode** - Debug/development flags disabled in production
- [ ] **Error exposure** - Stack traces not exposed to clients

### Web Security (if applicable)

- [ ] **CORS configuration** - Origins properly restricted
- [ ] **CSRF protection** - State-changing requests protected
- [ ] **Security headers** - CSP, HSTS, X-Frame-Options set
- [ ] **Cookie security** - Secure, HttpOnly, SameSite flags set
- [ ] **Rate limiting** - Brute force and abuse prevention

---

## Reliability & Correctness

### Idempotency & Retries

- [ ] **Idempotent writes** - POST/PUT operations safe to retry
- [ ] **Idempotency keys** - Client-provided keys for critical operations
- [ ] **Retry strategy** - Exponential backoff with jitter
- [ ] **Retry limits** - Max retries defined, dead letter handling
- [ ] **Circuit breakers** - Failing dependencies don't cascade
- [ ] **Timeouts** - All external calls have timeouts
- [ ] **Bulkheads** - Resource isolation prevents total failure

### Concurrency & Race Conditions

- [ ] **Race conditions** - Concurrent requests handled safely
- [ ] **Double-spend** - Financial operations atomic and locked
- [ ] **Ordering guarantees** - Event ordering preserved where needed
- [ ] **Optimistic locking** - Version checks prevent lost updates
- [ ] **Pessimistic locking** - Critical sections properly locked
- [ ] **Transaction boundaries** - ACID properties maintained
- [ ] **Distributed locks** - Coordination across instances correct

### Data Integrity

- [ ] **DB constraints** - Foreign keys, unique constraints, checks in place
- [ ] **Migration safety** - Migrations reversible, no data loss
- [ ] **Referential integrity** - Cascades and orphan prevention
- [ ] **Outbox pattern** - Events reliably published after DB commit
- [ ] **Inbox pattern** - Duplicate messages handled
- [ ] **Eventual consistency** - Async flows converge correctly

### Error Handling

- [ ] **Error taxonomy** - Retryable vs non-retryable distinguished
- [ ] **Error propagation** - Errors bubble up with context
- [ ] **Partial failures** - Graceful degradation, not total failure
- [ ] **Compensation** - Failed sagas have rollback logic
- [ ] **Client errors** - 4xx vs 5xx correctly distinguished

---

## Performance & Scalability

### Database Performance

- [ ] **N+1 queries** - Batch loading, no loops with queries
- [ ] **Missing indexes** - Query plans use indexes
- [ ] **Slow queries** - No unbounded or expensive operations
- [ ] **Connection pooling** - Pool size appropriate, connections reused
- [ ] **Query timeouts** - Long queries cancelled
- [ ] **Read replicas** - Read traffic distributed if applicable

### API Performance

- [ ] **Pagination** - All list endpoints paginated with limits
- [ ] **Payload size** - Responses reasonably sized, no over-fetching
- [ ] **Field selection** - Clients can request only needed fields
- [ ] **Compression** - Gzip/Brotli for large responses
- [ ] **Streaming** - Large files streamed, not buffered

### Caching

- [ ] **Cache correctness** - Cache invalidated on updates
- [ ] **Cache stampede** - Thundering herd prevention
- [ ] **TTL appropriateness** - Cache TTLs match data freshness needs
- [ ] **Cache key design** - Keys include tenant/user scope
- [ ] **Cold start** - System functions without warm cache

### Resource Management

- [ ] **Memory usage** - No unbounded growth, leaks prevented
- [ ] **File handles** - Resources properly closed
- [ ] **Thread/connection pools** - Bounded and monitored
- [ ] **Large file handling** - Streaming, temp file cleanup

---

## Observability & Operations

### Logging

- [ ] **Structured logs** - JSON format with consistent fields
- [ ] **Request ID** - Correlation ID propagated across services
- [ ] **Log levels** - Appropriate use of debug/info/warn/error
- [ ] **Sensitive data** - No PII, secrets, or tokens in logs
- [ ] **Log volume** - Not excessive, won't fill disk

### Metrics & Tracing

- [ ] **Request metrics** - Latency, throughput, error rate tracked
- [ ] **Business metrics** - Domain-specific KPIs instrumented
- [ ] **Distributed tracing** - Spans propagated across services
- [ ] **SLOs defined** - Target latency and availability documented
- [ ] **Queue metrics** - Lag, depth, processing rate monitored

### Alerting

- [ ] **Latency alerts** - P50/P95/P99 thresholds set
- [ ] **Error rate alerts** - Spike detection configured
- [ ] **Queue lag alerts** - Consumer falling behind detected
- [ ] **Dead letters** - Failed message alerts configured
- [ ] **Resource alerts** - CPU, memory, disk thresholds set

### Deployment & Operations

- [ ] **Feature flags** - New features toggleable
- [ ] **Rollback plan** - Can revert quickly if issues arise
- [ ] **Migration safety** - DB migrations tested, reversible
- [ ] **Canary deploys** - Gradual rollout capability
- [ ] **Health checks** - Liveness and readiness probes configured
- [ ] **Graceful shutdown** - In-flight requests completed on shutdown
- [ ] **Runbooks** - Operational procedures documented

---

## Quick Reference: Common Issues by Stack

### Node.js / TypeScript
- Prototype pollution
- Event loop blocking
- Unhandled promise rejections
- Memory leaks in closures

### Python
- Pickle deserialization
- SQL injection with f-strings
- GIL blocking in async code
- Import-time side effects

### Go
- Goroutine leaks
- Context cancellation handling
- Nil pointer dereferences
- Race conditions (use `-race`)

### Java / Spring
- Deserialization vulnerabilities
- SpEL injection
- Bean scope issues
- Transaction propagation

---

## Severity Classification Guide

| Severity | Criteria | Examples |
|----------|----------|----------|
| **CRITICAL** | Exploitable now, data breach imminent | SQL injection, auth bypass, exposed secrets |
| **HIGH** | Serious vulnerability, needs immediate fix | IDOR, missing auth on endpoint, unsafe deserialization |
| **MEDIUM** | Should fix soon, moderate risk | Missing rate limiting, verbose errors, weak session |
| **LOW** | Minor issue, fix when convenient | Outdated dependency (no CVE), missing headers |
| **INFO** | Observation, no immediate action | Code smell, potential improvement |
