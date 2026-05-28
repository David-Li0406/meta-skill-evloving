# ADR-003: Standalone MCP Server Architecture

## Status

**ACCEPTED** - 2025-12-09

## Context

The OpenShift Cluster Health MCP Server needs to provide AI assistants with access to cluster health data, monitoring metrics, and operational workflows. The architectural question is whether this MCP server should be:

1. **Embedded** within the existing Coordination Engine (Python/Flask)
2. **Standalone** as a separate Go service
3. **Hybrid** with shared components

### Current OpenShift AI Ops Platform Architecture

The parent platform consists of:

- **Coordination Engine** (Python/Flask): Remediation workflows, incident management
- **KServe Models** (Python/Notebooks): ML-powered anomaly detection
- **Prometheus**: Cluster metrics and alerting
- **Kubernetes API**: Cluster state and operations

### Integration Requirements

- **OpenShift Lightspeed**: Requires MCP server for natural language queries
- **Coordination Engine**: Needs to receive remediation triggers from AI assistants
- **KServe Models**: Should be accessible for anomaly analysis
- **Prometheus**: Must expose metrics for health queries
- **Multiple Clusters**: Should be deployable to any OpenShift 4.14+ cluster

### Lessons from Parent Platform

The parent platform's **ADR-015** (Service Separation - MCP Server vs REST API Service) established critical principles:

- **Single Responsibility**: Each service should have one clear purpose
- **Protocol Alignment**: MCP servers use stdio/HTTP, not embedded frameworks
- **Deployment Flexibility**: Different services have different scaling requirements
- **Maintenance Clarity**: Clear boundaries simplify debugging

## Decision

We will implement the **Standalone MCP Server Architecture** as a separate Go-based service, independent from the Coordination Engine and other platform components.

### Key Architectural Principles

1. **Separation of Concerns**: MCP server handles protocol communication only
2. **Lightweight**: Minimal dependencies, focused functionality
3. **Reusable**: Deployable on any OpenShift cluster
4. **Stateless**: No database, no persistent state
5. **Integration via HTTP**: Communicate with other services via REST APIs

## Alternatives Considered

### Embedded in Coordination Engine

**Architecture**:
```
┌─────────────────────────────────────┐
│   Coordination Engine (Python)      │
│  ┌──────────────────────────────┐   │
│  │  Flask REST API              │   │
│  ├──────────────────────────────┤   │
│  │  MCP Server (subprocess)     │   │
│  │  - Node.js or Go process     │   │
│  │  - Managed by Python parent  │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Pros**:
- Shared database access (PostgreSQL)
- Direct function calls (no HTTP overhead)
- Single deployment unit
- Simplified configuration

**Cons**:
- ❌ Mixed technology stack (Python + Go/Node.js)
- ❌ Complex process management
- ❌ Tight coupling to Coordination Engine
- ❌ Not reusable on other clusters
- ❌ Violates single responsibility principle
- ❌ Different scaling requirements (MCP vs Flask)
- ❌ Deployment complexity (multi-language container)

**Verdict**: Rejected due to tight coupling and complexity

### Hybrid with Shared Components

**Architecture**:
```
┌──────────────────┐     ┌──────────────────┐
│  MCP Server (Go) │────▶│  Shared Library  │
└──────────────────┘     │  (Coordination)  │
                         │  - Python module │
┌──────────────────┐     │  - Imported by   │
│ Coordination Eng │────▶│    both services │
│  (Python/Flask)  │     └──────────────────┘
└──────────────────┘
```

**Pros**:
- Code reuse for common functionality
- Consistent business logic

**Cons**:
- ❌ Requires polyglot shared library (Python + Go)
- ❌ Version synchronization complexity
- ❌ Still couples deployment lifecycles
- ❌ Difficult to maintain cross-language library
- ❌ Go cannot directly import Python modules

**Verdict**: Rejected due to cross-language sharing complexity

### Standalone with REST API Integration

**Architecture**:
```
┌──────────────────────────────────────────────────────────┐
│  MCP Clients (OpenShift Lightspeed, Claude Desktop)     │
└────────────────────┬─────────────────────────────────────┘
                     │ MCP Protocol (HTTP/stdio)
                     ▼
