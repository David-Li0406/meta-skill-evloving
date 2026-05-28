# ADR-009: Architecture Evolution Roadmap

## Status

**ACCEPTED** - 2025-12-09

## Context

The OpenShift Cluster Health MCP Server is being built to integrate with the existing **OpenShift AI Ops Platform**, which currently has:

- **Coordination Engine**: Python/Flask with PostgreSQL (remediation workflows, incident management)
- **ML Services**: Python/KServe models (anomaly detection, predictive analytics)
- **Prometheus**: OpenShift monitoring stack
- **Kubernetes API**: OpenShift 4.18.21

However, there are strategic questions about the long-term architecture:

1. **Should Coordination Engine stay in Python or move to Go?**
2. **Should ML Services stay in Python or move to Go?**
3. **Should the MCP server support standalone Kubernetes-only mode?**
4. **What's the migration path from current state to desired state?**

### Current Architecture Concerns

**Python Coordination Engine Issues**:
- Separate deployment from MCP server (two containers, two services)
- HTTP overhead for MCP ↔ Coordination Engine communication
- Different language ecosystems (Go vs Python)
- Heavier resource footprint (Flask + Gunicorn + PostgreSQL)

**Benefits of Current Architecture**:
- ✅ Working implementation (already deployed)
- ✅ Python ecosystem for data science integrations
- ✅ PostgreSQL for incident history and workflow state
- ✅ Separate scaling of MCP vs remediation workloads

### Strategic Considerations

1. **Reusability**: Could the Coordination Engine itself use the MCP server for K8s operations?
2. **Extensibility**: Can end users build their own ML services and integrate them?
3. **Simplicity**: Would a unified Go service be simpler to deploy and operate?
4. **Ecosystem Fit**: Python is better for ML/data science, Go is better for infrastructure

## Decision

We will evolve the architecture in **three phases**:

1. **Phase 1 (Current)**: Work with existing Python services
2. **Phase 2 (6-12 months)**: Move Coordination Engine to Go, keep ML Services in Python
3. **Phase 3 (12-18 months)**: Support standalone K8s-only mode for broader adoption

This phased approach allows us to:
- Ship value immediately with existing architecture
- Evolve toward optimal architecture without blocking current work
- Enable reusability and extensibility over time

## Architecture Evolution

### Phase 1: Integration with Existing Platform (Months 0-6)

**Status**: Current focus (PRD Phases 1-5)

**Architecture**:
```
┌────────────────────────────────────────────────────────┐
│  MCP Clients (OpenShift Lightspeed, Claude Desktop)   │
└──────────────────┬─────────────────────────────────────┘
                   │ MCP Protocol (HTTP/stdio)
                   ▼
┌──────────────────────────────────────────────────────────┐
│  OpenShift Cluster Health MCP Server (Go) - NEW          │
│  - MCP protocol handler                                  │
│  - HTTP clients for backend integration                  │
│  - Circuit breakers, caching, graceful degradation       │
└────┬─────────┬─────────┬─────────┬────────────────────────┘
     │ HTTP    │ HTTP    │ HTTP    │ K8s API
     ▼         ▼         ▼         ▼
┌──────────┐ ┌─────────┐ ┌────────┐ ┌──────────────┐
│Coord Eng │ │ KServe  │ │Prometh │ │ Kubernetes   │
│(Python)  │ │(Python) │ │(Metrics)│ │ API Server   │
│EXISTING  │ │EXISTING │ │EXISTING │ │              │
└──────────┘ └─────────┘ └────────┘ └──────────────┘
```

**Goal**: Prove MCP server value with existing services

**Integration Points**:
- **Required**: Kubernetes API, Prometheus (OpenShift monitoring)
- **Recommended**: Coordination Engine (remediation workflows)
- **Advanced**: KServe models (ML anomaly detection)

**Success Criteria**:
- ✅ MCP server deployed to production
- ✅ OpenShift Lightspeed integration working
- ✅ All existing Python services remain unchanged
- ✅ Natural language queries working end-to-end

**Deliverables**:
- Go-based MCP server (ADR-001, ADR-002)
- HTTP integration clients (ADR-006)
- Helm chart for deployment
- Production documentation

---

### Phase 2: Coordination Engine in Go (Months 6-12)

**Status**: Future roadmap

