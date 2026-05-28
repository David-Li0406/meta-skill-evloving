# ADR-012: Non-ArgoCD Application Remediation Strategy

## Status

**ACCEPTED** - 2025-12-17

## Context

While ArgoCD provides robust GitOps-based application management, many OpenShift clusters contain applications deployed through other methods:

1. **Manual kubectl/oc deployments**: Quick deployments, testing, debugging
2. **Helm releases**: Not managed by ArgoCD/Flux
3. **Operator-managed applications**: Managed by custom operators
4. **Legacy applications**: Pre-GitOps deployments
5. **Third-party tools**: CI/CD pipelines deploying directly

These applications fall outside ArgoCD's scope (per ADR-011), but still require remediation capabilities when issues occur.

### Problem Statement

**Without a remediation strategy for non-ArgoCD apps, we have gaps:**

- ✅ ArgoCD apps → Trigger ArgoCD sync (ADR-011)
- ❌ Manual deployments → **No remediation strategy defined**
- ❌ Helm releases → **No remediation strategy defined**
- ❌ Operator-managed apps → **No remediation strategy defined**

### Key Questions

1. **Is direct Kubernetes API remediation safe for non-GitOps apps?**
2. **How do we prevent configuration drift for Helm-managed apps?**
3. **Should we recommend GitOps adoption for manual deployments?**
4. **What remediation actions are appropriate for each deployment method?**

### Design Constraints

- **Respect Helm State**: Don't create drift between Helm release and K8s state
- **Operator Sovereignty**: Don't interfere with operator reconciliation loops
- **User Intent**: Preserve user's deployment methodology
- **Safety First**: Avoid destructive actions without confirmation
- **GitOps Encouragement**: Recommend GitOps where appropriate

## Decision

We will implement **deployment-method-aware remediation** with the following strategy:

### Core Principles

1. **Detection First**: Always detect deployment method before remediation
2. **Method-Specific Actions**: Different remediation strategies per deployment method
3. **Progressive Recommendation**: Suggest GitOps adoption for manual deployments
4. **Non-Destructive**: Prefer scaling, restarting over deletion
5. **User Confirmation**: Require confirmation for risky operations

### Remediation Strategy Matrix

| Deployment Method | Detection Criteria | Remediation Approach | Example Actions |
|-------------------|-------------------|----------------------|-----------------|
| **ArgoCD** | `argocd.argoproj.io/*` annotations | Trigger ArgoCD sync (ADR-011) | Sync app, refresh repo |
| **Helm** | `meta.helm.sh/release-name` annotation | Helm-compatible operations | Rollback, upgrade |
| **Operator** | `app.kubernetes.io/managed-by` label | Monitor operator, hands-off | Wait for operator reconciliation |
| **Manual** | No management indicators | Direct K8s API remediation | Restart pods, scale deployments |
| **Unknown** | Uncertain detection | Conservative + recommend investigation | Minimal action, suggest manual review |

### Decision Tree

```
┌─────────────────────────────┐
│  Detect Deployment Method   │
└──────────┬──────────────────┘
           │
           ├─ ArgoCD ────────────► Trigger ArgoCD Sync (ADR-011)
           │
           ├─ Helm ──────────────► Helm-Compatible Actions
           │                       - helm rollback
           │                       - helm upgrade (if chart available)
           │                       - Direct pod restart (safe)
           │
           ├─ Operator ──────────► Monitor + Wait
           │                       - Check operator logs
           │                       - Verify CR status
           │                       - Let operator self-heal
           │                       - Escalate if operator stuck
           │
           ├─ Manual ────────────► Direct K8s API Remediation
           │                       - Pod restart
           │                       - Deployment rollout restart
           │                       - Scale replicas
           │                       - Resource updates
           │                       + Recommend GitOps adoption
           │
           └─ Unknown ───────────► Conservative Approach
                                   - Minimal action
                                   - Recommend manual investigation
                                   - Provide diagnostic info
```

## Implementation

### 1. Helm-Managed Application Remediation

