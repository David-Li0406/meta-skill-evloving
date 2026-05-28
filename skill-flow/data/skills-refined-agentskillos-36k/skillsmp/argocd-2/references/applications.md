# ArgoCD Applications

## Application Structure

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io  # Cascade delete resources
spec:
  project: default  # AppProject name

  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD  # Branch, tag, or commit SHA
    path: manifests  # Path within repo

  destination:
    server: https://kubernetes.default.svc  # Or use 'name: cluster-name'
    namespace: myapp

  syncPolicy:
    automated:
      prune: true      # Delete resources removed from Git
      selfHeal: true   # Revert manual changes
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

## Source Configuration

### Multiple Sources
```yaml
spec:
  sources:
    - repoURL: https://github.com/org/repo.git
      targetRevision: HEAD
      path: base
    - repoURL: https://github.com/org/config.git
      targetRevision: main
      path: overlays/prod
```

### Directory Source
```yaml
source:
  path: manifests
  directory:
    recurse: true
    include: '*.yaml'
    exclude: 'test-*'
```

## CLI Commands

```bash
# Create application
argocd app create myapp \
  --repo https://github.com/org/repo.git \
  --path manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace myapp \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# Sync operations
argocd app sync myapp
argocd app sync myapp --prune
argocd app sync myapp --force
argocd app sync myapp --resource apps:Deployment:myapp

# Status and info
argocd app get myapp
argocd app list
argocd app history myapp
argocd app diff myapp

# Rollback
argocd app rollback myapp <history-id>

# Delete
argocd app delete myapp
argocd app delete myapp --cascade=false  # Keep resources
```

## App of Apps Pattern

Parent application managing child applications:

```yaml
# apps/Chart.yaml (parent)
apiVersion: v2
name: root-app
version: 1.0.0
```

```yaml
# apps/templates/child-app.yaml
{{- range $app := .Values.applications }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ $app.name }}
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: {{ $app.repoURL }}
    targetRevision: {{ $app.targetRevision | default "HEAD" }}
    path: {{ $app.path }}
  destination:
    server: https://kubernetes.default.svc
    namespace: {{ $app.namespace }}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
{{- end }}
```

```yaml
# apps/values.yaml
applications:
  - name: frontend
    repoURL: https://github.com/org/frontend.git
    path: k8s
    namespace: frontend
  - name: backend
    repoURL: https://github.com/org/backend.git
    path: k8s
    namespace: backend
```

## Ignore Differences

```yaml
spec:
  ignoreDifferences:
    # By JSON pointer
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
        - /metadata/annotations

    # By JQ expression
    - group: ""
      kind: ConfigMap
      jqPathExpressions:
        - '.data["config.yaml"]'

    # By managed fields manager
    - group: "*"
      kind: "*"
      managedFieldsManagers:
        - kube-controller-manager
```

## Info Annotations

```yaml
spec:
  info:
    - name: Documentation
      value: https://docs.example.com
    - name: Owner
      value: platform-team
```

## Revision History

```yaml
spec:
  revisionHistoryLimit: 10  # Default is 10
```
