# Kubernetes - Validations

## Container running as root

### **Id**
running-as-root
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - runAsNonRoot:\\s*false
  - containers:[\\s\\S]*?(?!securityContext)[\\s\\S]*?image:
### **Message**
Containers should not run as root
### **Fix Action**
Add securityContext.runAsNonRoot: true
### **Applies To**
  - *.yaml
  - *.yml

## Privileged container

### **Id**
privileged-container
### **Severity**
error
### **Type**
regex
### **Pattern**
  - privileged:\\s*true
### **Message**
Privileged containers have full host access - avoid in production
### **Fix Action**
Remove privileged: true or use specific capabilities
### **Applies To**
  - *.yaml
  - *.yml

## Using host network

### **Id**
host-network
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - hostNetwork:\\s*true
### **Message**
Host network bypasses network isolation
### **Fix Action**
Use ClusterIP service instead unless absolutely necessary
### **Applies To**
  - *.yaml
  - *.yml

## Using host PID namespace

### **Id**
host-pid
### **Severity**
error
### **Type**
regex
### **Pattern**
  - hostPID:\\s*true
### **Message**
Host PID allows seeing host processes - security risk
### **Fix Action**
Remove hostPID: true
### **Applies To**
  - *.yaml
  - *.yml

## Missing resource limits

### **Id**
no-resource-limits
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - containers:[\\s\\S]*?(?!resources:)[\\s\\S]*?image:
### **Message**
Containers should have resource requests and limits
### **Fix Action**
Add resources.requests and resources.limits
### **Applies To**
  - *.yaml
  - *.yml

## Using :latest image tag

### **Id**
latest-tag
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - image:\\s*[^:]+:latest
  - image:\\s*[^:\\s]+\\s*$
### **Message**
Use specific image tags for reproducibility
### **Fix Action**
Use version tag like :v1.2.3 or SHA digest
### **Applies To**
  - *.yaml
  - *.yml

## Missing liveness probe

### **Id**
no-liveness-probe
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - containers:[\\s\\S]*?(?!livenessProbe:)[\\s\\S]*?image:
### **Message**
Containers should have liveness probes
### **Fix Action**
Add livenessProbe with httpGet, tcpSocket, or exec
### **Applies To**
  - *.yaml
  - *.yml

## Missing readiness probe

### **Id**
no-readiness-probe
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - containers:[\\s\\S]*?(?!readinessProbe:)[\\s\\S]*?image:
### **Message**
Containers should have readiness probes for traffic management
### **Fix Action**
Add readinessProbe to control when pod receives traffic
### **Applies To**
  - *.yaml
  - *.yml

## ImagePullPolicy not set with latest tag

### **Id**
image-pull-policy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - image:[^\\n]*:latest(?![\\s\\S]*imagePullPolicy:\\s*Always)
### **Message**
With :latest tag, set imagePullPolicy: Always
### **Fix Action**
Add imagePullPolicy: Always or use specific tag
### **Applies To**
  - *.yaml
  - *.yml

## Only one replica for production

### **Id**
replicas-one
### **Severity**
info
### **Type**
regex
### **Pattern**
  - replicas:\\s*1\\s*$
### **Message**
Single replica means no high availability
### **Fix Action**
Use at least 2-3 replicas for production workloads
### **Applies To**
  - *.yaml
  - *.yml

## Deployment without PodDisruptionBudget

### **Id**
no-pdb
### **Severity**
info
### **Type**
regex
### **Pattern**
  - kind:\\s*Deployment(?![\\s\\S]*PodDisruptionBudget)
### **Message**
Consider adding PodDisruptionBudget for controlled disruptions
### **Fix Action**
Create PodDisruptionBudget with minAvailable or maxUnavailable
### **Applies To**
  - *.yaml
  - *.yml

## Secret value hardcoded in manifest

### **Id**
secret-in-env
### **Severity**
error
### **Type**
regex
### **Pattern**
  - value:\\s*["']?(sk_|pk_|api_|secret_|password)
  - password:\\s*["']?[^\\s]+
### **Message**
Secrets should not be hardcoded in manifests
### **Fix Action**
Use Secret resource and secretKeyRef
### **Applies To**
  - *.yaml
  - *.yml

## Using LoadBalancer without annotation

### **Id**
service-type-loadbalancer
### **Severity**
info
### **Type**
regex
### **Pattern**
  - type:\\s*LoadBalancer(?![\\s\\S]*annotations:)
### **Message**
LoadBalancer creates cloud resources - use Ingress for HTTP
### **Fix Action**
Consider Ingress for HTTP traffic, or add appropriate annotations
### **Applies To**
  - *.yaml
  - *.yml

## No NetworkPolicy in namespace

### **Id**
no-network-policy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - kind:\\s*Namespace(?![\\s\\S]*NetworkPolicy)
### **Message**
Consider adding NetworkPolicy for network isolation
### **Fix Action**
Create default-deny NetworkPolicy
### **Applies To**
  - *.yaml
  - *.yml