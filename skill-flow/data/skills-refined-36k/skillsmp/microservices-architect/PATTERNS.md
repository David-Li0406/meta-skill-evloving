# Microservices Patterns Reference

Detailed patterns from Chris Richardson's *Microservices Patterns* organized by domain.

---

## Data & Query Patterns

### API Composition

**Intent:** Implement queries by calling multiple services and combining their results.

**When to use:**
- Query requires data from multiple services
- Data is naturally partitioned by service boundaries
- Eventual consistency is acceptable

**Structure:**
```
┌─────────────────────────────────────────────┐
│              API Composer                    │
│  ┌─────────┬─────────┬─────────┐           │
│  │Service A│Service B│Service C│           │
│  │  Query  │  Query  │  Query  │           │
│  └────┬────┴────┬────┴────┬────┘           │
│       │         │         │                 │
│       └─────────┼─────────┘                 │
│                 ▼                           │
│          Combine Results                    │
└─────────────────────────────────────────────┘
```

**Trade-offs:**
| Pro | Con |
|-----|-----|
| Simple query model | Increased latency (multiple calls) |
| Services own their data | Complexity in error handling |
| No data duplication | Harder to implement complex joins |

**Operability requirements:**
- Timeout per service call
- Circuit breaker per dependency
- Partial result handling strategy

---

### Materialized View (CQRS)

**Intent:** Maintain pre-computed query views updated by domain events.

**When to use:**
- Query patterns are well-known
- Read performance is critical
- Eventual consistency is acceptable
- Complex joins/aggregations needed

**Structure:**
```
Events → Event Handler → Materialized View Store → Query API
```

**Implementation:**
```yaml
materialized_view:
  source_events:
    - OrderCreated
    - OrderShipped
    - OrderCancelled
  view_store:
    type: "read-optimized-db"  # ElasticSearch, Redis, dedicated SQL
  update_strategy: "async-event-driven"
  staleness_tolerance: "seconds"
```

**Operability requirements:**
- Lag metric (time since last event processed)
- View rebuild capability
- Consistency check tooling

---

## External API Patterns

### API Gateway

**Intent:** Single entry point for all clients; handles cross-cutting concerns.

**Responsibilities:**
- Request routing
- Protocol translation
- Authentication/authorization
- Rate limiting
- Response caching
- Request/response transformation

**Structure:**
```
Clients → API Gateway → Backend Services
              │
              ├── Auth
              ├── Rate Limit
              ├── Circuit Breaker
              └── Logging/Tracing
```

**Operability requirements:**
- Request latency percentiles (p50, p95, p99)
- Error rate by endpoint
- Rate limit metrics
- Circuit breaker state

---

### Backend-for-Frontend (BFF)

**Intent:** Dedicated API gateway for each client type.

**When to use:**
- Different clients need different data shapes
- Mobile vs web have different performance constraints
- Client-specific authentication flows

**Structure:**
```
┌───────────┐    ┌────────────┐
│  Mobile   │────│ Mobile BFF │────┐
│   App     │    └────────────┘    │
└───────────┘                      │
                                   ▼
┌───────────┐    ┌────────────┐  ┌──────────┐
│  Web App  │────│  Web BFF   │──│ Services │
└───────────┘    └────────────┘  └──────────┘
                                   ▲
┌───────────┐    ┌────────────┐    │
│ 3rd Party │────│Partner BFF │────┘
└───────────┘    └────────────┘
```

---

### Protocol Handler → Wireline Publisher

**Intent:** Decouple external protocol handling from internal message processing.

**Pattern:**
```
External Request → Protocol Handler → Wireline Event → Message Bus → Handler
        (HTTP/gRPC/WS)      │              │
                            ▼              ▼
                      Validate &     Schema-validated
                      Transform      internal format
```

**Key principle:** External protocol semantics do not propagate past the edge.

---

## Testing Patterns

### Consumer-Driven Contract Testing

**Intent:** Services define contracts based on consumer expectations, not provider assumptions.

**Process:**
1. Consumer writes contract (expected request/response)
2. Contract published to broker
3. Provider tests against consumer contracts
4. Breaking changes detected before deployment

**Tools:** Pact, Spring Cloud Contract

**Operability requirements:**
- Contract test results in CI
- Contract version tracking
- Breaking change alerts

---

### Service Component Testing

**Intent:** Test service in isolation with stubbed dependencies.

**Structure:**
```
┌─────────────────────────────────────┐
│        Test Harness                 │
│  ┌─────────────────────────────┐   │
│  │     Service Under Test      │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────┐           │
│  │   Stubbed Services  │           │
│  │   (WireMock, etc)   │           │
│  └─────────────────────┘           │
└─────────────────────────────────────┘
```

---

### Operational Testing

**Intent:** Validate that observability and control paths work, not just business logic.

**Test categories:**
- **Health check tests:** Verify endpoints respond correctly
- **Metric emission tests:** Verify metrics are published
- **Alert tests:** Verify alerts fire under conditions
- **Knob tests:** Verify feature flags/circuit breakers work
- **Chaos tests:** Verify resilience under failure

---

## Deployment Patterns

### Blue-Green Deployment

**Intent:** Zero-downtime deployment with instant rollback capability.

