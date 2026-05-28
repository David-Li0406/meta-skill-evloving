# Kubernetes Deployment - Validations

## Container Without Resource Limits

### **Id**
k8s-no-resource-limits
### **Severity**
error
### **Type**
regex
### **Pattern**
  - containers:\s*\n\s*-\s*name:[^\n]*(?:\n(?!.*limits:)[^\n]*)*(?=\n\s*-\s*name:|\n[a-zA-Z]|\Z)
  - kind:\s*Deployment(?:(?!limits:).)*$
### **Message**
Container without resource limits. Can consume entire node resources and cause OOMKilled cascade.
### **Fix Action**
Add resources.limits.memory and resources.limits.cpu to all containers
### **Applies To**
  - *.yaml
  - *.yml
  - *deployment*.yaml

## Container Without Resource Requests

### **Id**
k8s-no-resource-requests
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - containers:\s*\n\s*-\s*name:[^\n]*(?:\n(?!.*requests:)[^\n]*)*(?=\n\s*-\s*name:|\n[a-zA-Z]|\Z)
### **Message**
Container without resource requests. Scheduler can't make optimal placement decisions.
### **Fix Action**
Add resources.requests.memory and resources.requests.cpu
### **Applies To**
  - *.yaml
  - *.yml

## Image Using Latest Tag

