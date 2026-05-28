# Kubernetes

**Category**: cncf
**Description**: Container orchestration platform for automating deployment, scaling, and management
**Homepage**: https://kubernetes.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Kubernetes Go packages*

- `k8s.io/client-go` - Official Go client
- `k8s.io/api` - API types
- `k8s.io/apimachinery` - API machinery
- `k8s.io/kubectl` - kubectl library
- `k8s.io/kubernetes` - Kubernetes core
- `sigs.k8s.io/controller-runtime` - Controller runtime
- `sigs.k8s.io/kustomize` - Kustomize library

#### NPM
*Kubernetes Node.js packages*

- `@kubernetes/client-node` - Official Node.js client
- `kubernetes-client` - Alternative client
- `k8s` - Simple client

#### PYPI
*Kubernetes Python packages*

- `kubernetes` - Official Python client
- `kubernetes-asyncio` - Async Python client
- `kopf` - Kubernetes Operator Framework
- `kr8s` - Async Kubernetes client
- `pykube-ng` - Python Kubernetes client

#### MAVEN
*Kubernetes Java packages*

- `io.kubernetes:client-java` - Official Java client
- `io.fabric8:kubernetes-client` - Fabric8 client
- `io.fabric8:kubernetes-model` - Kubernetes models

#### NUGET
*Kubernetes .NET packages*

- `KubernetesClient` - Official .NET client
- `k8s` - .NET client

#### RUBYGEMS
*Kubernetes Ruby packages*

- `kubeclient` - Ruby client
- `kubernetes-client` - Alternative Ruby client

#### CARGO
*Kubernetes Rust packages*

- `kube` - Rust client
- `kube-runtime` - Runtime utilities
- `k8s-openapi` - OpenAPI types

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Kubernetes usage*

- `kubeconfig` - Kubernetes config
- `.kube/config` - Default kubeconfig
- `kustomization.yaml` - Kustomize configuration
- `kustomization.yml` - Alternative extension
- `skaffold.yaml` - Skaffold config
- `tilt.yaml` - Tilt config
- `Tiltfile` - Tilt configuration
- `k8s.yaml` - Generic K8s manifest
- `kubernetes.yaml` - Generic K8s manifest

### Configuration Directories
*Known directories that indicate Kubernetes usage*

- `k8s/` - Kubernetes manifests
- `kubernetes/` - Kubernetes manifests
- `deploy/` - Deployment manifests
- `manifests/` - K8s manifests
- `overlays/` - Kustomize overlays
- `base/` - Kustomize base

### Import Patterns

#### Go
Extensions: `.go`

**Pattern**: `"k8s\.io/client-go`
- Kubernetes client-go import
- Example: `import "k8s.io/client-go/kubernetes"`

**Pattern**: `"sigs\.k8s\.io/controller-runtime`
- Controller runtime import
- Example: `import "sigs.k8s.io/controller-runtime"`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+kubernetes\s+import|^import\s+kubernetes`
- Kubernetes Python client import
- Example: `from kubernetes import client, config`

**Pattern**: `^import\s+kopf`
- Kopf operator framework import
- Example: `import kopf`

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@kubernetes/client-node['"]`
- Kubernetes Node client import
- Example: `import { KubeConfig } from '@kubernetes/client-node'`

### Code Patterns

**Pattern**: `apiVersion:\s*[a-z]+/v[0-9]+|apiVersion:\s*v[0-9]+`
- Kubernetes API version
- Example: `apiVersion: apps/v1`

**Pattern**: `kind:\s*(Deployment|Service|Pod|ConfigMap|Secret|Ingress|StatefulSet|DaemonSet|Job|CronJob)`
- Kubernetes resource kinds
- Example: `kind: Deployment`

**Pattern**: `kubectl\s+(apply|create|get|delete|describe|logs|exec|port-forward)`
- kubectl commands
- Example: `kubectl apply -f deployment.yaml`

**Pattern**: `metadata:\s*\n\s*name:|spec:\s*\n\s*replicas:`
- Kubernetes manifest structure
- Example: `metadata:\n  name: my-app`

**Pattern**: `KUBECONFIG|KUBERNETES_SERVICE_HOST`
- Kubernetes environment variables
- Example: `KUBECONFIG=/path/to/config`

**Pattern**: `\.svc\.cluster\.local|kubernetes\.default\.svc`
- Kubernetes DNS names
- Example: `my-service.default.svc.cluster.local`

**Pattern**: `imagePullPolicy:|containerPort:|volumeMounts:`
- Kubernetes spec fields
- Example: `imagePullPolicy: Always`

---

## Environment Variables

- `KUBECONFIG` - Path to kubeconfig file
- `KUBERNETES_SERVICE_HOST` - In-cluster API host
- `KUBERNETES_SERVICE_PORT` - In-cluster API port
- `KUBE_NAMESPACE` - Default namespace
- `KUBE_CONTEXT` - Kubernetes context
- `KUBE_CLUSTER` - Cluster name

## Detection Notes

- Look for .yaml/.yml files with apiVersion and kind fields
- kustomization.yaml indicates Kustomize usage
- Dockerfile with kubectl indicates K8s deployment
- Common ports: 6443 (API server), 10250 (kubelet)
- ServiceAccount tokens in /var/run/secrets/kubernetes.io

---

## Secrets Detection

### Credentials

#### Kubernetes Token
**Pattern**: `bearer_token:\s*['"]?([A-Za-z0-9\-_\.]{20,})['"]?`
**Severity**: critical
**Description**: Kubernetes bearer token in kubeconfig
**Example**: `bearer_token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...`

#### Kubernetes Client Certificate
**Pattern**: `client-certificate-data:\s*([A-Za-z0-9+/=]+)`
**Severity**: critical
**Description**: Base64 encoded client certificate

#### Kubernetes Client Key
**Pattern**: `client-key-data:\s*([A-Za-z0-9+/=]+)`
**Severity**: critical
**Description**: Base64 encoded client private key

---

## TIER 3: Configuration Extraction

### Namespace Extraction

**Pattern**: `namespace:\s*['"]?([a-z0-9][a-z0-9-]*)['"]?`
- Kubernetes namespace
- Extracts: `namespace`
- Example: `namespace: production`

### Image Extraction

**Pattern**: `image:\s*['"]?([a-zA-Z0-9._\-/:]+)['"]?`
- Container image reference
- Extracts: `container_image`
- Example: `image: nginx:1.21`

### Replicas Extraction

**Pattern**: `replicas:\s*([0-9]+)`
- Deployment replicas
- Extracts: `replicas`
- Example: `replicas: 3`