**Architecture**:
```
┌────────────────────────────────────────────────────────┐
│  MCP Clients (OpenShift Lightspeed, Claude Desktop)   │
└──────────────────┬─────────────────────────────────────┘
                   │ MCP Protocol
                   ▼
┌──────────────────────────────────────────────────────────┐
│  Unified OpenShift AI Ops Server (Go) - EVOLVED         │
│  ┌────────────────┐  ┌─────────────────────────────┐   │
│  │ MCP Protocol   │  │ Coordination Engine (Go)    │   │
│  │ Handler        │  │ - Remediation workflows     │   │
│  └────────────────┘  │ - Incident management       │   │
│                      │ - PostgreSQL client         │   │
│  Shared Components:  └─────────────────────────────┘   │
│  - Kubernetes client-go                                 │
│  - Prometheus client                                    │
│  - Common logging, metrics, config                      │
└────┬─────────┬─────────┬────────────────────────────────┘
     │ HTTP    │ gRPC    │ K8s API
     ▼         ▼         ▼
┌─────────┐ ┌────────┐ ┌──────────────┐
│ KServe  │ │Prometh │ │ PostgreSQL   │
│(Python) │ │(Metrics)│ │ (State DB)   │
│ ML Svcs │ │        │ │              │
└─────────┘ └────────┘ └──────────────┘
```

**Why Move Coordination Engine to Go?**

1. **Shared Kubernetes Client**: Both MCP and Coordination Engine need K8s API access
   ```go
   // Single client-go instance used by both components
   k8sClient := kubernetes.NewForConfig(config)

   // MCP tools use it
   mcpServer.RegisterTool("get-cluster-health",
       NewClusterHealthTool(k8sClient))

   // Coordination Engine uses it
   remediationEngine.RegisterWorkflow("restart-pod",
       NewPodRestartWorkflow(k8sClient))
   ```

2. **Eliminate HTTP Overhead**: Direct function calls instead of HTTP
   ```go
   // Before (HTTP):
   resp, err := http.Post("http://coordination-engine/remediation/trigger", ...)
   // Latency: 10-20ms HTTP overhead

   // After (direct call):
   resp, err := coordinationEngine.TriggerRemediation(ctx, req)
   // Latency: <1ms
   ```

3. **Single Binary Deployment**: One container instead of two
   ```yaml
   # Before: 2 deployments
   - cluster-health-mcp (Go)
   - coordination-engine (Python/Gunicorn)

   # After: 1 deployment
   - openshift-aiops-server (Go)
   ```

4. **Unified Configuration**: Single values.yaml for entire service
   ```yaml
   # Before: Separate configs
   mcp-server: {...}
   coordination-engine: {...}

   # After: Unified config
   aiops-server:
     mcp: {...}
     coordination: {...}
   ```

5. **Resource Efficiency**:
   ```
   Before:
   - MCP Server: 50 MB memory
   - Coordination Engine: 200 MB (Python + Gunicorn)
   - Total: 250 MB

   After:
   - Unified Server: 120 MB (Go with PostgreSQL driver)
   - Savings: 52% memory reduction
   ```

6. **Operational Simplicity**:
   - One service to monitor (not two)
   - One set of logs to aggregate
   - One RBAC ServiceAccount
   - One NetworkPolicy

**Why Keep ML Services in Python?**

1. **Data Science Ecosystem**: NumPy, Pandas, scikit-learn, TensorFlow
2. **KServe Runtime**: KServe inference servers are Python-based
3. **Notebook Integration**: Jupyter notebooks for model development
4. **Team Expertise**: Data science team uses Python
5. **No Performance Penalty**: ML inference is async/batch, not latency-sensitive

**Migration Strategy**:

1. **Rewrite Coordination Engine in Go**:
   ```go
   // pkg/coordination/engine.go
   type Engine struct {
       k8sClient  *kubernetes.Clientset
       db         *sql.DB
       workflows  map[string]Workflow
   }

   func (e *Engine) TriggerRemediation(ctx context.Context, req *RemediationRequest) (*WorkflowResponse, error) {
       // Ported from Python coordination-engine
   }
   ```

2. **Maintain API Compatibility**: Keep same REST endpoints for backward compat
   ```go
   // Existing Python API: POST /api/v1/remediation/trigger
   // Go implementation provides same endpoint
   http.HandleFunc("/api/v1/remediation/trigger", e.handleTriggerRemediation)
   ```

