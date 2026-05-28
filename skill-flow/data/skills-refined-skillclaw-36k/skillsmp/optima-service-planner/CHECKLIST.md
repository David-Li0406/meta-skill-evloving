# Optima Implementation Checklist

Quality validation checklist for Optima service implementations.

---

## Optima Prime Directive Compliance

Every implementation MUST satisfy these:

### 1. Documentation with Code
- [ ] CLAUDE.md updated with new tables
- [ ] CLAUDE.md updated with new services
- [ ] Service spec document created
- [ ] API endpoints documented
- [ ] Event contracts documented

### 2. Data Model First
- [ ] Database schema designed before coding
- [ ] Migration SQL created and reviewed
- [ ] Migration applied to dev environment
- [ ] Indexes created for query patterns
- [ ] Using TEXT instead of VARCHAR

### 3. Message Bus Communication
- [ ] Service uses RabbitMQ for all inter-service communication
- [ ] No direct HTTP calls between services
- [ ] Correlation IDs used for request/response
- [ ] Events validated with Zod schemas

### 4. One Integration Service
- [ ] Only one service talks to each external system
- [ ] Other services communicate via message bus
- [ ] Credentials loaded at startup only
- [ ] Credential rotation subscription in place

### 5. API Backend via Bus
- [ ] Website backend publishes events to services
- [ ] No direct database access from API layer
- [ ] WebSocket updates via message bus events

### 6. Errors to Notifications
- [ ] NotifyingLogger implemented
- [ ] Global error handlers registered
- [ ] Error alerts published to notification service
- [ ] logger.error() used (not console.error())

### 7. Credentials in Database
- [ ] Secrets stored in `api_credentials` or `cex_credentials` table
- [ ] Encrypted at rest
- [ ] Access logged to `credential_access_logs`
- [ ] Not using environment variables for secrets

### 8. DigitalOcean Deployment
- [ ] Dockerfile created
- [ ] .do/app.yaml created
- [ ] Health check endpoints implemented
- [ ] Environment variables documented
- [ ] Separate worker if no HTTP needed

### 9. Append-Only Contracts
- [ ] New events added to message-bus-contracts
- [ ] Existing events NOT modified
- [ ] Package version bumped
- [ ] Consumer repos updated

### 10. Stateless Services
- [ ] No in-memory state between requests
- [ ] State stored in database or message bus
- [ ] Service can restart without losing data
- [ ] Multiple instances can run safely

---

## Phase Completion Checklists

### Phase 1: Data Model

- [ ] Schema design reviewed
- [ ] Migration SQL syntax verified
- [ ] Migration applied successfully
- [ ] database-service handlers added
- [ ] DatabaseClient methods exposed
- [ ] Documentation updated

### Phase 2: Contracts

- [ ] EVENT_TYPES defined (append-only)
- [ ] QUEUES defined
- [ ] Zod schemas created
- [ ] Schemas exported from index
- [ ] Package version bumped (minor for new events)
- [ ] Published to GitHub Packages
- [ ] Consumer repos updated

### Phase 3: Core Service

- [ ] Service scaffold created
- [ ] Message bus connection established
- [ ] NotifyingLogger integrated
- [ ] Global error handlers registered
- [ ] DatabaseClient initialized
- [ ] Health check endpoints working
- [ ] Message handlers implemented
- [ ] Business logic tested
- [ ] Unit tests passing

### Phase 4: Integration

- [ ] Connected to upstream services
- [ ] Connected to downstream services
- [ ] End-to-end flow tested
- [ ] Error scenarios tested
- [ ] Error notifications verified
- [ ] Staging environment validated

### Phase 5: Deployment

- [ ] Dockerfile builds successfully
- [ ] .do/app.yaml syntax valid
- [ ] Environment variables configured
- [ ] Deployed to staging
- [ ] Staging tests passed
- [ ] Deployed to production
- [ ] Health checks passing
- [ ] Monitoring verified

### Phase 6: Documentation

- [ ] CLAUDE.md updated with new tables
- [ ] CLAUDE.md updated with new services
- [ ] CLAUDE.md updated with new commands
- [ ] README.md updated with service info
- [ ] Service-specific documentation created
- [ ] API endpoints documented
- [ ] Operational runbook created
- [ ] All documentation reviewed for accuracy

### Phase 7: Testing

- [ ] Unit tests for business logic (services/)
- [ ] Unit tests for message handlers (handlers/)
- [ ] Integration tests for message bus flow
- [ ] Integration tests for database operations
- [ ] E2E tests for complete workflows
- [ ] Operational tests for health checks
- [ ] Operational tests for feature flags
- [ ] Error notification tests
- [ ] Manual testing scenarios documented
- [ ] All tests passing in CI
- [ ] Test coverage meets threshold (80%+)
- [ ] 24-48 hour production burn-in complete

---

## Code Quality Checklist

### TypeScript

- [ ] Strict mode enabled
- [ ] `noUncheckedIndexedAccess` enabled
- [ ] No `any` types (use `unknown` if needed)
- [ ] All external input validated with Zod
- [ ] ESM imports with `.js` extensions

### Logging

- [ ] Using Pino logger (not console)
- [ ] Structured logging with context objects
- [ ] No sensitive data in logs
- [ ] Correlation IDs included
- [ ] Log levels appropriate (info, warn, error)

### Error Handling

- [ ] All errors caught and handled
- [ ] Errors published via NotifyingLogger
- [ ] Meaningful error messages
- [ ] Stack traces preserved
- [ ] No swallowed errors

### Security

