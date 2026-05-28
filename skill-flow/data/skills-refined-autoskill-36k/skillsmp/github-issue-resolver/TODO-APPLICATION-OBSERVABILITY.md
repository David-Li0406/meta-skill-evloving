# TODO: Application Observability Tools for MCP Server

## Context
Per architectural clarification: **MCP server provides observability for applications, NOT deployment**.

GitOps/ArgoCD handles application deployment. The self-healing platform (MCP + Coordination Engine) provides:
- **Application health monitoring** (detect issues)
- **Anomaly detection** (KServe ML models)
- **Remediation triggering** (Coordination Engine fixes issues)

## Architecture Boundary
```
GitOps/ArgoCD → Deploys applications (Deployments, Pods, Services)
     ↓
MCP Server → Monitors application health (observability ONLY)
     ↓
Coordination Engine → Remediates application issues (business logic)
     ↓
Kubernetes API → Applies fixes (update resources, restart pods)
```

## MCP Server: Application Observability Tools (Priority: High)

### Phase 1: Essential Monitoring Tools

#### 1. `get-deployment-health` - Deployment Status Check
**Priority**: CRITICAL (needed for notebook workflow)
- **Purpose**: Check application deployment health
- **Integration**: Kubernetes Deployment API
- **Returns**:
  - Desired/current/ready replicas
  - Deployment conditions (Available, Progressing, ReplicaFailure)
  - Rollout status
  - Strategy (RollingUpdate, Recreate)
- **Use Case**: Verify deployment after remediation (Step 5 in notebook)

```go
// internal/tools/deployment_health.go
func (t *DeploymentHealthTool) Execute(args map[string]interface{}) (interface{}, error) {
    namespace := args["namespace"].(string)
    deploymentName := args["deployment_name"].(string)

    // Query Kubernetes Deployment API
    deployment, err := t.k8sClient.AppsV1().Deployments(namespace).Get(...)

    return map[string]interface{}{
        "name": deployment.Name,
        "replicas": {
            "desired": deployment.Spec.Replicas,
            "current": deployment.Status.Replicas,
            "ready": deployment.Status.ReadyReplicas,
            "updated": deployment.Status.UpdatedReplicas,
        },
        "conditions": deployment.Status.Conditions,
        "strategy": deployment.Spec.Strategy.Type,
        "health_status": calculateHealthStatus(deployment),
    }, nil
}
```

#### 2. `get-pod-logs` - Pod Log Retrieval
**Priority**: CRITICAL (needed for investigation - Step 2 in notebook)
- **Purpose**: Retrieve pod logs for troubleshooting
- **Integration**: Kubernetes Logs API
- **Parameters**:
  - `pod_name` (required)
  - `namespace` (required)
  - `container` (optional - defaults to first container)
  - `tail_lines` (optional - default 100)
  - `since_seconds` (optional)
  - `timestamps` (optional - default false)
- **Use Case**: Investigate CrashLoopBackOff, OOMKilled errors

```go
// internal/tools/pod_logs.go
func (t *PodLogsTool) Execute(args map[string]interface{}) (interface{}, error) {
    podName := args["pod_name"].(string)
    namespace := args["namespace"].(string)
    tailLines := int64(args["tail_lines"].(float64)) // default 100

    logOptions := &corev1.PodLogOptions{
        TailLines: &tailLines,
        Timestamps: args["timestamps"].(bool),
    }

    if container, ok := args["container"].(string); ok {
        logOptions.Container = container
    }

    logs := t.k8sClient.CoreV1().Pods(namespace).GetLogs(podName, logOptions)
    // Stream logs and return
}
```

#### 3. `get-pod-events` - Pod Event History
**Priority**: HIGH (helpful for root cause analysis)
- **Purpose**: Retrieve Kubernetes events for a pod
- **Integration**: Kubernetes Events API
- **Returns**: Events related to pod (Warning, Normal, Error)
- **Use Case**: Understand why pod failed (FailedScheduling, BackOff, etc.)

