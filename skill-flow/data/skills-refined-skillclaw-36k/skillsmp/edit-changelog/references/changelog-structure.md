# Changelog Structure Reference

Comprehensive reference for Keep a Changelog format and structure conventions.

## Keep a Changelog Specification

### Official Format

Keep a Changelog defines a standardized format for maintaining changelogs that is both human-readable and machine-parseable.

**Official site:** https://keepachangelog.com/

**Current version:** 1.1.0 (as of this document)

---

## Document Structure

### Complete Structure Hierarchy

```
CHANGELOG.md
├── Header
│   ├── Title (# Changelog)
│   └── Preamble (format references)
├── Unreleased Section
│   ├── Section header (## [Unreleased])
│   └── Categories
│       ├── ### Added
│       ├── ### Changed
│       ├── ### Deprecated
│       ├── ### Removed
│       ├── ### Fixed
│       └── ### Security
├── Version Sections (repeating)
│   ├── Section header (## [VERSION] - DATE)
│   └── Categories
│       └── (same as Unreleased)
└── Link References (optional)
    ├── [Unreleased]: URL
    └── [VERSION]: URL
```

---

## Header Section

### Minimal Header

```markdown
# Changelog
```

**Single H1 heading at the top of the file.**

### Standard Header

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

**Components:**
- Title: "# Changelog"
- Purpose statement
- Format reference (Keep a Changelog)
- Versioning reference (Semantic Versioning)

### Extended Header

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## How to Use This Changelog

- **Users:** Check the [Unreleased] section for upcoming features
- **Developers:** Add changes to [Unreleased] under appropriate categories
- **Maintainers:** Move [Unreleased] changes to new version sections when releasing

## Categories

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for removed features
- **Fixed** for bug fixes
- **Security** for vulnerability fixes
```

**Additional sections:**
- Usage instructions
- Category definitions
- Contribution guidelines

**Note:** Extended headers are optional. Standard header recommended for simplicity.

---

## Unreleased Section

### Purpose

The `[Unreleased]` section tracks changes that have been made but not yet released.

**Benefits:**
- Visibility into upcoming changes
- Easy preparation for next release
- Clear separation of released vs. unreleased work

### Format

```markdown
## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
```

**Rules:**
- Always present at the top (after header, before versions)
- Always uses `[Unreleased]` as the section name
- Never has a date
- Contains only categories with entries (empty categories are omitted)

### With Content

```markdown
## [Unreleased]

### Added
- User profile export to CSV format
- Real-time collaboration features

### Changed
- Improved dashboard performance by 50%

### Fixed
- Memory leak in background sync process
```

### Empty Unreleased Section

**Option 1: Remove empty categories (Recommended)**
```markdown
## [Unreleased]

_No unreleased changes yet._
```

**Option 2: Minimal (most concise)**
```markdown
## [Unreleased]
```

---

## Version Sections

### Format

```markdown
## [VERSION] - YYYY-MM-DD

### Category
- Change description
```

**Components:**
- `VERSION`: Semantic version number (e.g., "1.2.0", "0.9.1-beta")
- `YYYY-MM-DD`: Release date in ISO 8601 format
- Categories and entries

### Examples

**Stable release:**
```markdown
## [1.2.0] - 2025-01-15

### Added
- OAuth2 authentication support
- Dark mode toggle

### Fixed
- Login timeout bug
```

**Pre-release:**
```markdown
## [2.0.0-rc.1] - 2025-01-15

### Added
- Complete redesign of user interface

### Changed
- **BREAKING**: New API format (see migration guide)
```

**Patch release:**
```markdown
## [1.1.1] - 2025-01-15

### Fixed
- Critical security vulnerability in authentication
```

**Yanked release:**
```markdown
## [1.2.0] - 2025-01-15 [YANKED]

### Added
- Feature with critical bug

