---
title: "Changelog"
description: "Complete version history and release notes for [Product Name]"
type: changelog
category: releases
status: published
created: YYYY-MM-DD
lastUpdated: YYYY-MM-DD
---


All notable changes to [Product Name] are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- [New feature description]
- [New feature description]

### Changed

- [Changed feature description]
- [Changed feature description]

### Deprecated

- [Deprecated feature description]

### Removed

- [Removed feature description]

### Fixed

- [Bug fix description]
- [Bug fix description]

### Security

- [Security fix description]

## [X.Y.Z] - YYYY-MM-DD

### Added

- **[Feature Name]** - [Description of what was added and why it's useful]
  - [Sub-feature or detail]
  - [Sub-feature or detail]
- **[Feature Name]** - [Description]

### Changed

- **[Feature Name]** - [Description of what changed and why]
  - **Breaking Change**: [If applicable, describe what breaks]
  - **Migration**: [How to migrate from previous version]
- **[Feature Name]** - [Description]

### Deprecated

- **[Feature Name]** - [What's deprecated and what to use instead]
  - **Timeline**: Will be removed in version [X.Y.Z]
  - **Alternative**: Use [[New Feature]](/docs/[feature]) instead

### Removed

- **[Feature Name]** - [What was removed and why]
  - **Reason**: [Explanation]
  - **Alternative**: Use [[Replacement]](/docs/[replacement])

### Fixed

- **[Bug]** - [Description of bug fix]
  - **Issue**: [Link to issue if applicable]
  - **Impact**: [Who was affected]
- **[Bug]** - [Description]

### Security

- **[Vulnerability]** - [Description of security fix]
  - **Severity**: [Critical/High/Medium/Low]
  - **CVE**: [CVE-YYYY-XXXXX if applicable]
  - **Impact**: [Who is affected]
  - **Action Required**: [What users need to do]

## [X.Y.Z] - YYYY-MM-DD

### Added

- **API v2 Endpoints** - New REST API endpoints for resource management
  - `GET /api/v2/resources` - List all resources
  - `POST /api/v2/resources` - Create new resource
  - Rate limiting: 1000 requests/hour
- **CLI Export Command** - Export data in multiple formats
  - Supports JSON, CSV, and XML formats
  - Usage: `[product] export --format json`

### Changed

- **Configuration Format** - Updated from JSON to YAML for better readability
  - **Breaking Change**: Old JSON config files no longer supported
  - **Migration**: Run `[product] migrate-config` to convert
  - See [[Configuration Guide]](/docs/guides/configuration) for new format

### Fixed

- **Memory Leak** - Fixed memory leak in long-running processes
  - **Issue**: [#123](https://github.com/example/issues/123)
  - **Impact**: Affected users with processes running >24 hours
  - **Solution**: Improved garbage collection in event loop

## [X.Y.Z] - YYYY-MM-DD

### Added

- Initial release of [Product Name]
- Core functionality:
  - [Feature 1]
  - [Feature 2]
  - [Feature 3]
- Basic CLI with commands: `init`, `run`, `stop`
- REST API with authentication
- Configuration via YAML file

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0) - Incompatible API changes
- **MINOR** version (0.X.0) - New functionality (backwards-compatible)
- **PATCH** version (0.0.X) - Bug fixes (backwards-compatible)

## Categories

Changes are grouped by category:

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security fixes

## Release Schedule

New releases follow this schedule:

- **Major releases** - Every 12 months
- **Minor releases** - Every 2-3 months
- **Patch releases** - As needed for critical fixes

## Breaking Changes

Breaking changes are clearly marked with **Breaking Change** labels and include:

- Description of what breaks
- Why the change was necessary
- Migration guide for updating

## Support Policy

- **Latest major version** - Full support (features + bug fixes + security)
- **Previous major version** - Limited support (critical bugs + security)
- **Older versions** - Security fixes only

See [[Support Policy]](/docs/support-policy) for details.

## Getting Updates

**Subscribe to releases**:

- Watch the [GitHub repository](https://github.com/example/[product])
- Subscribe to the [mailing list](https://example.com/updates)
- Follow [@product](https://twitter.com/product) on Twitter

**Upgrade guide**:

- [[Upgrading]](/docs/guides/upgrading) - General upgrade instructions
- [[Migration Guides]](/docs/migration) - Version-specific migration

## Links

- [GitHub Releases](https://github.com/example/[product]/releases)
- [Release Blog Posts](https://blog.example.com/category/releases)
- [Download Page](https://example.com/download)

---

[Unreleased]: https://github.com/example/[product]/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/example/[product]/compare/vX.Y.Z-1...vX.Y.Z
