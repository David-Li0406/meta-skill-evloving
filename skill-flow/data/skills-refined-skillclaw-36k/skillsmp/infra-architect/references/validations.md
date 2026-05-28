# Infra Architect - Validations

## Container Without Resource Limits

### **Id**
no-resource-limits
### **Severity**
error
### **Type**
regex
### **Pattern**
  - containers:(?!.*limits)
  - image:.*(?!.*resources:)
### **Message**
Container defined without resource limits. Can starve node resources.
### **Fix Action**
Add resources.limits.cpu and resources.limits.memory
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml
  - **/manifests/**/*.yaml

## Using Latest Image Tag

### **Id**
latest-tag
### **Severity**
error
### **Type**
regex
### **Pattern**
  - image:.*:latest
  - image:[^:]+\s*$
### **Message**
Using :latest or untagged image. Not reproducible, can't rollback.
### **Fix Action**
Use specific version tags or SHA digests
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml
  - **/*deployment*.yaml

## Pod Without Health Probes

### **Id**
no-health-probes
### **Severity**
error
### **Type**
regex
### **Pattern**
  - containers:(?!.*livenessProbe)
  - containers:(?!.*readinessProbe)
### **Message**
Container without health probes. K8s can't detect failures.
### **Fix Action**
Add livenessProbe and readinessProbe
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml
  - **/*deployment*.yaml

## Privileged Container

### **Id**
privileged-container
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - privileged:\s*true
  - allowPrivilegeEscalation:\s*true
### **Message**
Privileged container. Container escape = full node access.
### **Fix Action**
Remove privileged: true, set allowPrivilegeEscalation: false
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml

## Container Running as Root

### **Id**
run-as-root
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - runAsUser:\s*0
  - runAsNonRoot:\s*false
### **Message**
Container running as root user. Increases blast radius of compromise.
### **Fix Action**
Set runAsNonRoot: true, runAsUser: 1000
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml

## Namespace Without Network Policy

### **Id**
no-network-policy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - kind:\s*Namespace(?!.*NetworkPolicy)
### **Message**
Namespace without default deny NetworkPolicy. All pods can talk to all pods.
### **Fix Action**
Add default-deny NetworkPolicy for the namespace
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml

## Secrets Hardcoded in Manifests

### **Id**
hardcoded-secrets
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - password:\s*["'][^"']+["']
  - apiKey:\s*["'][^"']+["']
  - secret:\s*["'][^"']+["']
  - token:\s*["'][A-Za-z0-9+/=]{20,}["']
### **Message**
Hardcoded secret in manifest. Will be in Git history forever.
### **Fix Action**
Use Kubernetes Secrets or external secrets manager
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml
  - **/terraform/**/*.tf

## Terraform Backend Without Locking

### **Id**
terraform-no-lock
### **Severity**
error
### **Type**
regex
### **Pattern**
  - backend\s+"s3"(?!.*dynamodb_table)
  - backend\s+"gcs"(?!.*lock)
### **Message**
Terraform backend without state locking. Concurrent runs will corrupt state.
### **Fix Action**
Add dynamodb_table for S3 or enable locking for GCS
### **Applies To**
  - **/terraform/**/*.tf
  - **/*.tf

## Terraform Provider Without Version Constraint

### **Id**
terraform-no-version
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - provider\s+"[^"]+"\s*\{(?!.*version)
  - source\s*=\s*"[^"]+/[^"]+"(?!.*version)
### **Message**
Provider without version constraint. Updates can break infrastructure.
### **Fix Action**
Add version constraint: version = "~> 4.0"
### **Applies To**
  - **/terraform/**/*.tf
  - **/*.tf

## Deployment Without PodDisruptionBudget

### **Id**
no-pdb
### **Severity**
info
### **Type**
regex
### **Pattern**
  - kind:\s*Deployment(?!.*PodDisruptionBudget)
  - replicas:\s*[3-9](?!.*PodDisruptionBudget)
### **Message**
Deployment without PDB. Cluster operations can take down all pods at once.
### **Fix Action**
Add PodDisruptionBudget with minAvailable or maxUnavailable
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml

## No Pod Topology Constraints

### **Id**
no-topology-spread
### **Severity**
info
### **Type**
regex
### **Pattern**
  - replicas:\s*[3-9](?!.*topologySpreadConstraints)
  - kind:\s*Deployment(?!.*podAntiAffinity)
### **Message**
Multiple replicas without spread constraints. May all land on same node.
### **Fix Action**
Add topologySpreadConstraints or podAntiAffinity
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml

## Service Without Pod Selector

### **Id**
service-without-selector
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - kind:\s*Service(?!.*selector:)
### **Message**
Service without selector. May be intentional (ExternalName) but usually a mistake.
### **Fix Action**
Add selector matching pod labels, or confirm ExternalName is intended
### **Applies To**
  - **/kubernetes/**/*.yaml
  - **/k8s/**/*.yaml