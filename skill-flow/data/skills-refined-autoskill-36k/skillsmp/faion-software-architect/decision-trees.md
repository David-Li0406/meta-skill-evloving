# Architecture Decision Trees

Detailed decision trees for common architecture decisions.

## 1. Architecture Style Selection

### Full Decision Tree

```
Q1: What is the team situation?
    │
    ├─ "Startup/MVP phase" ────────────────────────────────────────────────────┐
    │   Team: <10 people, need to move fast                                    │
    │   Recommendation: Monolith                                               │
    │   Reason: Simplicity, speed, easy debugging                              │
    │   Future: Extract services when pain points emerge                       │
    │
    ├─ "Growing product, unclear boundaries" ──────────────────────────────────┐
    │   Team: 10-30 people, some services but unclear where to split           │
    │   Recommendation: Modular Monolith                                       │
    │   Reason: Clear modules, can extract later, simpler operations           │
    │   Pattern: Domain modules with clear interfaces                          │
    │
    └─ "Mature product, clear domains" ────────────────────────────────────────┐
        Team: 30+ people, multiple teams, independent deployment needed        │
        Recommendation: Microservices                                          │
        Preconditions:                                                         │
        - Bounded contexts are clear                                           │
        - DevOps maturity (CI/CD, monitoring, logging)                         │
        - Team can handle distributed systems complexity                       │
```

### Architecture Style Comparison

| Criterion | Monolith | Modular Monolith | Microservices |
|-----------|----------|------------------|---------------|
| Deployment | Single unit | Single unit | Independent |
| Scaling | Vertical | Vertical | Horizontal per service |
| Team coordination | High | Medium | Low (within service) |
| Complexity | Low | Medium | High |
| DevOps maturity needed | Low | Low | High |
| Data consistency | Easy (ACID) | Easy (ACID) | Hard (eventual) |
| Debugging | Easy | Easy | Hard |
| Best for | MVP, <10 devs | Growing, 10-30 devs | Mature, 30+ devs |

---

## 2. Database Selection

### Primary Database Decision Tree

```
Q1: What is the primary data access pattern?
    │
    ├─ "Complex queries with joins" ───────────────────────────────────────────┐
    │   Data: Highly relational, integrity critical                            │
    │   Q2: Scale requirements?                                                │
    │       ├─ "Standard (< 1TB, < 10k QPS)" → PostgreSQL                      │
    │       ├─ "High read (> 50k QPS)" → PostgreSQL + read replicas            │
    │       └─ "Massive (> 100TB)" → CockroachDB / TiDB                        │
    │
    ├─ "Document-oriented, flexible schema" ───────────────────────────────────┐
    │   Data: Nested objects, evolving schema                                  │
    │   Q2: Consistency vs Availability?                                       │
    │       ├─ "Strong consistency" → MongoDB (w:majority)                     │
    │       └─ "High availability" → DynamoDB / Cassandra                      │
    │
    ├─ "Simple key-value lookups" ─────────────────────────────────────────────┐
    │   Data: Session, cache, simple objects                                   │
    │   Q2: Persistence needed?                                                │
    │       ├─ "Yes" → Redis with AOF                                          │
    │       └─ "No (cache only)" → Redis / Memcached                           │
    │
    ├─ "Time-series data" ─────────────────────────────────────────────────────┐
    │   Data: Metrics, logs, IoT events                                        │
    │   Q2: Query complexity?                                                  │
    │       ├─ "Simple aggregations" → InfluxDB                                │
    │       └─ "SQL-like queries" → TimescaleDB                                │
    │
    ├─ "Highly connected data" ────────────────────────────────────────────────┐
    │   Data: Social graph, recommendations, fraud detection                   │
    │   → Neo4j / Amazon Neptune                                               │
    │
    └─ "Full-text search" ─────────────────────────────────────────────────────┐
        Data: Search, faceted navigation, autocomplete                         │
        Q2: Scale?                                                             │
            ├─ "Small (< 1M docs)" → Meilisearch                               │
            └─ "Large (> 1M docs)" → Elasticsearch / OpenSearch                │
```

