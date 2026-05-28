# ADR-013: Multi-Layer Coordination Engine Design

## Status

**ACCEPTED** - 2025-12-17

## Context

The OpenShift Cluster Health MCP Server operates in a complex environment with multiple remediation layers:

1. **Application Layer**: Pods, Deployments, Services (managed by ArgoCD, Helm, Operators, or manually)
2. **Platform Layer**: OpenShift components, monitoring, networking, storage
3. **Infrastructure Layer**: Nodes, machine configs, OS updates (managed by MCO)

Issues often span multiple layers, requiring coordinated remediation:

- **Example 1**: Pod crash caused by insufficient node resources
  - Application layer: Pod is CrashLoopBackOff
  - Infrastructure layer: Node has memory pressure
  - **Solution**: Coordinate node resource increase + pod restart

- **Example 2**: Application degradation after OS update
  - Application layer: Increased latency, errors
  - Infrastructure layer: Node OS update via MCO
  - **Solution**: Coordinate MCO rollback + application health verification

- **Example 3**: Network connectivity issues
  - Application layer: Service unavailable
  - Platform layer: SDN reconfiguration
  - Infrastructure layer: Node network interface issues
  - **Solution**: Multi-layer diagnosis + coordinated fix

### Current Limitations

Without multi-layer coordination:
- ❌ **Incomplete Remediation**: Fixing app layer doesn't address root cause in infrastructure
- ❌ **Cascade Failures**: Infrastructure changes trigger application issues
- ❌ **Remediation Conflicts**: Simultaneous remediations at different layers conflict
- ❌ **Order Dependencies**: Infrastructure must be fixed before application layer
- ❌ **Verification Gaps**: Can't verify end-to-end health after multi-layer changes

### Integration with Existing Systems

Per ADR-011:
- **ArgoCD**: Handles application-layer GitOps sync
- **MCO**: Handles infrastructure-layer machine configs
- **Coordination Engine**: Orchestrates workflows, but currently lacks multi-layer awareness

## Decision

We will enhance the Coordination Engine with **multi-layer remediation orchestration** capabilities:

### Core Principles

1. **Layer Detection**: Identify which layers are affected by an issue
2. **Dependency Resolution**: Determine remediation order based on layer dependencies
3. **Coordinated Execution**: Execute remediations across layers in correct sequence
4. **Cross-Layer Verification**: Validate health at each layer before proceeding
5. **Rollback Coordination**: Coordinate rollbacks across all affected layers

### Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  Multi-Layer Coordination Engine                                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Layer Detection & Analysis                                │  │
│  │  - Identify affected layers (app/platform/infra)           │  │
│  │  - Determine root cause layer                              │  │
│  │  - Build dependency graph                                  │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Remediation Planning                                      │  │
│  │  - Generate multi-layer remediation plan                   │  │
│  │  - Determine execution order (infra → platform → app)      │  │
│  │  - Identify verification checkpoints                       │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Orchestration Engine                                      │  │
│  │  - Execute remediation steps in sequence                   │  │
│  │  - Wait for layer stabilization between steps              │  │
│  │  - Verify health at each checkpoint                        │  │
│  │  - Coordinate with ArgoCD/MCO APIs                         │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Rollback Coordinator                                      │  │
│  │  - Detect failures at any layer                            │  │
│  │  - Trigger coordinated rollback (reverse order)            │  │
│  │  - Restore stable state across all layers                  │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
┌───────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Infrastructure│ │ Platform │ │Application│ │ ArgoCD   │
│ Layer (MCO)   │ │ Services │ │ Layer     │ │ API      │
└───────────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Layer Model