```go
// internal/tools/pod_events.go
func (t *PodEventsTool) Execute(args map[string]interface{}) (interface{}, error) {
    podName := args["pod_name"].(string)
    namespace := args["namespace"].(string)

    events, err := t.k8sClient.CoreV1().Events(namespace).List(context.TODO(), metav1.ListOptions{
        FieldSelector: fmt.Sprintf("involvedObject.name=%s,involvedObject.kind=Pod", podName),
    })

    return filterAndFormatEvents(events), nil
}
```

### Phase 2: Advanced Observability Tools

#### 4. `get-replicaset-status` - ReplicaSet Health
**Priority**: MEDIUM
- **Purpose**: Check ReplicaSet status for deployment rollouts
- **Integration**: Kubernetes ReplicaSet API
- **Use Case**: Troubleshoot stuck rollouts

#### 5. `get-service-endpoints` - Service Endpoint Check
**Priority**: MEDIUM
- **Purpose**: Verify service endpoints are healthy
- **Integration**: Kubernetes Endpoints API
- **Use Case**: Detect service routing issues

#### 6. `stream-pod-logs` - Real-time Log Streaming
**Priority**: LOW (nice to have)
- **Purpose**: Stream pod logs in real-time
- **Integration**: Kubernetes Watch API
- **Use Case**: Live troubleshooting

## MCP Resources (Read-Only Application State)

### 1. `app://deployments/{namespace}` - Deployment Inventory
- List all deployments in namespace with health summary
- Cached for 30 seconds

### 2. `app://pods/{namespace}/failed` - Failed Pods
- List all failed/problematic pods in namespace
- Cached for 10 seconds (short TTL for fresh data)

### 3. `app://logs/{namespace}/{pod}` - Pod Logs Resource
- Alternative to tool-based log retrieval
- Supports MCP resource caching

## Implementation Timeline

### Week 1: Critical Tools
- [ ] `get-deployment-health` - Deployment status
- [ ] `get-pod-logs` - Log retrieval
- [ ] Update `list-pods` tool (already exists, may need enhancement)

### Week 2: Investigation Tools
- [ ] `get-pod-events` - Event history
- [ ] Add resource definitions (app:// URIs)
- [ ] Integration tests with sample app workflow

### Week 3: Enhancement
- [ ] `get-replicaset-status` - Rollout debugging
- [ ] `get-service-endpoints` - Service health
- [ ] Performance optimization and caching

## Integration with Notebook Workflow

The notebook demonstrates this workflow:
1. **Deploy** sample app (GitOps - NOT MCP)
2. **Detect** issues → `get-cluster-health`, `list-pods` ✅ (MCP)
3. **Investigate** → `get-pod-logs`, `get-pod-events` ⚠️ (MISSING)
4. **Analyze** → `analyze-anomalies` ✅ (MCP → KServe)
5. **Remediate** → `trigger-remediation` ✅ (MCP → Coordination Engine)
6. **Verify** → `get-deployment-health`, `list-pods` ⚠️ (MISSING get-deployment-health)
7. **Cleanup** → Delete deployment (oc command - NOT MCP)

Missing tools block Steps 3 and 6!

## Dependencies

- Kubernetes client library (already installed: `k8s.io/client-go`)
- RBAC permissions for:
  - Read deployments, replicasets, pods, services
  - Read events
  - Read pod logs

## Success Criteria

- ✅ Notebook workflow works end-to-end with MCP tools
- ✅ No need for manual `oc` commands for observability
- ✅ All investigation done via MCP server
- ✅ Clear separation: GitOps deploys, MCP observes, Coordination Engine remediates

## References
- Notebook: `../openshift-aiops-platform/notebooks/06-mcp-lightspeed-integration/end-to-end-troubleshooting-workflow.ipynb`
- ADR-036: Go-Based Standalone MCP Server
- ADR-002: Hybrid Deterministic-AI Self-Healing Approach

---
*Created: 2025-12-17*
*Owner: MCP Server Team*
*Related Project: openshift-cluster-health-mcp*
