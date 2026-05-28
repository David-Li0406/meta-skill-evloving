# ADR-006: Integration Architecture with Platform Services

## Status

**ACCEPTED** - 2025-12-09

## Context

The OpenShift Cluster Health MCP Server serves as an intelligent interface layer between AI assistants (OpenShift Lightspeed, Claude Desktop) and the operational data sources of the OpenShift AI Ops Platform. The server must integrate with multiple backend services while maintaining clean boundaries, graceful degradation, and operational flexibility.

### Integration Requirements

The MCP server needs to communicate with:

1. **Kubernetes API** (Required): Cluster state, pods, nodes, events
2. **Prometheus** (Optional): Metrics querying and alerting
3. **Coordination Engine** (Optional): Remediation workflows, incident management
4. **KServe InferenceServices** (Optional): ML-powered anomaly detection

### Current Platform Architecture

From the parent **OpenShift AI Ops Platform**:

```
┌─────────────────────────────────────────────────┐
│  OpenShift AI Ops Platform                      │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Coordination │  │  KServe      │            │
│  │ Engine       │  │  Models      │            │
│  │ (Flask/REST) │  │  (Predictor) │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Prometheus (OpenShift Monitoring)        │  │
│  │ - Metrics                                │  │
│  │ - Alerts                                 │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
         ▲
         │ HTTP REST APIs
         │
┌────────┴─────────────────────────────────────┐
│  OpenShift Cluster Health MCP Server (Go)    │
│  - HTTP Clients                              │
│  - Circuit Breakers                          │
│  - Graceful Degradation                      │
└──────────────────────────────────────────────┘
```

### Design Constraints

1. **Loose Coupling**: MCP server should work without all integrations
2. **Graceful Degradation**: Service unavailability shouldn't crash the server
3. **Performance**: Integration calls must not exceed tool latency targets (<100ms p95)
4. **Reusability**: MCP server deployable on clusters without Coordination Engine
5. **Testability**: Integration clients mockable for unit tests

### OpenShift Cluster Environment

Based on current cluster analysis:

- **Cluster**: OpenShift 4.18.21 (Kubernetes v1.31.10)
- **Nodes**: 7 nodes (3 control-plane, 4 workers including 1 GPU-enabled)
- **Installed Operators**: GPU, OpenShift AI, Serverless, Service Mesh, GitOps, Pipelines

## Decision

We will implement a **client-based integration architecture** with the following patterns:

1. **HTTP Client Abstraction**: One client per backend service
2. **Interface-Driven Design**: Mock-friendly interfaces for testing
3. **Graceful Degradation**: Fallback behavior when services unavailable
4. **Circuit Breaker Pattern**: Prevent cascading failures
5. **Connection Pooling**: Efficient HTTP connection reuse
6. **Configuration-Based Enablement**: Optional integrations via configuration

### Value Proposition by Integration Level

Even with only Kubernetes API integration (minimum configuration), the MCP server provides **significant value** by simplifying cluster operations through natural language. Each additional integration adds incremental capabilities:

#### Level 1: Kubernetes API Only (Minimum Viable Product)

**Core Value**: Natural language interface to cluster operations

**Capabilities**:
- ✅ **Cluster health queries**: "What's my cluster health?" → Node/pod counts, resource allocation, failed pods
- ✅ **Resource discovery**: "List deployments using >2GB memory" → AI translates to K8s API queries
- ✅ **Event debugging**: "Show recent errors in namespace production" → Filtered event lists
- ✅ **Simplified operations**: No need to remember `oc`/`kubectl` command syntax
- ✅ **Cross-namespace aggregation**: "Find all pods with high restart counts"

**Example User Experience**:
```
User: "What pods are failing?"
MCP:  "Found 3 failing pods:
       - app-worker-5 (CrashLoopBackOff, 12 restarts)
       - db-migration-job (Error, exit code 1)
       - cache-redis-2 (ImagePullBackOff)"

User: "Show me resource usage by namespace"
MCP:  "Top 5 namespaces by memory:
       1. data-processing: 45.2 GB (62% of requests)
       2. production-apps: 28.7 GB (89% of requests)
       ..."
```

**Why this is valuable**:
- Engineers avoid learning complex `oc` command syntax
- AI assistant interprets vague/ambiguous queries
- Aggregates multiple API calls into coherent answers
- Faster than manual kubectl/oc exploration

