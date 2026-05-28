---
name: skill-creator
description: Use this skill when creating new Claude Code skills, defining skill structures, or helping users build custom auto-invoked skills.
---

# Skill Creator Skill

You have expertise in creating Claude Code skills - auto-invoked capabilities that activate based on context.

## When to Use

This skill activates for:

- Creating new skills for Claude Code
- Defining skill structures and frontmatter
- Converting expertise into skill format
- Helping users build custom skills
- Organizing skill bundles

## Skill Structure

### Basic SKILL.md Template

```markdown
---
name: skill-name
description: When Claude should auto-invoke this skill. Be specific about triggers.
---

# Skill Name

Brief description of your expertise.

## When to Use

Bullet points of scenarios that trigger this skill:

- Scenario 1
- Scenario 2
- Scenario 3

## Core Capabilities

### Capability 1

Explanation and code examples...

### Capability 2

Explanation and code examples...

## Patterns & Templates

Code templates that users commonly need...

## Best Practices

1. **Practice 1** - Explanation
2. **Practice 2** - Explanation

## Common Pitfalls

- Pitfall 1: How to avoid
- Pitfall 2: How to avoid
```

### Frontmatter Fields

```yaml
---
name: kebab-case-name # Required: unique identifier
description: | # Required: triggers auto-invocation
  Detailed description of when Claude should use this skill.
  Include keywords that users might mention.
disable-model-invocation: false # Optional: set true for manual-only
---
```

## Skill Categories

### Development Skills

```
.claude/skills/
├── api-development/      # REST API, GraphQL, webhooks
├── frontend-development/ # React, Vue, components
├── database-operations/  # SQL, ORMs, migrations
├── testing/             # Unit, E2E, integration
└── devops/              # CI/CD, Docker, deployment
```

### Domain Skills

```
.claude/skills/
├── fintech/             # Payments, compliance, security
├── healthcare/          # HIPAA, HL7, medical systems
├── ecommerce/           # Carts, checkout, inventory
└── analytics/           # Metrics, dashboards, tracking
```

### Tool Skills

```
.claude/skills/
├── mcp-builder/         # Creating MCP servers
├── playwright/          # Browser automation
├── prisma/              # ORM operations
└── supabase/           # BaaS integration
```

## Writing Effective Descriptions

### Good Descriptions (Specific Triggers)

```yaml
description: |
  Use this skill when creating new Claude Code skills or defining skill structures.
```