```go
// pkg/remediation/helm.go
package remediation

import (
    "context"
    "fmt"
    "helm.sh/helm/v3/pkg/action"
    "helm.sh/helm/v3/pkg/cli"
)

type HelmRemediator struct {
    config *action.Configuration
    client *kubernetes.Clientset
}

func NewHelmRemediator(namespace string) (*HelmRemediator, error) {
    settings := cli.New()
    actionConfig := new(action.Configuration)

    if err := actionConfig.Init(settings.RESTClientGetter(), namespace,
        os.Getenv("HELM_DRIVER"), log.Printf); err != nil {
        return nil, err
    }

    return &HelmRemediator{
        config: actionConfig,
    }, nil
}

// RemediatePod handles pod issues for Helm-managed applications
func (h *HelmRemediator) RemediatePod(ctx context.Context, namespace, podName string, info *DeploymentInfo) (*Response, error) {
    releaseName := info.ManagedBy

    // Check Helm release status
    release, err := h.getReleaseStatus(releaseName)
    if err != nil {
        return nil, fmt.Errorf("failed to get Helm release: %w", err)
    }

    // Determine remediation action based on issue type
    switch {
    case isPodCrashLoop(podName):
        // Safe: Pod restart doesn't affect Helm state
        return h.restartPod(ctx, namespace, podName)

    case isImagePullError(podName):
        // Recommend Helm upgrade with corrected values
        return h.recommendHelmUpgrade(releaseName, "Update image tag in values.yaml and run helm upgrade")

    case isConfigurationIssue(podName):
        // Helm rollback to last working version
        return h.rollbackRelease(ctx, releaseName)

    default:
        return h.conservativeAction(releaseName)
    }
}

func (h *HelmRemediator) restartPod(ctx context.Context, namespace, podName string) (*Response, error) {
    // Direct pod deletion is safe - Helm doesn't track pod state
    err := h.client.CoreV1().Pods(namespace).Delete(ctx, podName, metav1.DeleteOptions{})
    if err != nil {
        return nil, err
    }

    return &Response{
        Status:  "success",
        Message: fmt.Sprintf("Restarted pod %s (Helm-managed)", podName),
        Details: map[string]interface{}{
            "method":       "direct_pod_restart",
            "helm_release": info.ManagedBy,
            "note":         "Pod restart does not affect Helm release state",
        },
    }, nil
}

func (h *HelmRemediator) rollbackRelease(ctx context.Context, releaseName string) (*Response, error) {
    rollback := action.NewRollback(h.config)
    rollback.Wait = true
    rollback.Timeout = 5 * time.Minute

    if err := rollback.Run(releaseName); err != nil {
        return nil, fmt.Errorf("helm rollback failed: %w", err)
    }

    return &Response{
        Status:  "success",
        Message: fmt.Sprintf("Rolled back Helm release '%s' to previous version", releaseName),
        Details: map[string]interface{}{
            "method": "helm_rollback",
            "release": releaseName,
        },
    }, nil
}

func (h *HelmRemediator) recommendHelmUpgrade(releaseName, recommendation string) (*Response, error) {
    return &Response{
        Status:  "recommendation",
        Message: fmt.Sprintf("Helm release '%s' requires upgrade", releaseName),
        Recommendation: recommendation,
        Commands: []string{
            fmt.Sprintf("helm upgrade %s <chart> -f values.yaml", releaseName),
        },
    }, nil
}
```

### 2. Operator-Managed Application Remediation