┌──────────────────────────────────────────────────────────┐
│  OpenShift Cluster Health MCP Server (Go) - STANDALONE   │
│  ┌────────────────────────────────────────────────────┐  │
│  │  MCP Server (modelcontextprotocol/go-sdk)          │  │
│  │  - Tools: 5 tools (cluster-health, anomalies, etc)│  │
│  │  - Resources: 3 resources (cluster://, model://)  │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  HTTP Clients (Go net/http)                        │  │
│  │  - CoordinationEngineClient                        │  │
│  │  - KServeClient                                    │  │
│  │  - PrometheusClient                                │  │
│  │  - KubernetesClient (client-go)                   │  │
│  └────────────────────────────────────────────────────┘  │
└────────┬─────────┬─────────┬─────────┬──────────────────┘
         │ HTTP    │ HTTP    │ HTTP    │ K8s API
         ▼         ▼         ▼         ▼
┌──────────┐ ┌─────────┐ ┌────────┐ ┌──────────────┐
│Coord Eng │ │ KServe  │ │Prometh │ │ Kubernetes   │
│(Python)  │ │(Models) │ │(Metrics)│ │ API Server   │
└──────────┘ └─────────┘ └────────┘ └──────────────┘
```

**Pros**:
- ✅ Clean separation of concerns
- ✅ Independent deployment and scaling
- ✅ Technology stack freedom (Go for MCP, Python for Coordination)
- ✅ Reusable across multiple clusters
- ✅ Simple HTTP-based integration
- ✅ No cross-language dependencies
- ✅ Follows containers/kubernetes-mcp-server pattern
- ✅ Aligns with parent platform ADR-015

**Cons**:
- ⚠️ HTTP latency for service-to-service calls
- ⚠️ Requires network configuration
- ⚠️ Multiple containers to manage

**Verdict**: **ACCEPTED** - Best balance of flexibility, maintainability, and reusability

## Consequences

### Positive

- ✅ **Clean Architecture**: Single responsibility, clear boundaries
- ✅ **Technology Freedom**: Go for MCP server, Python for Coordination Engine
- ✅ **Reusability**: Deployable to any OpenShift cluster independently
- ✅ **Scalability**: Scale MCP server independently from other services
- ✅ **Maintainability**: Separate codebases, clear ownership
- ✅ **Testing**: Test MCP server in isolation with mocked backends
- ✅ **Deployment Flexibility**: Can deploy MCP server without Coordination Engine
- ✅ **Security**: Separate RBAC, network policies per service
- ✅ **Standards Compliance**: Follows MCP best practices (ADR-015 from parent)

### Negative

- ⚠️ **Network Latency**: HTTP calls add 5-20ms overhead vs direct function calls
- ⚠️ **Service Discovery**: Requires Kubernetes Service DNS or service mesh
- ⚠️ **Error Handling**: Must handle network failures gracefully
- ⚠️ **Operational Complexity**: Multiple services to monitor and maintain
- ⚠️ **Configuration**: Each service needs separate configuration

### Neutral

- **Container Count**: 2 containers (MCP + Coordination Engine) vs 1 combined
- **Resource Usage**: Similar overall resource consumption
- **Development Velocity**: Slightly slower initial setup, faster long-term iteration

## Implementation Details

### Project Structure

```
openshift-cluster-health-mcp/          # Standalone repository
├── cmd/
│   └── mcp-server/
│       └── main.go                    # Server entry point
├── internal/
│   ├── server/                        # MCP server logic
│   ├── tools/                         # MCP tool implementations
│   └── resources/                     # MCP resource handlers
├── pkg/
│   └── clients/                       # HTTP clients for integrations
│       ├── coordination_engine.go     # REST client for Coordination Engine
│       ├── kserve.go                  # REST client for KServe
│       ├── prometheus.go              # REST client for Prometheus
│       └── kubernetes.go              # client-go wrapper
├── charts/                            # Helm chart for deployment
└── test/                              # Unit, integration, E2E tests
```

### Service Integration Pattern

```go
// pkg/clients/coordination_engine.go
type CoordinationEngineClient struct {
    baseURL    string
    httpClient *http.Client
    token      string
}

func (c *CoordinationEngineClient) TriggerRemediation(
    ctx context.Context,
    incidentID string,
    action string,
) (*RemediationResponse, error) {
    url := fmt.Sprintf("%s/api/v1/remediation/trigger", c.baseURL)

    payload := map[string]interface{}{
        "incident_id": incidentID,
        "action":      action,
    }

    // HTTP POST to Coordination Engine
    resp, err := c.httpClient.Post(url, "application/json", payload)
    // ... error handling and response parsing
}
```

### Configuration Management

```yaml
# values.yaml - Helm chart
mcp-server:
  replicas: 2
  resources:
    limits:
      memory: 100Mi
      cpu: 200m

  integrations:
    coordinationEngine:
      enabled: true
      url: http://coordination-engine:8080
    kserve:
      enabled: true
      namespace: self-healing-platform
    prometheus:
      enabled: true
      url: https://prometheus-k8s.openshift-monitoring.svc:9091
```

### Deployment Modes

#### Mode 1: Standalone (Minimal)
```bash
helm install cluster-health-mcp ./charts/openshift-cluster-health-mcp \
  --set coordinationEngine.enabled=false \
  --set kserve.enabled=false
```

**Use Case**: Read-only cluster monitoring

#### Mode 2: With Coordination Engine
```bash
helm install cluster-health-mcp ./charts/openshift-cluster-health-mcp \
  --set coordinationEngine.enabled=true \
  --set coordinationEngine.url=http://coordination-engine:8080
```

**Use Case**: Self-healing platform with remediation workflows

#### Mode 3: Full Stack (OpenShift AI Ops)
```bash
helm install cluster-health-mcp ./charts/openshift-cluster-health-mcp \
  --set coordinationEngine.enabled=true \
  --set kserve.enabled=true
```

**Use Case**: Complete AI Ops platform with ML-powered anomaly detection

### Graceful Degradation

The standalone architecture enables graceful degradation:

```go
// internal/tools/analyze_anomalies.go
func (t *AnalyzeAnomaliesHandler) Handle(ctx context.Context, params map[string]interface{}) (*Response, error) {
    // Try KServe model first
    if t.kserveClient.IsAvailable() {
        result, err := t.kserveClient.Predict(ctx, params)
        if err == nil {
            return result, nil
        }
        log.Warn("KServe unavailable, falling back to rule-based")
    }

    // Fallback to rule-based anomaly detection
    return t.ruleBasedAnalysis(ctx, params)
}
```

## Success Criteria

### Phase 1 Success (Week 2)
- ✅ MCP server runs independently without Coordination Engine
- ✅ HTTP clients successfully communicate with backend services
- ✅ Graceful degradation when services unavailable
- ✅ Unit tests pass with mocked HTTP clients

### Phase 2 Success (Week 3)
- ✅ Deployed to dev cluster as standalone service
- ✅ Integration tests pass with real Coordination Engine
- ✅ OpenShift Lightspeed connects successfully
- ✅ All three deployment modes tested

### Phase 3 Success (Week 4)
- ✅ Production deployment with monitoring
- ✅ Service-to-service communication metrics collected
- ✅ Performance meets targets (<100ms p95 tool latency)

## Monitoring and Observability

### Metrics to Track

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `mcp_tool_duration_seconds` | Tool execution time | p95 > 200ms |
| `mcp_integration_errors_total` | Backend integration failures | >5% error rate |
| `mcp_active_sessions` | Concurrent MCP sessions | >20 sessions |
| `mcp_http_client_duration_seconds` | Backend HTTP call latency | p95 > 100ms |

### Health Checks

```go
// cmd/mcp-server/main.go
http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
    // Check critical dependencies
    healthy := true

    if !kubernetesClient.Ping() {
        healthy = false
    }

    status := map[string]interface{}{
        "healthy": healthy,
        "integrations": map[string]bool{
            "kubernetes": kubernetesClient.Ping(),
            "coordinationEngine": coordinationEngineClient.Ping(),
            "kserve": kserveClient.Ping(),
            "prometheus": prometheusClient.Ping(),
        },
    }

    if healthy {
        w.WriteHeader(http.StatusOK)
    } else {
        w.WriteHeader(http.StatusServiceUnavailable)
    }
    json.NewEncoder(w).Encode(status)
})
```

## Related ADRs

- [ADR-001: Go Language Selection](001-go-language-selection.md)
- [ADR-002: Official MCP Go SDK Adoption](002-official-mcp-go-sdk-adoption.md)
- [ADR-005: Stateless Design (No Database)](005-stateless-design.md)
- [ADR-006: Integration Architecture](006-integration-architecture.md)
- **Parent Platform ADR-015**: Service Separation - MCP Server vs REST API Service

## References

- [OpenShift Cluster Health MCP PRD](../../PRD.md)
- [containers/kubernetes-mcp-server Architecture](https://github.com/containers/kubernetes-mcp-server)
- [Parent Platform ADR-015](https://github.com/[your-org]/openshift-aiops-platform/blob/main/docs/adrs/015-service-separation-mcp-vs-rest-api.md)
- [12-Factor App Principles](https://12factor.net/)

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Network latency** | Implement HTTP client connection pooling, 5s timeout |
| **Service discovery** | Use Kubernetes Service DNS, fallback to env vars |
| **Backend unavailability** | Graceful degradation, clear error messages to AI clients |
| **Configuration drift** | Centralized configuration via Helm chart values |

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-09