```go
// pkg/coordination/layer.go
package coordination

type Layer string

const (
    LayerInfrastructure Layer = "infrastructure"  // Nodes, MCO, OS
    LayerPlatform       Layer = "platform"        // OpenShift services, SDN, storage
    LayerApplication    Layer = "application"     // Pods, deployments, services
)

type LayeredIssue struct {
    ID              string
    Description     string
    AffectedLayers  []Layer            // Which layers are affected
    RootCauseLayer  Layer              // Which layer caused the issue
    ImpactedResources map[Layer][]Resource
}

type Resource struct {
    Kind      string
    Namespace string
    Name      string
    Status    string
}

// DetectAffectedLayers analyzes an issue and determines which layers are involved
func DetectAffectedLayers(issue *Issue) (*LayeredIssue, error) {
    layered := &LayeredIssue{
        ID:          issue.ID,
        Description: issue.Description,
        ImpactedResources: make(map[Layer][]Resource),
    }

    // Analyze symptoms to identify affected layers
    if hasNodeIssues(issue) {
        layered.AffectedLayers = append(layered.AffectedLayers, LayerInfrastructure)
        layered.ImpactedResources[LayerInfrastructure] = getNodeResources(issue)
    }

    if hasPlatformIssues(issue) {
        layered.AffectedLayers = append(layered.AffectedLayers, LayerPlatform)
        layered.ImpactedResources[LayerPlatform] = getPlatformResources(issue)
    }

    if hasApplicationIssues(issue) {
        layered.AffectedLayers = append(layered.AffectedLayers, LayerApplication)
        layered.ImpactedResources[LayerApplication] = getApplicationResources(issue)
    }

    // Determine root cause layer using ML or heuristics
    layered.RootCauseLayer = determineRootCause(layered)

    return layered, nil
}

// determineRootCause identifies which layer is the root cause
func determineRootCause(layered *LayeredIssue) Layer {
    // Heuristic: Infrastructure issues are often root cause
    if contains(layered.AffectedLayers, LayerInfrastructure) {
        return LayerInfrastructure
    }

    // Platform issues often cause app problems
    if contains(layered.AffectedLayers, LayerPlatform) {
        return LayerPlatform
    }

    // Application issues are least likely to be root cause
    return LayerApplication
}
```

### Remediation Planning

