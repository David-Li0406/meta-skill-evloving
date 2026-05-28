# Architecture Review Checklist

Complete checklist for reviewing architectural changes. Work through each section systematically.

---

## Coupling Analysis

### Cross-Service Dependencies

- [ ] **New service calls** - Are new synchronous calls to other services introduced?
- [ ] **Hidden sync calls** - Are there blocking calls disguised as async?
- [ ] **Circular dependencies** - Does this create A→B→A dependency chains?
- [ ] **Transitive dependencies** - Does A now implicitly depend on C through B?
- [ ] **Temporal coupling** - Does timing/ordering matter between services?
- [ ] **Deployment coupling** - Must multiple services deploy together?

### Shared State & Resources

- [ ] **Shared databases** - Multiple services writing to same tables?
- [ ] **Shared caches** - Cache keys that cross service boundaries?
- [ ] **Shared queues** - Multiple producers/consumers with implicit contracts?
- [ ] **Shared configs** - Configuration that must stay in sync?
- [ ] **Global state** - Singletons, static state, or ambient context?

### Interface Contracts

- [ ] **API changes** - Are endpoints added/modified/removed?
- [ ] **Request/response schemas** - Field additions, removals, type changes?
- [ ] **Event schemas** - Message format changes?
- [ ] **Database schemas** - Column/table changes affecting multiple services?
- [ ] **gRPC/protobuf** - Proto file changes and regeneration needed?

---

## Data Ownership

### Source of Truth

- [ ] **Single owner** - Is there exactly one source of truth for each data entity?
- [ ] **Data duplication** - Is data copied across services? Why?
- [ ] **Derived data** - Are derived/cached copies clearly marked as such?
- [ ] **Sync mechanisms** - How does duplicated data stay in sync?

### Schema Management

- [ ] **Schema drift** - Can schemas diverge between services?
- [ ] **Migration strategy** - How are schema changes deployed?
- [ ] **Backward compatibility** - Can old code read new data?
- [ ] **Forward compatibility** - Can new code read old data?
- [ ] **Default values** - Are new fields nullable or have defaults?

### Data Lifecycle

- [ ] **Creation** - Who creates this data? Is it clear?
- [ ] **Updates** - Who can modify? Concurrent updates handled?
- [ ] **Deletion** - Soft delete vs hard delete? Cascading?
- [ ] **Archival** - Is there a retention policy?
- [ ] **GDPR/Privacy** - PII handling, deletion requests?

---

## Contract Compatibility

### API Versioning

- [ ] **Breaking changes** - Any changes that break existing clients?
- [ ] **Version strategy** - URL versioning, header versioning, or none?
- [ ] **Deprecation path** - How long do old versions live?
- [ ] **Client migration** - Plan to update all consumers?

### Event/Message Contracts

- [ ] **Schema evolution** - Can consumers handle new fields?
- [ ] **Required fields** - Are new required fields added?
- [ ] **Semantic changes** - Same field, different meaning?
- [ ] **Event ordering** - Does consumer assume order?
- [ ] **Idempotency** - Can events be processed multiple times safely?

### Smart Contract / ABI

- [ ] **ABI compatibility** - Function signatures unchanged?
- [ ] **Storage layout** - Proxy upgrade storage collision?
- [ ] **State migration** - On-chain state handled correctly?
- [ ] **Upgrade path** - Can contract be upgraded safely?

---

## Performance & Latency

### Latency Analysis

- [ ] **Call chain depth** - How many hops to complete a request?
- [ ] **Serial vs parallel** - Are independent calls parallelized?
- [ ] **Latency amplification** - Does one slow service block everything?
- [ ] **Timeout configuration** - Are timeouts set appropriately?
- [ ] **P99 impact** - How does this affect tail latency?

### Fan-Out Risks

- [ ] **N+1 patterns** - Looping service calls?
- [ ] **Broadcast storms** - One event triggers many downstream events?
- [ ] **Cascade failures** - Can one failure bring down the system?
- [ ] **Retry storms** - Coordinated retries overwhelming a service?

### Resource Usage

- [ ] **Memory footprint** - Significant memory increase?
- [ ] **Connection pools** - New connections to external resources?
- [ ] **Thread/goroutine usage** - New concurrent workloads?
- [ ] **Storage growth** - New data that grows unbounded?

---

## Operational Impact

### Deployment

