# Progressive Disclosure (File Structure)

Keep SKILL.md under 500 lines. Link to reference files loaded on demand.

## How It Works

- SKILL.md loads when skill triggers
- Reference files load only when Claude needs them
- One level deep only (SKILL.md -> reference.md, not chained)

## Directory Structure

```
my-skill/
├── SKILL.md              # Main instructions (<500 lines)
├── reference.md          # Detailed API docs
├── examples.md           # Usage examples
├── templates/            # Template files
│   └── config.template
└── scripts/              # Executable scripts
    └── helper.py
```

## Examples

**API skill with reference:**

```yaml
---
name: stripe-helper
description: Interacts with Stripe API
---

# Stripe Helper

## Quick Reference

- Create customer: `stripe.customers.create()`
- Create payment: `stripe.paymentIntents.create()`

## Detailed Documentation

For complete API reference, see [reference.md](reference.md)
For code examples, see [examples.md](examples.md)
```

**Multi-domain skill:**

```yaml
---
name: analytics-query
description: Queries analytics across domains
---

# Analytics Query

## Domain References

- Sales metrics: see [reference/sales.md](reference/sales.md)
- Product usage: see [reference/product.md](reference/product.md)
- Marketing: see [reference/marketing.md](reference/marketing.md)

Choose the appropriate reference based on the query domain.
```

## Links

- Docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Issues:
  - [#15530](https://github.com/anthropics/claude-code/issues/15530) - Skills loading full files instead of frontmatter
