---
name: building-gitops-workflows
description: Use this skill to construct GitOps workflows with ArgoCD and Flux, generating production-ready configurations and implementing best practices for Kubernetes deployments.
---

# GitOps Workflows

Git as the single source of truth for declarative infrastructure and applications.

## When to Use

- Creating a new GitOps workflow using ArgoCD or Flux.
- Automating application deployments to a Kubernetes cluster.
- Managing infrastructure changes through Git.
- Setting up ArgoCD or Flux for continuous deployment.
- Designing promotion workflows (dev → staging → prod).

## Core Principles

| Principle | Description |
|-----------|-------------|
| Declarative | Desired state described in Git |
| Versioned | Full history of changes |
| Automated | Changes applied automatically |
| Auditable | Git commits = audit trail |

## Repository Structure

### Monorepo Pattern

```
gitops-repo/
├── apps/
│   ├── base/                    
│   │   └── myapp/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       └── kustomization.yaml
│   └── overlays/
│       ├── development/
│       ├── staging/
│       └── production/
│
├── infrastructure/
│   ├── base/
│   └── overlays/
│
└── clusters/
    ├── development/
    ├── staging/
    └── production/
```

## ArgoCD

### Installation

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Application Definition

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: <repository-url>
    targetRevision: main
    path: apps/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Flux

### Installation

```bash
flux bootstrap github \
  --owner=<owner> \
  --repository=<repository> \
  --branch=main \
  --path=clusters/production \
  --personal
```

### GitRepository Source

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: gitops-repo
  namespace: flux-system
spec:
  interval: 1m
  url: <repository-url>
  ref:
    branch: main
```

### Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  targetNamespace: myapp
  sourceRef:
    kind: GitRepository
    name: gitops-repo
  path: ./apps/overlays/production
  prune: true
```

## Best Practices

1. **Separate app and infra repos** for different change velocities.
2. **Use sealed-secrets or external-secrets** for secrets in Git.
3. **Implement branch protection** on GitOps repos.
4. **Use PR reviews** for production changes.
5. **Set up notifications** for sync failures.
6. **Implement rollback procedures** via Git revert.

## Troubleshooting

```bash
# ArgoCD
argocd app list
argocd app sync myapp

# Flux
flux get all
flux reconcile kustomization myapp
```

## Integration

This skill integrates with:
- Kubernetes manifests
- Infrastructure provisioning
- CI/CD pipelines
- Policy-as-code for pre-commit validation