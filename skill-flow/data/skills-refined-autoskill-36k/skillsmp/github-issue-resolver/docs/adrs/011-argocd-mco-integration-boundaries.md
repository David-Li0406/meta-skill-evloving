# ADR-011: ArgoCD and MCO Integration Boundaries

## Status

**ACCEPTED** - 2025-12-17

## Context

The OpenShift Cluster Health MCP Server operates in an environment where ArgoCD and Machine Config Operator (MCO) already provide robust application and infrastructure management capabilities. We must define clear boundaries to avoid duplicating their functionality while enabling intelligent coordination for AI-driven remediation.

### Existing Platform Capabilities

**ArgoCD (Application Layer)**:
- GitOps-based declarative application deployment
- Automated sync from Git repositories
- Application health assessment and status tracking
- Self-healing via automated sync
- Manual and automated sync strategies
- Rollback capabilities

**Machine Config Operator (Infrastructure Layer)**:
- Node-level configuration management
- OS updates and patches
- Machine configuration drift detection
- Rolling updates with safety mechanisms
- Automatic rollback on failures

**Coordination Engine (Remediation Layer)**:
- Multi-layer remediation orchestration
- Incident management and tracking
- Workflow execution
- Integration with monitoring and alerting

### Problem Statement

Without clear boundaries, we risk:
1. **Duplication**: Reimplementing ArgoCD sync or MCO config logic
2. **Conflicts**: MCP-triggered changes conflicting with GitOps/MCO automation
3. **Complexity**: Multiple systems making uncoordinated remediation decisions
4. **Maintenance Burden**: Maintaining parallel implementations of existing features

### Key Questions

1. **When should MCP trigger ArgoCD sync vs. direct Kubernetes API changes?**
2. **How do we detect if an application is ArgoCD-managed?**
3. **What remediation actions are appropriate for non-ArgoCD applications?**
4. **How do we coordinate with MCO for infrastructure-layer issues?**

## Decision

We will establish **clear integration boundaries** based on the principle: **Observe, Recommend, Coordinate - Don't Duplicate**.

### Core Principles

1. **Leverage Existing Capabilities**: Use ArgoCD for GitOps apps, MCO for node config
2. **Detection-Based Routing**: Automatically detect deployment method and route remediation appropriately
3. **Recommendation Over Execution**: For ArgoCD/MCO-managed resources, recommend actions rather than execute directly
4. **Direct Action for Gaps**: Only perform direct remediation for resources outside ArgoCD/MCO scope
5. **Coordination Layer**: Act as intelligent orchestrator across layers

### Integration Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│  MCP Server + Coordination Engine (Our Scope)               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  OBSERVABILITY & INTELLIGENCE                         │  │
│  │  ✅ Cluster health monitoring                         │  │
│  │  ✅ Anomaly detection (ML-powered)                    │  │
│  │  ✅ Root cause analysis                               │  │
│  │  ✅ Cross-layer correlation                           │  │
│  │  ✅ Deployment method detection                       │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  COORDINATION & RECOMMENDATIONS                       │  │
│  │  ✅ Multi-layer remediation orchestration             │  │
│  │  ✅ Recommendation generation                         │  │
│  │  ✅ Incident tracking and workflow management         │  │
│  │  ✅ Integration with ArgoCD/MCO APIs                  │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  DIRECT REMEDIATION (Non-ArgoCD/MCO Only)            │  │
│  │  ✅ Manual deployments (kubectl apply)                │  │
│  │  ✅ Helm releases (non-GitOps)                        │  │
│  │  ✅ Temporary debugging resources                     │  │
│  │  ✅ Operator-managed applications (case-by-case)      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ArgoCD (Application Layer) - DO NOT DUPLICATE              │
│  ❌ GitOps sync (handled by ArgoCD)                         │
│  ❌ Git repository polling (handled by ArgoCD)              │
│  ❌ Application manifest rendering (handled by ArgoCD)      │
│  ✅ Trigger sync via ArgoCD API (coordination)              │
│  ✅ Monitor ArgoCD Application status (observability)       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MCO (Infrastructure Layer) - DO NOT DUPLICATE              │
│  ❌ MachineConfig creation (handled by MCO)                 │
│  ❌ Node OS updates (handled by MCO)                        │
│  ❌ Config drift remediation (handled by MCO)               │
│  ✅ Monitor MachineConfigPool status (observability)        │
│  ✅ Recommend MachineConfig changes (coordination)          │
└─────────────────────────────────────────────────────────────┘
```

### Deployment Method Detection

```go
// pkg/detector/deployment_method.go
package detector