- [ ] Credentials not in code or env vars
- [ ] Input validation on all endpoints
- [ ] RLS policies if user-facing
- [ ] No SQL injection vulnerabilities
- [ ] HTTPS enforced

---

## Database Checklist

### Schema

- [ ] Using TEXT instead of VARCHAR
- [ ] UUID primary keys with gen_random_uuid()
- [ ] TIMESTAMPTZ for all timestamps
- [ ] DECIMAL for financial amounts
- [ ] JSONB for flexible metadata
- [ ] Foreign keys with proper references

### Indexes

- [ ] Primary key index (automatic)
- [ ] Foreign key indexes created
- [ ] Query pattern indexes created
- [ ] Partial indexes where applicable
- [ ] No duplicate/redundant indexes

### Migrations

- [ ] Idempotent (can run multiple times)
- [ ] Down migration documented (even if commented)
- [ ] update_updated_at trigger added
- [ ] RLS enabled if user-facing

---

## Message Bus Checklist

### Events

- [ ] Event type defined in contracts
- [ ] Zod schema validates payload
- [ ] Correlation ID for request/response
- [ ] Timestamp included
- [ ] Routing key follows convention

### Handlers

- [ ] Validates incoming payload
- [ ] Handles errors gracefully
- [ ] Publishes completion/failure events
- [ ] Idempotent (can handle duplicates)
- [ ] Timeout configured

### Queues

- [ ] Queue name follows convention
- [ ] Dead letter queue configured
- [ ] Retry policy defined
- [ ] Proper ack/nack handling

---

## Deployment Checklist

### Dockerfile

- [ ] Multi-stage build (builder + runner)
- [ ] Node 20 Alpine base
- [ ] pnpm for package management
- [ ] GH_PACKAGES_TOKEN for private packages
- [ ] HEALTHCHECK instruction
- [ ] Non-root user (if applicable)

### DigitalOcean

- [ ] App spec version 2
- [ ] Correct Dockerfile path
- [ ] Health check configured
- [ ] Proper instance size
- [ ] Environment variables set
- [ ] Secrets marked as SECRET type
- [ ] Deploy on push enabled

### Monitoring

- [ ] Health endpoint returns quickly
- [ ] Readiness endpoint checks dependencies
- [ ] Logs visible in DO dashboard
- [ ] Error rate alerts configured
- [ ] Response time alerts configured

---

## Documentation Checklist

### CLAUDE.md Updates

- [ ] New tables added to database section
- [ ] New services added to services section
- [ ] New event types documented
- [ ] Build commands updated if changed
- [ ] Environment variables documented

### Service Documentation

- [ ] Purpose clearly stated
- [ ] Events consumed listed
- [ ] Events published listed
- [ ] Database operations documented
- [ ] Configuration options documented
- [ ] Error handling documented

### Operational

- [ ] Runbook created
- [ ] Alert conditions documented
- [ ] Escalation path defined
- [ ] Recovery procedures documented

---

## Testing Checklist

### Unit Tests

- [ ] Business logic functions tested
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Mocks used for dependencies
- [ ] Tests are deterministic (no flaky tests)
- [ ] Each handler has corresponding test file

### Integration Tests

- [ ] Message bus publish/subscribe tested
- [ ] Database operations tested
- [ ] Correlation ID flow verified
- [ ] Error propagation tested
- [ ] Timeout handling tested
- [ ] Real connections (not mocks) in integration tests

### E2E / Workflow Tests

- [ ] Complete workflow from trigger to completion
- [ ] Multi-service flows tested
- [ ] Failure scenarios tested
- [ ] Recovery behavior verified
- [ ] Data consistency verified
- [ ] Events published correctly

### Operational Tests

- [ ] Health check endpoints respond correctly
- [ ] Readiness checks verify dependencies
- [ ] Feature flags work as expected
- [ ] Error notifications published
- [ ] Alerting conditions verified

### Test Infrastructure

- [ ] Tests run in CI pipeline
- [ ] Test database/message bus available
- [ ] Environment variables configured for tests
- [ ] Test data setup/teardown automated
- [ ] Coverage reports generated

---

## Quick Reference: Common Mistakes

| Mistake | Fix |
|---------|-----|
| VARCHAR columns | Change to TEXT |
| Direct Supabase import | Use DatabaseClient |
| console.log/error | Use Pino logger |
| Missing NotifyingLogger | Wrap app.log with wrapWithNotifications |
| No health checks | Add /health and /health/ready |
| Secrets in env vars | Move to database |
| Modifying existing contracts | Add new version instead |
| Missing correlation ID | Add to all request/response events |
| No error handling | Wrap in try/catch, publish failure |
| HTTP calls between services | Use message bus instead |

---

## Sign-Off Template

```markdown
## Implementation Sign-Off: [Service/Feature Name]

**Author:** [Name]
**Reviewer:** [Name]
**Date:** [YYYY-MM-DD]

### Phase Completion
| Phase | Status | Notes |
|-------|--------|-------|
| 1. Data Model | [ ] Complete | |
| 2. Contracts | [ ] Complete | |
| 3. Core Service | [ ] Complete | |
| 4. Integration | [ ] Complete | |
| 5. Deployment | [ ] Complete | |
| 6. Documentation | [ ] Complete | |
| 7. Testing | [ ] Complete | |

### Prime Directive Compliance
- [ ] All 10 directives satisfied

### Outstanding Issues
<!-- List any known issues or tech debt -->

### Approval
- [ ] Ready for production
- [ ] Needs additional work

**Comments:**
```
