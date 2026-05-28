# Production Readiness Checklist

Complete checklist for verifying production readiness. A single "No" in the BLOCKER sections means NOT READY.

---

## Startup & Shutdown Behavior

### Startup

- [ ] **Health check endpoint** - `/health` or `/ready` returns 200 when ready
- [ ] **Startup dependencies** - Service waits for required dependencies
- [ ] **Graceful startup** - No traffic accepted until fully initialized
- [ ] **Startup timeout** - Reasonable timeout before considered failed
- [ ] **Idempotent startup** - Safe to restart at any point
- [ ] **Cold start time** - Acceptable latency on first request

### Shutdown

- [ ] **Graceful shutdown** - SIGTERM handled, in-flight requests completed
- [ ] **Shutdown timeout** - Configurable drain period before forced exit
- [ ] **Connection cleanup** - DB connections, file handles closed properly
- [ ] **Queue consumption** - Stops consuming new messages, finishes current
- [ ] **No data loss** - Pending writes flushed before exit

### BLOCKER Checks
- [ ] :red_circle: Health endpoint exists and returns accurate status
- [ ] :red_circle: Graceful shutdown implemented

---

## Backward Compatibility

### API Compatibility

- [ ] **No breaking changes** - Existing clients continue to work
- [ ] **Additive changes only** - New fields optional, old fields preserved
- [ ] **Version header** - API version communicated clearly
- [ ] **Deprecation warnings** - Old features marked, timeline communicated

### Data Compatibility

- [ ] **Schema backward compatible** - Old code can read new data
- [ ] **Schema forward compatible** - New code can read old data
- [ ] **Migration reversible** - Can rollback schema changes
- [ ] **Default values** - New required fields have defaults

### Event/Message Compatibility

- [ ] **Event schema compatible** - Consumers handle new/missing fields
- [ ] **No required field additions** - New fields are optional
- [ ] **Semantic compatibility** - Field meanings unchanged

### BLOCKER Checks
- [ ] :red_circle: No breaking API changes without versioning
- [ ] :red_circle: Database migrations are reversible

---

## Rollback Feasibility

### Code Rollback

- [ ] **Previous version tagged** - Can identify last good version
- [ ] **Rollback tested** - Actually tried rolling back in staging
- [ ] **Rollback automated** - One-click or single command rollback
- [ ] **Rollback time** - Can rollback within SLA (e.g., <5 minutes)

### Data Rollback

- [ ] **No destructive migrations** - No DROP COLUMN, data deletion
- [ ] **Backups verified** - Recent backup exists and is restorable
- [ ] **Point-in-time recovery** - Can restore to specific timestamp
- [ ] **Data export** - Can export affected data before deploy

### State Rollback

- [ ] **Feature flags** - Can disable feature without deploy
- [ ] **Cache invalidation** - Can clear stale cache if needed
- [ ] **Queue draining** - Can stop processing new messages

### BLOCKER Checks
- [ ] :red_circle: Rollback is possible (not a one-way door)
- [ ] :red_circle: Rollback procedure documented
- [ ] :red_circle: Previous working version identified

---

## Partial Failure Handling

### Service Failures

- [ ] **Circuit breakers** - Failing dependencies isolated
- [ ] **Timeouts configured** - All external calls have timeouts
- [ ] **Retry with backoff** - Transient failures retried appropriately
- [ ] **Fallback behavior** - Graceful degradation when dependencies fail
- [ ] **Bulkheads** - Failure in one area doesn't cascade

### Data Failures

- [ ] **Transaction boundaries** - Atomic operations are atomic
- [ ] **Idempotency** - Safe to retry failed operations
- [ ] **Compensation logic** - Failed sagas can be rolled back
- [ ] **Duplicate detection** - Duplicate requests handled safely

### Infrastructure Failures

- [ ] **Multi-AZ/region** - Survives zone/region failure (if required)
- [ ] **Database failover** - Handles primary DB failure
- [ ] **Cache failure** - Works (degraded) without cache
- [ ] **Queue failure** - Messages not lost on queue failure

### BLOCKER Checks
- [ ] :red_circle: Timeouts on all external calls
- [ ] :red_circle: No unbounded retries that could cause storms

---

## Data Corruption Risks

### Write Safety

- [ ] **Validation** - All inputs validated before persistence
- [ ] **Constraints** - Database constraints prevent invalid data
- [ ] **Transactions** - Related writes are atomic
- [ ] **Audit trail** - Changes are logged/auditable

### Read Safety

- [ ] **Null handling** - Missing data handled gracefully
- [ ] **Type safety** - Data types enforced at boundaries
- [ ] **Stale data** - Cache invalidation correct

### Migration Safety

- [ ] **Dry run tested** - Migration tested on production-like data
- [ ] **Rollback tested** - Down migration verified
- [ ] **Performance tested** - Migration won't lock tables too long
- [ ] **Backup before** - Fresh backup before migration

### BLOCKER Checks
- [ ] :red_circle: No migrations that could corrupt existing data
- [ ] :red_circle: Backup exists and is tested

