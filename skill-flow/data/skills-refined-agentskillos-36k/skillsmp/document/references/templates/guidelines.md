# Guidelines Template

Use this template for documenting design systems, style guides, code standards, or project conventions.

## When to Use

- Creating design system component documentation
- Documenting code style guidelines
- Recording project conventions
- Establishing team standards

## Template Structure

```markdown
# {guidelines_title}

## Metadata

- **Timestamp**: {YYYY-MM-DD HH:MM:SS}
- **Project**: {project_name}
- **Category**: Guidelines
- **Tags**: {comma_separated_tags}
- **Version**: {version_number}

## Overview

General description of these guidelines:

- Purpose
- Scope
- Audience

## Principles

Fundamental principles guiding these decisions:

1. Principle 1: description
2. Principle 2: description
3. Principle 3: description

## Guidelines

### {Category 1}

#### Guideline 1.1

**Description:** Guideline description

**Rationale:** Why this guideline exists

**Example:**

\`\`\`{language}
// Correct example
\`\`\`

**Counter-example:**

\`\`\`{language}
// Incorrect example
\`\`\`

#### Guideline 1.2

(Repeat structure)

### {Category 2}

(Repeat structure)

## Visual Examples

(If applicable for design systems)

### Component: {component_name}

**Usage:**

- When to use
- When not to use

**Variants:**

- Variant 1: description
- Variant 2: description

**Properties:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| prop1    | type | value   | description |
| prop2    | type | value   | description |

**Code Example:**

\`\`\`{language}
// Component usage example
\`\`\`

## Exceptions

Situations where these guidelines don't apply or can be relaxed:

- Exception 1: context and justification
- Exception 2: context and justification

## Enforcement

How these guidelines are enforced:

- Automated tools (linters, formatters)
- Code review checklist
- CI/CD gates

## Evolution

Process for proposing changes to these guidelines:

1. Step 1
2. Step 2
3. Step 3

## References

- External resources
- Related documentation
```

## Field Descriptions

### Metadata
- **Timestamp**: Auto-generated current date/time
- **Project**: Auto-detected from directory or git repo
- **Category**: Always "Guidelines"
- **Tags**: Relevant tags (frontend, backend, style, etc.)
- **Version**: Semantic version number for these guidelines

### Overview
High-level description covering:
- **Purpose**: Why these guidelines exist
- **Scope**: What they cover and don't cover
- **Audience**: Who should follow them

### Principles
3-5 core principles that guide all specific guidelines. These are the "why" behind the rules.

### Guidelines
Specific, actionable rules organized by category. Each guideline should include:
- **Description**: What the guideline is
- **Rationale**: Why it exists
- **Example**: Correct implementation
- **Counter-example**: What to avoid

### Visual Examples
(Optional, mainly for design systems)

Component documentation including:
- Usage guidance (when to use/avoid)
- Available variants
- Properties/props table
- Code examples

### Exceptions
Legitimate situations where guidelines can be bent or broken. Always include justification.

### Enforcement
How compliance is ensured:
- Automated tooling (ESLint, Prettier, etc.)
- Manual review processes
- CI/CD integration

### Evolution
Process for updating guidelines:
- How to propose changes
- Approval process
- Communication plan

### References
Related resources:
- Style guides
- Design documentation
- External standards (WCAG, etc.)
