---
name: technical-documentation
description: Use this skill when creating, maintaining, or improving high-quality technical documentation, including API docs, user guides, README files, and architecture documentation.
---

# Technical Documentation

A comprehensive skill for generating and maintaining structured technical documentation across various formats and purposes.

## Workflow

### 1. Identify Documentation Type

Determine the type of documentation needed:

- **API Documentation** - REST, GraphQL, webhooks, authentication
- **User Guides** - Features, how-tos, troubleshooting
- **Tutorials** - Learning-focused with hands-on examples
- **Architecture Documents** - System design, technical decisions
- **README Files** - Project overview, quick start
- **Release Notes** - Changes, migrations, breaking changes
- **Technical Specifications** - Requirements, constraints

### 2. Gather Context

Collect essential information before writing:

- **Audience** - Developers, end-users, managers, administrators
- **Technical depth** - Beginner, intermediate, advanced
- **Scope** - Codebase/APIs/systems to document
- **Standards** - Style guides or organizational requirements
- **Related docs** - Existing documentation to reference or integrate with

### 3. Structure Content

Apply clear organization principles:

- Lead with overview/introduction
- Use descriptive heading hierarchy (H1 → H2 → H3)
- Include table of contents for documents with >3 sections
- Group related information logically
- Place examples immediately after concepts
- Add diagrams/visuals for complex workflows

### 4. Write Clear Content

Follow core writing principles:

- **Active voice** - "The API returns..." not "The response is returned..."
- **Specificity** - "Response time < 200ms" not "Fast response"
- **Define acronyms** - "API (Application Programming Interface)" on first use
- **Consistent terminology** - Same terms throughout document
- **Imperative instructions** - "Run the command" not "You should run..."
- **Show examples** - Provide code/output for every concept

### 5. Add Code Examples

Code example requirements:

- Specify language in code blocks: ```python,```javascript
- Show complete, runnable examples (not fragments)
- Include input/output pairs
- Add explanatory comments for complex logic
- Test all code before publishing

### 6. Review and Validate

Quality assurance checklist:

- ✓ Verify technical accuracy
- ✓ Test all code examples
- ✓ Check clarity and completeness
- ✓ Ensure consistent terminology
- ✓ Validate all links and references

## Documentation Templates

### README Files

Essential components for project documentation:

```markdown
# Project Name
Brief description of what the project does

## Features
- Key feature 1
- Key feature 2
- Key feature 3

## Installation
[step-by-step installation commands]

## Quick Start
[minimal working example]

## Configuration
[environment variables or config options]

## License
[license type]
```

### Release Notes

Structure for version releases:

```markdown
# Version X.X.X - YYYY-MM-DD

## Summary
[High-level overview of this release]

## New Features
- Feature description (#issue-number)
- Feature description (#issue-number)

## Bug Fixes
- Fix description (#issue-number)
- Fix description (#issue-number)

## Breaking Changes
⚠️ **Change that breaks compatibility**
Migration guide: [step-by-step migration instructions]

## Deprecations
- Deprecated feature (will be removed in vX.X)
```

## Best Practices

1. **Be Clear and Concise**: Use simple language, avoid jargon
2. **Include Examples**: Show, don't just tell
3. **Keep Updated**: Documentation should match current code
4. **Consider Audience**: Adjust detail level for target users
5. **Use Consistent Format**: Follow project conventions
6. **Link Related Content**: Cross-reference related documentation
7. **Test Examples**: Ensure code examples actually work
8. **Use Visual Aids**: Diagrams, screenshots when helpful
9. **Document Why**: Not just what, but why decisions were made
10. **Make Discoverable**: Clear organization and search

## When to Use This Skill

Use this skill when:
- Creating new project documentation
- Writing or updating README files
- Documenting APIs or functions
- Creating user guides or tutorials
- Recording architecture decisions
- Improving code comments
- Generating API reference documentation
- Documenting deployment processes
- Creating troubleshooting guides
- Writing contributing guidelines

## Tools and Formats

### Supported Formats

- **Markdown**: README, documentation files
- **reStructuredText**: Python projects (Sphinx)
- **AsciiDoc**: Complex documentation
- **OpenAPI/Swagger**: REST API documentation
- **GraphQL Schema**: GraphQL API documentation

### Documentation Generators

- **Sphinx**: Python documentation
- **JSDoc**: JavaScript documentation
- **Javadoc**: Java documentation
- **GoDoc**: Go documentation
- **Rustdoc**: Rust documentation
- **Swagger/OpenAPI**: API documentation
- **MkDocs**: Project documentation sites

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete documentation examples across different project types and languages.

For documentation templates, see [templates/](templates/).

For automated documentation generation, see [scripts/generate_docs.py](scripts/generate_docs.py).