#### Level 2: + Prometheus (Enhanced Metrics)

**Incremental Value**: Historical data, advanced metrics, alerting

**New Capabilities**:
- ✅ **Time-series queries**: "Show CPU usage over last 6 hours"
- ✅ **Alert correlation**: "What alerts are firing and why?"
- ✅ **PromQL simplification**: AI translates "high memory" → complex PromQL
- ✅ **Threshold detection**: "Is this metric abnormal?" (basic anomaly detection)

**Example User Experience**:
```
User: "Is CPU usage abnormally high right now?"
MCP:  "Current CPU: 78% (24h avg: 45%). Yes, +73% above baseline.
       Alert 'HighCPUUsage' firing since 2h ago.
       Top consumers: data-processing pods (32%), ML training (21%)"
```

#### Level 3: + Coordination Engine (Self-Healing Workflows)

**Incremental Value**: Automated remediation, incident management

**New Capabilities**:
- ✅ **Remediation triggering**: "Trigger restart for failing pods"
- ✅ **Incident tracking**: "Show active incidents and their resolution status"
- ✅ **Workflow orchestration**: "Run node drain workflow for node-5"
- ✅ **Historical analysis**: "What incidents occurred last week?"

**Example User Experience**:
```
User: "Trigger remediation for incident INC-12345"
MCP:  "Workflow WF-789 started: Restarting pods in app-tier deployment.
       Status: In Progress (2/5 pods restarted)
       ETA: 2 minutes
       Workflow logs: http://coordination-engine/workflows/WF-789"
```

#### Level 4: + KServe Models (ML-Powered Intelligence)

**Incremental Value**: Predictive analytics, pattern recognition

**New Capabilities**:
- ✅ **Predictive analytics**: "Will this cluster run out of memory?"
- ✅ **Advanced anomaly detection**: ML detects patterns humans miss
- ✅ **Smart alerting**: Reduces false positives vs threshold-based
- ✅ **Root cause analysis**: ML correlates metrics across dimensions

**Example User Experience**:
```
User: "Are there any anomalies in my cluster?"
MCP:  "ML model (confidence: 87%) detected anomaly:
       - Unusual pod restart pattern in 'data-processing' namespace
       - Correlation: Memory usage spikes every 4 hours
       - Likely cause: Memory leak in app version 1.2.3
       - Recommendation: Rollback to version 1.2.2 or apply patch"
```

### Integration Value Matrix

| Integration | Use Case | User Benefit | Business Value |
|-------------|----------|--------------|----------------|
| **K8s API only** | Basic cluster operations | 10x faster than manual `oc` commands | Reduced MTTR, lower skill barrier |
| **+ Prometheus** | Historical analysis, alerting | Deep insights without PromQL expertise | Proactive issue detection |
| **+ Coordination** | Automated remediation | AI-initiated self-healing | Reduced manual intervention |
| **+ KServe** | Predictive operations | Prevent issues before they occur | Minimize downtime |

**Key Insight**: Even at Level 1 (K8s API only), the MCP server provides **substantial value** by democratizing cluster operations through natural language. Each additional integration enhances capabilities but isn't required for core functionality.

### Integration Clients

```go
// pkg/clients/interfaces.go
type KubernetesClient interface {
    ListNodes(ctx context.Context) (*NodeList, error)
    ListPods(ctx context.Context, namespace string) (*PodList, error)
    GetClusterEvents(ctx context.Context) (*EventList, error)
}

type PrometheusClient interface {
    Query(ctx context.Context, query string) (*QueryResult, error)
    GetAlerts(ctx context.Context) (*AlertList, error)
}

type CoordinationEngineClient interface {
    GetClusterHealth(ctx context.Context) (*HealthSnapshot, error)
    TriggerRemediation(ctx context.Context, req *RemediationRequest) (*WorkflowResponse, error)
    ListIncidents(ctx context.Context) (*IncidentList, error)
}

type KServeClient interface {
    PredictAnomaly(ctx context.Context, req *PredictionRequest) (*PredictionResponse, error)
    GetModelStatus(ctx context.Context, modelName string) (*ModelStatus, error)
}
```

## Integration Details

### 1. Kubernetes API Integration (Required)

