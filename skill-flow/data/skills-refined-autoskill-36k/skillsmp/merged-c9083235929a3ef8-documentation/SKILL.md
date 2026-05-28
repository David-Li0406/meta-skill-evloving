---
name: documentation
description: Generate and maintain high-quality technical documentation including API docs, README files, architecture documentation, user guides, and code comments. Use when creating documentation, writing README files, documenting APIs, or when users mention "documentation", "docs", or "technical writing".
---

# Documentation

A comprehensive skill that helps create, maintain, and improve technical documentation across various formats and purposes.

## Documentation Types

### 1. README.md (Project Overview)

**Purpose**: First impression of your project.

**Template**:
```markdown
# Project Name

> One-line description of what the project does.

[![npm version](https://badge.fury.io/js/package-name.svg)](https://badge.fury.io/js/package-name)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## 📦 Installation

\`\`\`bash
npm install package-name
\`\`\`

## 🚀 Quick Start

\`\`\`typescript
import { MainClass } from 'package-name';

const instance = new MainClass();
instance.doSomething();
\`\`\`

## 📖 Documentation

- [Installation Guide](docs/INSTALL-GUIDE.md)
- [User Guide](docs/USER-GUIDE.md)
- [API Reference](docs/API-REFERENCE.md)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
```

### 2. API Documentation

Generate comprehensive API documentation:

- **REST APIs**: Endpoints, parameters, responses, examples
- **Function/Method Documentation**: Parameters, return values, exceptions
- **Type Definitions**: Interfaces, classes, data structures
- **Authentication**: Auth methods, security considerations
- **Error Handling**: Status codes, error messages, troubleshooting

### 3. User Guides

Create user-facing documentation:

- **Getting Started**: First steps for new users
- **Tutorials**: Step-by-step learning paths
- **How-To Guides**: Task-focused instructions
- **Reference**: Complete feature documentation
- **Troubleshooting**: Common issues and solutions

### 4. Architecture Documentation

Document system architecture:

- **Architecture Diagrams**: System components and relationships
- **Design Decisions**: ADRs (Architecture Decision Records)
- **Data Flow**: How data moves through the system
- **Technology Stack**: Technologies used and why
- **Deployment**: Infrastructure and deployment processes

### 5. Code Documentation

Improve inline code documentation:

- **Docstrings**: Function/class documentation following conventions
- **Comments**: Explanatory comments for complex logic
- **Type Hints**: Type annotations (Python, TypeScript)
- **JSDoc**: JavaScript documentation comments
- **Javadoc**: Java documentation comments

## Core Principles

### 1. Documentation as Code
Docs live with code, version with code, review with code.

```
✅ Docs in repo alongside source
✅ Markdown for portability
✅ Generated docs from source (OpenAPI, JSDoc)
✅ CI checks for doc freshness
```

### 2. Audience-First Writing
Write for who's reading, not what you know.

```
✅ README: "I just found this repo"
✅ API Docs: "How do I call this endpoint?"
✅ ADR: "Why was this decision made?"
✅ Guide: "How do I accomplish X?"
```

### 3. Maintainability Over Completeness
Less accurate docs are worse than no docs.

```
✅ Link to source of truth
✅ Automate what changes often
✅ Date and version sensitive content
❌ Duplicate information across docs
```

## Documentation Workflow

### 1. New Feature Documentation

```
Feature PR should include:
├── README updates (if user-facing)
├── API docs (if new endpoints)
├── ADR (if significant decision)
└── Code comments (if complex logic)
```

### 2. Keeping Docs in Sync

```yaml
# In PR template or CI
Documentation checklist:
- [ ] README updated if behavior changed
- [ ] API docs match implementation
- [ ] ADR written for architectural changes
- [ ] Examples tested and working
```

### 3. Documentation Review

Check for:
- Accuracy (does it match the code?)
- Completeness (all parameters documented?)
- Clarity (would a new dev understand?)
- Examples (do they work?)

## Common Documentation Tasks

### Add JSDoc to Existing Code

```typescript
// Before
function processData(data, options) {
  // ...
}

// After
/**
 * Processes raw data according to specified options.
 *
 * @param data - Raw data to process
 * @param options - Processing configuration
 * @param options.validate - Whether to validate input (default: true)
 * @param options.transform - Transform function to apply
 * @returns Processed data object
 *
 * @example
 * ```typescript
 * const result = processData(rawData, { validate: true });
 * ```
 */
function processData(data: RawData, options: ProcessOptions): ProcessedData {
  // ...
}
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

## Documentation Quality Checklist

- [ ] Clear purpose statement
- [ ] Logical structure with headings
- [ ] Working code examples
- [ ] Complete parameter documentation
- [ ] Error handling examples
- [ ] Up-to-date with current version
- [ ] Spell-checked and grammar-checked
- [ ] Links verified
- [ ] Screenshots/diagrams where helpful

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

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete documentation examples across different project types and languages.

For documentation templates, see [templates/](templates/).

For automated documentation generation, see [scripts/generate_docs.py](scripts/generate_docs.py).