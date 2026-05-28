---
name: documentation-templates
description: Use this skill when you need structured templates and guidelines for creating various types of documentation, including README files, API documentation, code comments, and changelogs.
---

# Documentation Templates

> Templates and structure guidelines for common documentation types.

---

## 1. README Structure

### Essential Sections (Priority Order)

| Section               | Purpose               |
| --------------------- | --------------------- |
| **Title + One-liner** | What is this?         |
| **Quick Start**       | Running in <5 min     |
| **Features**          | What can I do?        |
| **Configuration**     | How to customize      |
| **API Reference**     | Link to detailed docs |
| **Contributing**      | How to help           |
| **License**           | Legal                 |

### README Template

```markdown
# Project Name

Brief one-line description.

## Quick Start

[Minimum steps to run]

## Features

- Feature 1
- Feature 2

## Configuration

| Variable | Description | Default |
| -------- | ----------- | ------- |
| PORT     | Server port | 3000    |

## Documentation

- [API Reference](./docs/api.md)
- [Architecture](./docs/architecture.md)

## License

MIT
```

---

## 2. API Documentation Structure

### Per-Endpoint Template

```markdown
## GET /users/:id

Get a user by ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id   | string | Yes | User ID |

**Response:**
- 200: User object
- 404: User not found

**Example:**
[Request and response example]
```

---

## 3. Code Comment Guidelines

### JSDoc/TSDoc Template

```typescript
/**
 * Brief description of what the function does.
 * 
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws ErrorType - When this error occurs
 * 
 * @example
 * const result = functionName(input);
 */
```

### When to Comment

| ✅ Comment           | ❌ Don't Comment       |
| -------------------- | ---------------------- |
| Why (business logic) | What (obvious)         |
| Complex algorithms   | Every line             |
| Non-obvious behavior | Self-explanatory code  |
| API contracts        | Implementation details |

---

## 4. Changelog Template (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]

### Added

- New feature

## [1.0.0] - 2025-01-01

### Added

- Initial release

### Changed

- Updated dependency

### Fixed

- Bug fix
```

---

## 5. Architecture Decision Record (ADR)

```markdown
# ADR-001: [Title]

## Status
Accepted / Deprecated / Superseded

## Context
Why are we making this decision?

## Decision
What did we decide?

## Consequences
What are the trade-offs?
```

---

## 6. AI-Friendly Documentation

### Guidelines for AI-Friendly Documentation

- Use clear and concise language.
- Structure content logically for easy navigation.
- Include examples and use cases to enhance understanding.