```go
// pkg/coordination/planner.go
package coordination

type RemediationPlan struct {
    ID          string
    IssueID     string
    Layers      []Layer
    Steps       []RemediationStep
    Rollback    []RemediationStep  // Reverse order
    Checkpoints []HealthCheckpoint
}

type RemediationStep struct {
    Layer       Layer
    Order       int       // Execution order (lower = earlier)
    Description string
    Action      RemediationAction
    WaitTime    time.Duration  // Wait after this step
    Required    bool           // Is this step required for success?
}

type HealthCheckpoint struct {
    Layer       Layer
    After       int            // After which step
    Checks      []HealthCheck
}

// GenerateRemediationPlan creates a multi-layer remediation plan
func GenerateRemediationPlan(layered *LayeredIssue) (*RemediationPlan, error) {
    plan := &RemediationPlan{
        ID:      generateID(),
        IssueID: layered.ID,
        Layers:  layered.AffectedLayers,
    }

    // Generate steps for each affected layer
    // Order: Infrastructure → Platform → Application
    order := 0

    // Step 1: Infrastructure layer remediation (if affected)
    if contains(layered.AffectedLayers, LayerInfrastructure) {
        infraSteps := generateInfrastructureSteps(layered)
        for _, step := range infraSteps {
            step.Order = order
            order++
            plan.Steps = append(plan.Steps, step)
        }

        // Checkpoint: Verify infrastructure health
        plan.Checkpoints = append(plan.Checkpoints, HealthCheckpoint{
            Layer: LayerInfrastructure,
            After: order - 1,
            Checks: []HealthCheck{
                {Type: "node_ready", Timeout: 5 * time.Minute},
                {Type: "mco_stable", Timeout: 10 * time.Minute},
            },
        })
    }

    // Step 2: Platform layer remediation (if affected)
    if contains(layered.AffectedLayers, LayerPlatform) {
        platformSteps := generatePlatformSteps(layered)
        for _, step := range platformSteps {
            step.Order = order
            order++
            plan.Steps = append(plan.Steps, step)
        }

        // Checkpoint: Verify platform health
        plan.Checkpoints = append(plan.Checkpoints, HealthCheckpoint{
            Layer: LayerPlatform,
            After: order - 1,
            Checks: []HealthCheck{
                {Type: "openshift_operators_ready", Timeout: 5 * time.Minute},
                {Type: "networking_functional", Timeout: 3 * time.Minute},
            },
        })
    }

    // Step 3: Application layer remediation (if affected)
    if contains(layered.AffectedLayers, LayerApplication) {
        appSteps := generateApplicationSteps(layered)
        for _, step := range appSteps {
            step.Order = order
            order++
            plan.Steps = append(plan.Steps, step)
        }

        // Checkpoint: Verify application health
        plan.Checkpoints = append(plan.Checkpoints, HealthCheckpoint{
            Layer: LayerApplication,
            After: order - 1,
            Checks: []HealthCheck{
                {Type: "pods_running", Timeout: 5 * time.Minute},
                {Type: "endpoints_healthy", Timeout: 2 * time.Minute},
            },
        })
    }

    // Generate rollback plan (reverse order)
    plan.Rollback = reverseSteps(plan.Steps)

    return plan, nil
}

func generateInfrastructureSteps(layered *LayeredIssue) []RemediationStep {
    steps := []RemediationStep{}

    resources := layered.ImpactedResources[LayerInfrastructure]
    for _, resource := range resources {
        if resource.Kind == "Node" {
            // Check if node issue is MCO-related
            if isMCORelated(resource) {
                steps = append(steps, RemediationStep{
                    Layer:       LayerInfrastructure,
                    Description: fmt.Sprintf("Monitor MCO rollout for node %s", resource.Name),
                    Action: RemediationAction{
                        Type:   "monitor_mco",
                        Target: resource.Name,
                    },
                    WaitTime: 5 * time.Minute,
                    Required: true,
                })
            } else {
                // Direct node remediation
                steps = append(steps, RemediationStep{
                    Layer:       LayerInfrastructure,
                    Description: fmt.Sprintf("Drain and reboot node %s", resource.Name),
                    Action: RemediationAction{
                        Type:   "drain_and_reboot_node",
                        Target: resource.Name,
                    },
                    WaitTime: 10 * time.Minute,
                    Required: true,
                })
            }
        }
    }

    return steps
}

func generateApplicationSteps(layered *LayeredIssue) []RemediationStep {
    steps := []RemediationStep{}

    resources := layered.ImpactedResources[LayerApplication]
    for _, resource := range resources {
        // Detect deployment method (per ADR-011 and ADR-012)
        deploymentInfo, _ := detector.DetectDeploymentMethod(context.Background(),
            resource.Namespace, resource.Name, resource.Labels, resource.Annotations)

        switch deploymentInfo.Method {
        case detector.DeploymentMethodArgoCD:
            // Trigger ArgoCD sync
            steps = append(steps, RemediationStep{
                Layer:       LayerApplication,
                Description: fmt.Sprintf("Trigger ArgoCD sync for %s", deploymentInfo.ManagedBy),
                Action: RemediationAction{
                    Type:   "argocd_sync",
                    Target: deploymentInfo.ManagedBy,
                },
                WaitTime: 2 * time.Minute,
                Required: true,
            })

        case detector.DeploymentMethodManual:
            // Direct restart
            steps = append(steps, RemediationStep{
                Layer:       LayerApplication,
                Description: fmt.Sprintf("Restart deployment %s", resource.Name),
                Action: RemediationAction{
                    Type:   "restart_deployment",
                    Target: resource.Name,
                },
                WaitTime: 1 * time.Minute,
                Required: false, // Optional if infrastructure fix resolves issue
            })
        }
    }

    return steps
}
```

### Orchestration Engine

