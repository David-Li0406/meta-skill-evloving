---
name: musubix-technical-writing
description: Guide for creating technical documentation including README, user guides, API references, and changelogs. Use this when asked to write documentation, create user manuals, or generate API docs.
license: MIT
---

# MUSUBIX Technical Writing Skill

This skill guides you through creating high-quality technical documentation for software projects.

## Overview

Technical documentation bridges the gap between code and users. MUSUBIX supports generating various document types with consistent structure and traceability.

## Document Types

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

### 2. INSTALL-GUIDE.md (Installation Guide)

**Purpose**: Step-by-step setup instructions.

**Structure**:
```markdown
# Installation Guide

## Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Node.js | >= 20.0.0 | `node --version` |
| npm | >= 10.0.0 | `npm --version` |

## Installation Methods

### Method 1: npm (Recommended)

\`\`\`bash
npm install package-name
\`\`\`

### Method 2: From Source

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
npm install
npm run build
\`\`\`

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | API authentication key | - |
| `LOG_LEVEL` | Logging verbosity | `info` |

### Configuration File

Create `config.json`:
\`\`\`json
{
  "setting1": "value1",
  "setting2": true
}
\`\`\`

## Verification

\`\`\`bash
npx package-name --version
\`\`\`

## Troubleshooting

### Common Issues

#### Issue: Module not found
**Solution**: Run `npm install` again.

#### Issue: Permission denied
**Solution**: Use `sudo` or fix npm permissions.
```

### 3. USER-GUIDE.md (User Guide)

**Purpose**: Comprehensive usage instructions.

**Structure**:
```markdown
# User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Best Practices](#best-practices)

## Getting Started

### Your First Project

1. Create a new directory
2. Initialize the project
3. Run your first command

## Basic Usage

### Command: `command-name`

**Syntax**:
\`\`\`bash
npx tool command [options] <arguments>
\`\`\`

**Options**:
| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output directory |
| `--verbose` | `-v` | Enable verbose logging |

**Examples**:
\`\`\`bash
# Basic usage
npx tool command input.txt

# With options
npx tool command -o output/ -v input.txt
\`\`\`

## Advanced Features

### Feature: Custom Configuration

[Detailed explanation with examples]

## Best Practices

1. **Do**: Recommended approach
2. **Don't**: Anti-pattern to avoid
```

### 4. API-REFERENCE.md (API Reference)

**Purpose**: Complete API documentation.

**Structure**:
```markdown
# API Reference

## Classes

### `ClassName`

Description of the class.

#### Constructor

\`\`\`typescript
new ClassName(options?: ClassOptions)
\`\`\`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `ClassOptions` | Configuration options |

#### Methods

##### `methodName(param1, param2)`

Description of what the method does.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `param1` | `string` | Yes | First parameter |
| `param2` | `number` | No | Optional second parameter |

**Returns**: `Promise<Result>`

**Example**:
\`\`\`typescript
const result = await instance.methodName('value', 42);
\`\`\`

**Throws**:
- `ValidationError`: When param1 is empty

## Interfaces

### `InterfaceName`

\`\`\`typescript
interface InterfaceName {
  property1: string;
  property2?: number;
  method(arg: string): void;
}
\`\`\`

## Types

### `TypeName`

\`\`\`typescript
type TypeName = 'option1' | 'option2' | 'option3';
\`\`\`
```

### 5. CHANGELOG.md (Change Log)

**Purpose**: Track version history.

**Format**: Follow [Keep a Changelog](https://keepachangelog.com/)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Deprecated
- Feature to be removed in future

### Removed
- Deleted feature description

### Fixed
- Bug fix description

### Security
- Security fix description

## [1.0.0] - 2026-01-10

### Added
- Initial release
- Core functionality
- CLI interface
```

### 6. CONTRIBUTING.md (Contributing Guide)

**Purpose**: Guide for contributors.

```markdown
# Contributing Guide

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Install dependencies: `npm install`
4. Create a branch: `git checkout -b feature/your-feature`

## Code Standards

- Use TypeScript
- Follow ESLint rules
- Write tests for new features
- Maintain 80%+ code coverage

## Pull Request Process

1. Update documentation
2. Add tests
3. Run `npm test`
4. Submit PR with clear description

## Commit Message Format

\`\`\`
type(scope): description

[optional body]

[optional footer]
\`\`\`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Code of Conduct

Be respectful and inclusive.
```

## Writing Guidelines

### 1. Audience-Aware Writing

| Document | Audience | Tone | Technical Level |
|----------|----------|------|-----------------|
| README | Everyone | Welcoming | Low-Medium |
| INSTALL-GUIDE | Users | Instructive | Medium |
| USER-GUIDE | Users | Explanatory | Medium |
| API-REFERENCE | Developers | Technical | High |
| CONTRIBUTING | Contributors | Collaborative | High |

### 2. Formatting Best Practices

```markdown
# ✅ Good Practices

## Use Clear Headings
Structure content hierarchically.

## Include Code Examples
\`\`\`typescript
// Always show working examples
const example = 'value';
\`\`\`

## Use Tables for Structured Data
| Column 1 | Column 2 |
|----------|----------|
| Data | Data |

## Add Visual Cues
> 💡 **Tip**: Helpful advice
> ⚠️ **Warning**: Important caution
> ❌ **Error**: Common mistake
```

### 3. Multilingual Support

For projects requiring Japanese and English:

```
docs/
├── README.md          # English (default)
├── README.ja.md       # Japanese
├── USER-GUIDE.md      # English
├── USER-GUIDE.ja.md   # Japanese
└── ...
```

## CLI Integration

```bash
# Generate README from project analysis
npx musubix docs readme

# Generate API reference from TypeScript
npx musubix docs api --source src/

# Update CHANGELOG from git commits
npx musubix docs changelog --from v1.0.0

# Generate all documentation
npx musubix docs generate --all
```

## Traceability

Link documentation to requirements and design:

```markdown
<!-- @requirement REQ-DOC-001 -->
<!-- @design DES-DOC-001 -->

# User Guide

This guide covers the usage of...
```

## Document Quality Checklist

- [ ] Clear purpose statement
- [ ] Logical structure with headings
- [ ] Working code examples
- [ ] Complete parameter documentation
- [ ] Error handling examples
- [ ] Up-to-date with current version
- [ ] Spell-checked and grammar-checked
- [ ] Links verified
- [ ] Screenshots/diagrams where helpful

## Related Skills

- [musubix-sdd-workflow](../musubix-sdd-workflow/SKILL.md) - Overall development workflow
- [musubix-adr-generation](../musubix-adr-generation/SKILL.md) - Decision documentation
- [musubix-code-generation](../musubix-code-generation/SKILL.md) - Code with doc comments
