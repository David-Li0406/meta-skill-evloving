---
name: generate-docs
description: Generate comprehensive documentation for code following team patterns
agent: agent
tools:
  - search
  - edit
  - read
---

# Generate Documentation

Generate documentation for the specified code following team standards.

## Context

**File:** ${file}
**Selection:** ${selection}

## Standards

Follow the patterns in [documentation-patterns](../instructions/documentation-patterns.instructions.md).

## Process

1. **Analyze** the code to understand purpose, inputs, outputs
2. **Identify** documentation type needed (inline, README, API reference)
3. **Generate** documentation following the appropriate template
4. **Include** at least one practical code example
5. **Document** error conditions and edge cases

## Output

Create or update documentation with:

- Clear purpose statement
- Parameter descriptions
- Return value documentation
- Working code examples
- Error/exception documentation

Use the templates in [DOC-TEMPLATES](../references/DOC-TEMPLATES.md) as reference.
