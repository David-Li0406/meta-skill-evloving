---
name: claude-md-authoring
description: Use this skill when creating or updating CLAUDE.md files to provide project-specific context for Claude Code.
---

# CLAUDE.md Authoring

Create and update CLAUDE.md files tailored to project type with appropriate sections and content. CLAUDE.md serves as the primary tool for context management, providing Claude with essential information about the project.

## Purpose of CLAUDE.md

CLAUDE.md provides Claude Code with project-specific context, including:
- Project structure and architecture
- Common commands and workflows
- Conventions and preferences
- Quick reference information

## The WHAT-WHY-HOW Framework

Structure CLAUDE.md content around three categories:

| Category | Purpose | Examples |
|----------|---------|----------|
| **WHAT** | Technology stack, project structure, codebase organization | "This is a Next.js app using TypeScript and Prisma" |
| **WHY** | Project purpose, component functions | "The auth module handles OAuth2 flow for enterprise SSO" |
| **HOW** | Commands, testing procedures, verification methods | "Run `npm test` before commits; lint with `npm run lint`" |

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

## Update Workflow

To update an existing CLAUDE.md:

1. **Read current file** to understand existing structure.
2. **Analyze project** to detect current state.
3. **Compare** documented vs actual state.
4. **Generate diff** showing proposed changes.
5. **Present to user** for confirmation.
6. **Apply changes** if approved.

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

## Creation Workflow

To create an effective CLAUDE.md:

1. **Audit the codebase**: Identify build commands, test procedures, key patterns.
2. **Draft minimal content**: Start with WHAT-WHY-HOW essentials only.
3. **Remove task-specific content**: Move specialized instructions to separate documentation.
4. **Use pointers**: Replace code snippets with `file:line` references.
5. **Test for universality**: Ask "Will this help in every Claude session?"

## What to Avoid

- **Never Use as a Linter**: Avoid using CLAUDE.md for code style guidelines; use deterministic tools instead.
- **Avoid Auto-Generation**: Manually craft CLAUDE.md rather than relying on auto-generated content.
- **Skip Universally Irrelevant Content**: Ensure all content is relevant to Claude's tasks.
- **No Duplicate Information**: Use `file:line` pointers instead of copying code snippets.

## Additional Resources

For detailed examples and anti-patterns, consult:
- **`references/examples.md`** - Real CLAUDE.md examples.
- **`references/anti-patterns.md`** - Common mistakes to avoid.