**Purpose**: Foundation for all cluster operations

**Client**: Official `k8s.io/client-go` library

**Implementation**:
```go
// pkg/clients/kubernetes.go
package clients

import (
    "context"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/tools/clientcmd"
)

type K8sClient struct {
    clientset *kubernetes.Clientset
}

func NewK8sClient() (*K8sClient, error) {
    // Try in-cluster config first (production)
    config, err := rest.InClusterConfig()
    if err != nil {
        // Fallback to kubeconfig (local development)
        kubeconfig := os.Getenv("KUBECONFIG")
        if kubeconfig == "" {
            kubeconfig = filepath.Join(os.Getenv("HOME"), ".kube", "config")
        }
        config, err = clientcmd.BuildConfigFromFlags("", kubeconfig)
        if err != nil {
            return nil, err
        }
    }

    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        return nil, err
    }

    return &K8sClient{clientset: clientset}, nil
}

func (c *K8sClient) ListNodes(ctx context.Context) (*corev1.NodeList, error) {
    return c.clientset.CoreV1().Nodes().List(ctx, metav1.ListOptions{})
}

func (c *K8sClient) ListPods(ctx context.Context, namespace string) (*corev1.PodList, error) {
    return c.clientset.CoreV1().Pods(namespace).List(ctx, metav1.ListOptions{})
}
```

**Configuration**:
```yaml
# values.yaml
kubernetes:
  enabled: true  # Always required
  inCluster: true  # Use ServiceAccount token
```

**RBAC Requirements**: See ADR-007

---

### 2. Prometheus Integration (Optional)

**Purpose**: Metrics querying and alerting

**Endpoint**: `https://prometheus-k8s.openshift-monitoring.svc:9091`

**Implementation**:
```go
// pkg/clients/prometheus.go
package clients

import (
    "context"
    "fmt"
    "net/http"
    "time"
)

type PromClient struct {
    baseURL    string
    httpClient *http.Client
    token      string
    enabled    bool
}

func NewPromClient(config PromConfig) *PromClient {
    return &PromClient{
        baseURL: config.URL,
        httpClient: &http.Client{
            Timeout: 5 * time.Second,
            Transport: &http.Transport{
                MaxIdleConns:        10,
                MaxIdleConnsPerHost: 5,
                IdleConnTimeout:     30 * time.Second,
            },
        },
        token:   config.Token,
        enabled: config.Enabled,
    }
}

func (c *PromClient) Query(ctx context.Context, query string) (*QueryResult, error) {
    if !c.enabled {
        return nil, ErrServiceDisabled
    }

    url := fmt.Sprintf("%s/api/v1/query?query=%s", c.baseURL, url.QueryEscape(query))
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)

    // Bearer token authentication for OpenShift monitoring
    if c.token != "" {
        req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.token))
    }

    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("prometheus query failed: %w", err)
    }
    defer resp.Body.Close()

    // Parse Prometheus response
    var result QueryResult
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, err
    }

    return &result, nil
}
```

**Configuration**:
```yaml
# values.yaml
prometheus:
  enabled: true
  url: https://prometheus-k8s.openshift-monitoring.svc:9091
  tokenSecret: prometheus-token  # ServiceAccount token
```

**Fallback Behavior**:
```go
// Graceful degradation when Prometheus unavailable
func (t *ClusterHealthTool) getMetrics(ctx context.Context) (*Metrics, error) {
    if t.promClient.IsEnabled() {
        metrics, err := t.promClient.Query(ctx, "cluster:cpu_usage")
        if err != nil {
            log.Warn("Prometheus unavailable, using basic metrics", "error", err)
            return t.getBasicMetrics(ctx), nil
        }
        return metrics, nil
    }

    return t.getBasicMetrics(ctx), nil // Fallback: node allocatable resources
}
```

---

### 3. Coordination Engine Integration (Optional)

**Purpose**: Remediation workflows and incident management

**Endpoint**: `http://coordination-engine:8080/api/v1/`