3. **Gradual Migration**: Run both services in parallel, switch over
   ```bash
   # Stage 1: Deploy Go version alongside Python
   helm install aiops-server-go ./charts --set enabled=true

   # Stage 2: Route 10% traffic to Go version (canary)
   # Stage 3: Route 50% traffic (A/B test)
   # Stage 4: Route 100% traffic
   # Stage 5: Deprecate Python version
   ```

**Success Criteria**:
- ✅ Coordination Engine functionality ported to Go
- ✅ Single binary deployment working
- ✅ 50%+ memory reduction achieved
- ✅ All integration tests passing
- ✅ Production deployment stable for 30 days

---

### Phase 3: Standalone Kubernetes Mode (Months 12-18)

**Status**: Future roadmap

**Architecture**:
```
┌─────────────────────────────────────────────────────────┐
│  Deployment Mode Selection (Helm values.yaml)           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Mode 1: Standalone K8s (Minimal)                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  MCP Server (Go)                                  │  │
│  │  - Kubernetes API only                            │  │
│  │  - No Prometheus                                  │  │
│  │  - No Coordination Engine                         │  │
│  │  - No ML Services                                 │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  Use Case: Generic K8s MCP server for any cluster       │
│  Target: Users who want basic K8s queries via MCP        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Mode 2: OpenShift Monitoring (Standard)                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  MCP Server (Go)                                  │  │
│  │  - Kubernetes API ✅                              │  │
│  │  - Prometheus ✅ (OpenShift monitoring)           │  │
│  │  - No Coordination Engine                         │  │
│  │  - No ML Services                                 │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  Use Case: OpenShift monitoring via natural language    │
│  Target: OpenShift users without AI Ops platform         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Mode 3: Full AI Ops Stack (Advanced)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Unified AI Ops Server (Go)                       │  │
│  │  - Kubernetes API ✅                              │  │
│  │  - Prometheus ✅                                  │  │
│  │  - Coordination Engine ✅ (built-in)              │  │
│  │  - ML Services ✅ (external Python)               │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  Use Case: Complete self-healing platform               │
│  Target: OpenShift AI Ops platform users (our focus)    │
└─────────────────────────────────────────────────────────┘
```

**Why Support Standalone Mode?**

1. **Coordination Engine Can Use It**:
   ```go
   // Coordination Engine itself can use MCP server for K8s operations
   // Instead of direct client-go calls, use MCP tools

   // Before:
   pods, err := k8sClient.CoreV1().Pods(namespace).List(ctx, ...)

   // After (using MCP):
   result, err := mcpClient.CallTool("list-pods", map[string]interface{}{
       "namespace": namespace,
   })
   ```
   **Why?** Future AI-assisted remediation workflows can use LLMs

2. **End Users Build Custom ML Services**:
   ```python
   # User-defined ML service
   from flask import Flask, request
   import custom_anomaly_detector

   app = Flask(__name__)

   @app.route('/predict', methods=['POST'])
   def predict():
       data = request.json
       anomaly_score = custom_anomaly_detector.analyze(data)
       return {'anomaly_score': anomaly_score}
   ```

   ```yaml
   # User configures MCP server to use their ML service
   mlServices:
     customAnomalyDetector:
       enabled: true
       url: http://custom-ml-service:8080/predict
   ```

3. **Broader Community Adoption**:
   - Vanilla Kubernetes users (not just OpenShift)
   - Users without full AI Ops platform
   - Developers wanting MCP for their clusters

4. **Composability**:
   ```
   User A: K8s-only (basic queries)
   User B: K8s + Prometheus (monitoring)
   User C: K8s + Prometheus + Custom ML (their anomaly detection)
   User D: Full AI Ops stack (our platform)
   ```

**Implementation Strategy**:

```yaml
# values.yaml - Feature flags
deployment:
  mode: full  # standalone | monitoring | full

integrations:
  kubernetes:
    enabled: true  # Always required

  prometheus:
    enabled: true  # true for monitoring/full, false for standalone

  coordinationEngine:
    enabled: true     # true for full, false for others
    builtin: true     # Use built-in Go engine (Phase 2)

  mlServices:
    # Support multiple ML service backends
    kserve:
      enabled: true
      namespace: self-healing-platform

    # User-defined services
    custom:
      - name: custom-anomaly-detector
        url: http://custom-ml:8080/predict
        enabled: false
```

**Success Criteria**:
- ✅ All 3 deployment modes working
- ✅ Standalone mode documented
- ✅ Community adoption (external users)
- ✅ Plugin architecture for custom ML services
- ✅ Coordination Engine using MCP server for K8s ops

---