### Database Selection Matrix

| Use Case | Primary Choice | Alternative | Avoid |
|----------|----------------|-------------|-------|
| Transactional data | PostgreSQL | MySQL | MongoDB |
| User sessions | Redis | DynamoDB | PostgreSQL |
| Analytics | ClickHouse | BigQuery | MySQL |
| Search | Elasticsearch | Meilisearch | PostgreSQL (for large scale) |
| Caching | Redis | Memcached | File cache |
| Time-series | TimescaleDB | InfluxDB | PostgreSQL |
| Graph | Neo4j | Neptune | SQL joins |

---

## 3. Caching Strategy Selection

```
Q1: What are you caching?
    │
    ├─ "Database query results" ───────────────────────────────────────────────┐
    │   Q2: Write frequency?                                                   │
    │       ├─ "Rarely written" → Cache-aside with long TTL                    │
    │       ├─ "Sometimes written" → Cache-aside with short TTL + invalidation │
    │       └─ "Frequently written" → Write-through cache                      │
    │
    ├─ "API responses" ────────────────────────────────────────────────────────┐
    │   Q2: User-specific?                                                     │
    │       ├─ "No (public data)" → CDN caching (Cloudflare, CloudFront)       │
    │       └─ "Yes (per-user)" → Redis with user-scoped keys                  │
    │
    ├─ "Session data" ─────────────────────────────────────────────────────────┐
    │   → Redis with TTL matching session duration                             │
    │   Pattern: session:{user_id} → serialized session                        │
    │
    ├─ "Computed values" ──────────────────────────────────────────────────────┐
    │   Q2: Computation cost?                                                  │
    │       ├─ "Cheap (<100ms)" → Compute on demand, cache short TTL           │
    │       └─ "Expensive (>1s)" → Background refresh, serve stale             │
    │
    └─ "Static assets" ────────────────────────────────────────────────────────┐
        → CDN with long TTL + cache busting (versioned URLs)                   │
```

### Caching Pattern Reference

| Pattern | Use When | Implementation |
|---------|----------|----------------|
| **Cache-aside** | Read-heavy, tolerates staleness | App checks cache, fetches from DB if miss |
| **Write-through** | Need consistency, write-heavy | Write to cache and DB together |
| **Write-behind** | High write throughput | Write to cache, async to DB |
| **Read-through** | Simplify app code | Cache handles DB fetching |
| **Refresh-ahead** | Predictable access patterns | Pre-refresh before expiry |

---

## 4. API Design Selection

```
Q1: Who is the consumer?
    │
    ├─ "External developers / third-party" ────────────────────────────────────┐
    │   Recommendation: REST with OpenAPI                                      │
    │   Reason: Universal, well-documented, tooling                            │
    │   Format: JSON                                                           │
    │
    ├─ "Internal services (microservices)" ────────────────────────────────────┐
    │   Q2: Performance critical?                                              │
    │       ├─ "Yes (low latency)" → gRPC                                      │
    │       └─ "No" → REST (simpler debugging)                                 │
    │
    ├─ "Frontend (web/mobile)" ────────────────────────────────────────────────┐
    │   Q2: Data requirements?                                                 │
    │       ├─ "Complex, varied queries" → GraphQL                             │
    │       ├─ "Simple CRUD" → REST                                            │
    │       └─ "Real-time updates" → GraphQL subscriptions or WebSockets       │
    │
    └─ "Event-driven" ─────────────────────────────────────────────────────────┐
        Q2: Ordering required?                                                 │
            ├─ "Yes" → Kafka (partitioned by key)                              │
            └─ "No" → RabbitMQ / SQS                                           │
```

### API Style Comparison

| Criterion | REST | GraphQL | gRPC |
|-----------|------|---------|------|
| Best for | Public APIs | Frontend flexibility | Internal services |
| Tooling | Excellent | Good | Good |
| Performance | Good | Medium | Excellent |
| Learning curve | Low | Medium | Medium |
| Caching | HTTP caching | Requires effort | Custom |
| Schema | OpenAPI | GraphQL SDL | Protobuf |

