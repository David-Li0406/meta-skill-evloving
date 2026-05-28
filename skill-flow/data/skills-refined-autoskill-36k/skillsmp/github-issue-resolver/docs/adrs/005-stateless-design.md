# ADR-005: Stateless Design (No Database)

## Status

**ACCEPTED** - 2025-12-09

## Context

The OpenShift Cluster Health MCP Server needs to decide on data persistence strategy. Traditional application servers often include databases for storing state, caching, and historical data. However, MCP servers have unique characteristics that challenge the need for persistent storage.

### MCP Server Characteristics

1. **Request-Response Pattern**: MCP tools are invoked on-demand, process requests, and return responses
2. **No User Data**: MCP servers don't manage user accounts, profiles, or preferences
3. **External Data Sources**: All operational data comes from external systems (Kubernetes API, Prometheus, Coordination Engine)
4. **Ephemeral Sessions**: HTTP session state is minimal and short-lived
5. **Read-Heavy Workload**: Primarily queries external systems, minimal writes

### Data Categories Analysis

| Data Type | Source | Persistence Need | Rationale |
|-----------|--------|-----------------|-----------|
| **Cluster Health** | Kubernetes API | ❌ No | Real-time data, always query fresh |
| **Prometheus Metrics** | Prometheus | ❌ No | Time-series data stored in Prometheus |
| **Anomaly Results** | KServe Models | ❌ No | Computed on-demand, stored in Coordination Engine if needed |
| **Incidents** | Coordination Engine | ❌ No | Coordination Engine has PostgreSQL |
| **Remediation Status** | Coordination Engine | ❌ No | Coordination Engine manages workflow state |
| **MCP Session State** | In-memory | ⚠️ Maybe | Short-lived, can reconstruct from clients |
| **Metrics/Logs** | Prometheus/OpenShift Logging | ❌ No | Use platform observability |

### Current Platform Architecture

The parent **OpenShift AI Ops Platform** has:

- **Coordination Engine**: PostgreSQL database for incident history, workflow state
- **Prometheus**: Time-series database for metrics
- **OpenShift Logging**: Elasticsearch/Loki for log aggregation
- **KServe Models**: Stateless prediction services

### Operational Requirements

- **Scalability**: Horizontal scaling with multiple replicas
- **High Availability**: Tolerate pod restarts without data loss
- **Resource Efficiency**: Minimal memory and storage footprint
- **Deployment Simplicity**: Fast startup, no migration scripts

## Decision

We will implement a **fully stateless MCP server** with **no persistent database**. All state will be either:

1. **In-memory** (HTTP sessions, caching)
2. **Delegated** to external services (Coordination Engine, Prometheus)
3. **Reconstructed** from source systems (Kubernetes API)

### Key Design Principles

1. **No PostgreSQL, SQLite, or any database**
2. **In-memory session management** for HTTP transport
3. **Short-lived caches** with TTL (10-30 seconds)
4. **Delegate persistence** to Coordination Engine when needed
5. **Idempotent operations** for reliability
6. **12-Factor App compliance** (stateless processes)

## Rationale

### Why Stateless?

1. **MCP Protocol Nature**: Request-response pattern doesn't require persistence
2. **External Data Sources**: All authoritative data lives elsewhere
3. **Horizontal Scalability**: No database = easy horizontal scaling
4. **Operational Simplicity**: No backup/restore, no migrations, no schema management
5. **Resource Efficiency**: Lower memory and storage requirements
6. **Faster Startup**: No database connection pooling or schema validation
7. **High Availability**: Any replica can handle any request

### Why No Caching Database (Redis, Memcached)?

1. **Query Latency**: Kubernetes API and Prometheus respond in <50ms (acceptable)
2. **Data Freshness**: Real-time cluster health requires fresh data
3. **Operational Overhead**: Additional service to deploy and monitor
4. **Memory Efficiency**: In-memory Go maps sufficient for short TTL caching
5. **Complexity**: Redis clustering, failover adds unnecessary complexity

## Alternatives Considered

### PostgreSQL Database

**Architecture**:
```
┌─────────────────┐       ┌──────────────┐
│  MCP Server (Go)│──────▶│  PostgreSQL  │
│                 │       │  - Sessions  │
│                 │       │  - Cache     │
│                 │       │  - History   │
└─────────────────┘       └──────────────┘
```

