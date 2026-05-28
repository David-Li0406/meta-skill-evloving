---
id: argocd-gitops
name: "ArgoCD GitOps"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# ArgoCD GitOps

## Overview

ArgoCD is a declarative GitOps continuous delivery tool for Kubernetes. It synchronizes application state from Git repositories to Kubernetes clusters, providing automated deployment, drift detection, and rollback capabilities with a visual UI.

## When to Use

- Kubernetes-native deployments
- GitOps workflows (Git as source of truth)
- Multi-cluster deployments
- Teams requiring deployment visibility
- Progressive delivery with Argo Rollouts

## Key Concepts

| Concept | Description |
|---------|-------------|
| Application | ArgoCD resource defining source and destination |
| Project | Logical grouping of applications with RBAC |
| Repository | Git repo containing Kubernetes manifests |
| Sync | Process of applying Git state to cluster |
| Health | Application health status assessment |
| Refresh | Comparing Git state with cluster state |
| Rollback | Reverting to previous Git commit |

### GitOps Flow

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│    Git     │ ←─→ │   ArgoCD   │ ←─→ │ Kubernetes │
│ Repository │     │  Controller│     │  Cluster   │
└────────────┘     └────────────┘     └────────────┘
      ↑                  │
      │                  ▼
┌────────────┐     ┌────────────┐
│    CI      │     │  Metrics/  │
│  Pipeline  │     │   Alerts   │
└────────────┘     └────────────┘
```

## Implementation

### ArgoCD Installation

```yaml
# argocd-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: argocd
---
# Install with Helm
# helm repo add argo https://argoproj.github.io/argo-helm
# helm install argocd argo/argo-cd -n argocd -f values.yaml
```

### ArgoCD Helm Values

```yaml
# values.yaml
global:
  domain: argocd.example.com

configs:
  cm:
    url: https://argocd.example.com
    admin.enabled: false
    dex.config: |
      connectors:
        - type: github
          id: github
          name: GitHub
          config:
            clientID: $dex.github.clientID
            clientSecret: $dex.github.clientSecret
            orgs:
              - name: myorg

  params:
    server.insecure: false
    application.namespaces: "*"

  rbac:
    policy.csv: |
      p, role:developer, applications, get, */*, allow
      p, role:developer, applications, sync, */staging/*, allow
      p, role:deployer, applications, *, */*, allow
      g, developers, role:developer
      g, deployers, role:deployer

  repositories:
    - url: https://github.com/myorg/kubernetes-manifests
      type: git
    - url: https://charts.example.com
      type: helm
      name: private-charts

  credentialTemplates:
    github-https:
      url: https://github.com/myorg
      password: ${GITHUB_TOKEN}
      username: not-used

server:
  replicas: 2
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5

  ingress:
    enabled: true
    ingressClassName: nginx
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
      nginx.ingress.kubernetes.io/ssl-passthrough: "true"
      nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    hosts:
      - argocd.example.com
    tls:
      - secretName: argocd-tls
        hosts:
          - argocd.example.com

  metrics:
    enabled: true
    serviceMonitor:
      enabled: true

repoServer:
  replicas: 2
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5

controller:
  replicas: 1
  metrics:
    enabled: true
    serviceMonitor:
      enabled: true

applicationSet:
  enabled: true
  replicas: 2

notifications:
  enabled: true
  secret:
    items:
      slack-token: $SLACK_TOKEN
  notifiers:
    service.slack: |
      token: $slack-token
  triggers:
    trigger.on-sync-succeeded: |
      - send: [app-sync-succeeded]
        when: app.status.sync.status == 'Synced'
    trigger.on-sync-failed: |
      - send: [app-sync-failed]
        when: app.status.sync.status == 'OutOfSync' and time.Now().Sub(time.Parse(app.status.operationState.startedAt)).Minutes() > 5
    trigger.on-health-degraded: |
      - send: [app-health-degraded]
        when: app.status.health.status == 'Degraded'
  templates:
    template.app-sync-succeeded: |
      message: |
        Application {{.app.metadata.name}} has been synced successfully.
        Sync Status: {{.app.status.sync.status}}
        Health Status: {{.app.status.health.status}}
      slack:
        attachments: |
          [{
            "color": "good",
            "title": "{{.app.metadata.name}} Synced",
            "fields": [
              {"title": "Sync Status", "value": "{{.app.status.sync.status}}", "short": true},
              {"title": "Repository", "value": "{{.app.spec.source.repoURL}}", "short": true}
            ]
          }]
    template.app-sync-failed: |
      slack:
        attachments: |
          [{
            "color": "danger",
            "title": "{{.app.metadata.name}} Sync Failed",
            "text": "Application sync failed"
          }]
```

### Application Definition

```yaml
# applications/myapp.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: deployments
    notifications.argoproj.io/subscribe.on-sync-failed.slack: deployments
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/kubernetes-manifests
    targetRevision: main
    path: apps/myapp/overlays/production

    # For Helm charts
    # helm:
    #   releaseName: myapp
    #   valueFiles:
    #     - values.yaml
    #     - values-production.yaml
    #   parameters:
    #     - name: image.tag
    #       value: "1.0.0"

    # For Kustomize
    kustomize:
      images:
        - myapp=registry.example.com/myapp:1.0.0

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
      - ServerSideApply=true
      - ApplyOutOfSyncOnly=true
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
    - group: ""
      kind: ConfigMap
      jqPathExpressions:
        - .data["config.json"] | fromjson | del(.generatedAt)

  revisionHistoryLimit: 10
```

### AppProject

```yaml
# projects/team-a.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-a
  namespace: argocd
