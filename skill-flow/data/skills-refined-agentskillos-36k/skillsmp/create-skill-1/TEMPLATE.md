# Skill Template

Use this template as a starting point for creating new Skills. Copy and customize based on your Skill's scope and requirements.

## Basic Template

```yaml
---
name: skill-name
description: [Third-person description with trigger keywords. Include what the Skill does and when to use it. Max 1024 characters.]
---

# Skill Name

[Brief overview: 1-2 paragraphs explaining what this Skill does]

## Project Documentation References

**Critical**: Reference Cursor rules instead of duplicating their content.

For comprehensive project documentation and compatibility requirements, see:
- **[AGENTS.md](../../../AGENTS.md)** - Central reference for all project documentation
- **[@project-overview.md](../../.agent/rules/shared/project/project-overview.md)** - Project overview and tech stack
- [Add other relevant rule references based on Skill scope]

**Available Cursor Rules** (reference, don't duplicate):
- Control Plane: `@api-development.md`, `@domain-structure.md`, `@provisioning.md`
- Infrastructure: `@cloud-run.md`, `@cloudflare.md`, `@database.md`, `@secrets.md`
- Shared: `@project-overview.md`, `@coding-standards.md`, `@testing-strategy.md`, `@git-conventions.md`

## Instructions

[Clear, step-by-step guidance that references rules, not duplicates them]

**Pattern**: "Follow [pattern] from @rule-name.md" instead of repeating the pattern.

## Examples

[Concrete examples showing the Skill in action, with rule references]

## Additional Resources

[If using progressive disclosure, reference supporting files here]
```

## Control Plane Skill Template

```yaml
---
name: control-plane-skill-name
description: [What it does for Control Plane]. Use when [trigger conditions]. Control Plane-specific: REST API, tenant provisioning, domain logic.
---

# Control Plane Skill Name

[Overview specific to Control Plane development]

## Project Documentation References

- **[@api-development.md](../../.agent/rules/apps/control-plane/api-development.md)** - REST API patterns and procedures
- **[@domain-structure.md](../../.agent/rules/apps/control-plane/domain-structure.md)** - Domain-driven design patterns
- **[@provisioning.md](../../.agent/rules/apps/control-plane/provisioning.md)** - Tenant provisioning patterns

## Tech Stack

- Runtime: Bun
- Language: TypeScript (strict)
- API: RESTful (JSON)
- DB: PostgreSQL + Drizzle ORM
- Testing: Vitest

## Instructions

[Control Plane-specific instructions that reference rules, not duplicate them]

**Pattern**: "Follow [pattern] from @rule-name.md" instead of repeating the pattern.

Example: "Use provisioning patterns from @provisioning.md for tenant creation."

## Examples

[Control Plane examples that show rule references]
```

## Shared Skill Template (Adaptive)

