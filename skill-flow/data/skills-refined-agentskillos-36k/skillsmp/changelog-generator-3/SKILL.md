---
name: changelog-generator
description: Generate beautiful CHANGELOG.md from git commits following Keep a Changelog format
allowed-tools: ["Bash", "Write", "Read"]
version: 1.0.0
author: GLINCKER Team
license: Apache-2.0
keywords: [changelog, documentation, git, versioning]
---

# Changelog Generator

Automatically generate CHANGELOG.md from git commit history following Keep a Changelog format. Groups changes by type, links commits, and maintains semantic versioning.

## What This Skill Does

- Parses git commit history
- Groups changes by type (Added, Changed, Fixed, etc.)
- Follows Keep a Changelog format
- Links to commits and PRs
- Supports conventional commits
- Updates existing CHANGELOG.md

## Instructions

### Phase 1: Analyze Git History

```bash
# Get commits since last release
git log v1.0.0..HEAD --pretty=format:"%H|%s|%an|%ad" --date=short

# Or all commits if no releases
git log --pretty=format:"%H|%s|%an|%ad" --date=short
```

### Phase 2: Parse Commit Messages

Detect commit types (Conventional Commits):

```
feat: Add user authentication → Added
fix: Resolve login bug → Fixed
docs: Update README → Documentation
refactor: Simplify auth logic → Changed
perf: Optimize database queries → Changed
test: Add unit tests → Testing
chore: Update dependencies → Maintenance
```

### Phase 3: Generate CHANGELOG

**Format (Keep a Changelog)**:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- User authentication with JWT tokens [#42](https://github.com/user/repo/pull/42)
- Password reset functionality [@johndoe](https://github.com/johndoe) [abc123](https://github.com/user/repo/commit/abc123)
- Two-factor authentication support

### Changed
- Improved error handling in API endpoints
- Updated UI components to use new design system
- Refactored database connection pooling

### Fixed
- Login button not working on mobile devices [#38](https://github.com/user/repo/issues/38)
- Memory leak in background job processor
- SQL injection vulnerability in search endpoint

### Security
- Updated dependencies with known vulnerabilities
- Implemented rate limiting on auth endpoints
- Added CSRF protection

## [1.2.0] - 2025-01-10

### Added
- Dark mode support
- Export data to CSV functionality

### Fixed
- Cache invalidation issue
- Timezone handling in date picker

## [1.1.0] - 2025-01-05

### Added
- User profile customization
- Email notifications

### Changed
- Improved performance of dashboard queries

## [1.0.0] - 2025-01-01

### Added
- Initial release
- Core functionality
- Basic user management
- API endpoints

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

## Change Categories

### Added
- New features
- New functionality
- New endpoints

### Changed
- Changes in existing functionality
- Refactoring
- Performance improvements
- UI/UX updates

### Deprecated
- Soon-to-be removed features
- Marked for removal

### Removed
- Removed features
- Deleted functionality

### Fixed
- Bug fixes
- Issue resolutions
- Error corrections

### Security
- Security patches
- Vulnerability fixes
- Security improvements

## Conventional Commits Support

Automatically categorize based on prefix:

```
feat:     → Added
fix:      → Fixed
docs:     → Documentation
style:    → Changed
refactor: → Changed
perf:     → Changed
test:     → Testing
build:    → Build
ci:       → CI/CD
chore:    → Maintenance
revert:   → Reverted
```

## Advanced Features

### Link to Issues/PRs

```markdown
### Fixed
- Login bug (#42)           → Links to issue
- API timeout (PR #45)      → Links to PR
- Memory leak [abc123]      → Links to commit
```

### Breaking Changes

```markdown
## [2.0.0] - 2025-01-15

### ⚠️ BREAKING CHANGES
- Removed support for Node.js 14
- Changed API response format for /users endpoint
- Renamed environment variable `API_KEY` to `APP_API_KEY`

### Migration Guide
1. Update Node.js to version 18 or higher
2. Update API client to handle new response format
3. Rename environment variables in .env file
```

### Semantic Version Detection

Based on changes:
- **Major (X.0.0)**: Breaking changes
- **Minor (0.X.0)**: New features (backward compatible)
- **Patch (0.0.X)**: Bug fixes only

## Tool Requirements

- **Bash**: Execute git commands
- **Write**: Create/update CHANGELOG.md
- **Read**: Read existing CHANGELOG

## Examples

### Example 1: Generate from Scratch

**User**: "Generate CHANGELOG from git history"

**Output**:
```markdown
# Changelog

## [Unreleased]

### Added
- 15 new features

### Fixed
- 8 bug fixes

### Changed
- 12 improvements

(Full detailed changelog)
```

### Example 2: Update Existing

**User**: "Update CHANGELOG with latest commits"

**Process**:
1. Read existing CHANGELOG.md
2. Get commits since last version
3. Add to [Unreleased] section
4. Preserve existing entries

### Example 3: Release Version

**User**: "Generate CHANGELOG for v2.0.0 release"

**Process**:
1. Move [Unreleased] to [2.0.0]
2. Add release date
3. Create new [Unreleased] section
4. Update comparison links

## Best Practices

1. **Conventional Commits**: Use consistent commit message format
2. **Detailed Messages**: Write descriptive commit messages
3. **Link Issues**: Reference issues/PRs in commits
4. **Regular Updates**: Update CHANGELOG with each release
5. **Breaking Changes**: Always document breaking changes prominently

## Changelog

### Version 1.0.0
- Initial release
- Conventional Commits support
- Keep a Changelog format
- Issue/PR linking
- Breaking changes detection

## Author

**GLINCKER Team**
- Repository: [claude-code-marketplace](https://github.com/GLINCKER/claude-code-marketplace)
