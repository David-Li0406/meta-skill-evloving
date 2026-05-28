# ArgoCD Kustomize Integration

ArgoCD auto-detects Kustomize when `kustomization.yaml` exists in path.

## Basic Kustomize Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

## Kustomize Configuration

```yaml
spec:
  source:
    path: overlays/prod
    kustomize:
      # Name transformations
      namePrefix: prod-
      nameSuffix: -v1

      # Common metadata
      commonLabels:
        env: production
      commonAnnotations:
        owner: platform-team

      # Namespace override
      namespace: production

      # Image overrides
      images:
        - name: myapp
          newName: registry.example.com/myapp
          newTag: v1.2.3
        - name: nginx
          newTag: "1.25"

      # Replica overrides
      replicas:
        - name: myapp
          count: 5

      # Kustomize version
      version: v5.0.0
```

## Inline Patches

```yaml
spec:
  source:
    kustomize:
      patches:
        # Strategic merge patch
        - target:
            kind: Deployment
            name: myapp
          patch: |-
            - op: replace
              path: /spec/replicas
              value: 3

        # JSON patch
        - target:
            kind: ConfigMap
            name: myconfig
          patch: |-
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: myconfig
            data:
              key: newvalue
```

## Components

```yaml
spec:
  source:
    kustomize:
      components:
        - components/monitoring
        - components/logging
```

## Environment Variable Substitution

Enable in ArgoCD ConfigMap:
```yaml
# argocd-cm ConfigMap
data:
  kustomize.buildOptions: --enable-alpha-plugins
```

Then use in annotations:
```yaml
spec:
  source:
    kustomize:
      commonAnnotationsEnvsubst: true
      commonAnnotations:
        app-name: ${ARGOCD_APP_NAME}
        revision: ${ARGOCD_APP_REVISION}
```

Available variables: `ARGOCD_APP_NAME`, `ARGOCD_APP_NAMESPACE`, `ARGOCD_APP_REVISION`, `ARGOCD_APP_SOURCE_PATH`, `ARGOCD_APP_SOURCE_REPO_URL`, `ARGOCD_APP_SOURCE_TARGET_REVISION`

## Helm in Kustomize

Enable Helm chart inflation:

```yaml
# argocd-cm ConfigMap
data:
  kustomize.buildOptions: --enable-helm
```

Then use helmCharts in kustomization.yaml:
```yaml
# kustomization.yaml
helmCharts:
  - name: nginx
    repo: https://charts.bitnami.com/bitnami
    version: 15.1.0
    valuesFile: values.yaml
```

## Multiple Kustomize Versions

```yaml
# argocd-cm ConfigMap
data:
  kustomize.path.v5.0.0: /custom/path/kustomize5
  kustomize.path.v4.5.0: /custom/path/kustomize4
```

Reference in application:
```yaml
spec:
  source:
    kustomize:
      version: v5.0.0
```

## Private Remote Bases

Kustomize can reference remote bases. ArgoCD passes repo credentials automatically:

```yaml
# kustomization.yaml
resources:
  - https://github.com/org/private-base//manifests?ref=v1.0.0
```

Ensure repository credentials are configured in ArgoCD.

## CLI Commands

```bash
# Create Kustomize app
argocd app create myapp \
  --repo https://github.com/org/repo.git \
  --path overlays/production \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace myapp

# Override Kustomize settings
argocd app set myapp --kustomize-image myapp=registry.example.com/myapp:v2
argocd app set myapp --kustomize-common-label env=staging
argocd app set myapp --nameprefix staging-

# Show rendered manifests
argocd app manifests myapp
```

## Directory Structure Example

```
repo/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patch-replicas.yaml
    └── production/
        ├── kustomization.yaml
        ├── patch-replicas.yaml
        └── patch-resources.yaml
```
