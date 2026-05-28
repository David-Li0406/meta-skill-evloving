---
name: claude-md-authoring
description: Use this skill when you need to create or update a CLAUDE.md file to provide project-specific context for Claude Code, ensuring it has the necessary information to assist effectively.
---

# CLAUDE.md Authoring

This skill guides the creation and updating of CLAUDE.md files tailored to project types, ensuring that Claude has the essential context for effective interaction.

## Purpose of CLAUDE.md

CLAUDE.md serves as the primary tool for context management, providing Claude with project-specific information such as:
- Project structure and architecture
- Common commands and workflows
- Conventions and preferences
- Quick reference information

## Structure of CLAUDE.md

Follow this general structure for your CLAUDE.md:

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

## Section Selection by Project Type

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

## Writing Guidelines

1. **Be concise**: Use tables and bullet points for clarity.
2. **Focus on essential elements**: Include build and test commands, project structure overview, key architectural decisions, and patterns specific to the codebase.
3. **Avoid unnecessary details**: Keep the document under 300 lines, aiming for under 60 lines if possible.

## What to Avoid

- **Never use as a linter**: Rely on deterministic tools (ESLint, Prettier) for code style.
- **Avoid auto-generation**: Manually craft CLAUDE.md to maximize its effectiveness for Claude.