```go
// pkg/remediation/operator.go
package remediation

type OperatorRemediator struct {
    client       *kubernetes.Clientset
    dynamicClient dynamic.Interface
}

// RemediateOperatorManagedResource handles operator-managed applications
func (o *OperatorRemediator) RemediateOperatorManagedResource(
    ctx context.Context,
    namespace, resourceName string,
    info *DeploymentInfo,
) (*Response, error) {
    operatorName := info.ManagedBy

    // Step 1: Check operator health
    operatorHealth, err := o.checkOperatorHealth(ctx, operatorName)
    if err != nil {
        return nil, err
    }

    if !operatorHealth.Healthy {
        return &Response{
            Status:  "operator_unhealthy",
            Message: fmt.Sprintf("Operator '%s' is unhealthy", operatorName),
            Recommendation: fmt.Sprintf(
                "Fix operator '%s' first. Check operator logs:\n"+
                    "  kubectl logs -n <operator-namespace> -l app=%s",
                operatorName, operatorName,
            ),
            Details: map[string]interface{}{
                "operator_status": operatorHealth,
            },
        }, nil
    }

    // Step 2: Check Custom Resource status
    crStatus, err := o.getCustomResourceStatus(ctx, namespace, resourceName, info)
    if err != nil {
        return nil, err
    }

    // Step 3: Determine if operator is actively reconciling
    if o.isReconciling(crStatus) {
        return &Response{
            Status:  "reconciling",
            Message: fmt.Sprintf("Operator '%s' is actively reconciling resource", operatorName),
            Recommendation: "Wait for operator reconciliation to complete. " +
                "Operator should self-heal within 5 minutes.",
            Details: map[string]interface{}{
                "reconcile_status": crStatus.Conditions,
                "wait_time":        "5 minutes",
            },
        }, nil
    }

    // Step 4: If operator is stuck, recommend manual intervention
    if o.isStuck(crStatus) {
        return &Response{
            Status:  "operator_stuck",
            Message: fmt.Sprintf("Operator '%s' appears stuck", operatorName),
            Recommendation: fmt.Sprintf(
                "Manual intervention required:\n"+
                    "1. Check operator logs for errors\n"+
                    "2. Verify Custom Resource spec is valid\n"+
                    "3. Consider deleting and recreating the CR\n"+
                    "4. Restart operator if necessary",
            ),
            Details: map[string]interface{}{
                "cr_status": crStatus,
            },
        }, nil
    }

    // Step 5: For healthy operator, minimal action
    return &Response{
        Status:  "monitoring",
        Message: fmt.Sprintf("Operator '%s' is healthy, monitoring resource", operatorName),
        Recommendation: "Operator should handle remediation automatically. " +
            "Escalate if issue persists beyond 10 minutes.",
    }, nil
}

// isReconciling checks if operator is actively working
func (o *OperatorRemediator) isReconciling(status *CustomResourceStatus) bool {
    for _, condition := range status.Conditions {
        if condition.Type == "Reconciling" && condition.Status == "True" {
            return true
        }
    }
    return false
}

// isStuck detects if operator reconciliation is stuck
func (o *OperatorRemediator) isStuck(status *CustomResourceStatus) bool {
    for _, condition := range status.Conditions {
        // Degraded for > 10 minutes indicates stuck operator
        if condition.Type == "Degraded" && condition.Status == "True" {
            if time.Since(condition.LastTransitionTime.Time) > 10*time.Minute {
                return true
            }
        }
    }
    return false
}
```

### 3. Manual Deployment Remediation

