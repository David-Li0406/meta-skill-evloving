# YAML/Helm Standards Catalog - Vibe Canonical Reference

**Version:** 1.0.0
**Last Updated:** 2026-01-21
**Purpose:** Canonical YAML/Helm standards for vibe skill validation

---

## Table of Contents

1. [yamllint Configuration](#yamllint-configuration)
2. [Formatting Rules](#formatting-rules)
3. [Helm Chart Conventions](#helm-chart-conventions)
4. [Kustomize Patterns](#kustomize-patterns)
5. [Template Best Practices](#template-best-practices)
6. [Validation Workflow](#validation-workflow)
7. [Compliance Assessment](#compliance-assessment)

---

## yamllint Configuration

### Full Configuration

```yaml
# .yamllint.yml
extends: default
rules:
  line-length:
    max: 120
    allow-non-breakable-inline-mappings: true
  indentation:
    spaces: 2
    indent-sequences: consistent
  truthy:
    check-keys: false
  comments:
    min-spaces-from-content: 1
  document-start: disable
  empty-lines:
    max: 2
  brackets:
    min-spaces-inside: 0
    max-spaces-inside: 0
  colons:
    max-spaces-before: 0
    max-spaces-after: 1
  commas:
    max-spaces-before: 0
    min-spaces-after: 1
  hyphens:
    max-spaces-after: 1
```

### Usage

```bash
# Lint all YAML files
yamllint .

# Lint specific directory
yamllint apps/

# Lint with format output
yamllint -f parsable .
```

---

## Formatting Rules

### Quoting Strings

```yaml
# Quote strings that look like other types
enabled: "true"      # String, not boolean
port: "8080"         # String, not integer
version: "1.0"       # String, not float

# No quotes for actual typed values
enabled: true        # Boolean
port: 8080           # Integer
replicas: 3          # Integer
```

### Multi-line Strings

```yaml
# Literal block scalar (preserves newlines)
script: |
  #!/bin/bash
  set -euo pipefail
  echo "Hello"

# Folded block scalar (folds newlines to spaces)
description: >
  This is a long description that will be
  folded into a single line with spaces.

# BAD - Escaped newlines (hard to read)
script: "#!/bin/bash\nset -euo pipefail\necho \"Hello\""
```

### Comments

```yaml
# Section header (full line)
# =============================================================================
# Database Configuration
# =============================================================================

database:
  host: localhost      # Inline comment (1 space before #)
  port: 5432
  # Subsection comment
  credentials:
    username: admin
```

---

## Helm Chart Conventions

### Chart Structure

```text
charts/<chart-name>/
├── Chart.yaml
├── values.yaml
├── values.schema.json    # Optional: JSON Schema for values
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...
└── charts/               # Nested charts (if needed)
```

### Chart.yaml

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for my application
type: application
version: 1.0.0
appVersion: "2.0.0"

dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

### values.yaml Conventions

```yaml
# =============================================================================
# Application Configuration
# =============================================================================

app:
  name: my-app
  replicas: 3

# Resource limits (adjust for environment)
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

# =============================================================================
# Image Configuration
# =============================================================================

image:
  repository: myregistry/my-app
  tag: ""  # Defaults to appVersion
  pullPolicy: IfNotPresent
```

### Validation Commands

```bash
# Lint chart
helm lint charts/<chart-name>/

# Template with values (dry-run)
helm template <release> charts/<chart-name>/ -f values.yaml

# Validate rendered output
helm template <release> charts/<chart-name>/ | kubectl apply --dry-run=client -f -

# Debug template rendering
helm template <release> charts/<chart-name>/ --debug
```

---

## Kustomize Patterns

### Overlay Structure

```text
apps/<app>/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

### kustomization.yaml Template

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml

# Environment-specific patches
patches:
  - path: ./patches/replicas.yaml
    target:
      kind: Deployment
      name: my-app
```

### Patch Types

**Strategic Merge Patch:**
```yaml
# patches/extend-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: my-role
rules:
  - apiGroups: ["custom.io"]
    resources: ["widgets"]
    verbs: ["get", "list"]
```

**JSON Patch:**
```yaml
# patches/add-annotation.yaml
- op: add
  path: /metadata/annotations/custom.io~1managed
  value: "true"
```

**Delete Patch:**
```yaml
# patches/delete-resource.yaml
$patch: delete
apiVersion: v1
kind: ConfigMap
metadata:
  name: unused-config
```

---

## Template Best Practices

### Use include for Reusable Snippets

```yaml
# templates/_helpers.tpl
{{- define "app.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}

# templates/deployment.yaml
metadata:
  labels:
    {{- include "app.labels" . | nindent 4 }}
```

### Whitespace Control

```yaml
# GOOD - Use {{- and -}} to control whitespace
{{- if .Values.enabled }}
apiVersion: v1
kind: ConfigMap
{{- end }}

# BAD - Extra blank lines in output
{{ if .Values.enabled }}

apiVersion: v1

{{ end }}
```

### Required Values

```yaml
# Fail fast if required value missing
image: {{ required "image.repository is required" .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
```

### Default Values

```yaml
# Safe defaults
replicas: {{ .Values.replicas | default 1 }}

# Nested defaults
resources:
  {{- with .Values.resources }}
  {{- toYaml . | nindent 2 }}
  {{- else }}
  requests:
    cpu: 100m
    memory: 128Mi
  {{- end }}
```

---

## Validation Workflow

### Pre-commit Checks

```bash
# 1. Lint YAML
yamllint .

# 2. Lint Helm charts
for chart in charts/*/Chart.yaml; do
    helm lint "$(dirname "$chart")"
done

# 3. Build Kustomize overlays
kustomize build apps/<app>/ --enable-helm > /dev/null
```

### CI Pipeline Example

```yaml
# .github/workflows/validate.yaml
- name: Lint YAML
  run: yamllint .

- name: Lint Helm
  run: |
    for chart in charts/*/Chart.yaml; do
      helm lint "$(dirname "$chart")"
    done

- name: Validate Kustomize
  run: |
    for kust in apps/*/kustomization.yaml; do
      kustomize build "$(dirname "$kust")" --enable-helm > /dev/null
    done
```

---

## Compliance Assessment

**Use letter grades + evidence, NOT numeric scores.**

### Assessment Categories

| Category | Evidence Required |
|----------|------------------|
| **Formatting** | yamllint violations, tab count, indentation |
| **Helm Charts** | helm lint output, template rendering |
| **Kustomize** | kustomize build success, patch correctness |
| **Documentation** | values.yaml comments, section headers |
| **Security** | Hardcoded secrets, external secret refs |

### Grading Scale

| Grade | Criteria |
|-------|----------|
| A+ | 0 yamllint errors, 0 helm lint errors, documented, 0 secrets |
| A | <3 yamllint warnings, <3 helm lint warnings, documented |
| A- | <10 warnings, partial docs |
| B+ | <20 warnings |
| B | <40 warnings, templates render |
| C | Significant issues |

### Validation Commands

```bash
# Lint YAML
yamllint .
# Output: "X error(s), Y warning(s)"

# Check for tabs
grep -rP '\t' --include='*.yaml' --include='*.yml' . | wc -l
# Should be 0

# Helm lint
for chart in charts/*/Chart.yaml; do
  helm lint "$(dirname "$chart")"
done

# Check for hardcoded secrets
grep -r "password:\|secret:\|token:" --include='*.yaml' apps/
# Should only return external references
```

### Example Assessment

```markdown
## YAML/Helm Standards Compliance

| Category | Grade | Evidence |
|----------|-------|----------|
| Formatting | A+ | 0 yamllint errors, 0 tabs |
| Helm Charts | A- | 3 lint warnings (docs) |
| Kustomize | A | All overlays build |
| Security | A | 0 hardcoded secrets |
| **OVERALL** | **A** | **3 MEDIUM findings** |
```

---

## Additional Resources

- [YAML Spec](https://yaml.org/spec/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kustomize Documentation](https://kustomize.io/)
- [yamllint Documentation](https://yamllint.readthedocs.io/)

---

**Related:** Quick reference in Tier 1 `yaml.md`