import (
    "context"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

type DeploymentMethod string

const (
    DeploymentMethodArgoCD   DeploymentMethod = "argocd"
    DeploymentMethodHelm     DeploymentMethod = "helm"
    DeploymentMethodOperator DeploymentMethod = "operator"
    DeploymentMethodManual   DeploymentMethod = "manual"
    DeploymentMethodUnknown  DeploymentMethod = "unknown"
)

type DeploymentInfo struct {
    Method      DeploymentMethod
    Managed     bool              // Is it managed by GitOps/Operator?
    Source      string            // Git repo, Helm chart, etc.
    ManagedBy   string            // ArgoCD Application name, Operator name, etc.
}

// DetectDeploymentMethod determines how a resource was deployed
func DetectDeploymentMethod(ctx context.Context, namespace, name string, labels, annotations map[string]string) (*DeploymentInfo, error) {
    info := &DeploymentInfo{
        Method: DeploymentMethodUnknown,
    }

    // Check for ArgoCD annotations (primary indicator)
    if appName, ok := annotations["argocd.argoproj.io/tracking-id"]; ok {
        info.Method = DeploymentMethodArgoCD
        info.Managed = true
        info.ManagedBy = annotations["argocd.argoproj.io/application"]
        info.Source = annotations["argocd.argoproj.io/git-repository"]
        return info, nil
    }

    // Check for ArgoCD labels (fallback)
    if appInstance, ok := labels["app.kubernetes.io/instance"]; ok {
        if _, hasArgoLabel := labels["argocd.argoproj.io/instance"]; hasArgoLabel {
            info.Method = DeploymentMethodArgoCD
            info.Managed = true
            info.ManagedBy = appInstance
            return info, nil
        }
    }

    // Check for Helm annotations
    if helmRelease, ok := annotations["meta.helm.sh/release-name"]; ok {
        info.Method = DeploymentMethodHelm
        info.ManagedBy = helmRelease
        // Helm releases are NOT GitOps-managed unless via ArgoCD
        info.Managed = false
        return info, nil
    }

    // Check for Operator ownership
    if len(labels["app.kubernetes.io/managed-by"]) > 0 {
        info.Method = DeploymentMethodOperator
        info.ManagedBy = labels["app.kubernetes.io/managed-by"]
        // Operators are self-managing
        info.Managed = true
        return info, nil
    }

    // Default to manual deployment
    info.Method = DeploymentMethodManual
    info.Managed = false
    return info, nil
}
```

### Remediation Decision Logic

```go
// pkg/remediation/strategy.go
package remediation

type RemediationStrategy struct {
    Action      string   // What to do
    Method      string   // How to do it
    Reason      string   // Why this approach
    Commands    []string // Specific commands/API calls
}

// DetermineStrategy selects appropriate remediation based on deployment method
func DetermineStrategy(ctx context.Context, issue *Issue, deploymentInfo *DeploymentInfo) (*RemediationStrategy, error) {
    switch deploymentInfo.Method {
    case DeploymentMethodArgoCD:
        return argocdManagedStrategy(issue, deploymentInfo)

    case DeploymentMethodHelm:
        return helmManagedStrategy(issue, deploymentInfo)

    case DeploymentMethodOperator:
        return operatorManagedStrategy(issue, deploymentInfo)

    case DeploymentMethodManual:
        return manualDeploymentStrategy(issue, deploymentInfo)

    default:
        return conservativeStrategy(issue, deploymentInfo)
    }
}

func argocdManagedStrategy(issue *Issue, info *DeploymentInfo) (*RemediationStrategy, error) {
    return &RemediationStrategy{
        Action: "Trigger ArgoCD Sync",
        Method: "argocd_api",
        Reason: fmt.Sprintf("Application '%s' is managed by ArgoCD. Use GitOps workflow to ensure declarative state.", info.ManagedBy),
        Commands: []string{
            fmt.Sprintf("argocd app sync %s", info.ManagedBy),
            // Or via Kubernetes API:
            // kubectl patch application <app> -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"mcp-server"},"sync":{"revision":"HEAD"}}}'
        },
    }, nil
}

func manualDeploymentStrategy(issue *Issue, info *DeploymentInfo) (*RemediationStrategy, error) {
    // Direct Kubernetes API remediation is safe for manual deployments
    return &RemediationStrategy{
        Action: "Direct Kubernetes API Remediation",
        Method: "kubernetes_api",
        Reason: "Resource is manually deployed (no GitOps/Operator management). Direct remediation is appropriate.",
        Commands: []string{
            generateKubernetesAPICommand(issue),
        },
    }, nil
}
```

### Integration Patterns

#### Pattern 1: ArgoCD-Managed Application Remediation

```go
// internal/tools/trigger_remediation.go
func (t *RemediationTool) handleArgocdManagedApp(ctx context.Context, app string) (*Response, error) {
    // Step 1: Check ArgoCD Application status
    appStatus, err := t.argocdClient.GetApplication(ctx, app)
    if err != nil {
        return nil, fmt.Errorf("failed to get ArgoCD app: %w", err)
    }

    // Step 2: Determine if sync is needed
    if appStatus.Status.Sync.Status == "OutOfSync" {
        // Step 3: Trigger ArgoCD sync (don't apply manifests directly)
        syncResult, err := t.argocdClient.SyncApplication(ctx, app, &SyncOptions{
            Prune:  false, // Don't delete resources
            DryRun: false,
        })
        if err != nil {
            return nil, fmt.Errorf("argocd sync failed: %w", err)
        }

        return &Response{
            Status: "success",
            Message: fmt.Sprintf("Triggered ArgoCD sync for application '%s'", app),
            Details: map[string]interface{}{
                "sync_result": syncResult,
                "method":      "argocd_sync",
            },
        }, nil
    }

    return &Response{
        Status:  "no_action_needed",
        Message: fmt.Sprintf("Application '%s' is already in sync", app),
    }, nil
}
```

#### Pattern 2: MCO Integration (Node Issues)

```go
// internal/tools/node_remediation.go
func (t *RemediationTool) handleNodeIssue(ctx context.Context, nodeName string, issue *Issue) (*Response, error) {
    // Step 1: Check if issue is MCO-related
    if isMCOManaged(issue) {
        // Step 2: Monitor MachineConfigPool status
        mcp, err := t.k8sClient.GetMachineConfigPool(ctx, getPoolForNode(nodeName))
        if err != nil {
            return nil, err
        }

        // Step 3: Recommend action (don't create MachineConfig directly)
        if mcp.Status.DegradedMachineCount > 0 {
            return &Response{
                Status:  "recommendation",
                Message: "Node issue is related to MachineConfig rollout",
                Recommendation: "Check MCO logs and MachineConfigPool status. " +
                    "MCO will automatically remediate if configuration is correct. " +
                    "Manual intervention may be needed if MCO is stuck.",
                Details: map[string]interface{}{
                    "mcp_status":         mcp.Status,
                    "degraded_machines":  mcp.Status.DegradedMachineCount,
                    "updated_machines":   mcp.Status.UpdatedMachineCount,
                },
            }, nil
        }
    }

    // For non-MCO issues, we can perform direct remediation
    return t.directNodeRemediation(ctx, nodeName, issue)
}

func isMCOManaged(issue *Issue) bool {
    // Check if issue involves MachineConfig, kubelet config, OS updates, etc.
    mcoRelatedKeywords := []string{
        "machineconfig",
        "kubelet",
        "crio",
        "os-update",
        "node-config",
    }

    for _, keyword := range mcoRelatedKeywords {
        if strings.Contains(strings.ToLower(issue.Description), keyword) {
            return true
        }
    }
    return false
}
```

#### Pattern 3: Non-ArgoCD Application Remediation

```go
// internal/tools/pod_remediation.go
func (t *RemediationTool) handlePodIssue(ctx context.Context, namespace, podName string) (*Response, error) {
    // Step 1: Get pod details
    pod, err := t.k8sClient.CoreV1().Pods(namespace).Get(ctx, podName, metav1.GetOptions{})
    if err != nil {
        return nil, err
    }

    // Step 2: Detect deployment method
    deploymentInfo, err := detector.DetectDeploymentMethod(ctx, namespace, podName,
        pod.Labels, pod.Annotations)
    if err != nil {
        return nil, err
    }

    // Step 3: Route based on deployment method
    switch deploymentInfo.Method {
    case detector.DeploymentMethodArgoCD:
        // Use ArgoCD sync
        return t.handleArgocdManagedApp(ctx, deploymentInfo.ManagedBy)

    case detector.DeploymentMethodManual:
        // Safe to perform direct remediation
        return t.directPodRestart(ctx, namespace, podName)

    case detector.DeploymentMethodHelm:
        // Recommend Helm upgrade
        return &Response{
            Status:  "recommendation",
            Message: fmt.Sprintf("Pod is part of Helm release '%s'", deploymentInfo.ManagedBy),
            Recommendation: fmt.Sprintf("Use 'helm upgrade %s' to apply changes", deploymentInfo.ManagedBy),
        }, nil

    case detector.DeploymentMethodOperator:
        // Let operator handle it
        return &Response{
            Status:  "recommendation",
            Message: fmt.Sprintf("Pod is managed by operator '%s'", deploymentInfo.ManagedBy),
            Recommendation: "Check operator logs and CR status. Operator should self-heal.",
        }, nil

    default:
        // Conservative approach: recommend manual investigation
        return &Response{
            Status:  "requires_investigation",
            Message: "Unable to determine deployment method",
            Recommendation: "Manual investigation required before remediation",
        }, nil
    }
}
```

## Consequences

### Positive

- ✅ **No Duplication**: Leverages ArgoCD/MCO instead of reimplementing
- ✅ **Clear Boundaries**: Explicit decision logic for each deployment method
- ✅ **GitOps Compliance**: Respects declarative GitOps workflows
- ✅ **Safety**: Reduces risk of conflicting remediation actions
- ✅ **Maintainability**: Less code to maintain, rely on battle-tested tools
- ✅ **Flexibility**: Direct remediation available for non-managed apps

### Negative

- ⚠️ **Complexity**: Detection logic adds complexity
- ⚠️ **Dependency**: Relies on accurate labels/annotations
- ⚠️ **Limited Control**: Cannot directly modify ArgoCD-managed apps
- ⚠️ **Learning Curve**: Team must understand multiple deployment methods

### Neutral

- **API Calls**: Similar number of API calls (ArgoCD API vs. Kubernetes API)
- **Latency**: Minimal difference in remediation latency

## Implementation Phases

### Phase 1: Detection and Routing (Week 1)
- ✅ Implement deployment method detection
- ✅ Add routing logic to remediation tools
- ✅ Unit tests for detection algorithm

### Phase 2: ArgoCD Integration (Week 2)
- ✅ Implement ArgoCD API client
- ✅ Add sync triggering capability
- ✅ Integration tests with ArgoCD

### Phase 3: MCO Integration (Week 3)
- ✅ Add MachineConfigPool monitoring
- ✅ Implement MCO-aware recommendations
- ✅ Integration tests for node remediation

### Phase 4: Production Validation (Week 4)
- ✅ Test all deployment method scenarios
- ✅ Validate detection accuracy
- ✅ Production deployment with monitoring

## Configuration

```yaml
# values.yaml
remediation:
  deployment_detection:
    enabled: true
    # Annotations/labels to check for ArgoCD
    argocd_indicators:
      - "argocd.argoproj.io/tracking-id"
      - "argocd.argoproj.io/application"
    # When detection is uncertain, default behavior
    fallback_strategy: "recommend"  # recommend | manual | conservative

  argocd_integration:
    enabled: true
    # Prefer ArgoCD sync over direct changes
    prefer_sync: true
    # API endpoint (auto-discovered if in-cluster)
    api_url: "https://argocd-server.openshift-gitops.svc"

  mco_integration:
    enabled: true
    # Monitor MachineConfigPools
    watch_pools: true
    # Don't create MachineConfigs directly
    create_configs: false
```

## Related ADRs

- [ADR-006: Integration Architecture](006-integration-architecture.md)
- [ADR-009: Architecture Evolution Roadmap](009-architecture-evolution-roadmap.md)
- [ADR-012: Non-ArgoCD Application Remediation Strategy](012-non-argocd-application-remediation.md)
- [ADR-013: Multi-Layer Coordination Engine Design](013-multi-layer-coordination-engine.md)

## References

- [ArgoCD API Documentation](https://argo-cd.readthedocs.io/en/stable/developer-guide/api-docs/)
- [MCO Design Documentation](https://github.com/openshift/machine-config-operator/blob/master/docs/MachineConfigDaemon.md)
- [OpenShift GitOps Best Practices](https://docs.openshift.com/gitops/latest/gitops_best_practices.html)
- [TODO-APPLICATION-REMEDIATION.md](../../TODO-APPLICATION-REMEDIATION.md)

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **GitOps Team**: Approved
- **Date**: 2025-12-17