```go
// pkg/coordination/orchestrator.go
package coordination

type Orchestrator struct {
    k8sClient     *kubernetes.Clientset
    argocdClient  *argocd.Client
    mcoClient     *mco.Client
    healthChecker *HealthChecker
}

// ExecutePlan executes a multi-layer remediation plan
func (o *Orchestrator) ExecutePlan(ctx context.Context, plan *RemediationPlan) (*ExecutionResult, error) {
    result := &ExecutionResult{
        PlanID:    plan.ID,
        StartTime: time.Now(),
        Steps:     make([]StepResult, 0),
    }

    log.Info("Starting multi-layer remediation",
        "plan_id", plan.ID,
        "layers", plan.Layers,
        "steps", len(plan.Steps))

    // Execute steps in order
    for i, step := range plan.Steps {
        log.Info("Executing remediation step",
            "order", step.Order,
            "layer", step.Layer,
            "description", step.Description)

        stepResult := o.executeStep(ctx, &step)
        result.Steps = append(result.Steps, stepResult)

        if !stepResult.Success {
            if step.Required {
                // Required step failed, trigger rollback
                log.Error("Required step failed, initiating rollback",
                    "step", step.Description,
                    "error", stepResult.Error)

                rollbackResult := o.rollback(ctx, plan, result)
                result.Rollback = rollbackResult
                result.Success = false
                result.EndTime = time.Now()
                return result, fmt.Errorf("remediation failed at step %d: %w",
                    i, stepResult.Error)
            } else {
                // Optional step failed, continue
                log.Warn("Optional step failed, continuing",
                    "step", step.Description,
                    "error", stepResult.Error)
            }
        }

        // Wait after step
        if step.WaitTime > 0 {
            log.Info("Waiting for layer stabilization", "duration", step.WaitTime)
            time.Sleep(step.WaitTime)
        }

        // Run health checkpoint if defined
        if checkpoint := o.getCheckpoint(plan, i); checkpoint != nil {
            log.Info("Running health checkpoint", "layer", checkpoint.Layer)
            checkResult := o.runHealthCheckpoint(ctx, checkpoint)
            if !checkResult.Healthy {
                // Checkpoint failed, trigger rollback
                log.Error("Health checkpoint failed, initiating rollback",
                    "layer", checkpoint.Layer,
                    "checks_failed", checkResult.FailedChecks)

                rollbackResult := o.rollback(ctx, plan, result)
                result.Rollback = rollbackResult
                result.Success = false
                result.EndTime = time.Now()
                return result, fmt.Errorf("health checkpoint failed: %v",
                    checkResult.FailedChecks)
            }
        }
    }

    result.Success = true
    result.EndTime = time.Now()
    log.Info("Multi-layer remediation completed successfully",
        "plan_id", plan.ID,
        "duration", result.EndTime.Sub(result.StartTime))

    return result, nil
}

func (o *Orchestrator) executeStep(ctx context.Context, step *RemediationStep) StepResult {
    startTime := time.Now()

    var err error
    switch step.Action.Type {
    case "argocd_sync":
        err = o.argocdClient.SyncApplication(ctx, step.Action.Target)

    case "monitor_mco":
        err = o.monitorMCORollout(ctx, step.Action.Target)

    case "drain_and_reboot_node":
        err = o.drainAndRebootNode(ctx, step.Action.Target)

    case "restart_deployment":
        err = o.restartDeployment(ctx, step.Action.Target)

    default:
        err = fmt.Errorf("unknown action type: %s", step.Action.Type)
    }

    return StepResult{
        Step:      step.Description,
        Success:   err == nil,
        Error:     err,
        StartTime: startTime,
        EndTime:   time.Now(),
    }
}

func (o *Orchestrator) rollback(ctx context.Context, plan *RemediationPlan, result *ExecutionResult) *RollbackResult {
    log.Info("Initiating coordinated rollback", "plan_id", plan.ID)

    rollbackResult := &RollbackResult{
        StartTime: time.Now(),
        Steps:     make([]StepResult, 0),
    }

    // Execute rollback steps in reverse order
    for i := len(plan.Rollback) - 1; i >= 0; i-- {
        step := plan.Rollback[i]

        // Only rollback steps that were successfully executed
        if i < len(result.Steps) && result.Steps[i].Success {
            log.Info("Rolling back step", "description", step.Description)
            stepResult := o.executeStep(ctx, &step)
            rollbackResult.Steps = append(rollbackResult.Steps, stepResult)

            if !stepResult.Success {
                log.Error("Rollback step failed", "error", stepResult.Error)
                rollbackResult.Success = false
                rollbackResult.EndTime = time.Now()
                return rollbackResult
            }
        }
    }

    rollbackResult.Success = true
    rollbackResult.EndTime = time.Now()
    log.Info("Coordinated rollback completed", "duration",
        rollbackResult.EndTime.Sub(rollbackResult.StartTime))

    return rollbackResult
}
```