**Pros**:
- Persistent session state across restarts
- Historical query results for analytics
- Complex querying capabilities

**Cons**:
- ❌ Operational complexity (backup, HA, migrations)
- ❌ Resource overhead (CPU, memory, storage)
- ❌ Slower startup (connection pooling)
- ❌ Horizontal scaling complexity (connection limits)
- ❌ No clear use case (all data sources are external)
- ❌ Violates 12-factor stateless principle

**Verdict**: Rejected - unnecessary complexity with no clear benefit

### SQLite (Embedded Database)

**Pros**:
- No separate database process
- Simple file-based storage
- Good for local development

**Cons**:
- ❌ File I/O overhead in container
- ❌ Not suitable for concurrent writes
- ❌ Volume management complexity in Kubernetes
- ❌ Backup/restore complexity
- ❌ No clear use case

**Verdict**: Rejected - adds file system dependency without value

### Redis (Caching Layer)

**Architecture**:
```
┌─────────────────┐       ┌──────────────┐
│  MCP Server (Go)│──────▶│    Redis     │
│                 │       │  - Sessions  │
│                 │       │  - Cache     │
└─────────────────┘       └──────────────┘
```

**Pros**:
- Fast in-memory caching
- Distributed session storage
- TTL expiration built-in

**Cons**:
- ❌ Additional service to deploy/monitor
- ❌ Network latency (5-10ms per call)
- ❌ Operational complexity (Redis cluster, failover)
- ❌ Overkill for simple session management
- ❌ Go maps with TTL achieve same goal

**Verdict**: Rejected - Go in-memory caching is sufficient

## Implementation Details

### In-Memory Session Management

```go
// internal/server/session.go
package server

import (
    "sync"
    "time"
)

type SessionStore struct {
    sessions map[string]*Session
    mu       sync.RWMutex
    ttl      time.Duration
}

type Session struct {
    ID        string
    CreatedAt time.Time
    LastSeen  time.Time
    Data      map[string]interface{}
}

func NewSessionStore(ttl time.Duration) *SessionStore {
    store := &SessionStore{
        sessions: make(map[string]*Session),
        ttl:      ttl,
    }

    // Background cleanup goroutine
    go store.cleanupExpired()

    return store
}

func (s *SessionStore) Get(sessionID string) (*Session, bool) {
    s.mu.RLock()
    defer s.mu.RUnlock()

    session, exists := s.sessions[sessionID]
    if !exists {
        return nil, false
    }

    // Update last seen
    session.LastSeen = time.Now()
    return session, true
}

func (s *SessionStore) Set(sessionID string, data map[string]interface{}) {
    s.mu.Lock()
    defer s.mu.Unlock()

    s.sessions[sessionID] = &Session{
        ID:        sessionID,
        CreatedAt: time.Now(),
        LastSeen:  time.Now(),
        Data:      data,
    }
}

func (s *SessionStore) cleanupExpired() {
    ticker := time.NewTicker(1 * time.Minute)
    defer ticker.Stop()

    for range ticker.C {
        s.mu.Lock()
        now := time.Now()
        for id, session := range s.sessions {
            if now.Sub(session.LastSeen) > s.ttl {
                delete(s.sessions, id)
            }
        }
        s.mu.Unlock()
    }
}
```

### In-Memory Caching with TTL

```go
// pkg/cache/cache.go
package cache

import (
    "sync"
    "time"
)

type CacheEntry struct {
    Data      interface{}
    ExpiresAt time.Time
}

type Cache struct {
    entries map[string]*CacheEntry
    mu      sync.RWMutex
    ttl     time.Duration
}

func NewCache(ttl time.Duration) *Cache {
    cache := &Cache{
        entries: make(map[string]*CacheEntry),
        ttl:     ttl,
    }
    go cache.cleanup()
    return cache
}

func (c *Cache) Get(key string) (interface{}, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()

    entry, exists := c.entries[key]
    if !exists {
        return nil, false
    }

    if time.Now().After(entry.ExpiresAt) {
        return nil, false
    }

    return entry.Data, true
}

func (c *Cache) Set(key string, value interface{}) {
    c.mu.Lock()
    defer c.mu.Unlock()

    c.entries[key] = &CacheEntry{
        Data:      value,
        ExpiresAt: time.Now().Add(c.ttl),
    }
}

func (c *Cache) cleanup() {
    ticker := time.NewTicker(30 * time.Second)
    defer ticker.Stop()

    for range ticker.C {
        c.mu.Lock()
        now := time.Now()
        for key, entry := range c.entries {
            if now.After(entry.ExpiresAt) {
                delete(c.entries, key)
            }
        }
        c.mu.Unlock()
    }
}
```

