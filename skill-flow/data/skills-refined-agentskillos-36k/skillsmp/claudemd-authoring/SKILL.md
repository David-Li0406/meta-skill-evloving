---
name: CLAUDE.md Authoring
description: This skill should be used when the user asks to "update CLAUDE.md", "create CLAUDE.md", "write project documentation", "what should CLAUDE.md include", or when generating/updating project documentation for Claude Code. Provides templates and best practices for CLAUDE.md files.
version: 0.1.0
---

# CLAUDE.md Authoring

Create and update CLAUDE.md files tailored to project type with appropriate sections and content.

## Purpose of CLAUDE.md

CLAUDE.md provides Claude Code with project-specific context:
- Project structure and architecture
- Common commands and workflows
- Conventions and preferences
- Quick reference information

## Section Selection by Project Type

Select sections based on detected project type:

### Infrastructure Projects

| Section | Include | Content |
|---------|---------|---------|
| Quick Reference | Always | Common kubectl/helm commands |
| Cluster Architecture | Always | Nodes, resources, network |
| Service Catalog | Always | Services, URLs, ports |
| Storage | If NFS/PV used | Storage classes, PVCs |
| GitOps Workflow | If ArgoCD | App structure, deployment flow |
| Monitoring | If Prometheus/Grafana | Dashboards, alerts |
| Security | If secrets/certs | SealedSecrets, cert-manager |

### Code Projects

| Section | Include | Content |
|---------|---------|---------|
| Quick Reference | Always | Build, test, run commands |
| Project Structure | Always | Directory layout |
| Development | Always | Setup, dependencies |
| Testing | If tests exist | Test commands, coverage |
| API Reference | If API project | Endpoints, auth |
| Deployment | If CI/CD exists | Pipeline, environments |

### Monorepo Projects

| Section | Include | Content |
|---------|---------|---------|
| Quick Reference | Always | Workspace commands |
| Package Overview | Always | Package list, purposes |
| Dependency Graph | If complex | Internal dependencies |
| Build Order | If relevant | Build sequence |
| Shared Config | If exists | Shared tsconfig, eslint |

## CLAUDE.md Structure

Follow this general structure:

```markdown
# Project Name

## Quick Reference

\`\`\`bash
# Most common commands here
\`\`\`

---

## 1. [Primary Section]

### 1.1 [Subsection]

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |

---

## 2. [Secondary Section]

[Content]

---

## N. User Preferences

[Tools, aliases, conventions]
```

## Writing Guidelines

1. **Be concise**: Use tables over prose where possible
2. **Use headers**: Create scannable structure with `##` and `###`
3. **Include commands**: Wrap in code blocks with language hints
4. **Add separators**: Use `---` between major sections
5. **Prefer tables**: For lists of items with multiple attributes
6. **Keep current**: Only document what actually exists

## Update Workflow

To update an existing CLAUDE.md:

1. **Read current file** to understand existing structure
2. **Analyze project** to detect current state
3. **Compare** documented vs actual state
4. **Generate diff** showing proposed changes
5. **Present to user** for confirmation
6. **Apply changes** if approved

## Diff Format

Present changes as unified diff:

```diff
## Services

| Service | URL |
|---------|-----|
- | Old Service | old.url |
+ | New Service | new.url |
| Unchanged | same.url |
```

## Additional Resources

### Template Files

Project-specific templates:
- **`templates/infra-template.md`** - Kubernetes/ArgoCD template
- **`templates/code-template.md`** - Code project template
- **`templates/monorepo-template.md`** - Monorepo template
