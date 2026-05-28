# Changelog Guide

## Keep a Changelog Format

Based on [keepachangelog.com](https://keepachangelog.com/).

### Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature X that does Y

### Changed
- Improved performance of Z by 50%

### Deprecated
- Old API endpoint `/v1/foo` (use `/v2/foo` instead)

### Removed
- Support for Node.js 16

### Fixed
- Bug where users couldn't log in with special characters

### Security
- Updated dependency A to fix CVE-2024-1234

## [1.2.0] - 2024-01-15

### Added
- User profile pictures
- Dark mode support

### Fixed
- Memory leak in websocket handler

## [1.1.0] - 2024-01-01

### Added
- Initial release

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/releases/tag/v1.1.0
```

## Change Types

| Type | When to Use |
|------|-------------|
| **Added** | New features, endpoints, options |
| **Changed** | Changes to existing functionality |
| **Deprecated** | Features that will be removed |
| **Removed** | Features that were removed |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |

## Writing Good Entries

### Good Examples

```markdown
### Added
- User can now export data as CSV from the dashboard (#123)
- Support for PostgreSQL 16

### Changed
- Improved search performance by 3x for large datasets
- Login now requires email verification for new accounts

### Fixed
- Users with Unicode names can now log in successfully (#456)
- Memory usage no longer grows unbounded during file uploads
```

### Bad Examples

```markdown
### Added
- New feature          # Too vague
- Various improvements # What improvements?
- Bug fixes            # Should be under Fixed

### Changed
- Updated dependencies # Which ones? Breaking?
- Code cleanup         # Not user-facing, don't include
```

## Best Practices

### Do

- Write for users, not developers
- Link to issues/PRs where appropriate
- Use past tense ("Added", not "Add")
- Group related changes together
- Include migration notes for breaking changes
- Date each release (YYYY-MM-DD)

### Don't

- Include internal refactoring (unless it affects users)
- Use technical jargon users won't understand
- Leave [Unreleased] empty (add as you go)
- Skip versions or dates
- Include the same item in multiple categories

## Breaking Changes

```markdown
## [2.0.0] - 2024-02-01

### Changed
- **BREAKING**: `getUserById()` now returns `null` instead of throwing
  when user not found. Update error handling accordingly.
- **BREAKING**: Minimum Node.js version is now 18 (was 16)

### Removed
- **BREAKING**: Removed deprecated `legacyLogin()` method.
  Use `login()` instead.

### Migration Guide

1. Update Node.js to version 18+
2. Replace `legacyLogin()` calls with `login()`
3. Update error handling for `getUserById()`:
   ```javascript
   // Before
   try {
     const user = getUserById(id);
   } catch (e) {
     // handle not found
   }

   // After
   const user = getUserById(id);
   if (!user) {
     // handle not found
   }
   ```
```

## Automation

### Conventional Commits

Use with tools like `standard-version` or `semantic-release`:

```bash
# Commit messages that generate changelog
feat: add user profile pictures
fix: resolve login issue with special characters
feat!: change getUserById to return null

# Generate changelog
npx standard-version
```

### GitHub Releases

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          body_path: CHANGELOG.md
          generate_release_notes: true
```

## Tools

```bash
# Generate from git commits
npx standard-version          # Node.js
npx conventional-changelog    # More options

# Validate changelog format
npx changelog-lint CHANGELOG.md

# Auto-generate from conventional commits
npx semantic-release
```

## Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

[Unreleased]: https://github.com/OWNER/REPO/compare/v0.0.1...HEAD
```
