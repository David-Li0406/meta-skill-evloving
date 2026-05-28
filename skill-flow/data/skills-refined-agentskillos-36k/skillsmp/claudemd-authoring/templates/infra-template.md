# Infrastructure CLAUDE.md Template

Use this template for Kubernetes, ArgoCD, Helm, and other infrastructure projects.

---

```markdown
# [Project Name]

## Quick Reference

\`\`\`bash
# Cluster management
kubectl get nodes
kubectl get pods -A

# Health check
./scripts/verify-cluster.sh

# Common operations
kubectl logs -f deployment/[name] -n [namespace]
kubectl exec -it deployment/[name] -n [namespace] -- /bin/sh
\`\`\`

---

## 1. Cluster Architecture

### 1.1 Node Configuration

| Node | IP | Role | Resources |
|------|----|------|-----------|
| [node-1] | [IP] | Control Plane | [cores]/[RAM] |
| [node-2] | [IP] | Worker | [cores]/[RAM] |

### 1.2 Network Architecture

| Component | Configuration |
|-----------|---------------|
| Ingress | [Controller] ([IP]) |
| DNS | [Provider] ([IP]) |
| Domain | `*.[domain]` |
| LoadBalancer Pool | [IP range] |

### 1.3 Storage Architecture

| StorageClass | Provisioner | Use Case |
|--------------|-------------|----------|
| `local-path` | rancher | Node-local data |
| `nfs-client` | NFS | Shared/persistent data |

---

## 2. Service Catalog

### 2.1 Service Access

| Service | URL | Notes |
|---------|-----|-------|
| [Service 1] | https://[host] | [Description] |
| [Service 2] | https://[host] | [Description] |

### 2.2 ArgoCD Applications

| Application | Namespace | Chart |
|-------------|-----------|-------|
| [app-1] | [ns] | [chart-name] |
| [app-2] | [ns] | [chart-name] |

---

## 3. GitOps Workflow

### 3.1 Repository Structure

\`\`\`
[repo-name]/
├── argocd/
│   ├── root-app.yaml
│   └── apps/           # Application definitions
├── helm/               # Local charts
├── manifests/          # Raw K8s manifests
└── scripts/            # Utilities
\`\`\`

### 3.2 Deployment Process

1. Edit configuration in `argocd/apps/[service].yaml`
2. Commit and push changes
3. ArgoCD auto-syncs (or manual sync)

---

## 4. Monitoring

### 4.1 Access

| Tool | URL |
|------|-----|
| Grafana | https://grafana.[domain] |
| Prometheus | [internal only] |

### 4.2 Key Dashboards

- [Dashboard 1]: [Purpose]
- [Dashboard 2]: [Purpose]

---

## 5. Security

### 5.1 Secrets Management

Use SealedSecrets for all sensitive data:

\`\`\`bash
kubectl create secret generic [name] --namespace=[ns] \\
  --from-literal=key="value" \\
  --dry-run=client -o yaml | \\
  kubeseal --controller-name=sealed-secrets-controller \\
  --controller-namespace=kube-system -o yaml > manifests/[path].yaml
\`\`\`

### 5.2 Certificates

[Certificate management approach - cert-manager, manual, etc.]

---

## 6. User Preferences

- kubectl alias: `[alias]`
- Cluster UI: [k9s, lens, etc.]
- Documentation: [Notion, wiki, etc.]
```

---

## Customization Notes

- Remove sections not applicable to the project
- Add project-specific sections as needed
- Keep Quick Reference focused on daily commands
- Update Service Catalog when services change
