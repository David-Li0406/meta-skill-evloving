---
name: create-demo
description: Use this skill when you want to create a Red Hat Showroom demo module using the Know/Show structure for presenter-led demonstrations.
---

# Demo Module Generator

Guide you through creating a Red Hat Showroom demo module using the Know/Show structure for presenter-led demonstrations.

## When to Use

**Use this skill when you want to**:
- Create presenter-led demo content
- Transform technical documentation into business-focused demos
- Add a module to an existing demo
- Create content for sales engineers or field demonstrations

**Don't use this for**:
- Hands-on workshop content → use `/create-lab`
- Converting to blog posts → use `/blog-generate`
- Reviewing existing content → use `/verify-content`

## Shared Rules

**IMPORTANT**: This skill follows shared contracts defined in `.claude/docs/SKILL-COMMON-RULES.md`:
- Version pinning or attribute placeholders (REQUIRED)
- Reference enforcement (REQUIRED)
- Attribute file location (REQUIRED)
- Image path conventions (REQUIRED)
- Navigation update expectations (REQUIRED)
- Failure-mode behavior (stop if cannot proceed safely)

See SKILL-COMMON-RULES.md for complete details.

## Know/Show Structure

Demos use a different format than workshops:

- **Know sections**: Business context, customer pain points, value propositions, why this matters
- **Show sections**: Step-by-step presenter instructions, what to demonstrate, expected outcomes

This separates what presenters need to **understand** (business value) from what they need to **do** (technical demonstration).

## Arguments (Optional)

This skill supports optional command-line arguments for faster workflows.

**Usage Examples**:
```bash
/create-demo                                   # Interactive mode (asks all questions)
/create-demo <directory>                       # Specify target directory
/create-demo <directory> --new                 # Create new demo in directory
/create-demo <directory> --continue <module>   # Continue from specific module
```

**Parameters**:
- `<directory>` - Target directory for demo files
  - Example: `/create-demo content/modules/ROOT/pages/`
  - If not provided, defaults to `content/modules/ROOT/pages/`
- `--new` - Flag to create new demo (generates index + overview + details + module-01)
- `--continue <module-path>` - Continue from specified previous demo module
  - Example: `/create-demo content/modules/ROOT/pages/ --continue content/modules/ROOT/pages/03-module-`