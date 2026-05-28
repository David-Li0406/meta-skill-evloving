# Operator Framework

**Category**: cncf
**Description**: Toolkit for building Kubernetes operators
**Homepage**: https://operatorframework.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Operator Framework Go packages*

- `github.com/operator-framework/operator-sdk` - Operator SDK
- `github.com/operator-framework/operator-lib` - Operator library
- `github.com/operator-framework/api` - OLM API
- `sigs.k8s.io/controller-runtime` - Controller runtime
- `sigs.k8s.io/kubebuilder` - Kubebuilder

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Operator Framework usage*

- `PROJECT` - Operator SDK/Kubebuilder project
- `Makefile` - Operator Makefile
- `config/manager/manager.yaml` - Manager deployment
- `bundle.Dockerfile` - OLM bundle Dockerfile
- `config/manifests/bases/*.clusterserviceversion.yaml` - CSV

### Configuration Directories
*Known directories that indicate Operator Framework usage*

- `config/crd/` - CRD definitions
- `config/rbac/` - RBAC manifests
- `config/samples/` - Sample CRs
- `bundle/` - OLM bundle

### Code Patterns

**Pattern**: `operators\.coreos\.com/|olm\.operatorframework\.io/`
- OLM API groups
- Example: `operators.coreos.com/v1alpha1`

**Pattern**: `kind:\s*(ClusterServiceVersion|InstallPlan|Subscription|CatalogSource|OperatorGroup)`
- OLM CRD kinds
- Example: `kind: ClusterServiceVersion`

**Pattern**: `operator-sdk\s+(init|create|build|bundle|run|scorecard)`
- Operator SDK commands
- Example: `operator-sdk init --domain example.com`

**Pattern**: `kubebuilder:\s*(object|subresource|rbac|webhook)`
- Kubebuilder markers
- Example: `// +kubebuilder:object:root=true`

**Pattern**: `ctrl\.NewControllerManagedBy|SetupWithManager`
- Controller setup patterns
- Example: `ctrl.NewControllerManagedBy(mgr)`

**Pattern**: `Reconcile\(ctx|func.*Reconcile`
- Reconcile function
- Example: `func (r *MyReconciler) Reconcile(ctx context.Context`

**Pattern**: `domain:|layout:|projectName:|version:`
- PROJECT file fields
- Example: `domain: example.com`

**Pattern**: `displayName:|description:|installModes:|owned:`
- ClusterServiceVersion fields
- Example: `displayName: My Operator`

---

## Environment Variables

- `OPERATOR_NAME` - Operator name
- `OPERATOR_NAMESPACE` - Operator namespace
- `WATCH_NAMESPACE` - Namespace to watch
- `POD_NAME` - Pod name
- `LEADER_ELECTION_NAMESPACE` - Leader election namespace

## Detection Notes

- Operator SDK for building operators
- OLM for lifecycle management
- Kubebuilder for scaffolding
- CRDs define custom resources
- CSV for OLM metadata

---

## Secrets Detection

### Credentials

#### OLM Pull Secret
**Pattern**: `secrets:\s*\n\s*-\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Image pull secrets in CatalogSource
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Domain Extraction

**Pattern**: `domain:\s*['"]?([a-zA-Z0-9.-]+)['"]?`
- Operator domain
- Extracts: `domain`
- Example: `domain: example.com`

### Operator Version Extraction

**Pattern**: `version:\s*['"]?([0-9]+\.[0-9]+\.[0-9]+)['"]?`
- Operator version
- Extracts: `version`
- Example: `version: 0.0.1`

### Group Extraction

**Pattern**: `group:\s*['"]?([a-zA-Z0-9.-]+)['"]?`
- API group
- Extracts: `api_group`
- Example: `group: cache.example.com`
