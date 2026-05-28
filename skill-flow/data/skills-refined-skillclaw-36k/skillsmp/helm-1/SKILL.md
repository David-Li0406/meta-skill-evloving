---
name: helm
description: Kubernetes package management with Helm. This skill should be used when installing/upgrading Helm releases, developing Helm charts, debugging template rendering issues, managing chart dependencies, or troubleshooting release failures. Covers helm install/upgrade/rollback commands, chart structure, Go template syntax, values handling, and common debugging patterns.
---

# Helm

Kubernetes package manager for deploying and managing applications via charts.

## Quick Commands

```bash
# Install/Upgrade
helm install myapp ./mychart -f values.yaml
helm upgrade --install myapp ./mychart -f values.yaml

# Debug templates
helm template myapp ./mychart --debug
helm install myapp ./mychart --dry-run --debug

# Release info
helm list -A
helm status myapp
helm get values myapp
helm history myapp

# Rollback
helm rollback myapp [REVISION]
```

For complete command reference, see `references/commands.md`.

## Chart Development

### Minimal Chart Structure
```
mychart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── _helpers.tpl
    └── deployment.yaml
```

### Template Basics
```yaml
# Access values
replicas: {{ .Values.replicaCount }}

# Quote strings
name: {{ .Values.name | quote }}

# Default values
port: {{ .Values.port | default 8080 }}

# Required values
password: {{ required "password required" .Values.password }}

# Conditional blocks
{{- if .Values.ingress.enabled }}
...
{{- end }}

# Include helpers with proper indentation
labels:
  {{- include "mychart.labels" . | nindent 4 }}
```

For complete chart development guide, see `references/chart-development.md`.

## Debugging

### Template Issues
```bash
# Render without installing
helm template myapp ./mychart --debug

# Render single template
helm template myapp ./mychart -s templates/deployment.yaml

# Lint for errors
helm lint ./mychart --strict
```

### Release Issues
```bash
# Get deployed state
helm get all myapp
helm get manifest myapp
helm get values myapp --revision 1

# Check history
helm history myapp
```

For debugging patterns and common fixes, see `references/debugging.md`.

## Common Patterns

### ConfigMap/Secret Rollout
```yaml
# Trigger pod restart when config changes
annotations:
  checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
```

### Optional Sections
```yaml
# Avoid nil pointer errors
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

### Install or Upgrade
```bash
helm upgrade --install myapp ./mychart -f values.yaml
```

## References

- `references/commands.md` - Full command reference
- `references/chart-development.md` - Chart structure, templates, values
- `references/debugging.md` - Debugging techniques and common fixes
