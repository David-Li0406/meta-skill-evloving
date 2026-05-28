---
name: agent-ops-docs
description: Use this skill when creating or updating project documentation, including README, CHANGELOG, and API docs, to ensure consistency and traceability.
---

# Documentation Workflow

## Purpose

Manage user-facing documentation (README, CHANGELOG, API docs) with consistency and traceability. Ensures documentation stays synchronized with code changes.

## When to Use

- After implementing a feature that affects public API or usage
- When creating a new project (initial README)
- Before release (CHANGELOG update)
- When user requests documentation updates
- During critical review (docs consistency check)

## Documentation Types

### README.md

**Purpose**: First point of contact for new users/developers

**Required Sections**:
- Project title and description
- Installation/setup instructions
- Basic usage examples
- Configuration options (if applicable)
- Contributing guidelines (or link)
- License

**Update Triggers**:
- New feature that changes usage
- Installation process changes
- Dependencies change significantly
- Project scope/purpose evolves

### CHANGELOG.md

**Purpose**: Track notable changes between versions

**Format** (Keep a Changelog standard):
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature X

### Changed
- Modified behavior Y

### Fixed
- Bug fix Z

### Removed
- Deprecated feature W

## [1.0.0] - YYYY-MM-DD

### Added
- Initial release features
```

**Update Triggers**:
- Any user-facing change
- Bug fixes
- Breaking changes (MUST document)
- Deprecations

### API Documentation

**Purpose**: Technical reference for developers

**Formats**:
- Inline docstrings (for code-level docs)
- OpenAPI/Swagger (for REST APIs)
- TypeDoc/JSDoc (for TypeScript/JavaScript)
- Sphinx/MkDocs (for Python)

**Update Triggers**:
- New public function/method/endpoint
- Parameter changes
- Return type changes
- Behavior changes

## Procedure

### Creating Documentation

1. **Identify audience**: Who will read this?
2. **Determine scope**: What must be covered?
3. **Check constitution**: Any doc-related constraints?
4. **Draft content**: Use appropriate template
5. **Review for accuracy**: Cross-check with code
6. **Update focus.md**: Note what was documented