# Argo (Argo CD, Workflows, Rollouts, Events)

**Category**: cncf
**Description**: GitOps and workflow automation for Kubernetes
**Homepage**: https://argoproj.github.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Argo Go packages*

- `github.com/argoproj/argo-cd` - Argo CD
- `github.com/argoproj/argo-workflows` - Argo Workflows
- `github.com/argoproj/argo-rollouts` - Argo Rollouts
- `github.com/argoproj/argo-events` - Argo Events

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Argo usage*

- `argocd-cm.yaml` - Argo CD ConfigMap
- `argocd-secret.yaml` - Argo CD secrets
- `application.yaml` - Argo CD Application
- `workflow.yaml` - Argo Workflow

### Kubernetes Resources (YAML files)

**Pattern**: `kind:\s*(?:Application|ApplicationSet|AppProject|Workflow|CronWorkflow|WorkflowTemplate|Rollout|AnalysisTemplate|Sensor|EventSource)`
- Argo CRD kinds
- Example: `kind: Application`

**Pattern**: `apiVersion:\s*argoproj\.io/v[0-9]+`
- Argo API group
- Example: `apiVersion: argoproj.io/v1alpha1`

### Code Patterns

**Pattern**: `argocd|argo-cd|argoproj`
- Argo references
- Example: `argocd.argoproj.io`

**Pattern**: `ARGOCD_|ARGO_`
- Argo environment variables
- Example: `ARGOCD_SERVER`

**Pattern**: `argocd\s+app|argocd\s+sync`
- Argo CD CLI commands
- Example: `argocd app sync myapp`

**Pattern**: `argo\s+submit|argo\s+list`
- Argo Workflows CLI
- Example: `argo submit workflow.yaml`

**Pattern**: `:8080/api/v1/applications|/argocd/`
- Argo CD API endpoints
- Example: `https://argocd.example.com/api/v1/applications`

**Pattern**: `spec:\s*\n\s*(?:source:|destination:|syncPolicy:|strategy:)`
- Argo Application spec
- Example: Argo CD Application YAML

---

## Environment Variables

- `ARGOCD_SERVER` - Argo CD server URL
- `ARGOCD_AUTH_TOKEN` - Authentication token
- `ARGOCD_OPTS` - CLI options
- `ARGO_NAMESPACE` - Workflows namespace
- `ARGO_TOKEN` - Workflows token
- `ARGO_SERVER` - Workflows server

## Detection Notes

- Argo CD for GitOps continuous delivery
- Argo Workflows for CI/CD pipelines
- Argo Rollouts for progressive delivery
- Argo Events for event-driven automation
- Application CRD is the primary Argo CD resource

---

## Secrets Detection

### Credentials

#### Argo CD Auth Token
**Pattern**: `(?:argocd|ARGOCD).*(?:auth[_-]?token|AUTH[_-]?TOKEN|token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9._-]+)['"]?`
**Severity**: critical
**Description**: Argo CD authentication token
**Example**: `ARGOCD_AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

#### Argo CD Admin Password
**Pattern**: `admin\.password:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Argo CD admin password in ConfigMap
**Context Required**: In argocd-secret

#### Argo Workflows Token
**Pattern**: `(?:argo|ARGO).*(?:token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9._-]+)['"]?`
**Severity**: high
**Description**: Argo Workflows authentication token

### Validation

#### API Documentation
- **Argo CD API**: https://argo-cd.readthedocs.io/en/stable/developer-guide/api-docs/
- **Argo Workflows**: https://argoproj.github.io/argo-workflows/

---

## TIER 3: Configuration Extraction

### Application Name Extraction

**Pattern**: `metadata:\s*\n\s*name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Argo Application name
- Extracts: `app_name`
- Multiline: true

### Repo URL Extraction

**Pattern**: `repoURL:\s*['"]?([^\s'"]+)['"]?`
- Git repository URL
- Extracts: `repo_url`
- Example: `repoURL: https://github.com/org/repo`

### Target Revision Extraction

**Pattern**: `targetRevision:\s*['"]?([^\s'"]+)['"]?`
- Git target revision
- Extracts: `target_revision`
- Example: `targetRevision: HEAD`