### Security
- DO NOT USE - contains security vulnerability
```

---

## Category Sections

### Standard Categories

Keep a Changelog defines exactly six categories:

1. **Added** - New features
2. **Changed** - Changes in existing functionality
3. **Deprecated** - Soon-to-be removed features
4. **Removed** - Removed features
5. **Fixed** - Bug fixes
6. **Security** - Security vulnerability fixes

**Order matters:** Always use this order in changelogs.

### Added

**For new features and capabilities.**

**Format:**
```markdown
### Added
- Feature description
- Another feature
```

**Examples:**
```markdown
### Added
- User authentication via OAuth2
- Export reports to CSV and JSON formats
- Dark mode toggle in user settings
- Keyboard shortcuts for common actions
- API endpoint for bulk user operations
```

**Language:**
- Use past tense: "Added" not "Add"
- Or use present tense consistently: "Add" not "Added"
- Focus on user-visible features

### Changed

**For changes in existing functionality.**

**Format:**
```markdown
### Changed
- Change description
- **BREAKING**: Breaking change description
```

**Examples:**
```markdown
### Changed
- Updated user dashboard layout for better mobile experience
- Improved search algorithm for 50% faster results
- Modified API response format to include metadata
- **BREAKING**: Renamed `getUser()` method to `fetchUser()`
- **BREAKING**: Changed authentication to require OAuth2 tokens
```

**Breaking changes:**
- Prefix with `**BREAKING**:`
- Describe what broke and how to migrate
- Breaking changes trigger MAJOR version bump

### Deprecated

**For soon-to-be removed features.**

**Format:**
```markdown
### Deprecated
- Feature name (will be removed in VERSION)
- Another deprecated feature
```

**Examples:**
```markdown
### Deprecated
- API v1 endpoints (will be removed in v3.0.0)
- Legacy CSV export format (use JSON export instead)
- Old authentication method (migrate to OAuth2)
```

**Best practices:**
- Always include removal timeline
- Provide migration path or alternative
- Reference version when feature will be removed

### Removed

**For features that have been removed.**

**Format:**
```markdown
### Removed
- Feature that was removed
```

**Examples:**
```markdown
### Removed
- Support for Internet Explorer 11
- Deprecated API v1 endpoints
- Legacy XML export format
- Old authentication method
```

**Note:**
- Removals often constitute breaking changes
- Usually trigger MAJOR version bump
- Should have been in Deprecated section of previous version

### Fixed

**For bug fixes.**

**Format:**
```markdown
### Fixed
- Bug description
- Another bug fix
```

**Examples:**
```markdown
### Fixed
- Crash when uploading files larger than 10MB
- Incorrect date formatting in exported reports
- Memory leak in background synchronization
- Race condition in concurrent API requests
- Login timeout after 5 minutes of inactivity
```

**Best practices:**
- Describe the problem, not the implementation
- User-facing description, not technical details
- Include issue references if helpful

### Security

**For security vulnerability fixes.**

**Format:**
```markdown
### Security
- Vulnerability description
- CVE references if applicable
```

**Examples:**
```markdown
### Security
- Fixed SQL injection vulnerability in search endpoint
- Patched XSS vulnerability in user-generated content
- Updated dependencies to address CVE-2025-1234
- Resolved authentication bypass in password reset flow
```

**Best practices:**
- Reference CVE numbers when available
- Be specific enough for users to understand impact
- Don't reveal exploit details that could aid attackers
- Security fixes typically warrant immediate patch releases

---

## Entry Formatting

### Bullet Points

**Standard format:**
```markdown
### Category
- Entry text
- Another entry
```

**Rules:**
- Use dash (`-`) for bullet points
- One space after dash
- One entry per line
- Start with capital letter
- End without period (or use periods consistently)

### Multi-line Entries

**With context:**
```markdown
### Added
- User authentication
  - OAuth2 support for Google, GitHub, and Microsoft
  - Two-factor authentication via TOTP
  - Session management with automatic timeout