## Roadmap Timeline

| Phase | Timeline | Focus | Deliverables |
|-------|----------|-------|--------------|
| **Phase 1** | Months 0-6 | Integration with existing Python services | MCP server (Go), OpenShift Lightspeed integration |
| **Phase 2** | Months 6-12 | Move Coordination Engine to Go | Unified Go server, 50% memory reduction |
| **Phase 3** | Months 12-18 | Standalone mode, extensibility | 3 deployment modes, plugin architecture |

## Decision Rationale

### Why This Phased Approach?

1. **Deliver Value Immediately**: Don't block on architecture debates
2. **Learn from Production**: Phase 1 informs Phase 2 design decisions
3. **Minimize Risk**: Gradual migration vs big-bang rewrite
4. **Backward Compatibility**: Python services continue working during transition
5. **Community Building**: Phase 3 enables broader adoption

### Why Go for Coordination Engine?

| Aspect | Python/Flask | Go | Winner |
|--------|--------------|-----|--------|
| **Memory** | 200 MB | 70 MB | Go (-65%) |
| **Startup** | 3-5s | <1s | Go (5x faster) |
| **Deployment** | Gunicorn + workers | Single binary | Go (simpler) |
| **K8s Integration** | kubernetes-python | client-go (official) | Go (native) |
| **MCP Integration** | HTTP calls | Direct functions | Go (no overhead) |
| **Type Safety** | Dynamic typing | Static typing | Go (fewer bugs) |
| **Ecosystem** | Better for ML/data | Better for infra | **Context-dependent** |

**Conclusion**: Go is better for infrastructure orchestration, Python is better for ML/data science.

### Why Keep ML Services in Python?

| Aspect | Go | Python | Winner |
|--------|-----|--------|--------|
| **ML Libraries** | Limited | NumPy, Pandas, scikit-learn, TensorFlow | Python |
| **KServe** | Not supported | Native runtime | Python |
| **Notebooks** | Not applicable | Jupyter integration | Python |
| **Data Science Team** | Learning curve | Existing expertise | Python |
| **Performance** | Faster (not needed for ML) | Adequate for ML | Python (ecosystem wins) |

**Conclusion**: Python is the right choice for ML/data science workloads.

## Migration Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Phase 2 rewrite takes longer** | High | Medium | Incremental migration, canary deployments |
| **Breaking changes in Go port** | Medium | High | API compatibility tests, parallel deployment |
| **Team Go expertise gap** | Medium | Low | 6-month ramp-up during Phase 1, training |
| **Community adoption (Phase 3)** | Medium | Low | Documentation, examples, support forum |
| **PostgreSQL performance in Go** | Low | Low | Use pgx driver (proven, high-performance) |

## Related ADRs

- [ADR-001: Go Language Selection](001-go-language-selection.md) - Foundation for Phase 1
- [ADR-003: Standalone MCP Server Architecture](003-standalone-mcp-server-architecture.md) - Phase 1 architecture
- [ADR-006: Integration Architecture](006-integration-architecture.md) - Phase 1 integration patterns

## References

- [OpenShift Cluster Health MCP PRD](../../PRD.md) - Phase 1 requirements
- [OpenShift AI Ops Platform](https://github.com/[your-org]/openshift-aiops-platform) - Current platform
- [Coordination Engine Source](https://github.com/[your-org]/openshift-aiops-platform/tree/main/src/coordination-engine)

## Success Metrics

### Phase 1 Success
- ✅ MCP server deployed to production
- ✅ 100+ natural language queries/day via OpenShift Lightspeed
- ✅ <100ms p95 tool latency
- ✅ Integration with all Python services working

### Phase 2 Success
- ✅ Unified Go server in production
- ✅ 50%+ memory reduction vs Phase 1
- ✅ All Coordination Engine features ported
- ✅ Zero downtime migration

### Phase 3 Success
- ✅ 3 deployment modes documented and tested
- ✅ 5+ external organizations using standalone mode
- ✅ 3+ custom ML service integrations by users
- ✅ Coordination Engine using MCP for K8s operations

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **Data Science Team**: Approved (keeping ML in Python)
- **Date**: 2025-12-09

---

**Next Actions**:
1. Focus on Phase 1 implementation (PRD Phases 1-5)
2. Document Coordination Engine API for Phase 2 migration planning
3. Create proof-of-concept for Go Coordination Engine (Month 6)
4. Gather community feedback on standalone mode requirements (Month 9)