---

## External Dependencies

### Rate Limits & Quotas

- [ ] **Rate limits known** - External API limits documented
- [ ] **Rate limiting implemented** - Respect limits, backoff when hit
- [ ] **Quota monitoring** - Alert before hitting quotas
- [ ] **Burst handling** - Can handle traffic spikes within limits

### Dependency Failures

- [ ] **Dependency health checks** - Monitor dependency availability
- [ ] **Fallback for each dependency** - Graceful degradation defined
- [ ] **Timeout configuration** - Appropriate timeouts per dependency
- [ ] **Circuit breaker thresholds** - Tuned for each dependency

### Third-Party Services

- [ ] **SLA known** - Understand dependency SLAs
- [ ] **Support contact** - Know how to escalate issues
- [ ] **Status page** - Monitor dependency status pages
- [ ] **Alternative provider** - Backup plan if provider fails

### BLOCKER Checks
- [ ] :red_circle: Rate limits configured to avoid being blocked
- [ ] :red_circle: Timeouts on all external calls

---

## Observability

### Logging

- [ ] **Structured logs** - JSON format with consistent fields
- [ ] **Request IDs** - Correlation IDs for request tracing
- [ ] **Log levels** - Appropriate use of info/warn/error
- [ ] **No sensitive data** - No PII, secrets, or tokens in logs
- [ ] **Log retention** - Logs retained long enough for debugging

### Metrics

- [ ] **Request metrics** - Latency (p50, p95, p99), throughput, errors
- [ ] **Business metrics** - Domain-specific KPIs
- [ ] **Resource metrics** - CPU, memory, connections, disk
- [ ] **Dependency metrics** - External call latency and errors
- [ ] **Queue metrics** - Depth, lag, processing rate

### Tracing

- [ ] **Distributed tracing** - Spans propagated across services
- [ ] **Trace sampling** - Appropriate sampling rate configured
- [ ] **Critical paths traced** - Key user journeys instrumented

### Alerting

- [ ] **Error rate alerts** - Alert on spike in errors
- [ ] **Latency alerts** - Alert on p95/p99 degradation
- [ ] **Saturation alerts** - Alert before resources exhausted
- [ ] **Business alerts** - Alert on critical business events
- [ ] **Alert routing** - Alerts go to right team/channel

### BLOCKER Checks
- [ ] :red_circle: Health check endpoint exists
- [ ] :red_circle: Error logging in place
- [ ] :red_circle: At least one alert configured for failures

---

## Manual Intervention

### Runbooks

- [ ] **Startup runbook** - How to start/restart the service
- [ ] **Shutdown runbook** - How to gracefully stop
- [ ] **Rollback runbook** - Step-by-step rollback procedure
- [ ] **Incident runbook** - Common issues and fixes
- [ ] **Escalation path** - Who to contact for each issue type

### Access

- [ ] **Production access** - Team can access production logs/metrics
- [ ] **Emergency access** - Break-glass procedure documented
- [ ] **Audit logging** - Production access is logged

### Recovery Procedures

- [ ] **Data recovery** - How to restore from backup
- [ ] **Cache rebuild** - How to warm/rebuild cache
- [ ] **Queue replay** - How to replay failed messages
- [ ] **State reset** - How to reset to known good state

### BLOCKER Checks
- [ ] :red_circle: Rollback runbook exists
- [ ] :red_circle: Escalation path defined

---

## Smart Contract Specific (if applicable)

### Pre-Deployment

- [ ] **Audit completed** - Security audit by reputable firm
- [ ] **Test coverage** - >95% coverage on critical paths
- [ ] **Formal verification** - Critical invariants verified
- [ ] **Testnet deployment** - Tested on testnet with real scenarios

### Upgrade Safety

- [ ] **Proxy pattern** - Upgradeable if needed
- [ ] **Storage layout** - No storage collisions
- [ ] **Upgrade timelock** - Delay on upgrades for review
- [ ] **Multisig control** - No single key controls upgrades

### Emergency Procedures

- [ ] **Pause mechanism** - Can pause in emergency
- [ ] **Emergency withdrawal** - Users can withdraw if paused
- [ ] **Admin key security** - Admin keys in cold storage/multisig

### BLOCKER Checks
- [ ] :red_circle: Security audit completed
- [ ] :red_circle: Testnet deployment successful
- [ ] :red_circle: Pause mechanism exists

---

## Final Sign-Off

### Pre-Deploy

- [ ] All BLOCKER checks pass
- [ ] Staging deployment successful
- [ ] Load testing completed (if applicable)
- [ ] Security review completed (if applicable)
- [ ] Stakeholders notified of deployment

### Deploy Window

- [ ] Deploy during low-traffic period (if possible)
- [ ] On-call engineer available
- [ ] Rollback procedure reviewed by deployer
- [ ] Monitoring dashboards open

### Post-Deploy

- [ ] Health checks passing
- [ ] Error rates normal
- [ ] Latency within bounds
- [ ] Business metrics normal
- [ ] No customer complaints
