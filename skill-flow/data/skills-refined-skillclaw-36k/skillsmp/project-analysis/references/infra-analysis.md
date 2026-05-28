# Infrastructure Project Analysis

Detailed patterns for analyzing Kubernetes, ArgoCD, Helm, and other infrastructure projects.

## Kubernetes Analysis

### Core Resources to Catalog

| Resource Type | What to Extract |
|---------------|-----------------|
| Namespaces | Names, purpose, resource quotas |
| Deployments | Name, replicas, image, resources |
| Services | Type (ClusterIP/LoadBalancer/NodePort), ports |
| Ingress | Hosts, paths, TLS configuration |
| ConfigMaps | Names, key purposes |
| Secrets | Names (not values!), types |
| PersistentVolumeClaims | Storage class, size, access modes |

### Extraction Patterns

```bash
# Find all namespaces
grep -r "kind: Namespace" --include="*.yaml"

# Find services with LoadBalancer
grep -r "type: LoadBalancer" --include="*.yaml" -B 10

# Find ingress hosts
grep -r "host:" --include="*.yaml" -A 1 -B 5
```

## ArgoCD Analysis

### Application Structure

Extract from ArgoCD Application manifests:
- Application name and namespace
- Source repository and path
- Target namespace
- Sync policy (automated/manual)
- Helm values (if using Helm)

### Key Patterns

```yaml
# Look for these fields
spec.source.repoURL      # Git repository
spec.source.path         # Application path
spec.source.chart        # Helm chart name
spec.destination.namespace
spec.syncPolicy.automated
```

## Helm Analysis

### Chart Structure

```
chart-name/
├── Chart.yaml      # Name, version, dependencies
├── values.yaml     # Default configuration
├── templates/      # Kubernetes manifests
└── charts/         # Subcharts
```

### Values to Document

From `values.yaml`:
- Image configuration (repository, tag)
- Resource limits/requests
- Replica counts
- Service configuration
- Ingress settings
- Environment variables

## Node Architecture

For clusters, document:
- Node names and roles (control-plane, worker, GPU)
- Node selectors used in deployments
- Taints and tolerations
- Resource capacity per node

## Storage Architecture

Document:
- StorageClasses available
- Default storage class
- PV reclaim policies
- NFS/local-path configurations

## Network Architecture

Document:
- Ingress controller (Traefik, nginx, etc.)
- LoadBalancer provider (MetalLB, cloud)
- DNS configuration
- Certificate management (cert-manager)
