---
name: create-skill
description: Creates new Claude Skills following official format and learning-infra monorepo structure. Guides through Skill creation workflow, validates format, and ensures proper organization (control-plane/, shared/, infrastructure/). Use when creating new Skills, migrating Cursor commands to Skills, or when asked to create a Skill.
---

# Create Skill

Creates new Claude Skills for the learning-infra monorepo following official format, proper structure, and monorepo organization patterns.

## Project Documentation References

For comprehensive project documentation and compatibility requirements, see:

- **[AGENTS.md](../../../AGENTS.md)** - Central reference for all project documentation
- **[@project-overview.md](../../.agent/rules/shared/project/project-overview.md)** - Project overview and tech stack
- **[@coding-standards.md](../../.agent/rules/shared/quality/coding-standards.md)** - Coding standards and guidelines
- **[@api-development.md](../../.agent/rules/apps/control-plane/api-development.md)** - Control Plane REST API patterns
- **[@provisioning.md](../../.agent/rules/apps/control-plane/provisioning.md)** - Tenant provisioning patterns

## Skill Creation Workflow

Follow these steps to create a new Skill:

1. **Determine scope**
   - Control Plane: REST API, tenant provisioning -> `.skills/skills/control-plane/`
   - Shared: Cross-app functionality -> `.skills/skills/shared/`
   - Infrastructure: Cloud Run, Cloudflare, Neon -> `.skills/skills/infrastructure/`
   - Package: Config, utils -> Context-aware placement

2. **Choose location**
   - Create directory: `.skills/skills/{scope}/{skill-name}/`
   - Skill name: lowercase, hyphens, max 64 chars, no reserved words

3. **Write description**
   - Third-person format
   - Include what the Skill does and when to use it
   - Add trigger keywords users would naturally say
   - Max 1024 characters

4. **Structure content**
   - Main `SKILL.md` (keep under 500 lines)
   - Supporting files if needed (TEMPLATE.md, EXAMPLES.md, etc.)
   - Use progressive disclosure for complex Skills

5. **Validate format**
   - Check YAML frontmatter syntax
   - Verify name and description requirements
   - Ensure file paths use forward slashes
   - See [VALIDATION.md](VALIDATION.md) for complete checklist

6. **Test discovery**
   - Ask Claude: "What Skills are available?"
   - Verify Skill appears with correct description
   - Test triggering with natural language requests

## Monorepo Organization

### Control Plane Skills (`.skills/skills/control-plane/`)

For Skills specific to Control Plane development:

- REST API patterns
- Tenant provisioning workflows
- Domain-driven design
- Control Plane testing

**Example locations:**

- `control-plane/provision-tenant/`
- `control-plane/create-api-endpoint/`

### Shared Skills (`.skills/skills/shared/`)

For Skills used across multiple apps:

- Code review
- General debugging
- Test creation
- Lint and type fixing

**Example locations:**

- `shared/review-code/`
- `shared/debug-code/`
- `shared/create-skill/` (this Skill)

### Infrastructure Skills (`.skills/skills/infrastructure/`)

For Skills specific to infrastructure:

- Cloud Run deployment
- Cloudflare configuration
- Neon database provisioning
- Secret management

**Example locations:**

- `infrastructure/deploy-cloud-run/`
- `infrastructure/provision-database/`

### Package Skills (Context-Aware Placement)

Package Skills are typically placed in `shared/` but include context detection for specific package types.

**Package Types and Their Skills:**

- **`packages/config/` -> Config package context**
  - ESLint, TypeScript, Prettier configuration
  - Shared config patterns

- **`packages/utils/` -> Utils package context**
  - Logger patterns
  - Shared utility functions
  - Utility validation

**Placement**: Place Package Skills in `shared/` with context detection logic that adapts behavior based on the package being worked on.

## Referencing Cursor Rules

**Critical**: Skills must reference Cursor rules, not duplicate their content.

