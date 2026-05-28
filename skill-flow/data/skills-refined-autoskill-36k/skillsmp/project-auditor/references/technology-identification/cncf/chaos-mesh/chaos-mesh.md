# Chaos Mesh

**Category**: cncf
**Description**: Cloud-native chaos engineering platform for Kubernetes
**Homepage**: https://chaos-mesh.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Chaos Mesh Go packages*

- `github.com/chaos-mesh/chaos-mesh` - Chaos Mesh core
- `github.com/chaos-mesh/chaos-mesh/api` - API types

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Chaos Mesh usage*

- `chaos-mesh.yaml` - Chaos Mesh deployment
- `podchaos.yaml` - PodChaos experiment
- `networkchaos.yaml` - NetworkChaos experiment

### Code Patterns

**Pattern**: `chaos-mesh\.org/|chaos-mesh-`
- Chaos Mesh annotations and naming
- Example: `chaos-mesh.org/chaos: "true"`

**Pattern**: `kind:\s*(PodChaos|NetworkChaos|StressChaos|IOChaos|TimeChaos|DNSChaos|HTTPChaos|JVMChaos|KernelChaos)`
- Chaos Mesh CRD kinds
- Example: `kind: PodChaos`

**Pattern**: `apiVersion:\s*chaos-mesh\.org/v[0-9]+`
- Chaos Mesh API version
- Example: `apiVersion: chaos-mesh.org/v1alpha1`

**Pattern**: `action:\s*(pod-kill|pod-failure|container-kill|netem|delay|loss|duplicate|corrupt)`
- Chaos actions
- Example: `action: pod-kill`

**Pattern**: `selector:|mode:|duration:|scheduler:`
- Chaos spec fields
- Example: `selector:\n  namespaces:\n    - default`

**Pattern**: `chaos-controller-manager|chaos-daemon|chaos-dashboard`
- Chaos Mesh components
- Example: `name: chaos-controller-manager`

**Pattern**: `Workflow|Schedule|StatusCheck`
- Chaos Mesh workflow CRDs
- Example: `kind: Workflow`

**Pattern**: `chaosd|chaosctl`
- Chaos Mesh CLI tools
- Example: `chaosctl debug`

---

## Environment Variables

- `CHAOS_MESH_NAMESPACE` - Chaos Mesh namespace
- `CHAOS_DAEMON_PORT` - Daemon port

## Detection Notes

- Visual dashboard for chaos experiments
- Supports pod, network, stress, IO chaos
- Workflow for complex scenarios
- Schedule for recurring experiments
- Supports physical machine chaos

---

## Secrets Detection

### Credentials

#### Dashboard Auth
**Pattern**: `security\.secret:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Chaos Dashboard authentication secret

---

## TIER 3: Configuration Extraction

### Action Extraction

**Pattern**: `action:\s*['"]?([a-z-]+)['"]?`
- Chaos action type
- Extracts: `action`
- Example: `action: pod-kill`

### Duration Extraction

**Pattern**: `duration:\s*['"]?([0-9]+[smh])['"]?`
- Chaos duration
- Extracts: `duration`
- Example: `duration: 30s`

### Mode Extraction

**Pattern**: `mode:\s*['"]?(one|all|fixed|fixed-percent|random-max-percent)['"]?`
- Target selection mode
- Extracts: `mode`
- Example: `mode: one`
