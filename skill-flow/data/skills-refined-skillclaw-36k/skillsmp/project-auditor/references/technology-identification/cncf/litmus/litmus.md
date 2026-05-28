# Litmus

**Category**: cncf
**Description**: Cloud-native chaos engineering platform
**Homepage**: https://litmuschaos.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Litmus Go packages*

- `github.com/litmuschaos/litmus-go` - Litmus Go SDK
- `github.com/litmuschaos/chaos-operator` - Chaos operator
- `github.com/litmuschaos/chaos-exporter` - Chaos exporter

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Litmus usage*

- `chaosengine.yaml` - ChaosEngine definition
- `chaosexperiment.yaml` - ChaosExperiment
- `litmus-portal.yaml` - Litmus portal

### Code Patterns

**Pattern**: `litmuschaos\.io/|litmus-`
- Litmus annotations and naming
- Example: `litmuschaos.io/chaos: "true"`

**Pattern**: `kind:\s*(ChaosEngine|ChaosExperiment|ChaosResult|ChaosSchedule)`
- Litmus CRD kinds
- Example: `kind: ChaosEngine`

**Pattern**: `apiVersion:\s*litmuschaos\.io/v[0-9]+`
- Litmus API version
- Example: `apiVersion: litmuschaos.io/v1alpha1`

**Pattern**: `appinfo:|experiments:|chaosServiceAccount:|engineState:`
- ChaosEngine spec fields
- Example: `appinfo:\n  appns: default`

**Pattern**: `pod-delete|container-kill|node-drain|network-loss|cpu-hog|memory-hog`
- Common chaos experiments
- Example: `name: pod-delete`

**Pattern**: `litmusctl|litmus-portal`
- Litmus tools
- Example: `litmusctl create chaos-scenario`

**Pattern**: `chaosresult|chaos-runner`
- Litmus components
- Example: `chaos-runner`

**Pattern**: `TOTAL_CHAOS_DURATION|CHAOS_INTERVAL|LIB:`
- Chaos experiment environment variables
- Example: `TOTAL_CHAOS_DURATION: "30"`

---

## Environment Variables

- `CHAOS_NAMESPACE` - Chaos namespace
- `TOTAL_CHAOS_DURATION` - Chaos duration
- `CHAOS_INTERVAL` - Chaos interval
- `LITMUS_PORTAL_ENDPOINT` - Portal endpoint

## Detection Notes

- ChaosEngine links app to experiments
- ChaosExperiment defines chaos logic
- ChaosResult stores experiment outcomes
- Supports scheduled chaos
- Hub for sharing experiments

---

## Secrets Detection

### Credentials

#### Chaos Service Account
**Pattern**: `chaosServiceAccount:\s*['"]?([^\s'"]+)['"]?`
**Severity**: medium
**Description**: Service account for chaos execution

---

## TIER 3: Configuration Extraction

### App Namespace Extraction

**Pattern**: `appns:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Target application namespace
- Extracts: `app_namespace`
- Example: `appns: default`

### Chaos Duration Extraction

**Pattern**: `TOTAL_CHAOS_DURATION:\s*['"]?([0-9]+)['"]?`
- Total chaos duration in seconds
- Extracts: `chaos_duration`
- Example: `TOTAL_CHAOS_DURATION: "30"`

### Experiment Name Extraction

**Pattern**: `name:\s*['"]?([a-z-]+)['"]?`
- Chaos experiment name
- Extracts: `experiment_name`
- Example: `name: pod-delete`
