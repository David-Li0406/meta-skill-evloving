# Skills Reference

Detailed guide for creating specialized knowledge domains.

> **📘 New to skills?** Start with [COMPONENTS.md](COMPONENTS.md#skill-templates) for complete templates with examples.
>
> **This file provides:** Organization patterns, progressive disclosure strategies, content guidelines, and validation checklists.

## Quick Links

- [File Format](#file-format)
- [Skill Types](#skill-types)
- [Organization Patterns](#organization-patterns)
- [Content Guidelines](#content-guidelines)
- [Validation Checklist](#validation-checklist)

## File Format

`skills/skill-name.md`

## Template

```markdown
---
description: What this skill provides and when to use it (max 1024 chars)
---

# Skill Title

Comprehensive guide for [domain/topic].

## When to Use This Skill

Use this skill when:
- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## Quick Start

[Basic usage example or core workflow]

## Core Concepts

[Essential knowledge about the domain]

## Process

[Step-by-step workflows]

## Best Practices

[Guidelines and patterns]

## Examples

[Practical examples]

## See Also

- [ADVANCED.md](references/ADVANCED.md) for advanced topics
- [EXAMPLES.md](references/EXAMPLES.md) for more examples
```

## Frontmatter Fields

### Required

- `description`: Clear description including WHAT and WHEN (max 1024 chars)
  - What: What the skill provides
  - When: When to use the skill
  - Must be comprehensive to help Claude discover the skill

## Best Practices

1. **Progressive disclosure**: Keep SKILL.md lean, move details to references/
2. **Clear triggers**: Describe specific scenarios in description
3. **Self-contained**: Include all necessary domain knowledge
4. **Practical examples**: Show real-world usage
5. **Avoid duplication**: Don't repeat what Claude already knows

## Skill Types

### 1. Framework-Specific Skills

```markdown
---
description: React best practices and patterns. Use when working with React components, hooks, state management, or React-specific workflows for: (1) Component design, (2) Performance optimization, (3) State management, (4) Testing React apps
---

# React Best Practices

Use this skill for React development guidance.

## Quick Start

```jsx
function MyComponent({ prop }) {
  return <div>{prop}</div>;
}
```

## Core Patterns

- Functional components with hooks
- Prop drilling vs context
- Custom hooks for logic reuse

See [PATTERNS.md](references/PATTERNS.md) for detailed patterns.
```

### 2. Domain Knowledge Skills

```markdown
---
description: Financial modeling and analysis. Use when working with financial calculations, reports, or accounting systems for: (1) Revenue recognition, (2) Cost analysis, (3) Financial reporting
---

# Financial Modeling

Use this skill for financial domain knowledge.

## Core Concepts

- Revenue recognition principles
- Cost allocation methods
- Financial statement structures

See [FINANCE.md](references/FINANCE.md) for detailed schemas.
```

### 3. Best Practice Skills

```markdown
---
description: Security best practices for web applications. Use when implementing authentication, authorization, or data protection for: (1) OWASP compliance, (2) Secure authentication, (3) Data encryption
---

# Security Best Practices

Use this skill for security guidance.

## Quick Start

```python
# Never do this
password = request.GET['password']

# Do this instead
password = request.POST.get('password', '')
```

## Core Principles

- Never trust client input
- Always encrypt sensitive data
- Use parameterized queries
```

### 4. Workflow Skills

```markdown
---
description: Code review workflow and standards. Use when reviewing code changes, pull requests, or conducting code audits for: (1) Quality checks, (2) Security review, (3) Performance analysis
---

# Code Review Workflow

Use this skill for systematic code reviews.

## Process

1. Read all changes
2. Check security issues
3. Verify best practices
4. Test functionality
5. Provide feedback
```

## Progressive Disclosure Pattern

### SKILL.md (Lean)

```markdown
---
description: PDF processing guide
---

# PDF Processing

## Quick Start

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced Features

- **Forms**: See [FORMS.md](references/FORMS.md)
- **API**: See [API.md](references/API.md)
- **Examples**: See [EXAMPLES.md](references/EXAMPLES.md)
```

### references/FORMS.md (Detailed)

```markdown
# PDF Forms

Complete guide for working with PDF forms.

## Fill Form Fields

```python
# Detailed form filling code
```

## Validate Forms

```python
# Validation code
```
```

## Organization Patterns

### By Domain

```
bigquery-skill/
├── SKILL.md (overview)
└── references/
    ├── finance.md (revenue, billing)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage)
    └── marketing.md (campaigns)
```

### By Complexity

```
react-skill/
├── SKILL.md (quick start)
└── references/
    ├── PATTERNS.md (design patterns)
    ├── PERFORMANCE.md (optimization)
    └── TESTING.md (testing strategies)
```

### By Variant

```
deploy-skill/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md (AWS deployment)
    ├── gcp.md (GCP deployment)
    └── azure.md (Azure deployment)
```

## Content Guidelines

### What to Include

- **Domain-specific knowledge**: Things Claude doesn't know
- **Company-specific patterns**: Internal conventions
- **Complex workflows**: Multi-step procedures
- **API documentation**: Specific APIs
- **Schemas**: Data structures

### What to Exclude

- **Generic programming**: Claude knows this
- **Basic language syntax**: Assume Claude knows the language
- **Obvious patterns**: Common patterns
- **Verbose explanations**: Prefer code examples

## Examples

### Example 1: API Skill

```markdown
---
description: Stripe API integration guide. Use when working with Stripe payments, subscriptions, or webhooks for: (1) Payment processing, (2) Subscription management, (3) Webhook handling
---

# Stripe API

Use this skill for Stripe integration.

## Quick Start

```python
import stripe
stripe.api_key = "sk_test_..."

charge = stripe.Charge.create(
    amount=2000,
    currency="usd",
    source="token",
    description="Order"
)
```

## Common Patterns

- **Create charge**: See [CHARGES.md](references/CHARGES.md)
- **Handle webhooks**: See [WEBHOOKS.md](references/WEBHOOKS.md)
- **Manage subscriptions**: See [SUBSCRIPTIONS.md](references/SUBSCRIPTIONS.md)
```

### Example 2: Company Style Guide

```markdown
---
description: Company coding standards and conventions. Use when writing or modifying code for: (1) File structure, (2) Naming conventions, (3) Error handling
---

# Coding Standards

Follow these standards for all code.

## File Structure

```
src/
├── components/
├── utils/
└── tests/
```

## Naming

- Components: PascalCase
- Functions: camelCase
- Constants: UPPER_SNAKE_CASE

## Error Handling

```python
def process(data):
    try:
        result = validate(data)
        return result
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise
```
```

## Validation Checklist

- [ ] YAML frontmatter valid with name and description
- [ ] Description includes both WHAT and WHEN
- [ ] SKILL.md under 500 lines
- [ ] Detailed content moved to references/
- [ ] All references linked from SKILL.md
- [ ] No duplication between SKILL.md and references
- [ ] Examples are practical and runnable
- [ ] Domain-specific knowledge included
- [ ] Generic content excluded
- [ ] Clear when to read each reference file