### **Id**
k8s-latest-tag
### **Severity**
error
### **Type**
regex
### **Pattern**
  - image:\s*[^:\s]+:latest
  - image:\s*[^:\s]+\s*$
  - image:\s*["'][^:]+["']
### **Message**
Image using :latest tag or no tag. Deployments become non-deterministic and rollbacks don't work.
### **Fix Action**
Pin to specific version tag (e.g., v1.2.3) or use image digest
### **Applies To**
  - *.yaml
  - *.yml

## Container Without Liveness Probe

### **Id**
k8s-no-liveness-probe
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - kind:\s*Deployment[\s\S]*containers:[\s\S]*?(?!livenessProbe)(?=\n\s{4,}[a-zA-Z]|\nkind:|\Z)
### **Message**
Container without liveness probe. Kubernetes can't detect if app is stuck and needs restart.
### **Fix Action**
Add livenessProbe with appropriate httpGet, tcpSocket, or exec check
### **Applies To**
  - *deployment*.yaml
  - *.yaml

## Container Without Readiness Probe

### **Id**
k8s-no-readiness-probe
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - kind:\s*Deployment[\s\S]*containers:[\s\S]*?(?!readinessProbe)(?=\n\s{4,}[a-zA-Z]|\nkind:|\Z)
### **Message**
Container without readiness probe. Traffic routed to pods that aren't ready to serve.
### **Fix Action**
Add readinessProbe to control when pod receives traffic
### **Applies To**
  - *deployment*.yaml
  - *.yaml

## Container Running as Root

### **Id**
k8s-running-as-root
### **Severity**
error
### **Type**
regex
### **Pattern**
  - runAsNonRoot:\s*false
  - runAsUser:\s*0
  - privileged:\s*true
### **Message**
Container running as root or privileged. Container escape vulnerabilities become full node compromise.
### **Fix Action**
Add securityContext with runAsNonRoot: true and runAsUser: non-zero UID
### **Applies To**
  - *.yaml
  - *.yml

## Container Without Security Context

### **Id**
k8s-no-security-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - containers:\s*\n\s*-\s*name:[^\n]*(?:\n(?!.*securityContext:)[^\n]*)*(?=\n\s*-\s*name:|\n[a-zA-Z]|\Z)
### **Message**
Container without securityContext. Running with default (often root) permissions.
### **Fix Action**
Add securityContext with runAsNonRoot, readOnlyRootFilesystem, allowPrivilegeEscalation: false
### **Applies To**
  - *.yaml
  - *.yml

## Naked Pod Without Controller

### **Id**
k8s-naked-pod
### **Severity**
error
### **Type**
regex
### **Pattern**
  - kind:\s*Pod\s*\n(?!.*ownerReferences)
### **Message**
Naked Pod detected. Won't be rescheduled on node failure, no rolling updates or rollback.
### **Fix Action**
Use Deployment for stateless, StatefulSet for stateful, DaemonSet for node-level workloads
### **Applies To**
  - *.yaml
  - *.yml
  - pod*.yaml

## Hardcoded Replicas With HPA

### **Id**
k8s-hardcoded-replicas-with-hpa
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - replicas:\s*\d+[\s\S]*HorizontalPodAutoscaler
  - HorizontalPodAutoscaler[\s\S]*replicas:\s*\d+
### **Message**
Deployment has hardcoded replicas with HPA. Helm upgrade resets replicas to hardcoded value, fighting HPA.
### **Fix Action**
Omit replicas from Deployment when using HPA, or use helm lookup function
### **Applies To**
  - *.yaml
  - *.yml

## Secret Data in ConfigMap

### **Id**
k8s-secret-in-configmap
### **Severity**
error
### **Type**
regex
### **Pattern**
  - kind:\s*ConfigMap[\s\S]*(?:password|secret|api[_-]?key|token|credential):
  - ConfigMap[\s\S]*DATABASE_URL:
  - ConfigMap[\s\S]*AWS_SECRET
### **Message**
Sensitive data in ConfigMap. ConfigMaps aren't encrypted at rest and have weaker RBAC.
### **Fix Action**
Use Secret for sensitive data. Enable encryption at rest for Secrets.
### **Applies To**
  - *.yaml
  - *.yml
  - *configmap*.yaml

## Production Deployment Without PDB

### **Id**
k8s-no-pod-disruption-budget
### **Severity**
info
### **Type**
regex
### **Pattern**
  - kind:\s*Deployment[\s\S]*replicas:\s*[3-9]|replicas:\s*\d{2,}(?![\s\S]*PodDisruptionBudget)
### **Message**
Production deployment without PodDisruptionBudget. Node drains could take down all replicas.
### **Fix Action**
Add PodDisruptionBudget with minAvailable or maxUnavailable
### **Applies To**
  - *.yaml
  - *.yml

## Potential Selector Mismatch

### **Id**
k8s-selector-mismatch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - selector:\s*\n\s*matchLabels:[\s\S]*?app:\s*(\S+)[\s\S]*?template:[\s\S]*?labels:[\s\S]*?app:\s*(?!\1)
### **Message**
Potential label selector mismatch. Service selector must exactly match pod labels.
### **Fix Action**
Ensure selector.matchLabels matches spec.template.metadata.labels exactly
### **Applies To**
  - *.yaml
  - *.yml

## Ingress Without IngressClass

### **Id**
k8s-no-ingress-class
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - kind:\s*Ingress[\s\S]*?spec:(?![\s\S]*?ingressClassName)
### **Message**
Ingress without ingressClassName. In multi-controller clusters, wrong controller may handle it.
### **Fix Action**
Add spec.ingressClassName to specify which controller handles this Ingress
### **Applies To**
  - *.yaml
  - *.yml
  - *ingress*.yaml

## HostPath Volume Mount

### **Id**
k8s-hostpath-volume
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - hostPath:\s*\n\s*path:
### **Message**
HostPath volume mount detected. Breaks pod portability and can be security risk.
### **Fix Action**
Use PersistentVolumeClaim or cloud storage instead of hostPath
### **Applies To**
  - *.yaml
  - *.yml

## Privileged Port Binding

### **Id**
k8s-privileged-port
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - containerPort:\s*([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|10[0-1][0-9]|102[0-3])\s*$
  - hostPort:\s*([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|10[0-1][0-9]|102[0-3])
### **Message**
Container binding to privileged port (<1024). Requires root or special capabilities.
### **Fix Action**
Use port > 1024 in container, let Service/Ingress handle external port mapping
### **Applies To**
  - *.yaml
  - *.yml

## Aggressive Liveness Probe Settings

### **Id**
k8s-aggressive-probe
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - livenessProbe:[\s\S]*?failureThreshold:\s*1
  - livenessProbe:[\s\S]*?timeoutSeconds:\s*1
  - livenessProbe:[\s\S]*?periodSeconds:\s*[1-3]\s
### **Message**
Aggressive liveness probe settings. Under load, healthy pods may be killed unnecessarily.
### **Fix Action**
Use failureThreshold >= 3, timeoutSeconds >= 3, periodSeconds >= 5 for liveness probes
### **Applies To**
  - *.yaml
  - *.yml

## EmptyDir for Persistent Data

### **Id**
k8s-empty-dir-prod
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - emptyDir:\s*\{\}[\s\S]*?mountPath:\s*/data
  - emptyDir:[\s\S]*?(database|storage|uploads)
### **Message**
EmptyDir used for data that should persist. Data lost when pod is rescheduled.
### **Fix Action**
Use PersistentVolumeClaim for data that must survive pod restarts
### **Applies To**
  - *.yaml
  - *.yml