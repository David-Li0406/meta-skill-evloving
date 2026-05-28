---
name: k8s-service
description: Add a new service to the k3s Kubernetes cluster. Use when the user wants to deploy an application to Kubernetes, add a new app to k8s, create a HelmRelease, set up an IngressRoute, or configure Homepage discovery for a service.
---

# Add Service to k3s Skill

Deploy applications to the k3s cluster using FluxCD and Helm charts.

## Directory Structure

Create a new directory for the app at `k8s/apps/<app-name>/`:

```
k8s/apps/<app-name>/
├── kustomization.yaml   # Lists all files to apply
├── namespace.yaml       # Isolated namespace for the app
├── helmrelease.yaml     # Helm chart deployment (recommended)
├── ingressroute.yaml    # Traefik routing (for HTTP services)
└── pvc.yaml             # Persistent storage (if not managed by chart)
```

## Reference Examples

Use existing deployments in `k8s/apps/` as templates:

| Example | Good for |
|---------|----------|
| `chromadb/` | Simple Helm chart with persistence |
| `open-webui/` | Helm chart connecting to external services |
| `homepage/` | Service with Homepage widget configuration |
| `immich/` | Complex app with multiple components |
| `forgejo/` | App with SOPS-encrypted secrets |
| `attic/` | Raw manifests (no Helm chart available) |

## Step-by-Step Process

### 1. Find and Evaluate a Helm Chart

Search for charts at:
- [ArtifactHub](https://artifacthub.io/) - Main Helm chart registry
- GitHub repos of the project

**Before using a chart, verify it's actively maintained:**

1. Check the chart's GitHub repo for:
   - Last commit date (should be within 6 months)
   - Open issues/PRs being addressed
   - Regular releases

2. Compare chart version to upstream app version:
   - Find the latest release of the application (e.g., on GitHub releases)
   - Check if the chart's `appVersion` matches or is close to latest
   - A chart several major versions behind is a red flag

3. Check ArtifactHub metrics:
   - Stars and downloads indicate community trust
   - "Verified Publisher" badge is a good sign
   - Security scan results (no critical vulnerabilities)

**When to use raw manifests instead:**

- Chart is abandoned (no updates in 1+ year)
- Chart is multiple major versions behind upstream
- Chart has unresolved critical security issues
- App is simple (single container, minimal config)
- Official project only provides manifests, not a chart

See `k8s/apps/attic/` for a raw manifest example.

### 2. Add HelmRepository (if new source)

Add to `k8s/infrastructure/sources/helm-repos.yaml`:

```yaml
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: chart-repo-name
  namespace: flux-system
spec:
  interval: 1h
  url: https://charts.example.com
```

### 3. Create App Files

Copy and modify from a similar existing app in `k8s/apps/`:
1. `namespace.yaml` - Always needed
2. `helmrelease.yaml` - Configure chart values (or `deployment.yaml` for raw manifests)
3. `ingressroute.yaml` - If HTTP service needs hostname access
4. `kustomization.yaml` - List all resources

### 4. Register with FluxCD

Add the app to `k8s/apps/kustomization.yaml`:

```yaml
resources:
  - existing-app
  - new-app    # Add this line
```

### 5. Git Add and Deploy

**CRITICAL**: Nix flakes and FluxCD only see git-tracked files!

```bash
git add k8s/apps/<app-name>/
git commit -m "feat(k8s): add <app-name> deployment"
git push
```

FluxCD auto-applies, or manually trigger:
```bash
ssh root@boromir.lan "flux reconcile kustomization apps --with-source"
```

### 6. Add DNS Rewrite (for HTTP services)

Add to `modules/nixos/server/adguard.nix` under `filtering.rewrites`:

```nix
{
  domain = "<app-name>.lan";
  answer = "192.168.1.52";  # Traefik LoadBalancer IP
}
```

Then deploy:
```bash
deploy .#theoden && deploy .#boromir && deploy .#samwise
```

### 7. Verify Deployment

```bash
# Check HelmRelease status
ssh root@boromir.lan "kubectl get helmrelease -n <app-name>"

# Check pod status
ssh root@boromir.lan "kubectl get pods -n <app-name>"

# Check services (important for IngressRoute!)
ssh root@boromir.lan "kubectl get svc -n <app-name>"
```

## Critical Gotchas

1. **Git add new files** - FluxCD only sees tracked files
2. **Namespace everywhere** - Include `namespace: <app-name>` in every resource
3. **MetalLB IPs** - Pick unused IPs from pool (192.168.1.50-59)
4. **Helm service names** - Charts create their own service names; verify with `kubectl get svc`
5. **Helm service ports** - Charts often use different ports than expected
6. **accessModes array** - PVC accessModes must be arrays: `[ReadWriteOnce]`
7. **Both entrypoints** - Always include both `web` and `websecure` in IngressRoute (Traefik redirects HTTP to HTTPS)
8. **MetalLB annotation only** - Don't use both `loadBalancerIP` field AND annotation
9. **DNS cache** - After adding rewrites: `resolvectl flush-caches`
10. **Flux reverts manual changes** - Always commit to Git first

## Homepage Auto-Discovery

Homepage automatically discovers k8s services via Traefik IngressRoute annotations - no manual Homepage config needed. Just add these annotations to your IngressRoute:

```yaml
metadata:
  annotations:
    gethomepage.dev/enabled: "true"
    gethomepage.dev/name: "App Name"
    gethomepage.dev/group: "Infrastructure"  # or Media, AI, etc.
    gethomepage.dev/icon: "app-icon.png"
    gethomepage.dev/description: "Short description"
    gethomepage.dev/href: "https://app-name.lan"
    gethomepage.dev/pod-selector: "app.kubernetes.io/name=app-name"
    gethomepage.dev/siteMonitor: "http://service-name.app-name.svc:port"
```

For widget support, see `k8s/apps/immich/ingressroute.yaml` as an example.

## Storage Recommendations

| App Type | Storage |
|----------|---------|
| Stateless / config-driven | ConfigMap |
| Media (Jellyfin, Plex) | NFS |
| Databases | Longhorn or local-path |
| General stateful apps | Longhorn (preferred) or NFS |

## Quick Reference

| Want to... | Use |
|------------|-----|
| Deploy an app | HelmRelease (preferred) or Deployment |
| Expose via hostname | IngressRoute |
| Expose with dedicated IP | Service (LoadBalancer) + MetalLB |
| Store config | Chart values or ConfigMap |
| Store secrets | Secret (SOPS-encrypted) |
| Persist data (replicated) | PVC with Longhorn |
| Persist data (single node) | PVC with local-path |
| Persist data (shared) | NFS from faramir |

## Useful Commands

```bash
# Force Flux reconcile
ssh root@boromir.lan "flux reconcile kustomization apps --with-source"

# Check HelmRelease errors
ssh root@boromir.lan "kubectl describe helmrelease -n <app-name> <app-name>"

# Check logs
ssh root@boromir.lan "kubectl logs -n <app-name> -l app.kubernetes.io/name=<app-name>"

# Restart deployment
ssh root@boromir.lan "kubectl rollout restart deployment -n <app-name>"
```
