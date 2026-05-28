# Keep a Changelog Format Specification

Reference guide for the Keep a Changelog format used in changelog generation.

## Overview

Keep a Changelog is a specification for changelog files that emphasizes human readability and machine parseability. The official specification is maintained at [keepachangelog.com](https://keepachangelog.com/).

## Core Principles

### 1. Changelogs are for Humans

Changelogs should be written for humans to read, not machines. While machine-parseability is valuable, human readability is the primary goal.

**Good:**
```markdown
### Added
- User authentication via OAuth2 for improved security
```

**Bad:**
```markdown
### Added
- feat(auth): impl oauth2 (PR #123)
```

### 2. One Entry Per Version

Each version gets its own section with all changes grouped under that version.

### 3. Reverse Chronological Order

Latest versions appear first (top of file). Within a version, latest changes appear first.

### 4. Date Format

Always use ISO 8601 format: YYYY-MM-DD

### 5. Semantic Versioning

Versions should follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality
- PATCH version for backwards-compatible bug fixes

## File Structure

### Header

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

### Unreleased Section

Always maintain an `[Unreleased]` section at the top for upcoming changes:

```markdown
## [Unreleased]

### Added
- New features that haven't been released yet

### Fixed
- Bug fixes pending release
```

**Rules:**
- Always maintain an `[Unreleased]` section at the top for upcoming changes
- Omit empty categories (only include categories that contain entries)
- Use standard category names and order

**Purpose:**
- Track work in progress
- Prepare for next release
- Provide visibility into upcoming changes

### Version Sections

Each released version follows this format:

```markdown
## [VERSION] - YYYY-MM-DD

### Category
- Change description
```

**Example:**
```markdown
## [1.2.0] - 2025-01-15

### Added
- User profile export to CSV format
- Dark mode toggle in settings

### Fixed
- Memory leak in background sync process
```

## Standard Categories

Keep a Changelog defines six standard categories:

### Added

**For new features.**

Examples:
```markdown
### Added
- User authentication via OAuth2
- Export functionality for reports
- Dark mode support
- Real-time notifications
```

**When to use:**
- New user-facing features
- New API endpoints
- New configuration options
- New documentation sections

### Changed

**For changes in existing functionality.**

Examples:
```markdown
### Changed
- Updated user dashboard layout for better usability
- Improved search algorithm for faster results
- Modified API response format to include timestamps
```

**When to use:**
- Modifications to existing features
- UI/UX improvements
- Performance optimizations
- API changes that maintain compatibility
- Behavior changes

### Deprecated

**For soon-to-be removed features.**

Examples:
```markdown
### Deprecated
- Old authentication API (use OAuth2 instead)
- Legacy CSV export format (will be removed in v3.0.0)
```

**When to use:**
- Features marked for future removal
- Old APIs that should no longer be used
- Legacy functionality being phased out

**Best practice:** Include migration guidance and removal timeline

### Removed

**For now removed features.**

Examples:
```markdown
### Removed
- Support for Internet Explorer 11
- Deprecated v1 authentication API
- Legacy XML export format
```

**When to use:**
- Removed features or functionality
- Dropped support for platforms/browsers
- Deleted APIs or endpoints

**Note:** Removals typically trigger a MAJOR version bump

### Fixed

**For bug fixes.**

Examples:
```markdown
### Fixed
- Crash when uploading files larger than 10MB
- Incorrect date formatting in reports
- Memory leak in background sync
- Race condition in concurrent requests
```

**When to use:**
- Bug fixes
- Crash fixes
- Data corruption fixes
- Logic errors

### Security

**For security vulnerability fixes.**

Examples:
```markdown
### Security
- Fixed SQL injection vulnerability in search endpoint
- Patched XSS vulnerability in user comments
- Updated dependencies to address CVE-2025-1234
```

**When to use:**
- Security vulnerability fixes
- Security-related dependency updates
- Security hardening changes

**Best practice:** Reference CVE numbers when applicable

## Advanced Formatting

### Links

Link version numbers to release tags or diff pages:

```markdown
## [1.2.0] - 2025-01-15

[1.2.0]: https://github.com/user/repo/releases/tag/v1.2.0
```

Or link to diff between versions:

```markdown
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

### Sub-items

Use sub-lists for additional context:

```markdown
### Added
- User authentication
  - OAuth2 support for Google, GitHub, and Microsoft
  - Two-factor authentication via TOTP
  - Password reset via email
```

### Breaking Changes

Highlight breaking changes prominently:

```markdown
### Changed
- **BREAKING**: Modified API response format to use snake_case instead of camelCase
- **BREAKING**: Renamed `getUsers()` method to `fetchUsers()`
```

Or use a separate section:

```markdown
### Breaking Changes
- Modified API response format to use snake_case
- Renamed `getUsers()` method to `fetchUsers()`
```

### Contributors

Optionally acknowledge contributors:

```markdown
### Added
- User profile export feature (@username)
- Dark mode support (thanks @contributor)
```

## Version Numbering

### Unreleased Changes

Use `[Unreleased]` for changes not yet released:

```markdown
## [Unreleased]

### Added
- Feature pending release
```

### Initial Release

First public release:

```markdown
## [0.1.0] - 2025-01-15

### Added
- Initial release
```

### Pre-releases

Use semver pre-release notation:

```markdown
## [1.0.0-rc.1] - 2025-01-15
## [1.0.0-beta.2] - 2025-01-10
## [1.0.0-alpha.1] - 2025-01-05
```

### Yanked Releases

Mark withdrawn releases:

```markdown
## [1.2.0] - 2025-01-15 [YANKED]

### Security
- Critical security flaw (DO NOT USE)
```

## Complete Example

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Real-time collaboration features

### Changed
- Improved dashboard performance

## [1.2.0] - 2025-01-15

### Added
- User profile export to CSV and JSON formats
- Dark mode toggle in user settings
- Keyboard shortcuts for common actions

### Changed
- Updated user dashboard layout for better mobile experience
- Improved search performance by 50%

### Fixed
- Memory leak in background sync process
- Incorrect timezone handling in reports

## [1.1.0] - 2025-01-01

### Added
- User authentication via OAuth2 (Google, GitHub, Microsoft)
- Two-factor authentication support

### Changed
- Migrated to new API v2 endpoints

### Deprecated
- API v1 endpoints (will be removed in v2.0.0)

### Security
- Fixed XSS vulnerability in user comments

## [1.0.0] - 2024-12-15

### Added
- Initial stable release
- User management
- Report generation
- Data export functionality

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

## Best Practices

### Do:
- ✓ Write for humans, not machines
- ✓ Keep descriptions concise but informative
- ✓ Group related changes together
- ✓ Use consistent tense (past tense recommended)
- ✓ Include context when helpful
- ✓ Highlight breaking changes prominently
- ✓ Use ISO 8601 date format (YYYY-MM-DD)

### Don't:
- ✗ Dump raw commit messages
- ✗ Include internal/irrelevant changes (refactoring, test updates)
- ✗ Use vague descriptions ("Various fixes")
- ✗ Mix changes from different versions
- ✗ Forget to update the Unreleased section
- ✗ Use inconsistent formatting

## Category Selection Guide

| Change Type | Category | Example |
|------------|----------|---------|
| New feature | Added | "User authentication via OAuth2" |
| Feature modification | Changed | "Updated dashboard layout" |
| Performance improvement | Changed | "Improved search speed by 50%" |
| UI/UX update | Changed | "Redesigned settings page" |
| Bug fix | Fixed | "Fixed crash on file upload" |
| Security fix | Security | "Patched XSS vulnerability" |
| Feature removal | Removed | "Removed support for IE11" |
| Future removal notice | Deprecated | "Old API (use v2 instead)" |
| Breaking change | Changed (with BREAKING) | "**BREAKING**: Renamed getUsers() method" |
| Dependency update (user-facing) | Changed | "Updated to Node.js 18" |
| Dependency update (security) | Security | "Updated library to fix CVE-2025-1234" |
| Documentation | Added/Changed | Generally not included unless significant |
| Internal changes | - | Not included in changelog |

## Automation Considerations

When generating changelogs programmatically:

1. **Parse commit messages**: Extract type and description from conventional commits
2. **Map to categories**: feat → Added, fix → Fixed, etc.
3. **Filter noise**: Exclude chore, style, test, refactor (unless significant)
4. **Detect breaking changes**: Look for `BREAKING CHANGE:` or `!` in commit type
5. **Group by scope**: Consider grouping changes by affected component
6. **Preserve manual edits**: Don't overwrite hand-written sections
7. **Human review**: Always allow human editing before publishing

## References

- Official specification: https://keepachangelog.com/
- Semantic Versioning: https://semver.org/
- Conventional Commits: https://www.conventionalcommits.org/
