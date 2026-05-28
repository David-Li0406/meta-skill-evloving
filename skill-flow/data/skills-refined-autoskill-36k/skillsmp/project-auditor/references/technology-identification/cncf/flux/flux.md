# Flux

**Category**: cncf
**Description**: GitOps toolkit for Kubernetes
**Homepage**: https://fluxcd.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Flux Go packages*

- `github.com/fluxcd/flux2` - Flux v2
- `github.com/fluxcd/source-controller` - Source controller
- `github.com/fluxcd/kustomize-controller` - Kustomize controller
- `github.com/fluxcd/helm-controller` - Helm controller

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Flux usage*

- `flux-system/` - Flux system directory
- `gotk-components.yaml` - GitOps Toolkit components
- `gotk-sync.yaml` - GitOps Toolkit sync

### Kubernetes Resources (YAML files)

**Pattern**: `kind:\s*(?:GitRepository|HelmRepository|Kustomization|HelmRelease|ImagePolicy|ImageRepository|ImageUpdateAutomation|Receiver|Alert|Provider)`
- Flux CRD kinds
- Example: `kind: GitRepository`

**Pattern**: `apiVersion:\s*(?:source\.toolkit\.fluxcd\.io|kustomize\.toolkit\.fluxcd\.io|helm\.toolkit\.fluxcd\.io|notification\.toolkit\.fluxcd\.io|image\.toolkit\.fluxcd\.io)/v[0-9]+`
- Flux API groups
- Example: `apiVersion: source.toolkit.fluxcd.io/v1`

### Code Patterns

**Pattern**: `fluxcd\.io|flux-system|gotk-`
- Flux references
- Example: `flux-system namespace`

**Pattern**: `FLUX_|flux\s+bootstrap|flux\s+reconcile`
- Flux CLI and environment
- Example: `flux bootstrap github`

**Pattern**: `toolkit\.fluxcd\.io`
- Flux toolkit annotations
- Example: `kustomize.toolkit.fluxcd.io/reconcile`

---

## Environment Variables

- `FLUX_FORWARD_NAMESPACE` - Forward namespace
- `GITHUB_TOKEN` - GitHub token for bootstrap
- `GITLAB_TOKEN` - GitLab token for bootstrap

## Detection Notes

- GitOps alternative to Argo CD
- flux-system namespace is standard
- Uses toolkit controllers for different concerns
- Image automation for container updates

---

## Secrets Detection

### Credentials

#### Flux Git Credentials
**Pattern**: `password:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Git password in Flux secret
**Context Required**: Near GitRepository or flux-system

---

## TIER 3: Configuration Extraction

### Git Repository URL Extraction

**Pattern**: `url:\s*['"]?(https?://[^\s'"]+|ssh://[^\s'"]+)['"]?`
- Git repository URL
- Extracts: `repo_url`
- Context Required: In GitRepository spec

### Interval Extraction

**Pattern**: `interval:\s*['"]?([0-9]+[smh])['"]?`
- Reconciliation interval
- Extracts: `interval`
- Example: `interval: 5m`