```

**Format:**
- Main entry at level 1 (single dash)
- Sub-items indented 2 spaces
- Sub-items use same dash format

### Links in Entries

**Issue references:**
```markdown
### Fixed
- Login timeout bug (#123)
- Memory leak in sync process (#456)
```

**Pull request references:**
```markdown
### Added
- OAuth2 authentication (PR #789)
```

**External links:**
```markdown
### Changed
- Updated to [React 18](https://reactjs.org/blog/2022/03/29/react-v18.html)
```

### Breaking Changes

**Inline format:**
```markdown
### Changed
- **BREAKING**: Renamed `getUser()` method to `fetchUser()`
```

**With explanation:**
```markdown
### Changed
- **BREAKING**: Modified authentication to use OAuth2 tokens instead of API keys
  - See [migration guide](./docs/migration-v2.md) for details
  - Old API keys will be deprecated on 2025-03-01
```

---

## Link References

### Purpose

Link version numbers to release pages or diffs.

**Format:**
```markdown
[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

**Placement:** At the bottom of the file, after all version sections.

### Link Formats

**Unreleased (compare with latest version):**
```markdown
[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
```

**Version diff (compare with previous version):**
```markdown
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

**Release page:**
```markdown
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

**GitLab:**
```markdown
[Unreleased]: https://gitlab.com/user/repo/-/compare/v1.2.0...main
[1.2.0]: https://gitlab.com/user/repo/-/compare/v1.1.0...v1.2.0
```

**Bitbucket:**
```markdown
[Unreleased]: https://bitbucket.org/user/repo/branches/compare/main%0Dv1.2.0
[1.2.0]: https://bitbucket.org/user/repo/branches/compare/v1.2.0%0Dv1.1.0
```

---

## Complete Example

### Full Changelog Example

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Real-time collaboration features
- Offline mode support

### Changed
- Improved dashboard load time by 50%

## [1.2.0] - 2025-01-15

### Added
- User profile export to CSV and JSON formats
- Dark mode toggle in user settings
- Keyboard shortcuts for common actions

### Changed
- Updated user dashboard layout for better mobile experience
- Improved search performance by optimizing database queries

### Fixed
- Memory leak in background sync process
- Incorrect timezone handling in report generation

### Security
- Updated dependencies to address CVE-2025-1234

## [1.1.0] - 2025-01-01

### Added
- OAuth2 authentication support
- Two-factor authentication

### Changed
- Migrated API from v1 to v2 format

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

### Changed
- **BREAKING**: Redesigned API for better performance

## [0.9.0] - 2024-12-01

### Added
- Beta release
- Core features implementation

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/user/repo/releases/tag/v0.9.0
```

---

## Validation Rules

### Structural Validation

**Required elements:**
- [ ] H1 header: `# Changelog`
- [ ] Unreleased section: `## [Unreleased]`
- [ ] At least one version or unreleased content

**Optional elements:**
- [ ] Preamble text
- [ ] Link references
- [ ] Version sections

### Formatting Validation

**Date format:**
- [ ] Dates use ISO 8601: `YYYY-MM-DD`
- [ ] No other date formats accepted

**Version format:**
- [ ] Versions follow Semantic Versioning
- [ ] Format: `MAJOR.MINOR.PATCH` or `MAJOR.MINOR.PATCH-prerelease`

**Category order:**
- [ ] Categories appear in standard order:
  1. Added
  2. Changed
  3. Deprecated
  4. Removed
  5. Fixed
  6. Security

### Content Validation

**Entry format:**
- [ ] Bullet points use dash: `-`
- [ ] One space after dash
- [ ] Entries are clear and concise
- [ ] Breaking changes prefixed with `**BREAKING**:`

---

## Version Ordering

### Chronological Order

**Rule:** Versions appear in reverse chronological order (newest first).

**Correct:**
```markdown
## [Unreleased]
## [2.0.0] - 2025-02-01
## [1.2.0] - 2025-01-15
## [1.1.0] - 2025-01-01
## [1.0.0] - 2024-12-15
```

**Incorrect:**
```markdown
## [1.0.0] - 2024-12-15
## [1.1.0] - 2025-01-01
## [1.2.0] - 2025-01-15
```

### Pre-release Ordering

**Rule:** Pre-releases appear before their stable version.

**Correct:**
```markdown
## [2.0.0] - 2025-02-01
## [2.0.0-rc.2] - 2025-01-29
## [2.0.0-rc.1] - 2025-01-22
## [2.0.0-beta.1] - 2025-01-15
## [1.2.0] - 2025-01-01
```

---

## Anti-Patterns

### Don't: Dump Git Logs

**Bad:**
```markdown
### Changed
- feat(auth): add OAuth2
- fix: null pointer exception
- chore: update dependencies
- refactor: extract validation
```

**Good:**
```markdown
### Added
- OAuth2 authentication support

### Fixed
- Crash when processing null data
```

### Don't: Use Vague Descriptions

**Bad:**
```markdown
### Changed
- Various improvements
- Bug fixes
- Updates
```

**Good:**
```markdown
### Changed
- Improved search performance by 50%

### Fixed
- Login timeout after 5 minutes
```

### Don't: Mix Versions

**Bad:**
```markdown
## [1.2.0] - 2025-01-15

### Added
- Feature A (released in 1.2.0)
- Feature B (will be in 1.3.0)
```

**Good:**
```markdown
## [Unreleased]

### Added
- Feature B

## [1.2.0] - 2025-01-15

### Added
- Feature A
```

### Don't: Skip Dates

**Bad:**
```markdown
## [1.2.0]

### Added
- OAuth2 authentication
```

**Good:**
```markdown
## [1.2.0] - 2025-01-15

### Added
- OAuth2 authentication
```

---

## References

- Official Keep a Changelog: https://keepachangelog.com/
- Semantic Versioning: https://semver.org/
- ISO 8601 Date Format: https://www.iso.org/iso-8601-date-and-time-format.html
- CommonMark Markdown Spec: https://spec.commonmark.org/
