{{/*
Expand the name of the chart.
*/}}
{{- define "openshift-cluster-health-mcp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "openshift-cluster-health-mcp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "openshift-cluster-health-mcp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "openshift-cluster-health-mcp.labels" -}}
helm.sh/chart: {{ include "openshift-cluster-health-mcp.chart" . }}
{{ include "openshift-cluster-health-mcp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "openshift-cluster-health-mcp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "openshift-cluster-health-mcp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app: {{ include "openshift-cluster-health-mcp.fullname" . }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "openshift-cluster-health-mcp.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "openshift-cluster-health-mcp.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