**Implementation**:
```go
// pkg/clients/coordination_engine.go
package clients

type CoordEngineClient struct {
    baseURL    string
    httpClient *http.Client
    enabled    bool
}

func NewCoordEngineClient(config CoordEngineConfig) *CoordEngineClient {
    return &CoordEngineClient{
        baseURL: config.URL,
        httpClient: &http.Client{Timeout: 10 * time.Second},
        enabled: config.Enabled,
    }
}

func (c *CoordEngineClient) TriggerRemediation(
    ctx context.Context,
    req *RemediationRequest,
) (*WorkflowResponse, error) {
    if !c.enabled {
        return nil, ErrServiceDisabled
    }

    url := fmt.Sprintf("%s/remediation/trigger", c.baseURL)
    body, _ := json.Marshal(req)

    httpReq, _ := http.NewRequestWithContext(ctx, "POST", url, bytes.NewBuffer(body))
    httpReq.Header.Set("Content-Type", "application/json")

    resp, err := c.httpClient.Do(httpReq)
    if err != nil {
        return nil, fmt.Errorf("coordination engine failed: %w", err)
    }
    defer resp.Body.Close()

    var response WorkflowResponse
    if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
        return nil, err
    }

    return &response, nil
}
```

**Configuration**:
```yaml
# values.yaml
coordinationEngine:
  enabled: true
  url: http://coordination-engine:8080/api/v1
```

**Fallback Behavior**:
```go
// Disable remediation tools when Coordination Engine unavailable
func (t *RemediationTool) Execute(ctx context.Context, params map[string]interface{}) (*Response, error) {
    if !t.coordEngine.IsEnabled() {
        return &Response{
            Error: "Coordination Engine not available. Remediation disabled.",
        }, nil
    }

    return t.coordEngine.TriggerRemediation(ctx, params)
}
```

---

### 4. KServe Model Integration (Optional)

**Purpose**: ML-powered anomaly detection

**Endpoint**: `http://{model}-predictor.{namespace}.svc.cluster.local:{port}/v2/models/{model}/infer`

**Protocol**: KServe V2 Inference Protocol (KServe 0.11+)

**Actual Deployment**:
- Service: `anomaly-detector-predictor.self-healing-platform.svc.cluster.local`
- Service: `predictive-analytics-predictor.self-healing-platform.svc.cluster.local`
- Port: 8080 (RawDeployment mode) or 80 (Serverless mode) - configurable via `KSERVE_PREDICTOR_PORT`
- Protocol: KServe V2 (recommended over deprecated V1)

**Implementation**:
```go
// pkg/clients/kserve.go
package clients

type KServeClient struct {
    namespace  string
    httpClient *http.Client
    enabled    bool
}

type KServeConfig struct {
    Namespace string
    Timeout   time.Duration
    Enabled   bool
}

func NewKServeClient(config KServeConfig) *KServeClient {
    timeout := config.Timeout
    if timeout == 0 {
        timeout = 15 * time.Second
    }

    return &KServeClient{
        namespace:  config.Namespace,
        httpClient: &http.Client{Timeout: timeout},
        enabled:    config.Enabled,
    }
}

func (c *KServeClient) IsEnabled() bool {
    return c.enabled
}

func (c *KServeClient) DetectAnomalies(
    ctx context.Context,
    metrics []MetricData,
) (*AnomalyDetectionResult, error) {
    if !c.enabled {
        return nil, fmt.Errorf("kserve not enabled")
    }

    // Construct KServe predictor URL (V2 protocol)
    url := fmt.Sprintf("http://anomaly-detector-predictor.%s.svc.cluster.local/v2/models/anomaly-detector/infer",
        c.namespace)

    // Build V2 inference request
    inferReq := buildInferenceRequest(metrics)
    body, _ := json.Marshal(inferReq)

    httpReq, _ := http.NewRequestWithContext(ctx, "POST", url, bytes.NewBuffer(body))
    httpReq.Header.Set("Content-Type", "application/json")

    resp, err := c.httpClient.Do(httpReq)
    if err != nil {
        return nil, fmt.Errorf("kserve prediction failed: %w", err)
    }
    defer resp.Body.Close()

    var result AnomalyDetectionResult
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, err
    }

    return &result, nil
}
```

**Configuration**:
```yaml
# values.yaml
kserve:
  enabled: true
  namespace: self-healing-platform
  models:
    - name: predictive-analytics
      endpoint: predictive-analytics-predictor
```