```yaml
---
name: shared-skill-name
description: [What it does across apps]. Use when [trigger conditions]. Adapts behavior based on context (control-plane, storefront, infrastructure, packages).
---

# Shared Skill Name

[Overview for cross-app functionality]

## Project Documentation References

- **[@project-overview.md](../../.agent/rules/shared/project/project-overview.md)** - Project overview and tech stack
- **[@coding-standards.md](../../.agent/rules/shared/quality/coding-standards.md)** - Coding standards and guidelines

## Context Detection

1. Check current file path:
   - `apps/control-plane/**` -> Control Plane context (REST API, tenant provisioning)
   - `apps/storefront/**` -> Storefront context (Next.js, multi-tenant routing)
   - `apps/tenant-instance/**` -> Tenant instance context (MedusaJS)
   - `infrastructure/**` -> Infrastructure context (Cloud Run, Cloudflare, Neon)
   - `packages/config/**` -> Config package context
   - `packages/utils/**` -> Utils package context

2. Adapt behavior:
   - Control Plane: Use REST API patterns, provisioning workflows
   - Storefront: Use Next.js patterns, multi-tenant routing
   - Tenant Instance: Use MedusaJS patterns
   - Infrastructure: Use Cloud Run, Cloudflare, Neon patterns
   - Packages: Use appropriate patterns for package type

## Instructions

[Context-aware instructions]

## Examples

[Examples for different contexts]
```

## Infrastructure Skill Template

```yaml
---
name: infrastructure-skill-name
description: [What it does for infrastructure]. Use when [trigger conditions]. Infrastructure-specific: Cloud Run, Cloudflare, Neon, secrets.
---

# Infrastructure Skill Name

[Overview specific to infrastructure development]

## Project Documentation References

- **[@cloud-run.md](../../.agent/rules/infrastructure/cloud-run.md)** - Google Cloud Run deployment patterns
- **[@cloudflare.md](../../.agent/rules/infrastructure/cloudflare.md)** - Cloudflare for SaaS patterns
- **[@database.md](../../.agent/rules/infrastructure/database.md)** - Neon database provisioning patterns
- **[@secrets.md](../../.agent/rules/infrastructure/secrets.md)** - GCP Secret Manager patterns

## Instructions

[Infrastructure-specific instructions that reference rules, not duplicate them]

**Pattern**: "Follow [pattern] from @rule-name.md" instead of repeating the pattern.

## Examples

[Infrastructure examples that show rule references]
```

## Package Skill Template

```yaml
---
name: package-skill-name
description: [What it does for packages]. Use when [trigger conditions]. Works with [package type]: config or utils. Adapts behavior based on package context.
---

# Package Skill Name

[Overview specific to package development]

## Project Documentation References

- **[@project-overview.md](../../.agent/rules/shared/project/project-overview.md)** - Project overview and tech stack

## Package Context Detection

This Skill works with shared packages and adapts behavior based on package type:

1. **`packages/config/`** - Shared configuration
   - ESLint, TypeScript, Prettier configuration
   - Shared config patterns
   - Tooling: Config validation, pattern checks

2. **`packages/utils/`** - Shared utilities
   - Logger patterns
   - Shared utility functions
   - Utility validation
   - Tooling: Unit tests, utility patterns

## Context Detection

1. Check current file path:
   - `packages/config/**` -> Config package context
   - `packages/utils/**` -> Utils package context

2. Adapt behavior:
   - Config: Validate configs, check patterns, verify consistency
   - Utils: Test utilities, validate patterns, check exports

## Instructions

[Package-specific instructions that adapt based on detected context]

## Examples

[Examples for each package type]
```

## Template Sections Explained

### YAML Frontmatter

**Required fields:**

- `name`: Skill identifier (lowercase, hyphens, max 64 chars)
- `description`: Third-person description with triggers (max 1024 chars)

**Optional fields** (for Claude Code):

- `allowed-tools`: Restrict tool access
- `context`: Fork context for isolation
- `user-invocable`: Control slash menu visibility

### Project Documentation References

Reference relevant project rules based on Skill scope:

- Control Plane Skills -> API, Domain, Provisioning rules
- Infrastructure Skills -> Cloud Run, Cloudflare, Database, Secrets rules
- Shared Skills -> Project overview, coding standards
- Package Skills -> Project overview, package-specific rules

### Context Detection

Include for adaptive Skills that work across multiple contexts. Helps Skills adapt behavior based on current file location.

### Instructions

Main content section. Keep concise, assume Claude knows basics. Focus on:

- What makes this Skill unique
- Specific patterns and conventions
- Step-by-step workflows
- Error handling

### Examples

Concrete input/output examples. Show:

- Real usage scenarios
- Expected behavior
- Edge cases
- Different contexts (if adaptive)

## Customization Guidelines

1. **Remove unused sections**: Delete sections not relevant to your Skill
2. **Add domain-specific sections**: Include sections specific to your Skill's purpose
3. **Reference supporting files**: If using progressive disclosure, add references
4. **Keep under 500 lines**: Split into supporting files if neede
