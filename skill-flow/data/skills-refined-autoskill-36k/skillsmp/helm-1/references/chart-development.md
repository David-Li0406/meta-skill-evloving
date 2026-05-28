# Chart Development

## Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata (required)
├── values.yaml         # Default values (required)
├── charts/             # Dependencies
├── templates/          # Kubernetes manifests
│   ├── NOTES.txt       # Post-install notes
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...
└── README.md
```

## Chart.yaml

```yaml
apiVersion: v2
name: mychart
version: 0.1.0           # Chart version (SemVer)
appVersion: "1.0.0"      # Application version
description: My application
type: application        # or 'library'
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

## Template Syntax

### Basic Directives
```yaml
# Variable access
name: {{ .Release.Name }}
namespace: {{ .Release.Namespace }}

# Values access
replicas: {{ .Values.replicaCount }}
image: {{ .Values.image.repository }}:{{ .Values.image.tag }}

# Quote strings
name: {{ .Values.name | quote }}

# Default values
port: {{ .Values.port | default 8080 }}

# Required values
password: {{ required "password is required" .Values.password }}
```

### Built-in Objects
- `.Release.Name` - Release name
- `.Release.Namespace` - Target namespace
- `.Release.IsInstall` - True if install
- `.Release.IsUpgrade` - True if upgrade
- `.Chart.Name` - Chart name
- `.Chart.Version` - Chart version
- `.Values` - Merged values
- `.Files` - Access non-template files
- `.Template.Name` - Current template path

### Control Flow
```yaml
# Conditionals
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
...
{{- end }}

# With (scope change)
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}

# Range (loops)
{{- range .Values.ports }}
- port: {{ .port }}
  name: {{ .name }}
{{- end }}

# Range with index
{{- range $index, $value := .Values.items }}
- name: item-{{ $index }}
{{- end }}
```

### Template Helpers (_helpers.tpl)
```yaml
{{/*
Create chart name and version as used by chart label.
*/}}
{{- define "mychart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

# Usage
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

### Include vs Template
```yaml
# include - captures output as string (preferred)
{{ include "mychart.labels" . | nindent 4 }}

# template - outputs directly (no pipeline)
{{ template "mychart.labels" . }}
```

## Common Functions

| Function | Usage |
|----------|-------|
| `quote` | Wrap in quotes |
| `default` | Fallback value |
| `required` | Fail if missing |
| `toYaml` | Convert to YAML |
| `nindent N` | Newline + indent N spaces |
| `indent N` | Indent N spaces |
| `trim` | Remove whitespace |
| `lower/upper` | Case conversion |
| `replace` | String replace |
| `trunc N` | Truncate to N chars |
| `trimSuffix` | Remove suffix |
| `sha256sum` | SHA256 hash |
| `b64enc/b64dec` | Base64 encode/decode |
| `lookup` | Query K8s resources |

## Values Best Practices

```yaml
# values.yaml
replicaCount: 1

image:
  repository: nginx
  tag: ""              # Default to Chart.appVersion
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts: []
  tls: []

resources: {}
  # limits:
  #   cpu: 100m
  #   memory: 128Mi

nodeSelector: {}
tolerations: []
affinity: {}
```

Use `{}` or `[]` for optional objects/arrays to avoid nil pointer errors.
