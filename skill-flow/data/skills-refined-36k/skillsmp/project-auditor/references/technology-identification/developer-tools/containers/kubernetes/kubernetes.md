# Kubernetes

**Category**: developer-tools/containers
**Description**: Container orchestration platform for automating deployment, scaling, and management
**Homepage**: https://kubernetes.io

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `@kubernetes/client-node` - Official Kubernetes client for Node.js

#### PYPI
- `kubernetes` - Official Kubernetes client for Python
- `kopf` - Kubernetes Operator Framework for Python
- `kr8s` - Async Kubernetes client for Python

#### GO
- `k8s.io/client-go` - Official Kubernetes Go client
- `k8s.io/api` - Kubernetes API types
- `k8s.io/apimachinery` - Kubernetes API machinery
- `sigs.k8s.io/controller-runtime` - Controller runtime for building operators

#### MAVEN
- `io.kubernetes:client-java` - Java client for Kubernetes

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### Configuration Files
*Known configuration files that indicate Kubernetes usage*

- `kustomization.yaml` - Kustomize configuration (strong indicator)
- `kustomization.yml` - Kustomize configuration
- `Chart.yaml` - Helm chart definition (strong indicator)
- `values.yaml` - Helm chart values
- `helmfile.yaml` - Helmfile configuration
- `skaffold.yaml` - Skaffold configuration
- `.kube/config` - Kubernetes config
- `kubeconfig` - Kubernetes config

### Configuration Directories
*Known directories that indicate Kubernetes usage*

- `.kube/` - Kubernetes configuration directory
- `charts/` - Helm charts directory
- `helm/` - Helm configurations
- `k8s/` - Kubernetes manifests directory
- `kubernetes/` - Kubernetes manifests directory
- `manifests/` - Kubernetes manifests directory
- `deploy/` - Deployment configurations

### File Patterns
*Common Kubernetes manifest file names*

- `deployment.yaml` / `deployment.yml`
- `service.yaml` / `service.yml`
- `configmap.yaml` / `configmap.yml`
- `secret.yaml` / `secret.yml`
- `ingress.yaml` / `ingress.yml`
- `namespace.yaml` / `namespace.yml`
- `pod.yaml` / `pod.yml`
- `statefulset.yaml` / `statefulset.yml`
- `daemonset.yaml` / `daemonset.yml`
- `cronjob.yaml` / `cronjob.yml`
- `job.yaml` / `job.yml`
- `pvc.yaml` / `pvc.yml`
- `pv.yaml` / `pv.yml`
- `hpa.yaml` / `hpa.yml`
- `networkpolicy.yaml` / `networkpolicy.yml`

### Code Patterns
*Kubernetes YAML patterns*

**Pattern**: `^apiVersion:\s*`
- Kubernetes API version declaration
- Example: `apiVersion: apps/v1`

**Pattern**: `^kind:\s*(Deployment|Service|ConfigMap|Secret|Ingress|Pod|StatefulSet|DaemonSet|Job|CronJob|Namespace|PersistentVolumeClaim|HorizontalPodAutoscaler|NetworkPolicy|ServiceAccount|Role|RoleBinding|ClusterRole|ClusterRoleBinding)`
- Kubernetes resource kind
- Example: `kind: Deployment`

**Pattern**: `^\s+containers:\s*$`
- Container specification
- Example: `containers:`

**Pattern**: `^\s+image:\s*`
- Container image specification
- Example: `image: nginx:latest`

**Pattern**: `^\s+ports:\s*$`
- Ports specification
- Example: `ports:`

**Pattern**: `^\s+env:\s*$`
- Environment variables specification
- Example: `env:`

**Pattern**: `^\s+volumeMounts:\s*$`
- Volume mounts specification
- Example: `volumeMounts:`

**Pattern**: `^\s+volumes:\s*$`
- Volumes specification
- Example: `volumes:`

**Pattern**: `^\s+resources:\s*$`
- Resource limits/requests
- Example: `resources:`

**Pattern**: `^\s+selector:\s*$`
- Label selector
- Example: `selector:`

**Pattern**: `^\s+replicas:\s*\d+`
- Replica count
- Example: `replicas: 3`

*Helm chart patterns*

**Pattern**: `^\{\{-?\s*`
- Helm template syntax
- Example: `{{ .Values.image.repository }}`

**Pattern**: `\.Values\.\w+`
- Helm values reference
- Example: `{{ .Values.replicaCount }}`

**Pattern**: `\.Release\.Name`
- Helm release name reference
- Example: `{{ .Release.Name }}`

---

## Environment Variables

- `KUBECONFIG` - Path to kubeconfig file
- `KUBERNETES_SERVICE_HOST` - Kubernetes API server host (in-cluster)
- `KUBERNETES_SERVICE_PORT` - Kubernetes API server port (in-cluster)
- `KUBERNETES_SERVICE_PORT_HTTPS` - Kubernetes API server HTTPS port
- `HELM_HOME` - Helm home directory
- `HELM_CACHE_HOME` - Helm cache directory
- `HELM_CONFIG_HOME` - Helm config directory
- `HELM_DATA_HOME` - Helm data directory

## Detection Notes