### Caching Strategy

| Data | Cache | TTL | Rationale |
|------|-------|-----|-----------|
| **Cluster Health** | ✅ Yes | 10s | Reduce K8s API load |
| **Node List** | ✅ Yes | 30s | Nodes rarely change |
| **Prometheus Metrics** | ❌ No | N/A | Always query fresh |
| **KServe Status** | ✅ Yes | 20s | Reduce KServe API load |
| **Incidents** | ❌ No | N/A | Must be real-time |

### Usage Example

```go
// internal/tools/cluster_health.go
package tools

type ClusterHealthTool struct {
    k8sClient *kubernetes.Clientset
    cache     *cache.Cache
}

func (t *ClusterHealthTool) Execute(ctx context.Context) (*Response, error) {
    // Try cache first
    if cached, ok := t.cache.Get("cluster-health"); ok {
        return cached.(*Response), nil
    }

    // Query Kubernetes API
    nodes, err := t.k8sClient.CoreV1().Nodes().List(ctx, metav1.ListOptions{})
    if err != nil {
        return nil, err
    }

    pods, err := t.k8sClient.CoreV1().Pods("").List(ctx, metav1.ListOptions{})
    if err != nil {
        return nil, err
    }

    // Build response
    response := &Response{
        NodeCount:      len(nodes.Items),
        PodCount:       len(pods.Items),
        HealthyNodes:   countHealthyNodes(nodes),
        RunningPods:    countRunningPods(pods),
    }

    // Cache for 10 seconds
    t.cache.Set("cluster-health", response)

    return response, nil
}
```

## Consequences

### Positive

- ✅ **Operational Simplicity**: No database to backup, restore, or migrate
- ✅ **Fast Startup**: No connection pooling or schema validation
- ✅ **Horizontal Scaling**: Any replica can handle any request
- ✅ **Resource Efficiency**: Lower memory and storage footprint
- ✅ **High Availability**: Pod restarts don't cause data loss (data is external)
- ✅ **12-Factor Compliance**: Stateless processes principle
- ✅ **Testing Simplicity**: No database mocking or fixtures
- ✅ **Deployment Simplicity**: No schema migrations or seed data

### Negative

- ⚠️ **Session Loss on Restart**: HTTP sessions lost on pod restart
- ⚠️ **No Historical Data**: Cannot query past results (delegate to Coordination Engine)
- ⚠️ **Repeated Queries**: May query same data multiple times without persistence
- ⚠️ **Memory Limits**: In-memory cache limited by pod memory

### Mitigation Strategies

| Concern | Mitigation |
|---------|-----------|
| **Session loss** | Sessions are short-lived (minutes), acceptable for AI queries |
| **Historical data** | Coordination Engine PostgreSQL for incident history |
| **Query duplication** | Short TTL cache (10-30s) reduces redundant queries |
| **Memory limits** | Cache eviction with TTL, bounded session count |

## Session Persistence Handling

### HTTP Session Loss on Restart

When a pod restarts, in-memory sessions are lost:

```
Client (Lightspeed)  →  Pod A (session ABC)  →  Pod restarts
Client (Lightspeed)  →  Pod B (no session)   →  Returns error
```

**Mitigation**:
- **Session Reconstruction**: Client can re-establish session
- **Session Stickiness**: Kubernetes Service session affinity (if needed)
- **Stateless Tools**: Most MCP tools are stateless, don't require session continuity

```yaml
# Optional: Session affinity (if needed)
apiVersion: v1
kind: Service
metadata:
  name: cluster-health-mcp
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 600  # 10 minutes
```

### Delegation to Coordination Engine

For persistent data needs, delegate to Coordination Engine:

