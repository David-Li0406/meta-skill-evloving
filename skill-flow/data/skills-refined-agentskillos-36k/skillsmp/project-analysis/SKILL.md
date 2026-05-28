---
name: Project Analysis
description: This skill should be used when the user asks to "analyze this project", "what type of project is this", "detect project structure", "understand this codebase", or when Claude needs to determine project type for documentation purposes. Provides patterns for identifying project types and analyzing codebase structure.
version: 0.1.0
---

# Project Analysis

Analyze codebases to detect project type, structure, and key components for documentation purposes.

## Project Type Detection

Identify project type by checking for signature files in priority order:

### Infrastructure Projects

| Indicator Files | Project Type |
|-----------------|--------------|
| `argocd/`, `*/Application.yaml` | ArgoCD GitOps |
| `helm/`, `Chart.yaml` | Helm Charts |
| `manifests/`, `*.yaml` with `kind:` | Kubernetes |
| `*.tf`, `terraform/` | Terraform |
| `ansible/`, `playbook*.yml` | Ansible |

**Analysis focus**: Namespaces, services, deployments, ingress, storage classes, node selectors.

### Code Projects

| Indicator Files | Project Type |
|-----------------|--------------|
| `package.json` | Node.js (check for framework: next, react, express) |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `go.mod` | Go |
| `pom.xml` | Java Maven |
| `build.gradle` | Java Gradle |
| `Cargo.toml` | Rust |

**Analysis focus**: Dependencies, scripts, entry points, test configuration.

### Monorepo Detection

| Indicator Files | Monorepo Type |
|-----------------|---------------|
| `nx.json` | Nx |
| `turbo.json` | Turborepo |
| `lerna.json` | Lerna |
| `pnpm-workspace.yaml` | pnpm Workspaces |
| `packages/`, `apps/` directories | Generic Monorepo |

**Analysis focus**: Workspace packages, shared dependencies, build order.

## Analysis Workflow

To analyze a project:

1. **Scan root directory** for indicator files using Glob tool
2. **Identify primary type** from highest-priority match
3. **Detect secondary characteristics** (testing framework, CI/CD, containerization)
4. **Extract key metrics**:
   - For infra: service count, namespace count, storage classes
   - For code: dependency count, script count, test coverage config
   - For monorepo: package count, shared dependencies

## Detection Commands

Use these Glob patterns for quick detection:

```bash
# Infrastructure
**/Chart.yaml
**/Application.yaml
**/*.tf
**/kustomization.yaml

# Code projects
package.json
pyproject.toml
go.mod
pom.xml
Cargo.toml

# Monorepo
nx.json
turbo.json
lerna.json
pnpm-workspace.yaml
```

## Output Format

Report project analysis as structured data:

```
Project Type: [Primary Type]
Secondary: [Framework, CI/CD, Container]
Key Components:
  - [Component 1]: [Count/Details]
  - [Component 2]: [Count/Details]
Files Analyzed: [Count]
```

## Additional Resources

### Reference Files

For detailed analysis patterns per project type:
- **`references/infra-analysis.md`** - Kubernetes, ArgoCD, Helm analysis patterns
- **`references/code-analysis.md`** - Language-specific analysis patterns
