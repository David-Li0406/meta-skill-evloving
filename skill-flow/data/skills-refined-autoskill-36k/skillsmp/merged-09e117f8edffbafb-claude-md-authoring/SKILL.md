---
name: claude-md-authoring
description: Use this skill when you need to create or update a CLAUDE.md file for project documentation, providing essential context and instructions for Claude.
---

# CLAUDE.md Authoring

Create and update CLAUDE.md files tailored to project type with appropriate sections and content, ensuring that Claude has the necessary context for effective interaction.

## Purpose of CLAUDE.md

CLAUDE.md provides Claude with project-specific context, including:
- Project structure and architecture
- Common commands and workflows
- Conventions and preferences
- Quick reference information

## Core Principles

1. **Keep It Short**: Aim for 50-200 lines, with a maximum of 500 lines to ensure content is manageable and relevant.
2. **Link, Don't Duplicate**: Reference existing documentation instead of repeating it to save tokens and maintain clarity.
3. **Project-Specific Only**: Include unique workflows, critical gotchas, and common commands while avoiding general programming knowledge and code style guidelines.

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

1. **Be concise**: Use tables over prose where possible.
2. **Use headers**: Create a scannable structure with `##` and `###`.
3. **Include commands**: Wrap in code blocks with language hints.
4. **Add separators**: Use `---` between major sections.
5. **Prefer tables**: For lists of items with multiple attributes.
6. **Keep current**: Only document what actually exists.

## Creation Workflow

To create an effective CLAUDE.md:

1. **Audit the codebase**: Identify build commands, test procedures, key patterns.
2. **Draft minimal content**: Start with WHAT-WHY-HOW essentials only.
3. **Remove task-specific content**: Move specialized instructions to separate documentation files.
4. **Use pointers**: Replace code snippets with `file:line` references.
5. **Test for universality**: Ensure content is relevant for every Claude session.

## Additional Resources

For detailed examples and anti-patterns, consult:
- **`references/examples.md`** - Real CLAUDE.md examples
- **`references/anti-patterns.md`** - Common mistakes to avoid

## Common Mistakes

- **Too long**: Avoid excessive length that discourages reading.
- **Duplicates docs**: Refrain from repeating README or API specs.
- **Code style rules**: Use linters instead of including style guidelines.
- **General knowledge**: Focus on project-specific information.

## Usage

When a user requests to create or improve a CLAUDE.md, follow the outlined workflow to ensure the document is concise, relevant, and useful for Claude's interactions.