spec:
  description: Team A applications

  sourceRepos:
    - 'https://github.com/myorg/team-a-*'
    - 'https://charts.example.com'

  destinations:
    - namespace: 'team-a-*'
      server: https://kubernetes.default.svc
    - namespace: 'team-a-*'
      server: https://staging-cluster.example.com

  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
    - group: 'networking.k8s.io'
      kind: Ingress

  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota
    - group: ''
      kind: LimitRange

  roles:
    - name: developer
      description: Developer access
      policies:
        - p, proj:team-a:developer, applications, get, team-a/*, allow
        - p, proj:team-a:developer, applications, sync, team-a/*, allow
      groups:
        - team-a-developers

    - name: admin
      description: Admin access
      policies:
        - p, proj:team-a:admin, applications, *, team-a/*, allow
      groups:
        - team-a-admins

  syncWindows:
    - kind: allow
      schedule: '0 * * * *'
      duration: 1h
      applications:
        - '*'
      namespaces:
        - 'team-a-staging'
    - kind: deny
      schedule: '0 22 * * 5'  # Friday 10pm
      duration: 48h
      applications:
        - '*-production'
```

### ApplicationSet

```yaml
# applicationsets/microservices.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices
  namespace: argocd
spec:
  generators:
    # Matrix generator: environments x services
    - matrix:
        generators:
          - list:
              elements:
                - env: staging
                  cluster: https://staging.k8s.example.com
                  values: values-staging.yaml
                - env: production
                  cluster: https://prod.k8s.example.com
                  values: values-production.yaml
          - git:
              repoURL: https://github.com/myorg/microservices
              revision: HEAD
              directories:
                - path: 'services/*'

  template:
    metadata:
      name: '{{path.basename}}-{{env}}'
      labels:
        app: '{{path.basename}}'
        env: '{{env}}'
    spec:
      project: microservices
      source:
        repoURL: https://github.com/myorg/microservices
        targetRevision: HEAD
        path: '{{path}}'
        helm:
          valueFiles:
            - '{{values}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
---
# Pull Request generator for preview environments
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: preview-environments
  namespace: argocd
spec:
  generators:
    - pullRequest:
        github:
          owner: myorg
          repo: myapp
          tokenRef:
            secretName: github-token
            key: token
        requeueAfterSeconds: 60

  template:
    metadata:
      name: 'preview-{{number}}'
      annotations:
        notifications.argoproj.io/subscribe.on-sync-succeeded.github: ""
    spec:
      project: previews
      source:
        repoURL: 'https://github.com/myorg/myapp'
        targetRevision: '{{head_sha}}'
        path: deploy/preview
        kustomize:
          nameSuffix: '-{{number}}'
          images:
            - 'myapp=ghcr.io/myorg/myapp:pr-{{number}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: 'preview-{{number}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Repository Structure

```
kubernetes-manifests/
├── apps/
│   └── myapp/
│       ├── base/
│       │   ├── kustomization.yaml
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── configmap.yaml
│       └── overlays/
│           ├── staging/
│           │   ├── kustomization.yaml
│           │   └── patch-replicas.yaml
│           └── production/
│               ├── kustomization.yaml
│               ├── patch-replicas.yaml
│               └── patch-resources.yaml
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   └── external-secrets/
└── projects/
    ├── team-a.yaml
    └── team-b.yaml
```

### Kustomize Base

```yaml
# apps/myapp/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app.kubernetes.io/name: myapp
  app.kubernetes.io/managed-by: argocd

images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: latest
```

```yaml
# apps/myapp/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  template:
    metadata:
      labels:
        app.kubernetes.io/name: myapp
    spec:
      containers:
        - name: myapp
          image: myapp
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: myapp-config
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
```

### Production Overlay

```yaml
# apps/myapp/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - ../../base

patches:
  - path: patch-replicas.yaml
  - path: patch-resources.yaml

images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: v1.2.3

configMapGenerator:
  - name: myapp-config
    behavior: merge
    literals:
      - LOG_LEVEL=info
      - ENVIRONMENT=production
```

```yaml
# apps/myapp/overlays/production/patch-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
```

### Sync Waves and Hooks

```yaml
# Hook for database migration
apiVersion: batch/v1
kind: Job
metadata:
  name: myapp-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: migration
          image: registry.example.com/myapp:v1.2.3
          command: ['python', 'manage.py', 'migrate']
      restartPolicy: Never
  backoffLimit: 3
---
# Sync wave ordering
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

## Best Practices

1. **Use ApplicationSets** - Automate application generation for multiple environments
2. **Implement sync waves** - Control deployment order with annotations
3. **Enable auto-sync with self-heal** - Maintain desired state automatically
4. **Use Kustomize overlays** - Manage environment-specific configurations
5. **Configure notifications** - Alert on sync failures and health degradation
6. **Set up RBAC** - Control access with projects and roles
7. **Use sync windows** - Prevent deployments during maintenance
8. **Implement health checks** - Custom health checks for CRDs
9. **Version pin ArgoCD** - Avoid unexpected behavior from upgrades
10. **Separate app configs from source** - Use dedicated GitOps repository

## Common Pitfalls

1. **Storing secrets in Git** - Use external secrets operators (External Secrets, Sealed Secrets).

2. **No sync windows for production** - Uncontrolled deployments during incidents. Set maintenance windows.

3. **Missing ignoreDifferences** - Constant sync due to controller-managed fields. Configure ignore rules.

4. **Overly permissive projects** - Security risk. Scope projects to specific namespaces and repos.

5. **Not using ApplicationSets** - Managing many similar apps manually. Use generators for automation.

6. **No retry policy** - Transient failures stop sync. Configure retry with backoff.

## References

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ApplicationSet Documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/application-set/)
- [GitOps Best Practices](https://www.gitops.tech/)
- [Argo Project](https://argoproj.github.io/)