---

## 5. Authentication/Authorization Selection

```
Q1: What type of application?
    │
    ├─ "SaaS / Web app" ────────────────────────────────────────────────────────┐
    │   Q2: Multi-tenant?                                                       │
    │       ├─ "Yes" → JWT + tenant claims, RBAC per tenant                    │
    │       └─ "No" → JWT + RBAC                                                │
    │   Implementation: Auth0 / Clerk / Supabase Auth / Custom                 │
    │
    ├─ "API for third-party developers" ───────────────────────────────────────┐
    │   → OAuth 2.0 + API keys                                                  │
    │   Scopes: define granular permissions                                     │
    │
    ├─ "Internal services" ────────────────────────────────────────────────────┐
    │   Q2: Zero-trust required?                                               │
    │       ├─ "Yes" → mTLS + service tokens                                   │
    │       └─ "No" → API keys + network isolation                             │
    │
    └─ "Mobile app" ────────────────────────────────────────────────────────────┐
        → OAuth 2.0 with PKCE flow                                             │
        Token storage: Secure enclave / Keychain                               │
```

---

## 6. Scaling Strategy Selection

```
Q1: What is the bottleneck?
    │
    ├─ "CPU-bound" ────────────────────────────────────────────────────────────┐
    │   Examples: Image processing, complex calculations                        │
    │   Strategy: Horizontal scaling (more instances)                          │
    │   Consider: Queue + workers for async processing                         │
    │
    ├─ "Memory-bound" ─────────────────────────────────────────────────────────┐
    │   Examples: Large datasets in memory, caching                            │
    │   Strategy: Vertical scaling (bigger instances) + sharding               │
    │
    ├─ "I/O-bound (database)" ─────────────────────────────────────────────────┐
    │   Q2: Read or write heavy?                                               │
    │       ├─ "Read heavy" → Read replicas + caching                          │
    │       └─ "Write heavy" → Sharding + write-through cache                  │
    │
    ├─ "I/O-bound (external APIs)" ────────────────────────────────────────────┐
    │   Strategy: Async processing + circuit breakers + retries                 │
    │
    └─ "Network-bound" ────────────────────────────────────────────────────────┐
        Examples: Streaming, real-time                                         │
        Strategy: CDN + edge computing + efficient protocols (gRPC, WebSockets)│
```

---

## 7. Error Handling Strategy

```
Q1: What type of system?
    │
    ├─ "User-facing application" ──────────────────────────────────────────────┐
    │   Strategy:                                                              │
    │   - Graceful degradation (show partial data)                             │
    │   - User-friendly error messages                                         │
    │   - Fallback UI states                                                   │
    │   - Error reporting (Sentry, etc.)                                       │
    │
    ├─ "API service" ──────────────────────────────────────────────────────────┐
    │   Strategy:                                                              │
    │   - Structured error responses (RFC 7807)                                │
    │   - Appropriate HTTP status codes                                        │
    │   - Request IDs for tracing                                              │
    │   - Rate limiting with clear feedback                                    │
    │
    ├─ "Background job processing" ────────────────────────────────────────────┐
    │   Strategy:                                                              │
    │   - Retry with exponential backoff                                       │
    │   - Dead letter queue for failed jobs                                    │
    │   - Idempotency for retries                                              │
    │   - Alerting on failure thresholds                                       │
    │
    └─ "Distributed system" ───────────────────────────────────────────────────┐
        Strategy:                                                              │
        - Circuit breakers                                                     │
        - Bulkheads (isolate failures)                                         │
        - Timeouts everywhere                                                  │
        - Saga pattern for distributed transactions                            │
```

---

## Decision Tree Usage Guidelines

1. **Start from requirements** - Understand functional and non-functional requirements first
2. **Consider constraints** - Team skills, timeline, budget
3. **Document decisions** - Use ADRs for important choices
4. **Plan for change** - Architecture should allow evolution
5. **Validate assumptions** - POC critical components early

---

*Architecture Decision Trees v1.0*
