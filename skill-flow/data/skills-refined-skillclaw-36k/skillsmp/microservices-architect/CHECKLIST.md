# Microservices Design Checklist

Quality validation checklist for microservices designs. Use before approving any design.

---

## Prime Directive Compliance

Every design MUST satisfy these non-negotiables:

### 1. Nothing Unwatched Exists
- [ ] Service has health check endpoints (liveness + readiness)
- [ ] Key metrics are defined and will be emitted
- [ ] Logs include structured fields for debugging
- [ ] Distributed tracing is configured
- [ ] Alerts are defined for critical conditions

### 2. Produce → Publish, Consume → All
- [ ] Events have defined schemas
- [ ] Consumers handle full event payload (no cherry-picking)
- [ ] Schema versioning strategy is defined

### 3. Pub/Sub by Default
- [ ] Async communication is the default
- [ ] Events are used for state changes
- [ ] Commands are used for requests requiring response

### 4. Async by Default
- [ ] Synchronous calls are justified
- [ ] Sync calls are isolated with feature flags
- [ ] Timeouts are configured for all sync calls

### 5. Explicit Trust
- [ ] Authentication method is specified
- [ ] Authorization rules are defined
- [ ] Trust failures emit insight events

### 6. No Surprise Failures
- [ ] Monitoring covers all failure modes
- [ ] Alerts fire before customer impact
- [ ] Dashboards show system health

### 7. Observability Over Performance
- [ ] Observability overhead is acceptable (~20-30%)
- [ ] No blind spots in the system
- [ ] Debug information is available

### 8. Bulkheading By Design
- [ ] Isolation boundaries are defined
- [ ] Resource pools are separated
- [ ] Blast radius is documented

### 9. Runtime Trust Profile
- [ ] Trust scope is defined
- [ ] Trust expiration is specified
- [ ] Policy changes don't require code changes

### 10. Operational Knobs Exposed
- [ ] Feature flags are defined
- [ ] Rate limits are configurable
- [ ] Circuit breakers are configurable

---

## Design Quality Checklist

### Architecture
- [ ] High-level architecture diagram exists
- [ ] Component responsibilities are clear
- [ ] Service boundaries are well-defined
- [ ] Data ownership is explicit

### Message Design
- [ ] Event schemas are versioned
- [ ] Command schemas are versioned
- [ ] Idempotency strategy is defined
- [ ] Message ordering requirements are documented

### Data Design
- [ ] Data model is documented
- [ ] Storage technology is justified
- [ ] Migration strategy exists
- [ ] Backup/restore is planned

### API Design
- [ ] API endpoints are documented
- [ ] Error responses are standardized
- [ ] Rate limiting is configured
- [ ] Versioning strategy is defined

---

## Operability Checklist

### Observability
- [ ] Metrics cover the four golden signals:
  - [ ] Latency
  - [ ] Traffic
  - [ ] Errors
  - [ ] Saturation
- [ ] Logs are structured and searchable
- [ ] Traces span service boundaries
- [ ] Dashboards are created

### Alerting
- [ ] Alert conditions are defined
- [ ] Alert severity levels are appropriate
- [ ] Runbooks exist for each alert
- [ ] Escalation paths are documented

### Operations
- [ ] Deployment procedure is documented
- [ ] Rollback procedure is documented
- [ ] Feature flags are configured
- [ ] Circuit breakers are configured

---

## Safety Checklist

### Resilience
- [ ] Failure modes are documented
- [ ] Recovery procedures exist
- [ ] Timeouts are configured
- [ ] Retries have backoff
- [ ] Circuit breakers prevent cascade

### Containment
- [ ] Bulkhead boundaries are defined
- [ ] Blast radius is limited
- [ ] Graceful degradation is possible

### Security
- [ ] Authentication is required
- [ ] Authorization is enforced
- [ ] Secrets are managed securely
- [ ] Data is encrypted in transit
- [ ] PII handling is compliant

---

## Testing Checklist

### Test Coverage
- [ ] Unit tests for business logic
- [ ] Integration tests for data access
- [ ] Contract tests for API consumers
- [ ] E2E tests for critical paths

### Operational Tests
- [ ] Health check tests
- [ ] Metric emission tests
- [ ] Alert condition tests
- [ ] Feature flag tests
- [ ] Circuit breaker tests

### Chaos/Resilience Tests
- [ ] Dependency failure handling
- [ ] Network partition handling
- [ ] Resource exhaustion handling

---

## Implementation Plan Checklist

### Incremental Delivery
- [ ] Work is broken into small steps
- [ ] Each step is independently deployable
- [ ] Rollback is possible at each step

### Strangler Fig (for migrations)
- [ ] Facade is in place
- [ ] Traffic can be split
- [ ] Insight events track migration progress

### Documentation
- [ ] Design doc is complete
- [ ] API docs are generated
- [ ] Runbook is written
- [ ] Architecture diagrams are updated

---

## Quick Reference: Common Mistakes

| Mistake | Fix |
|---------|-----|
| No health checks | Add liveness + readiness endpoints |
| Missing metrics | Define and emit golden signals |
| Sync by default | Convert to async with events |
| No timeouts | Add timeouts to all external calls |
| No circuit breakers | Add circuit breakers for dependencies |
| Implicit trust | Make auth/authz explicit |
| No feature flags | Add kill switches for new features |
| No rollback plan | Document rollback procedure |
| Missing schemas | Define and version all messages |
| No bulkheading | Define isolation boundaries |

---

## Sign-off Template

```markdown
## Design Review Sign-off

**Design:** [Name]
**Date:** [YYYY-MM-DD]
**Reviewer:** [Name]

### Prime Directive Compliance
- [ ] All 10 directives satisfied

### Checklist Results
| Category | Pass | Fail | N/A |
|----------|------|------|-----|
| Architecture | | | |
| Operability | | | |
| Safety | | | |
| Testing | | | |
| Implementation | | | |

### Open Issues
<!-- List any blocking issues -->

### Approval
- [ ] Approved
- [ ] Approved with conditions
- [ ] Not approved

**Comments:**
```
