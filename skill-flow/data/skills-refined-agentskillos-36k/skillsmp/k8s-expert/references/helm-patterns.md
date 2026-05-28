# Helm Patterns & Best Practices

## Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── NOTES.txt       # Post-install notes
└── charts/             # Dependencies
```

## Values Management

### Environment-Specific Values

```bash
# Base values + environment overlay
helm upgrade myapp ./chart \
  -f values.yaml \
  -f values-prod.yaml \
  -n prod

# Structure
values.yaml          # defaults
values-dev.yaml      # dev overrides
values-staging.yaml  # staging overrides
values-prod.yaml     # prod overrides
```

### Value Precedence

```bash
# Later values override earlier (left to right)
helm install myapp ./chart \
  -f base.yaml \
  -f env.yaml \
  --set image.tag=v1.2.3

# Precedence: defaults < base.yaml < env.yaml < --set
```

## Template Patterns

### Conditional Resources

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
# ...
{{- end }}
```

### Default Values

```yaml
replicas: {{ .Values.replicas | default 1 }}
resources:
  {{- toYaml (.Values.resources | default dict) | nindent 2 }}
```

### Labels and Selectors

```yaml
# _helpers.tpl
{{- define "mychart.labels" -}}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

# deployment.yaml
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

### ConfigMap from Files

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}-config
data:
  {{- (.Files.Glob "config/*").AsConfig | nindent 2 }}
```

## ArgoCD + Helm

### Helm Chart via ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  source:
    repoURL: https://charts.example.com
    chart: mychart
    targetRevision: 1.2.3
    helm:
      releaseName: myapp
      valueFiles:
        - values-prod.yaml
      values: |
        replicas: 3
        image:
          tag: v1.0.0
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

### Git Repo with Helm Chart

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: charts/myapp
    helm:
      valueFiles:
        - ../../environments/prod/values.yaml
```

## Dependency Management

### Chart.yaml Dependencies

```yaml
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

### Update Dependencies

```bash
helm dependency update ./mychart
helm dependency build ./mychart
```

## Debugging Helm

### Template Rendering

```bash
# Render without installing
helm template myrelease ./chart -f values.yaml

# Render specific template
helm template myrelease ./chart -s templates/deployment.yaml

# With debug output
helm template myrelease ./chart --debug
```

### Dry Run

```bash
# Server-side dry run (validates against cluster)
helm install myrelease ./chart --dry-run --debug

# Client-side only
helm template myrelease ./chart
```

### Get Rendered Manifests

```bash
# From installed release
helm get manifest myrelease -n namespace

# Compare with chart
helm template myrelease ./chart | diff - <(helm get manifest myrelease -n namespace)
```

## Upgrade Strategies

### Safe Upgrade Pattern

```bash
# 1. Diff first
helm diff upgrade myrelease ./chart -f values.yaml -n namespace

# 2. Dry run
helm upgrade myrelease ./chart -f values.yaml -n namespace --dry-run

# 3. Actual upgrade
helm upgrade myrelease ./chart -f values.yaml -n namespace

# 4. Verify
helm status myrelease -n namespace
kubectl rollout status deployment/myrelease -n namespace
```

### Rollback

```bash
# Check history
helm history myrelease -n namespace

# Rollback to previous
helm rollback myrelease -n namespace

# Rollback to specific revision
helm rollback myrelease 3 -n namespace
```

## Hooks

### Common Hook Types

```yaml
metadata:
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
```

Hook types:
- `pre-install` - Before resources created
- `post-install` - After resources created
- `pre-upgrade` - Before upgrade
- `post-upgrade` - After upgrade
- `pre-delete` - Before deletion
- `post-delete` - After deletion

### Database Migration Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-migrate
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-1"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
          command: ["./migrate.sh"]
      restartPolicy: Never
```

## Testing

### Helm Test

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "mychart.fullname" . }}-test"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "mychart.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

```bash
helm test myrelease -n namespace
```