### Available Cursor Rules

**Control Plane Rules** (`.agent/rules/apps/control-plane/`):

- `@api-development.md` - REST API patterns and procedures
- `@domain-structure.md` - Domain-driven design patterns
- `@provisioning.md` - Tenant provisioning patterns

**Infrastructure Rules** (`.agent/rules/infrastructure/`):

- `@cloud-run.md` - Google Cloud Run deployment patterns
- `@cloudflare.md` - Cloudflare for SaaS patterns
- `@database.md` - Neon database provisioning patterns
- `@secrets.md` - GCP Secret Manager patterns

**Shared Rules** (`.agent/rules/shared/`):

- `@project-overview.md` - Project overview and tech stack
- `@coding-standards.md` - Coding standards and guidelines
- `@testing-strategy.md` - Testing patterns and strategies
- `@git-conventions.md` - Conventional commits specification

### Reference Pattern

**In "Project Documentation References" section:**

```markdown
## Project Documentation References

For comprehensive project documentation and compatibility requirements, see:

- **[@provisioning.md](../../.agent/rules/apps/control-plane/provisioning.md)** - Tenant provisioning patterns
- **[@database.md](../../.agent/rules/infrastructure/database.md)** - Neon database patterns
```

**In instructions:**

```markdown
## Instructions

Follow provisioning patterns from @provisioning.md and database patterns from @database.md.

[Only Skill-specific guidance here - how to use the Skill, not the rules themselves]
```

**❌ Bad**: Duplicating rule content

```markdown
## Provisioning Workflow

The Control Plane orchestrates complete tenant provisioning:

1. Merchant Signup -> Receive tenant creation request
2. Create Neon Database -> Via Neon API
   [Duplicates @provisioning.md content]
```

**✅ Good**: Referencing rules

```markdown
## Project Documentation References

- **[@provisioning.md](../../.agent/rules/apps/control-plane/provisioning.md)** - Tenant provisioning patterns

## Instructions

This Skill generates provisioning code following patterns from @provisioning.md.

[Only Skill-specific guidance]
```

## Skill Template

Use the template in [TEMPLATE.md](TEMPLATE.md) as a starting point. It includes:

- Proper YAML frontmatter format
- Required sections
- Project documentation references (references rules, doesn't duplicate them)
- Context detection patterns (if adaptive)

**Important**: Templates show how to reference Cursor rules, not duplicate their content.

## Format Requirements

### YAML Frontmatter

```yaml
---
name: skill-name
description: Third-person description with trigger keywords. Max 1024 chars.
---
```

**Name requirements:**

- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- No XML tags
- No reserved words: "anthropic", "claude"

**Description requirements:**

- Third-person format (e.g., "Creates...", "Generates...")
- Must include what the Skill does and when to use it
- Include trigger keywords users would naturally say
- Maximum 1024 characters
- No XML tags

### SKILL.md Structure

1. **YAML frontmatter** (required)
2. **Title** (H1 with Skill name)
3. **Brief overview** (1-2 paragraphs)
4. **Project Documentation References** (if applicable)
5. **Context Detection** (if adaptive Skill)
6. **Instructions** (main content)
7. **Examples** (concrete examples)
8. **Supporting file references** (if using progressive disclosure)

Keep main body under 500 lines. Split into separate files if needed.

## Context Detection (for Adaptive Skills)

If creating an adaptive Skill that works across multiple contexts, include context detection logic:

```markdown
## Context Detection

1. Check current file path:
   - `apps/control-plane/**` -> Control Plane context (REST API, tenant provisioning)
   - `apps/storefront/**` -> Storefront context (Next.js, multi-tenant routing)
   - `apps/tenant-instance/**` -> Tenant instance context (MedusaJS)
   - `infrastructure/**` -> Infrastructure context (Cloud Run, Cloudflare, Neon)
   - `packages/config/**` -> Config package context
   - `packages/u
```
