# Kyverno

**Category**: cncf
**Description**: Kubernetes native policy management
**Homepage**: https://kyverno.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Kyverno Go packages*

- `github.com/kyverno/kyverno` - Kyverno core
- `github.com/kyverno/kyverno/api` - API types
- `github.com/kyverno/kyverno/pkg` - Packages

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Kyverno usage*

- `kyverno-policy.yaml` - Kyverno policy
- `clusterpolicy.yaml` - ClusterPolicy
- `policy.yaml` - Policy

### Code Patterns

**Pattern**: `kyverno\.io/|kyverno-`
- Kyverno annotations and naming
- Example: `kyverno.io/last-applied-patches`

**Pattern**: `kind:\s*(ClusterPolicy|Policy|ClusterPolicyReport|PolicyReport)`
- Kyverno CRD kinds
- Example: `kind: ClusterPolicy`

**Pattern**: `apiVersion:\s*kyverno\.io/v[0-9]+`
- Kyverno API version
- Example: `apiVersion: kyverno.io/v1`

**Pattern**: `rules:|match:|exclude:|validate:|mutate:|generate:|verifyImages:`
- Kyverno policy sections
- Example: `rules:\n  - name: require-labels`

**Pattern**: `pattern:|anyPattern:|deny:|foreach:|context:`
- Kyverno rule patterns
- Example: `pattern:\n  metadata:\n    labels:`

**Pattern**: `preconditions:|conditions:|message:`
- Kyverno conditions
- Example: `preconditions:\n  all:`

**Pattern**: `kyverno\s+(apply|test|version)`
- Kyverno CLI commands
- Example: `kyverno apply policy.yaml --resource pod.yaml`

**Pattern**: `imageVerify:|attestors:|attestations:`
- Image verification
- Example: `verifyImages:\n  - imageReferences:`

---

## Environment Variables

- `KYVERNO_NAMESPACE` - Kyverno namespace
- `KYVERNO_DEPLOYMENT` - Deployment name
- `KYVERNO_SVC` - Service name

## Detection Notes

- Kubernetes native policies (no new language)
- Validate, mutate, generate resources
- Image signature verification
- Policy reports for compliance
- Background scanning

---

## Secrets Detection

### Credentials

#### Image Registry Credentials
**Pattern**: `imagePullSecrets:|registry:`
**Severity**: medium
**Description**: Image registry configuration in policies

#### Cosign Public Key
**Pattern**: `key:\s*['"]?([^\s'"]+\.pub)['"]?`
**Severity**: medium
**Description**: Cosign public key reference for image verification

---

## TIER 3: Configuration Extraction

### Policy Name Extraction

**Pattern**: `name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Kyverno policy name
- Extracts: `policy_name`
- Example: `name: require-labels`

### Validation Action Extraction

**Pattern**: `validationFailureAction:\s*['"]?(enforce|audit)['"]?`
- Validation failure action
- Extracts: `validation_action`
- Example: `validationFailureAction: enforce`

### Background Extraction

**Pattern**: `background:\s*(true|false)`
- Background processing enabled
- Extracts: `background`
- Example: `background: true`