```go
// pkg/remediation/manual.go
package remediation

type ManualDeploymentRemediator struct {
    client *kubernetes.Clientset
}

// RemediateManualDeployment handles manually deployed applications
func (m *ManualDeploymentRemediator) RemediateManualDeployment(
    ctx context.Context,
    namespace, resourceName string,
    issue *Issue,
) (*Response, error) {
    // For manual deployments, direct K8s API remediation is safe
    // (no GitOps state to preserve)

    response := &Response{
        Details: map[string]interface{}{
            "deployment_method": "manual",
        },
    }

    switch issue.Type {
    case "CrashLoopBackOff":
        // Safe action: Restart deployment
        err := m.restartDeployment(ctx, namespace, resourceName)
        if err != nil {
            return nil, err
        }
        response.Status = "success"
        response.Message = fmt.Sprintf("Restarted deployment %s", resourceName)
        response.Recommendation = "Consider moving to GitOps (ArgoCD) for better deployment management"

    case "ImagePullBackOff":
        // Informational: Can't fix without image access
        response.Status = "info"
        response.Message = "Image pull error detected"
        response.Recommendation = "Verify image exists and ImagePullSecrets are configured"

    case "InsufficientResources":
        // Safe action: Suggest scaling down or increasing limits
        response.Status = "recommendation"
        response.Message = "Resource limits preventing pod scheduling"
        response.Recommendation = "Option 1: Scale down deployment\n" +
            "Option 2: Increase resource limits\n" +
            "Option 3: Add more cluster capacity"

    default:
        response.Status = "unknown"
        response.Message = "Unknown issue type"
        response.Recommendation = "Manual investigation required"
    }

    // Add GitOps recommendation for all manual deployments
    response.AdditionalRecommendations = []string{
        "💡 **Consider GitOps Adoption**: This application is manually deployed. " +
            "Migrating to ArgoCD would provide:\n" +
            "  - Declarative configuration (Git as source of truth)\n" +
            "  - Automated sync and self-healing\n" +
            "  - Audit trail and rollback capabilities\n" +
            "  - Learn more: https://docs.openshift.com/gitops/",
    }

    return response, nil
}

func (m *ManualDeploymentRemediator) restartDeployment(ctx context.Context, namespace, name string) error {
    // Trigger rollout restart
    deployment, err := m.client.AppsV1().Deployments(namespace).Get(ctx, name, metav1.GetOptions{})
    if err != nil {
        return err
    }

    // Add restart annotation
    if deployment.Spec.Template.Annotations == nil {
        deployment.Spec.Template.Annotations = make(map[string]string)
    }
    deployment.Spec.Template.Annotations["kubectl.kubernetes.io/restartedAt"] = time.Now().Format(time.RFC3339)

    _, err = m.client.AppsV1().Deployments(namespace).Update(ctx, deployment, metav1.UpdateOptions{})
    return err
}
```

### 4. Unknown Deployment Method (Conservative Approach)

```go
// pkg/remediation/unknown.go
package remediation

type ConservativeRemediator struct {
    client *kubernetes.Clientset
}

// RemediateUnknownDeployment handles cases where deployment method is unclear
func (c *ConservativeRemediator) RemediateUnknownDeployment(
    ctx context.Context,
    namespace, resourceName string,
    issue *Issue,
) (*Response, error) {
    // When uncertain, provide diagnostic info and recommend manual action

    // Gather diagnostic information
    diagnostics, err := c.gatherDiagnostics(ctx, namespace, resourceName)
    if err != nil {
        return nil, err
    }

    return &Response{
        Status:  "requires_investigation",
        Message: fmt.Sprintf("Unable to determine deployment method for %s", resourceName),
        Recommendation: "Manual investigation required. Review diagnostic information below:\n\n" +
            "**Next Steps:**\n" +
            "1. Check resource labels and annotations\n" +
            "2. Verify if resource is managed by ArgoCD/Helm/Operator\n" +
            "3. Review owner references\n" +
            "4. Check for related CRs or parent resources\n\n" +
            "**Safe Actions You Can Take:**\n" +
            "- View pod logs: kubectl logs <pod> -n <namespace>\n" +
            "- Describe resource: kubectl describe <resource> -n <namespace>\n" +
            "- Check events: kubectl get events -n <namespace>\n\n" +
            "**Risky Actions (Require Confirmation):**\n" +
            "- Restart pods\n" +
            "- Scale deployments\n" +
            "- Modify resources",
        Details: map[string]interface{}{
            "diagnostics": diagnostics,
        },
    }, nil
}

func (c *ConservativeRemediator) gatherDiagnostics(ctx context.Context, namespace, resourceName string) (*Diagnostics, error) {
    diag := &Diagnostics{}

    // Get resource details
    pod, err := c.client.CoreV1().Pods(namespace).Get(ctx, resourceName, metav1.GetOptions{})
    if err != nil {
        return nil, err
    }

    diag.Labels = pod.Labels
    diag.Annotations = pod.Annotations
    diag.OwnerReferences = pod.OwnerReferences

    // Check for common management indicators
    diag.Indicators = map[string]bool{
        "has_argocd_annotations": hasArgoCDAnnotations(pod.Annotations),
        "has_helm_annotations":   hasHelmAnnotations(pod.Annotations),
        "has_operator_labels":    hasOperatorLabels(pod.Labels),
        "has_owner_references":   len(pod.OwnerReferences) > 0,
    }

    return diag, nil
}
```