```go
// internal/tools/trigger_remediation.go
func (t *RemediationTool) Execute(ctx context.Context, params map[string]interface{}) (*Response, error) {
    incidentID := params["incident_id"].(string)
    action := params["action"].(string)

    // Delegate to Coordination Engine (has PostgreSQL)
    resp, err := t.coordinationEngine.TriggerRemediation(ctx, &RemediationRequest{
        IncidentID: incidentID,
        Action:     action,
    })

    // Coordination Engine persists workflow state, incident history
    return &Response{
        WorkflowID: resp.WorkflowID,
        Status:     resp.Status,
    }, nil
}
```

## Resource Management

### Memory Footprint

| Component | Memory (Est.) | Notes |
|-----------|--------------|-------|
| **Go Runtime** | 10-15 MB | Base Go process |
| **MCP SDK** | 5-10 MB | MCP protocol handling |
| **Session Store** | 1-5 MB | 20 sessions × ~100KB each |
| **Cache** | 5-10 MB | Bounded cache entries |
| **HTTP Clients** | 5 MB | Connection pools |
| **Total** | **30-50 MB** | Well within 100MB limit |

### Kubernetes Resource Limits

```yaml
# charts/openshift-cluster-health-mcp/values.yaml
resources:
  requests:
    memory: 64Mi
    cpu: 50m
  limits:
    memory: 128Mi
    cpu: 200m
```

## Monitoring

### Key Metrics

```go
// internal/metrics/metrics.go
var (
    cacheHits = prometheus.NewCounter(prometheus.CounterOpts{
        Name: "mcp_cache_hits_total",
        Help: "Total number of cache hits",
    })

    cacheMisses = prometheus.NewCounter(prometheus.CounterOpts{
        Name: "mcp_cache_misses_total",
        Help: "Total number of cache misses",
    })

    sessionCount = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "mcp_active_sessions",
        Help: "Number of active HTTP sessions",
    })

    cacheSize = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "mcp_cache_entries",
        Help: "Number of cached entries",
    })
)
```

### Alerts

```yaml
# Prometheus alert rules
groups:
- name: mcp-server
  rules:
  - alert: MCPHighMemoryUsage
    expr: container_memory_usage_bytes{pod=~"cluster-health-mcp-.*"} > 100 * 1024 * 1024
    for: 5m
    annotations:
      summary: "MCP server memory usage above 100MB"

  - alert: MCPLowCacheHitRate
    expr: rate(mcp_cache_hits_total[5m]) / rate(mcp_cache_misses_total[5m]) < 0.5
    for: 10m
    annotations:
      summary: "MCP server cache hit rate below 50%"
```

## Success Criteria

### Phase 1 Success (Week 2)
- ✅ MCP server runs without database dependency
- ✅ In-memory session management working
- ✅ Cache hit rate >70% for repeated queries
- ✅ Memory usage <50MB at rest

### Phase 2 Success (Week 3)
- ✅ Horizontal scaling tested (3 replicas)
- ✅ Pod restart doesn't affect functionality
- ✅ Session cleanup working (no memory leaks)
- ✅ Integration tests pass without database

### Phase 3 Success (Week 4)
- ✅ Production deployment stable for 7 days
- ✅ Cache performance meets latency targets
- ✅ Memory limits never exceeded
- ✅ No persistent storage claims

## Future Considerations

If stateful requirements emerge, we will:

1. **Evaluate Need**: Validate whether external delegation is insufficient
2. **Prefer External Services**: Use Coordination Engine PostgreSQL if possible
3. **Minimal Database**: SQLite for truly local-only needs
4. **Document Decision**: Create new ADR for stateful design

## Related ADRs

- [ADR-003: Standalone MCP Server Architecture](003-standalone-mcp-server-architecture.md)
- [ADR-006: Integration Architecture](006-integration-architecture.md)

## References

- [12-Factor App: Stateless Processes](https://12factor.net/processes)
- [Kubernetes Best Practices: Stateless Applications](https://kubernetes.io/docs/concepts/workloads/)
- [OpenShift Cluster Health MCP PRD](../../PRD.md)

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Memory leaks** | Low | Medium | Automated cache cleanup, session TTL, monitoring |
| **Cache miss performance** | Medium | Low | TTL tuning, metrics monitoring |
| **Session loss annoyance** | Low | Low | Acceptable for AI query use case |
| **Future state requirements** | Medium | Medium | Delegate to Coordination Engine |

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-09
