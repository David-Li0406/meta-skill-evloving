---
name: changelog-guide
description: Use this skill when you need to write and maintain a CHANGELOG.md file following the Keep a Changelog format, ensuring clear communication of changes to users.
---

# Changelog Guide

## Purpose

This skill helps you write and maintain a CHANGELOG.md file according to the Keep a Changelog format, ensuring that changes are clearly communicated to users.

## Quick Reference

### File Structure

```markdown
# Changelog

All significant changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.2.0] - 2025-12-15

### Added
- Description of the feature

### Changed
- Description of the change

### Fixed
- Description of the bug fix

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

### Change Categories

| Category | When to Use | Example |
|----------|-------------|---------|
| **Added** | New features | Added support for dark mode |
| **Changed** | Modifications to existing functionality | Improved search performance by 50% |
| **Deprecated** | Features that will be removed in the future | Deprecated legacyParse() |
| **Removed** | Features that have been removed | Removed support for Node.js 14 |
| **Fixed** | Bug fixes | Fixed login timeout issue |
| **Security** | Security fixes | Fixed XSS vulnerability |

### Commit Type Correspondence to Changelog

| Commit Type | Changelog Category | Notes |
|-------------|--------------------|-------|
| `feat` | **Added** | New feature |
| `fix` | **Fixed** | Bug fix |
| `perf` | **Changed** | Performance improvement |
| `security` | **Security** | Security fix |
| `BREAKING CHANGE` | **Changed** or **Removed** | Prefix with **BREAKING** |
| `refactor`, `docs`, `style`, `test`, `chore` | *(usually omitted)* | No impact on users |

## Entry Format

### Standard Format

```markdown
- [Action verb] [Change content] ([Reference])
```

### Examples

```markdown
### Added
- Added customizable user dashboard (#123)
- Added support for PostgreSQL 15 (PR #456)

### Changed
- **BREAKING**: API response format changed from XML to JSON (#789)
- Updated minimum Node.js version to 18.0 (#101)

### Fixed
- Fixed memory leak when handling large files (#112)
- Fixed date format error in reports (#134)

### Security
- Fixed SQL injection vulnerability in search endpoint (high risk, CVE-2025-12345)
```

## Detailed Guide

For complete standards, please refer to:
- [Changelog Standards](../../../core/changelog-standards.md)

### AI Optimized Format (Token Saving)

AI assistants can use YAML format files to reduce token usage:
- Basic standard: `ai/standards/changelog.ai.yaml`

## Writing Guidelines

### Write for Users, Not Developers

| ✅ Good | ❌ Bad | Reason |
|---------|--------|--------|
| Added dark mode theme option | Implemented ThemeProvider using context | Benefits visible to users |
| Fixed login timeout on slow networks | Fixed race condition in AuthService | Impact description |
| Page load speed improved by 40% | Optimized SQL queries using indexing | Quantifiable results |

### Breaking Changes

Be sure to clearly mark breaking changes:

```markdown
### Changed
- **BREAKING**: Removed deprecated `getUserById()` method, please use `getUser()`
- **BREAKING**: Configuration file format changed from YAML to TOML

### Removed
- **BREAKING**: Removed No
```