# Helm

**Category**: cncf
**Description**: Package manager for Kubernetes
**Homepage**: https://helm.sh

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Helm Go SDK*

- `helm.sh/helm/v3` - Helm v3 SDK
- `github.com/helm/helm` - Helm library

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Helm usage*

- `Chart.yaml` - Helm chart metadata
- `Chart.lock` - Chart dependency lock
- `values.yaml` - Default chart values
- `values-*.yaml` - Environment-specific values
- `helmfile.yaml` - Helmfile configuration
- `.helmignore` - Files to ignore in chart
- `requirements.yaml` - Legacy dependencies
- `requirements.lock` - Legacy lock file

### Configuration Directories
*Known directories that indicate Helm usage*

- `charts/` - Chart dependencies
- `templates/` - Kubernetes manifests
- `crds/` - Custom Resource Definitions

### Code Patterns

**Pattern**: `helm\s+install|helm\s+upgrade|helm\s+repo`
- Helm CLI commands
- Example: `helm install myrelease ./mychart`

**Pattern**: `{{-?\s*\.|{{-?\s*include|{{-?\s*define`
- Helm template syntax
- Example: `{{ .Values.image.repository }}`

**Pattern**: `\.Values\.|\.Release\.|\.Chart\.`
- Helm built-in objects
- Example: `{{ .Values.replicaCount }}`

**Pattern**: `HELM_|helm\.sh`
- Helm environment variables
- Example: `HELM_REPOSITORY_CACHE`

**Pattern**: `apiVersion:\s*v2|apiVersion:\s*v1`
- Chart.yaml API version
- Example: `apiVersion: v2`

**Pattern**: `artifacthub\.io|charts\.helm\.sh`
- Helm chart repositories
- Example: `https://charts.helm.sh/stable`

---

## Environment Variables

- `HELM_CACHE_HOME` - Helm cache directory
- `HELM_CONFIG_HOME` - Helm config directory
- `HELM_DATA_HOME` - Helm data directory
- `HELM_REPOSITORY_CACHE` - Repository cache
- `HELM_REPOSITORY_CONFIG` - Repository config
- `HELM_NAMESPACE` - Default namespace
- `HELM_KUBECONTEXT` - Kubernetes context
- `HELM_DRIVER` - Storage driver

## Detection Notes

- Chart.yaml is the primary indicator of Helm charts
- templates/ contains Go template files
- values.yaml provides default configuration
- Helmfile for declarative Helm deployments
- OCI registry support for chart hosting

---

## Secrets Detection

### Credentials

#### Helm Repository Password
**Pattern**: `(?:helm|HELM).*(?:password|PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Helm repository authentication password

#### Helm Registry Token
**Pattern**: `(?:helm|HELM).*(?:token|TOKEN)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Helm OCI registry token

---

## TIER 3: Configuration Extraction

### Chart Name Extraction

**Pattern**: `name:\s*['"]?([a-zA-Z0-9._-]+)['"]?`
- Chart name from Chart.yaml
- Extracts: `chart_name`
- Example: `name: mychart`

### Chart Version Extraction

**Pattern**: `version:\s*['"]?([0-9]+\.[0-9]+\.[0-9]+[a-zA-Z0-9._-]*)['"]?`
- Chart version
- Extracts: `chart_version`
- Example: `version: 1.2.3`

### App Version Extraction

**Pattern**: `appVersion:\s*['"]?([^\s'"]+)['"]?`
- Application version
- Extracts: `app_version`
- Example: `appVersion: "2.0.0"`
