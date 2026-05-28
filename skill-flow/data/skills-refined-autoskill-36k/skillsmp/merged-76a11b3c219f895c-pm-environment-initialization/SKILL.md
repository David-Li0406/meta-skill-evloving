---
name: pm-environment-initialization
description: Use this skill to initialize the product management environment by creating a constitution document from a template.
---

# PM Environment Initialization

This skill initializes the product constitution document that provides shared constraints and domain information for all product management activities.

## Language Configuration

Before generating any content, check `aico.json` in the project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Check existing**: Look for `docs/reference/pm/constitution.md`.
2. **If exists**: Ask the user if they want to overwrite or update specific sections.
3. **If not exists**:
   - Read the template from `references/constitution.template.md`.
   - Guide the user through questions to fill the template.
4. **Save output**: Write to `docs/reference/pm/constitution.md`.

## Document Header Format

All generated documents MUST use this unified header format:

```markdown
# [Document Title]

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
```

## Guided Questions

Ask the user about:

| Section          | Questions                                                  |
| ---------------- | ---------------------------------------------------------- |
| Product Overview | What is the product name? One-line description? Who are the target users? |
| Domain Info      | What is the industry/market? What are the key terminology and compliance requirements? |
| Constraints      | What is the technical stack? What are the business constraints? |
| Standards        | What is the documentation language? What are the naming conventions? |

## Output

```
✓ Created docs/reference/pm/constitution.md
✓ PM environment initialized
```

## Key Rules

- ALWAYS use the unified header format.
- MUST guide the user through key questions before generating.
- ALWAYS save to `docs/reference/pm/constitution.md`.