- YAML files with both `apiVersion:` and `kind:` fields indicate Kubernetes manifests
- `kustomization.yaml` indicates Kustomize usage
- `Chart.yaml` is definitive for Helm charts
- `k8s/` or `kubernetes/` directories are common conventions
- Check for kubectl commands in scripts and CI/CD pipelines
- Helm template syntax `{{ }}` indicates Helm charts

---

## TIER 3: Configuration Extraction

These patterns extract specific configuration values for infrastructure inventory.

### Cluster Extraction

**Pattern**: `server:\s*['"]?(https?://[^'"\s]+)`
- Kubernetes API server URL
- Extracts: `cluster_endpoint`
- Example: `server: https://kubernetes.default.svc`

**Pattern**: `([a-z0-9-]+)\.([a-z]{2}-[a-z]+-[0-9])\.eks\.amazonaws\.com`
- EKS cluster endpoint
- Extracts: `cluster_name`, `aws_region`
- Example: `https://ABC123.us-west-2.eks.amazonaws.com`

**Pattern**: `container\.googleapis\.com/projects/([^/]+)/(?:locations|zones)/([^/]+)/clusters/([^/\s'"]+)`
- GKE cluster resource name
- Extracts: `project_id`, `location`, `cluster_name`
- Example: `container.googleapis.com/projects/my-proj/zones/us-central1-a/clusters/prod`

**Pattern**: `([a-z0-9-]+)\.([a-z]+)\.azmk8s\.io`
- AKS cluster endpoint
- Extracts: `cluster_name`, `region`
- Example: `https://mycluster.eastus.azmk8s.io`

### Namespace Extraction

**Pattern**: `^metadata:\s*\n\s+namespace:\s*['"]?([a-z0-9][a-z0-9-]{0,62})['"]?`
- Resource namespace
- Extracts: `namespace`
- Example: `namespace: production`

**Pattern**: `^kind:\s*Namespace\s*\n.*name:\s*['"]?([a-z0-9][a-z0-9-]{0,62})['"]?`
- Namespace definition
- Extracts: `namespace_name`
- Example: `name: production`

### Container Image Extraction

**Pattern**: `image:\s*['"]?([a-z0-9.-]+(?::[0-9]+)?/[^:'"]+)(?::([^'"]+))?['"]?`
- Container image with registry
- Extracts: `image`, `tag`
- Example: `image: 123456789012.dkr.ecr.us-west-2.amazonaws.com/app:v1.2.3`

### Resource Limits Extraction

**Pattern**: `limits:\s*\n\s+cpu:\s*['"]?([^'"\n]+)['"]?\s*\n\s+memory:\s*['"]?([^'"\n]+)['"]?`
- Resource limits
- Extracts: `cpu_limit`, `memory_limit`
- Example: `cpu: "500m"`, `memory: "512Mi"`

### Service Extraction

**Pattern**: `type:\s*(ClusterIP|NodePort|LoadBalancer|ExternalName)`
- Service type
- Extracts: `service_type`
- Example: `type: LoadBalancer`

**Pattern**: `port:\s*(\d+)`
- Service port
- Extracts: `port`
- Example: `port: 80`

### Ingress Extraction

**Pattern**: `host:\s*['"]?([a-z0-9.-]+\.[a-z]{2,})['"]?`
- Ingress hostname
- Extracts: `hostname`
- Example: `host: app.example.com`

**Pattern**: `kubernetes\.io/ingress\.class:\s*['"]?([a-z0-9-]+)['"]?`
- Ingress class annotation
- Extracts: `ingress_class`
- Example: `kubernetes.io/ingress.class: nginx`

### Helm Chart Extraction

**Pattern**: `^name:\s*['"]?([a-z0-9-]+)['"]?`
- Chart name (from Chart.yaml)
- Extracts: `chart_name`
- Example: `name: my-application`

**Pattern**: `^version:\s*['"]?([0-9]+\.[0-9]+\.[0-9]+[^'"]*)['"]?`
- Chart version (from Chart.yaml)
- Extracts: `chart_version`
- Example: `version: 1.2.3`

**Pattern**: `repository:\s*['"]?(https?://[^'"]+)['"]?`
- Helm repository URL
- Extracts: `helm_repo`
- Example: `repository: https://charts.bitnami.com/bitnami`

### Extraction Output Example

```json
{
  "extractions": {
    "kubernetes_clusters": [
      {
        "type": "eks",
        "cluster_name": "prod-cluster",
        "region": "us-west-2",
        "endpoint": "https://ABC123.us-west-2.eks.amazonaws.com",
        "source_file": ".kube/config"
      }
    ],
    "namespaces": ["default", "production", "staging", "monitoring"],
    "container_images": [
      {
        "registry": "123456789012.dkr.ecr.us-west-2.amazonaws.com",
        "repository": "myapp",
        "tag": "v1.2.3",
        "source_file": "k8s/deployment.yaml",
        "line": 25
      }
    ],
    "ingress_hosts": ["app.example.com", "api.example.com"],
    "helm_charts": [
      {
        "name": "my-application",
        "version": "1.2.3",
        "source_file": "charts/myapp/Chart.yaml"
      }
    ]
  }
}
```
