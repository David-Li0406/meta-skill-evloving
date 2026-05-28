---
name: release-standards
description: Use this skill when preparing for a software release, updating version numbers, or writing changelogs.
---

# Release Standards

> **Language**: [English](../../../../../skills/claude-code/release-standards/SKILL.md) | 繁體中文

**Version**: 1.1.0  
**Last Updated**: 2026-01-02  
**Applicable Scope**: Claude Code Skills

## Purpose

This skill provides standards for semantic versioning and changelog formatting.

## Quick Reference

### Semantic Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
2.3.1
1.0.0-alpha.1
3.2.0-beta.2+20250112
```

### Version Increment Rules

| Component | When to Increment | Example |
|-----------|-------------------|---------|
| **MAJOR** | Major changes | 1.9.5 → 2.0.0 |
| **MINOR** | New features (backward compatible) | 2.3.5 → 2.4.0 |
| **PATCH** | Bug fixes (backward compatible) | 3.1.2 → 3.1.3 |

### Pre-release Identifiers

| Identifier | Stability | Target Audience |
|------------|-----------|-----------------|
| `alpha`    | Unstable  | Internal teams   |
| `beta`     | Generally stable | Early adopters |
| `rc`       | Stable    | Beta testers     |

### CHANGELOG Categories

| Category   | Purpose |
|------------|---------|
| **Added**  | New features |
| **Changed**| Changes to existing features |
| **Deprecated** | Features that will be removed in the future |
| **Removed** | Features that have been removed |
| **Fixed**  | Bug fixes |
| **Security**| Security vulnerability fixes |

## Detailed Guide

For complete standards, please refer to:
- [Semantic Versioning Guide](./semantic-versioning.md)
- [Changelog Format](./changelog-format.md)
- [Release Workflow Guide](./release-workflow.md) - Complete release process for this project

## CHANGELOG Entry Format

```markdown
## [VERSION] - YYYY-MM-DD

### Added
- Add user dashboard with customizable widgets (#123)

### Changed
- **BREAKING**: Change API response format from XML to JSON

### Fixed
- Fix memory leak when processing large files (#456)

### Security
- Fix SQL injection vulnerability (CVE-2025-12345)
```

## Major Changes

Use the **BREAKING** prefix to indicate major changes:

```markdown
### Changed
- **BREAKING**: Remove deprecated `getUserById()`, use `getUser()` instead
```

## Git Tags

```bash
# Create annotated tag (recommended)
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push tag to remote
git push origin v1.2.0
```

## Version Sorting

```
1.0.0-alpha.1 < 1.0.0-alpha.2 < 1.0.0-beta.1 < 1.0.0-rc.1 < 1.0.0
```

---

## Configuration Detection

This skill supports project-specific configurations.

### Detection Order

1. Check the "Disabled Skills" section in `CONTRIBUTING.md`
   - If this skill is listed, it is disabled for that project.
2. Check the "Release Standards" section in `CONTRIBUTING.md`
3. If not found, **default to using semantic versioning and Keep a Changelog format**.

### Initial Setup

If no configuration is found and context is unclear:

1. Ask the user: "This project has not configured release standards. Would you like to use semantic versioning?"
2. Based on the user's choice, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Release Standards

### Versioning
This project uses **Semantic Versioning** (MAJOR.MINOR.PATCH).

### Changelog
This project follows **Keep a Changelog** format.
```