- [ ] **Deploy order** - Must services deploy in specific order?
- [ ] **Zero-downtime** - Can this deploy without downtime?
- [ ] **Rollback plan** - What if we need to rollback?
- [ ] **Rollback complexity** - Is rollback simple, complex, or impossible?
- [ ] **Database migrations** - Are migrations reversible?
- [ ] **Feature flags** - Should this be behind a flag?

### Failure Handling

- [ ] **Partial failure** - What if only some components update?
- [ ] **Graceful degradation** - Can system work with reduced functionality?
- [ ] **Circuit breakers** - Are failing dependencies isolated?
- [ ] **Fallbacks** - What happens when dependencies fail?
- [ ] **Dead letter handling** - What happens to failed messages?

### Monitoring & Alerting

- [ ] **New metrics needed** - What should we measure?
- [ ] **Alert thresholds** - What conditions should alert?
- [ ] **Dashboards** - Do existing dashboards cover this?
- [ ] **Logging** - Are logs sufficient for debugging?
- [ ] **Tracing** - Is distributed tracing maintained?

---

## Migration Safety

### Data Migrations

- [ ] **Backfill strategy** - How is existing data migrated?
- [ ] **Backfill performance** - Will migration impact production?
- [ ] **Validation** - How do we verify migration correctness?
- [ ] **Rollback data** - Can we undo the data migration?

### Dual-Write / Dual-Read

- [ ] **Dual-write period** - Writing to old and new simultaneously?
- [ ] **Consistency** - How to handle writes during migration?
- [ ] **Cutover plan** - When/how to switch fully to new system?
- [ ] **Comparison tooling** - Can we compare old vs new outputs?

### Feature Flags

- [ ] **Flag granularity** - Per-user, per-tenant, percentage?
- [ ] **Flag cleanup** - Plan to remove flag after rollout?
- [ ] **Flag dependencies** - Do flags depend on each other?
- [ ] **Emergency kill switch** - Can we disable quickly?

---

## Future Cost Analysis

### Technical Debt

- [ ] **Accidental complexity** - Does this add unnecessary complexity?
- [ ] **Intentional debt** - Is debt documented with payback plan?
- [ ] **Maintenance burden** - Does this increase ongoing maintenance?
- [ ] **Testing complexity** - Does this make testing harder?

### Extensibility

- [ ] **Future changes** - Does this make next change harder?
- [ ] **Pattern consistency** - Does this follow or deviate from patterns?
- [ ] **Abstraction level** - Right level of abstraction?
- [ ] **Lock-in risks** - Are we locked into specific vendors/tools?

### Team Impact

- [ ] **Knowledge silos** - Does this require specialized knowledge?
- [ ] **Documentation** - Is the design documented?
- [ ] **Onboarding** - Can new team members understand this?

---

## Blast Radius Assessment

### Severity Matrix

| Impact Scope | Data Loss | Service Down | Degraded | No Impact |
|--------------|-----------|--------------|----------|-----------|
| All users | CRITICAL | CRITICAL | HIGH | - |
| Many users | CRITICAL | HIGH | MEDIUM | - |
| Few users | HIGH | MEDIUM | LOW | - |
| Internal only | MEDIUM | LOW | LOW | INFO |

### Failure Modes to Consider

1. **Component crashes** - What happens if the new code throws exceptions?
2. **Slow performance** - What if latency increases 10x?
3. **Bad data** - What if incorrect data is written?
4. **Partial deploy** - What if only some instances have new code?
5. **Dependency failure** - What if a new dependency is unavailable?
6. **Rollback needed** - What state is the system in after rollback?

---

## Quick Reference: Red Flags

| Red Flag | Risk Level | Action |
|----------|------------|--------|
| New synchronous cross-service call | HIGH | Consider async/events |
| Shared mutable state between services | CRITICAL | Establish single owner |
| Breaking API change without versioning | CRITICAL | Add versioning strategy |
| Database migration not reversible | HIGH | Make reversible or add flag |
| No rollback plan documented | MEDIUM | Document rollback steps |
| Multiple services must deploy together | HIGH | Decouple deployments |
| New required field in event schema | HIGH | Make optional with default |
| Unbounded data growth | MEDIUM | Add retention/archival |
| Missing circuit breaker on new dependency | MEDIUM | Add circuit breaker |
| No feature flag for major change | MEDIUM | Add feature flag |
