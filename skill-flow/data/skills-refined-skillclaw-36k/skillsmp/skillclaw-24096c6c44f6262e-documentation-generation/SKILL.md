---
name: documentation-generation
description: Use this skill when creating or improving project documentation, including READMEs, API docs, and inline comments, to ensure clarity and consistency with the code.
---

# Documentation Generation

Generate comprehensive documentation that stays in sync with code. This includes READMEs, API documentation, and inline comments.

## Quick Reference

| Doc Type            | Primary File      | When to Use                          |
|---------------------|-------------------|--------------------------------------|
| Project README      | `README.md`       | New project, major updates           |
| API Documentation   | JSDoc/docstrings  | New functions, API changes           |
| OpenAPI/Swagger     | `openapi.yaml`    | REST API documentation               |
| Architecture        | `ARCHITECTURE.md` | System design, major components      |
| Change Log          | `CHANGELOG.md`    | Each release                         |
| Migration Guide     | `MIGRATION.md`    | Breaking changes                     |

## Documentation Principles

### 1. Document the Why, Not Just the What

```markdown
// Bad: Documents what the code does (obvious from code)
// Increments counter by 1

// Good: Documents why
// Prevents race condition by using atomic increment
```

### 2. Keep Docs Close to Code

| Pattern                | Benefit                             |
|-----------------------|-------------------------------------|
| JSDoc above functions  | Updates when code changes           |
| README.md in package   | Visible in package managers         |
| Inline comments        | Context at point of use            |

### 3. Use Examples Liberally

Every API function should have at least one working example. Examples are:
- Tested implicitly when code runs
- More useful than prose descriptions
- Easier to keep up to date

## README Structure

A good README follows this structure:

```markdown
# Project Name

One-sentence description of what this does.

## Quick Start

\`\`\`bash
npm install package-name
\`\`\`

\`\`\`typescript
import { main } from 'package-name';
main();
\`\`\`

## Features

- Feature 1 - brief description
- Feature 2 - brief description

## Installation

Detailed installation instructions.

## Usage

### Basic Usage
...

### Advanced Usage
...

## API Reference

Link to detailed API docs or inline reference.

## Configuration

Environment variables, config files.

## Contributing

How to contribute.

## License

License information.
```

### README Anti-Patterns

| Avoid                | Instead                             |
|---------------------|-------------------------------------|
| Wall of text        | Short paragraphs, bullet points     |
| Outdated examples    | Use tested examples                 |