**Fallback Behavior**:
```go
// Fallback to rule-based anomaly detection when KServe unavailable
func (t *AnomalyTool) Execute(ctx context.Context, params map[string]interface{}) (*Response, error) {
    if t.kserveClient.IsEnabled() {
        result, err := t.kserveClient.PredictAnomaly(ctx, params)
        if err == nil {
            return result, nil
        }
        log.Warn("KServe unavailable, falling back to rule-based detection", "error", err)
    }

    // Fallback: Threshold-based anomaly detection
    return t.ruleBasedAnomaly Detection(ctx, params), nil
}
```

## Circuit Breaker Pattern

Prevent cascading failures when backend services are slow or unavailable:

```go
// pkg/clients/circuit_breaker.go
package clients

import (
    "sync"
    "time"
)

type CircuitBreaker struct {
    maxFailures  int
    resetTimeout time.Duration
    failures     int
    lastFailure  time.Time
    state        string // "closed", "open", "half-open"
    mu           sync.RWMutex
}

func NewCircuitBreaker(maxFailures int, resetTimeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{
        maxFailures:  maxFailures,
        resetTimeout: resetTimeout,
        state:        "closed",
    }
}

func (cb *CircuitBreaker) Call(fn func() error) error {
    cb.mu.RLock()
    state := cb.state
    cb.mu.RUnlock()

    switch state {
    case "open":
        // Circuit open, check if reset timeout passed
        if time.Since(cb.lastFailure) > cb.resetTimeout {
            cb.mu.Lock()
            cb.state = "half-open"
            cb.mu.Unlock()
        } else {
            return ErrCircuitOpen
        }

    case "half-open":
        // Try one request
        err := fn()
        if err != nil {
            cb.recordFailure()
            return err
        }
        cb.reset()
        return nil
    }

    // Closed state, execute normally
    err := fn()
    if err != nil {
        cb.recordFailure()
        return err
    }

    return nil
}

func (cb *CircuitBreaker) recordFailure() {
    cb.mu.Lock()
    defer cb.mu.Unlock()

    cb.failures++
    cb.lastFailure = time.Now()

    if cb.failures >= cb.maxFailures {
        cb.state = "open"
        log.Warn("Circuit breaker opened", "failures", cb.failures)
    }
}

func (cb *CircuitBreaker) reset() {
    cb.mu.Lock()
    defer cb.mu.Unlock()

    cb.failures = 0
    cb.state = "closed"
}
```

**Usage**:
```go
// Wrap HTTP calls with circuit breaker
func (c *CoordEngineClient) TriggerRemediation(ctx context.Context, req *RemediationRequest) (*WorkflowResponse, error) {
    var response *WorkflowResponse

    err := c.circuitBreaker.Call(func() error {
        resp, err := c.httpClient.Post(c.baseURL+"/remediation/trigger", "application/json", req)
        if err != nil {
            return err
        }
        response = parseResponse(resp)
        return nil
    })

    if err == ErrCircuitOpen {
        return nil, fmt.Errorf("coordination engine circuit breaker open")
    }

    return response, err
}
```

## Configuration Management

### values.yaml

```yaml
# Helm chart configuration
integrations:
  kubernetes:
    enabled: true
    inCluster: true

  prometheus:
    enabled: true
    url: https://prometheus-k8s.openshift-monitoring.svc:9091
    tokenSecret: prometheus-token

  coordinationEngine:
    enabled: false  # Optional
    url: http://coordination-engine:8080/api/v1
    timeout: 10s

  kserve:
    enabled: false  # Optional
    namespace: self-healing-platform
    timeout: 15s

circuitBreaker:
  maxFailures: 5
  resetTimeout: 30s
```

### Environment Variables

```bash
# Production (in Kubernetes)
KUBERNETES_SERVICE_HOST=10.0.0.1
COORDINATION_ENGINE_URL=http://coordination-engine:8080/api/v1
KSERVE_NAMESPACE=self-healing-platform
PROMETHEUS_URL=https://prometheus-k8s.openshift-monitoring.svc:9091

# Local development
KUBECONFIG=/Users/dev/.kube/config
COORDINATION_ENGINE_URL=http://localhost:8080/api/v1
KSERVE_ENABLED=false
```

## Testing Strategy

### Unit Tests with Mocks