**Structure:**
```
              ┌─────────────────┐
              │   Load Balancer │
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼                           ▼
    ┌─────────┐                 ┌─────────┐
    │  Blue   │                 │  Green  │
    │ (Live)  │                 │ (Staged)│
    └─────────┘                 └─────────┘
```

**Process:**
1. Deploy new version to Green
2. Test Green
3. Switch traffic Blue → Green
4. Keep Blue ready for rollback

---

### Canary Deployment

**Intent:** Gradually roll out changes to a subset of users.

**Process:**
```
100% → Stable
         │
         ├── 1% → Canary (new version)
         │        Monitor for 1 hour
         │
         ├── 10% → Canary
         │         Monitor for 4 hours
         │
         └── 100% → New version (or rollback)
```

**Operability requirements:**
- Per-version error rates
- Latency comparison dashboards
- Automated rollback triggers

---

### Strangler Fig Pattern

**Intent:** Incrementally replace legacy system without big-bang migration.

**Process:**
1. Create facade in front of legacy
2. Implement new functionality in microservice
3. Route specific requests to new service
4. Incrementally migrate until legacy is empty
5. Decommission legacy

**Key:** Each step must emit insight events describing what changed.

---

## Observability Patterns

### Health Checks

**Types:**
- **Liveness:** Is the process alive? (restart if not)
- **Readiness:** Can it serve traffic? (remove from LB if not)
- **Startup:** Has it initialized? (don't check liveness until ready)

**Implementation:**
```yaml
health_check:
  liveness:
    endpoint: /health/live
    interval: 10s
    timeout: 5s
    failure_threshold: 3
  readiness:
    endpoint: /health/ready
    interval: 5s
    checks:
      - database_connection
      - cache_connection
      - downstream_services
```

---

### Observability Triad

| Type | Purpose | Retention |
|------|---------|-----------|
| **Metrics** | Aggregated measurements | Long (months) |
| **Logs** | Discrete events with context | Medium (weeks) |
| **Traces** | Request flow across services | Short (days) |

**Correlation requirement:** All three must share correlation IDs.

---

### Alerting Strategy

**Alert levels:**
| Level | Response | Example |
|-------|----------|---------|
| **Page** | Wake someone up | Service down, data loss risk |
| **Ticket** | Fix within hours | Elevated error rate |
| **Log** | Review in aggregate | Unusual but not urgent |

**Golden signals to alert on:**
1. **Latency** — p99 > threshold
2. **Traffic** — Unexpected spike or drop
3. **Errors** — Error rate > threshold
4. **Saturation** — Resource usage > threshold

---

## Resilience Patterns

### Circuit Breaker

**Intent:** Prevent cascade failures by failing fast when dependency is unhealthy.

**States:**
```
CLOSED → (failures exceed threshold) → OPEN
                                          │
                                   (timeout)
                                          │
                                          ▼
                                     HALF-OPEN
                                          │
                          (success)       │       (failure)
                              ↓           │           ↓
                          CLOSED ←────────┴───────→ OPEN
```

**Configuration:**
```yaml
circuit_breaker:
  failure_threshold: 5          # Failures before opening
  success_threshold: 3          # Successes to close
  timeout: 30s                  # Time in OPEN before HALF-OPEN
  failure_rate_threshold: 50%   # Alternative: rate-based
```

---

### Bulkhead

**Intent:** Isolate failures to prevent resource exhaustion across the system.

**Types:**
- **Thread pool isolation:** Separate pools per dependency
- **Connection pool isolation:** Separate DB connections per service
- **Silo isolation:** Event/tenant partitioning

**Configuration:**
```yaml
bulkhead:
  service_a:
    type: thread_pool
    max_threads: 10
    queue_size: 100
  service_b:
    type: semaphore
    max_concurrent: 25
```

---

## Security Patterns

### Zero Trust

**Principles:**
1. Never trust, always verify
2. Assume breach
3. Verify explicitly
4. Use least privilege access
5. Inspect and log all traffic

**Implementation:**
- mTLS between all services
- JWT/token validation at every hop
- Network segmentation
- Continuous verification

---

### Runtime Trust Profile (RTP)

**Intent:** Define explicit, time-bound trust state for all operations.

**Components:**
```yaml
rtp:
  identity:
    principal: "service-a"
    authenticated_via: "mTLS"
  context:
    tenant: "acme-corp"
    jurisdiction: "EU"
    regulatory: "GDPR"
  capabilities:
    - "read:orders"
    - "write:orders"
  constraints:
    rate_limit: 1000/min
    data_classification: "confidential"
  isolation:
    silo: "tenant-acme"
    fault_domain: "us-east-1a"
  provenance:
    code_version: "v2.3.1"
    config_hash: "abc123"
  expiry: "2024-01-15T12:00:00Z"
```

**Lifecycle:**
1. **Issued:** Generated via identity lookup and trust evaluation
2. **Updated:** Modified by context shifts, decay, or policy changes
3. **Revoked:** Invalidated by violations or explicit revocation

---

### Trust-as-Actor

**Intent:** Model trust as a first-class service that emits promises and revocations.

**Trust service responsibilities:**
- Issue trust profiles
- Evaluate trust requests
- Emit trust change events
- Monitor trust violations
- Revoke compromised profiles

**Events:**
- `TrustProfileIssued`
- `TrustProfileUpdated`
- `TrustViolationDetected`
- `TrustProfileRevoked`
