# GitOps Patterns and Best Practices

GitOps is a declarative approach to continuous deployment where Git repositories serve as the source of truth for infrastructure and application configurations.

## GitOps Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Git Repo  │───▶│   ArgoCD    │───▶│  Kubernetes │
│  (Source)   │    │  (Sync)     │    │  (Target)   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │
       │    Reconciliation Loop
       │                  │
       └──────────────────┘
```

## Core Principles

1. **Declarative**: Desired state is described declaratively
2. **Versioned**: All configuration is stored in Git
3. **Automated**: Changes are automatically applied
4. **Auditable**: Git history provides audit trail

## ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/manifests
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true      # Remove resources not in Git
      selfHeal: true   # Revert manual changes
    syncOptions:
      - CreateNamespace=true
```

## ArgoCD ApplicationSet

For managing multiple similar applications:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-set
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - env: dev
        namespace: myapp-dev
      - env: staging
        namespace: myapp-staging
      - env: prod
        namespace: myapp-prod
  template:
    metadata:
      name: 'myapp-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/manifests
        targetRevision: HEAD
        path: 'apps/myapp/overlays/{{env}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Flux CD Configuration

Alternative to ArgoCD:

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/manifests
  ref:
    branch: main
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./apps/myapp
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: myapp
      namespace: myapp
```

## Repository Structure

Recommended GitOps repository layout:

```
manifests/
├── apps/
│   ├── myapp/
│   │   ├── base/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       │   ├── kustomization.yaml
│   │       │   └── patches/
│   │       ├── staging/
│   │       └── prod/
│   └── another-app/
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   └── monitoring/
└── clusters/
    ├── dev/
    ├── staging/
    └── prod/
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Separate repos | Keep app code and manifests in separate repos |
| Environment branches | Use branches or directories for environments |
| Sealed secrets | Never commit plain secrets |
| PR-based changes | All changes through pull requests |
| Automated sync | Let GitOps operator handle deploys |
| Health checks | Define application health criteria |
| Rollback strategy | Know how to revert via Git |

## Common Patterns

### Image Update Automation

```yaml
# Flux Image Update Automation
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  sourceRef:
    kind: GitRepository
    name: myapp
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: flux@example.com
        name: Flux
      messageTemplate: 'Update image to {{range .Updated.Images}}{{println .}}{{end}}'
    push:
      branch: main
  update:
    path: ./apps/myapp
    strategy: Setters
```

### Progressive Delivery with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 5m}
      - setWeight: 40
      - pause: {duration: 5m}
      - setWeight: 60
      - pause: {duration: 5m}
      - setWeight: 80
      - pause: {duration: 5m}
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1.2.3
```