```go
// test/unit/tools_test.go
package tools_test

import (
    "testing"
    "github.com/stretchr/testify/mock"
)

type MockK8sClient struct {
    mock.Mock
}

func (m *MockK8sClient) ListNodes(ctx context.Context) (*NodeList, error) {
    args := m.Called(ctx)
    return args.Get(0).(*NodeList), args.Error(1)
}

func TestClusterHealthTool(t *testing.T) {
    mockK8s := new(MockK8sClient)
    mockK8s.On("ListNodes", mock.Anything).Return(&NodeList{
        Items: []Node{{Name: "node-1", Status: "Ready"}},
    }, nil)

    tool := NewClusterHealthTool(mockK8s, nil, nil)
    result, err := tool.Execute(context.Background())

    assert.NoError(t, err)
    assert.Equal(t, 1, result.NodeCount)
    mockK8s.AssertExpectations(t)
}
```

### Integration Tests with Real Backends

```go
// test/integration/integration_test.go
func TestRealK8sIntegration(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test")
    }

    k8sClient, err := NewK8sClient()
    require.NoError(t, err)

    nodes, err := k8sClient.ListNodes(context.Background())
    require.NoError(t, err)
    assert.Greater(t, len(nodes.Items), 0)
}
```

## Deployment Modes

### Mode 1: Standalone (Minimal)

```bash
helm install cluster-health-mcp ./charts \
  --set coordinationEngine.enabled=false \
  --set kserve.enabled=false
```

**Available Tools**:
- ✅ get-cluster-health (Kubernetes API only)
- ✅ list-pods (Kubernetes API)
- ❌ analyze-anomalies (requires KServe)
- ❌ trigger-remediation (requires Coordination Engine)

### Mode 2: With Coordination Engine

```bash
helm install cluster-health-mcp ./charts \
  --set coordinationEngine.enabled=true \
  --set coordinationEngine.url=http://coordination-engine:8080/api/v1
```

**Available Tools**:
- ✅ get-cluster-health
- ✅ list-pods
- ❌ analyze-anomalies
- ✅ trigger-remediation

### Mode 3: Full Stack (All Integrations)

```bash
helm install cluster-health-mcp ./charts \
  --set coordinationEngine.enabled=true \
  --set kserve.enabled=true
```

**Available Tools**:
- ✅ get-cluster-health
- ✅ list-pods
- ✅ analyze-anomalies
- ✅ trigger-remediation

## Monitoring and Observability

### Metrics

```go
var (
    integrationCallsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "mcp_integration_calls_total",
            Help: "Total integration API calls",
        },
        []string{"service", "method", "status"},
    )

    integrationDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "mcp_integration_duration_seconds",
            Help:    "Integration call duration",
            Buckets: []float64{.01, .05, .1, .5, 1, 2, 5},
        },
        []string{"service", "method"},
    )

    circuitBreakerState = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "mcp_circuit_breaker_state",
            Help: "Circuit breaker state (0=closed, 1=open, 2=half-open)",
        },
        []string{"service"},
    )
)
```

## Success Criteria

### Phase 1 Success (Week 2)
- ✅ All 4 integration clients implemented
- ✅ Unit tests with mocks passing
- ✅ Graceful degradation working
- ✅ Circuit breakers functioning

### Phase 2 Success (Week 3)
- ✅ Integration tests with real backends passing
- ✅ All 3 deployment modes tested
- ✅ Fallback behaviors validated
- ✅ Performance targets met (<100ms p95)

### Phase 3 Success (Week 4)
- ✅ Production deployment stable
- ✅ Circuit breakers preventing cascading failures
- ✅ Integration metrics collected
- ✅ Documentation complete

## Related ADRs

- [ADR-003: Standalone MCP Server Architecture](003-standalone-mcp-server-architecture.md)
- [ADR-005: Stateless Design (No Database)](005-stateless-design.md)
- [ADR-007: RBAC-Based Security Model](007-rbac-based-security-model.md)

## References

- [OpenShift Cluster Health MCP PRD](../../PRD.md)
- [Coordination Engine API Documentation](https://github.com/[your-org]/openshift-aiops-platform/blob/main/src/coordination-engine/README.md)
- [KServe V2 Inference Protocol](https://kserve.github.io/website/modelserving/data_plane/v2_protocol/)
- [KServe V1 Protocol (deprecated)](https://kserve.github.io/website/modelserving/v1beta1/serving_runtime/)
- [Prometheus HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/)

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-09
