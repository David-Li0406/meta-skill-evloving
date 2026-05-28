# Helm Debugging

## Template Debugging

### Dry Run
```bash
# Render templates without installing
helm install myapp ./mychart --dry-run --debug

# Upgrade dry run
helm upgrade myapp ./mychart --dry-run --debug

# Template command (no cluster needed)
helm template myapp ./mychart --debug
```

### Render Specific Template
```bash
helm template myapp ./mychart -s templates/deployment.yaml
helm template myapp ./mychart -s templates/configmap.yaml --debug
```

### Lint Chart
```bash
helm lint ./mychart
helm lint ./mychart --strict    # Warnings as errors
helm lint ./mychart --with-subcharts
```

## Release Debugging

### Get Release Info
```bash
helm get all myapp              # All release data
helm get values myapp           # Deployed values
helm get values myapp --all     # Include defaults
helm get manifest myapp         # Deployed manifests
helm get notes myapp            # NOTES.txt output
helm get hooks myapp            # Hooks info
```

### Check Status
```bash
helm status myapp
helm status myapp --show-desc   # Include description
helm history myapp              # Revision history
```

### Compare Values
```bash
# Show difference between releases
helm get values myapp --revision 1 > v1.yaml
helm get values myapp --revision 2 > v2.yaml
diff v1.yaml v2.yaml
```

## Common Issues

### Template Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `nil pointer evaluating` | Accessing undefined value | Use `{{- if .Values.foo }}` or `{{ .Values.foo \| default "" }}` |
| `can't evaluate field X` | Wrong object type | Check value structure in values.yaml |
| `YAML parse error` | Invalid indentation | Use `nindent` instead of `indent` |
| `mapping values not allowed` | Missing newline before block | Add `-` to trim whitespace: `{{-` |

### Whitespace Control
```yaml
# Problem: extra whitespace
metadata:
  labels:
    {{ include "mychart.labels" . }}    # Adds leading whitespace

# Solution: trim and nindent
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

### Nil Value Handling
```yaml
# Problem: crashes if nodeSelector not defined
nodeSelector:
  {{- toYaml .Values.nodeSelector | nindent 2 }}

# Solution: wrap with conditional
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}

# Or check for content
{{- if .Values.nodeSelector }}
nodeSelector:
  {{- toYaml .Values.nodeSelector | nindent 2 }}
{{- end }}
```

### Release Stuck

```bash
# Check release status
helm status myapp

# If stuck in pending-install/pending-upgrade
helm history myapp
# Look for failed revision

# Force rollback
helm rollback myapp [REVISION]

# If completely stuck, uninstall with keep-history
helm uninstall myapp --keep-history
# Then reinstall
helm install myapp ./mychart
```

### Upgrade Failures

```bash
# Check what changed
helm diff upgrade myapp ./mychart  # Requires helm-diff plugin

# Rollback to working revision
helm rollback myapp 1

# Check revision values
helm get values myapp --revision 1
helm get values myapp --revision 2
```

## Debug Print

Add to template for debugging:
```yaml
# Print variable value
{{- printf "%#v" .Values.myVar | fail }}

# Print entire values
{{- toYaml .Values | fail }}

# Conditional debug output
{{- if .Values.debug }}
# DEBUG: {{ .Values.someValue }}
{{- end }}
```

## Kubernetes Debugging

```bash
# After install, check resources
kubectl get all -l app.kubernetes.io/instance=myapp

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check pod logs
kubectl logs -l app.kubernetes.io/instance=myapp

# Describe failing pods
kubectl describe pod -l app.kubernetes.io/instance=myapp
```