### Health Verification

```go
// pkg/coordination/health_checker.go
package coordination

type HealthChecker struct {
    k8sClient *kubernetes.Clientset
}

func (h *HealthChecker) runHealthCheckpoint(ctx context.Context, checkpoint *HealthCheckpoint) *CheckpointResult {
    result := &CheckpointResult{
        Layer:   checkpoint.Layer,
        Healthy: true,
        FailedChecks: make([]string, 0),
    }

    for _, check := range checkpoint.Checks {
        checkResult := h.runCheck(ctx, &check)
        if !checkResult.Passed {
            result.Healthy = false
            result.FailedChecks = append(result.FailedChecks, check.Type)
        }
    }

    return result
}

func (h *HealthChecker) runCheck(ctx context.Context, check *HealthCheck) *HealthCheckResult {
    ctx, cancel := context.WithTimeout(ctx, check.Timeout)
    defer cancel()

    switch check.Type {
    case "node_ready":
        return h.checkNodesReady(ctx)

    case "mco_stable":
        return h.checkMCOStable(ctx)

    case "pods_running":
        return h.checkPodsRunning(ctx)

    case "openshift_operators_ready":
        return h.checkOpenShiftOperators(ctx)

    case "networking_functional":
        return h.checkNetworking(ctx)

    default:
        return &HealthCheckResult{
            Passed: false,
            Error:  fmt.Errorf("unknown check type: %s", check.Type),
        }
    }
}

func (h *HealthChecker) checkMCOStable(ctx context.Context) *HealthCheckResult {
    // Check all MachineConfigPools are updated and not degraded
    mcps, err := h.k8sClient.MachineconfigurationV1().MachineConfigPools().List(ctx, metav1.ListOptions{})
    if err != nil {
        return &HealthCheckResult{Passed: false, Error: err}
    }

    for _, mcp := range mcps.Items {
        if mcp.Status.DegradedMachineCount > 0 {
            return &HealthCheckResult{
                Passed: false,
                Error:  fmt.Errorf("MachineConfigPool %s has degraded machines", mcp.Name),
            }
        }

        if mcp.Status.UpdatedMachineCount < mcp.Status.MachineCount {
            return &HealthCheckResult{
                Passed: false,
                Error:  fmt.Errorf("MachineConfigPool %s update in progress", mcp.Name),
            }
        }
    }

    return &HealthCheckResult{Passed: true}
}
```

## Example Scenarios

### Scenario 1: Node Pressure Causing Application Issues

```
Issue: Application pods crashing due to node memory pressure

Layer Detection:
- Infrastructure: Node memory pressure (root cause)
- Application: Pods in CrashLoopBackOff (symptom)

Remediation Plan:
1. [Infrastructure] Drain node-worker-3
2. [Infrastructure] Increase node memory (or add new node)
3. [Checkpoint] Verify node ready and no pressure
4. [Application] Trigger ArgoCD sync for affected app
5. [Checkpoint] Verify pods running and healthy

Execution:
✅ Step 1: Drained node-worker-3
✅ Step 2: Added new node-worker-7
✅ Checkpoint: Node ready ✓
✅ Step 3: Triggered ArgoCD sync for "payment-service"
✅ Checkpoint: All pods running ✓
✅ Remediation successful
```