## Safety Mechanisms

### 1. Dry Run Mode

```go
// All remediation actions support dry-run
type RemediationOptions struct {
    DryRun  bool
    Confirm bool  // Require explicit confirmation for risky actions
}

func (r *Remediator) Execute(ctx context.Context, action *RemediationAction, opts *RemediationOptions) (*Response, error) {
    if opts.DryRun {
        return &Response{
            Status:  "dry_run",
            Message: "Dry run: No changes made",
            Details: map[string]interface{}{
                "would_execute": action.Description,
                "affected_resources": action.Resources,
            },
        }, nil
    }

    // Execute actual remediation
    return r.executeAction(ctx, action)
}
```

### 2. Confirmation for Risky Actions

```go
// Risky actions require explicit confirmation
var riskyActions = []string{
    "delete_pod",
    "delete_deployment",
    "scale_to_zero",
    "update_image",
}

func requiresConfirmation(action string) bool {
    for _, risky := range riskyActions {
        if action == risky {
            return true
        }
    }
    return false
}
```

### 3. Audit Logging

```go
// Log all remediation actions for audit trail
func (r *Remediator) logAction(ctx context.Context, action *RemediationAction, result *Response) {
    auditLog := &AuditEntry{
        Timestamp:        time.Now(),
        User:             getUserFromContext(ctx),
        Action:           action.Type,
        Resource:         action.Resource,
        Namespace:        action.Namespace,
        DeploymentMethod: action.DeploymentMethod,
        Result:           result.Status,
        Details:          result.Details,
    }

    r.auditLogger.Log(auditLog)
}
```

## Consequences

### Positive

- ✅ **Comprehensive Coverage**: Remediation for all deployment methods
- ✅ **Method-Aware**: Respects deployment methodology
- ✅ **Safety First**: Conservative approach for unknown cases
- ✅ **GitOps Encouragement**: Recommends GitOps adoption
- ✅ **Helm Compatibility**: Doesn't create drift for Helm releases
- ✅ **Operator Respect**: Doesn't interfere with operator reconciliation
- ✅ **Audit Trail**: All actions logged

### Negative

- ⚠️ **Complexity**: Multiple remediation paths to maintain
- ⚠️ **Detection Dependency**: Relies on accurate deployment method detection
- ⚠️ **Limited Helm Integration**: Requires Helm client library
- ⚠️ **Operator Variability**: Operator behavior is not standardized

### Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| **Incorrect detection → wrong remediation** | Conservative fallback, dry-run mode, audit logging |
| **Helm drift** | Only perform pod-level actions (don't modify Helm-managed resources) |
| **Operator conflicts** | Monitor operator status, wait for operator reconciliation |
| **Destructive actions** | Confirmation required, dry-run mode available |

## Testing Strategy

### Unit Tests
- Deployment method detection accuracy
- Remediation strategy selection
- Safety mechanism validation

### Integration Tests
- Helm-managed application remediation
- Operator-managed application remediation
- Manual deployment remediation
- Mixed deployment methods

### E2E Tests
- Full remediation workflow for each deployment method
- GitOps recommendation flow
- Audit logging verification

## Related ADRs

- [ADR-011: ArgoCD and MCO Integration Boundaries](011-argocd-mco-integration-boundaries.md)
- [ADR-013: Multi-Layer Coordination Engine Design](013-multi-layer-coordination-engine.md)
- [ADR-006: Integration Architecture](006-integration-architecture.md)

## References

- [Helm Architecture](https://helm.sh/docs/topics/architecture/)
- [Kubernetes Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [OpenShift GitOps Adoption Guide](https://docs.openshift.com/gitops/)
- [TODO-APPLICATION-REMEDIATION.md](../../TODO-APPLICATION-REMEDIATION.md)

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **Date**: 2025-12-17