### Scenario 2: MCO Update Causing Application Degradation

```
Issue: Increased application latency after OS update

Layer Detection:
- Infrastructure: MCO rollout in progress (root cause)
- Application: Increased latency (symptom)

Remediation Plan:
1. [Infrastructure] Check MCO status
2. [Infrastructure] If degraded, rollback MachineConfig
3. [Checkpoint] Verify MCO stable
4. [Application] Monitor application metrics
5. [Checkpoint] Verify latency normalized

Execution:
✅ Step 1: MCO rollout degraded on worker pool
✅ Step 2: Initiated MCO rollback
⏱️  Waiting 10 minutes for MCO stabilization...
✅ Checkpoint: MCO stable ✓
✅ Step 3: Application metrics improving
✅ Checkpoint: Latency back to normal ✓
✅ Remediation successful
```

## Consequences

### Positive

- ✅ **Comprehensive Remediation**: Addresses root cause across all layers
- ✅ **Coordinated Execution**: Prevents conflicting remediations
- ✅ **Dependency Awareness**: Executes in correct order (infra → platform → app)
- ✅ **Health Verification**: Validates each layer before proceeding
- ✅ **Rollback Coordination**: Can revert changes across all layers
- ✅ **Integration with ADR-011/012**: Leverages deployment method detection

### Negative

- ⚠️ **Complexity**: Multi-layer orchestration is complex
- ⚠️ **Longer Remediation Time**: Sequential execution with wait times
- ⚠️ **Failure Amplification**: Failure at one layer can trigger full rollback
- ⚠️ **Testing Challenges**: Need to test all layer combinations

### Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| **Cascading failures during remediation** | Health checkpoints between layers, coordinated rollback |
| **Excessive remediation time** | Parallel execution where safe, optimized wait times |
| **Incorrect layer detection** | ML-assisted root cause analysis, conservative fallbacks |
| **Rollback failures** | Test rollback procedures, manual intervention documentation |

## Implementation Phases

### Phase 1: Layer Detection (Week 1)
- ✅ Implement layer detection logic
- ✅ Build resource impact analysis
- ✅ Root cause determination

### Phase 2: Planning Engine (Week 2)
- ✅ Remediation plan generation
- ✅ Dependency resolution
- ✅ Checkpoint definition

### Phase 3: Orchestration (Week 3)
- ✅ Sequential execution engine
- ✅ Health verification
- ✅ Rollback coordination

### Phase 4: Integration & Testing (Week 4)
- ✅ Integration with ArgoCD/MCO APIs
- ✅ End-to-end testing
- ✅ Production validation

## Related ADRs

- [ADR-011: ArgoCD and MCO Integration Boundaries](011-argocd-mco-integration-boundaries.md)
- [ADR-012: Non-ArgoCD Application Remediation Strategy](012-non-argocd-application-remediation.md)
- [ADR-006: Integration Architecture](006-integration-architecture.md)
- [ADR-009: Architecture Evolution Roadmap](009-architecture-evolution-roadmap.md)

## References

- [TODO-APPLICATION-REMEDIATION.md](../../TODO-APPLICATION-REMEDIATION.md)
- [TODO-MCO-INTEGRATION.md](../../TODO-MCO-INTEGRATION.md)
- [OpenShift Machine Config Operator](https://docs.openshift.com/container-platform/latest/post_installation_configuration/machine-configuration-tasks.html)
- [ArgoCD Sync Phases](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-phases/)

## Approval

- **Architect**: Approved
- **Platform Team**: Approved
- **SRE Team**: Approved
- **Date**: 2025-12-17
