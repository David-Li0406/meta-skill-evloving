# Changelog Guidelines

Critical rules for documenting changes that users actually care about.

## Table of Contents

- [Format Standards](#format-standards)
- [Sections Explained](#sections-explained)
- [Critical Rules](#critical-rules)
- [Common Mistakes](#common-mistakes)
- [Examples](#examples)
- [Multi-Component Changelogs](#multi-component-changelogs)

## Format Standards

### Required Structure

```markdown
# Changelog

All notable changes to this project documented here.

## [Unreleased]
### Added
- Feature in development

## [1.2.1] - 2026-01-21
### Fixed
- Bug description

## [1.2.0] - 2026-01-20
### Added
- New feature
```

### Date Format

Always use ISO format: `YYYY-MM-DD`

```
✓ 2026-01-21
✗ 01/21/2026
✗ Jan 21, 2026
✗ 21 January 2026
```

### Semantic Sections

| Section | When to Use | Example |
|---------|-------------|---------|
| **Added** | New user-facing feature, command, capability | "Add webhook support", "Add PDF export" |
| **Changed** | Existing behavior modified (backward compatible) | "Improved error messages", "Reorganized navigation" |
| **Deprecated** | Feature marked for future removal | "Deprecate old API, use new method instead" |
| **Removed** | Deprecated feature now gone | "Remove old API" |
| **Fixed** | Bug fixes | "Fix timeout in requests", "Fix memory leak" |
| **Security** | Vulnerability patches | "Fix XSS vulnerability in sanitizer", "Fix SQL injection in query builder" |

## Sections Explained

### Added

**What:** New features, commands, or capabilities users can now use.

**Trigger questions:**
- Can a user do something NEW that wasn't possible before?
- Is this a new command, flag, or interface?
- Does this expand what the tool can do?

**Examples:**
```markdown
### Added
- Support for encrypted message transport
- New `--dry-run` flag for preview mode
- Webhook endpoints for real-time notifications
- Export to PDF format
- API v2 with GraphQL support
```

**NOT Added:**
- Internal refactoring (users don't see it)
- Code cleanup
- Performance optimization without user-visible change
- Developer API changes that don't affect users

### Changed

**What:** Existing behavior modified in a backward-compatible way.

**Trigger questions:**
- Did something work BEFORE but works DIFFERENTLY now?
- Is the change backward compatible?
- Will users need to know about this?

**Examples:**
```markdown
### Changed
- Improved error messages with actionable suggestions
- Reorganized settings panel for better discoverability
- Increased search timeout from 5s to 10s
- Updated dependencies for security patches
- Changed default output format to JSON (backward compatible)
```

**NOT Changed:**
- Bug fixes (use Fixed section)
- New features (use Added section)
- Breaking changes (use Changed + note as **BREAKING**)

### Fixed

**What:** Bug fixes that restore intended behavior.

**Trigger questions:**
- Was something broken?
- Is this restoring it to working state?
- Do users have a workaround they can now remove?

**Examples:**
```markdown
### Fixed
- Fix timeout bug in long-running queries
- Fix crash when uploading files > 1GB
- Fix incorrect sorting in results
- Fix memory leak in event listener cleanup
```

**NOT Fixed:**
- Refactoring that doesn't change behavior
- Documentation corrections (use Changed or leave out)
- Version number changes (never document these!)

### Removed

**What:** Features that were deprecated and are now gone.

**Rules:**
1. Only remove after deprecation period
2. Always provide migration path
3. Reference the feature that replaces it

**Examples:**
```markdown
### Removed
- Deprecated `old_api()` function (use `new_api()` instead)
- Support for Python 2.7 (upgrade to Python 3.6+)
- Legacy authentication method (migrate to OAuth2)
```

### Deprecated

**What:** Features marked for future removal.

**Rules:**
1. Announce what's going away
2. Explain when (rough timeline)
3. Provide replacement
4. Only use when deprecation spans multiple releases

**Examples:**
```markdown
### Deprecated
- `old_api()` function deprecated in favor of `new_api()` (remove in v3.0)
- YAML config format deprecated (migrate to JSON by v2.5)
```

### Security

**What:** Security vulnerabilities that are patched.

**Always include:**
1. What was vulnerable
2. Who is affected
3. What the fix does

**Examples:**
```markdown
### Security
- Fix XSS vulnerability in user input sanitizer
- Fix SQL injection in report generator (affects reports with user-provided filters)
- Update cryptography library to address CBC padding oracle vulnerability
- Fix authentication bypass in API token validation
```

## Critical Rules

### Rule 1: Document User-Facing Changes ONLY

**Document:**
- ✓ Features users interact with
- ✓ API changes users need to know
- ✓ Behavior changes
- ✓ Security issues

**Don't document:**
- ✗ Internal refactoring
- ✗ Code cleanup
- ✗ Token optimization
- ✗ Developer-only improvements

**Example:**

```markdown
✓ GOOD
### Fixed
- Fix timeout in API request handling (was causing 502 errors)

✗ BAD
### Changed
- Refactored request handler for better code organization
- Optimized token usage in API calls
```

### Rule 2: NEVER Document Version Bumps Themselves

This is a critical rule. Your changelog documents **changes**, not **version management**.

**Never write:**
```markdown
✗ Bumped to 1.2.3
✗ Updated version for compatibility
✗ skill-creator: 1.0.0 → 1.0.1
✗ Release 1.2.3
```

**Write instead:**
```markdown
✓ Fixed timeout issue in request handling
✓ Added support for encrypted documents
✓ **BREAKING**: Renamed command from 'validate' to 'verify'
```

The version number is in the header already: `## [1.2.3] - 2026-01-21`

### Rule 3: Verify Against git diff

**Don't assume or infer.** Run `git diff` and document what actually changed.

```bash
# Before writing changelog
git diff

# Check what's actually in the diff
git diff --stat

# Look at specific file changes
git diff src/components/
```

**Don't write:**
```markdown
✗ "Improved password security" (unless you can see the change in git diff)
✗ "No longer asks for X" (unless you verified X existed before)
```

**Write instead:**
```markdown
✓ "Added password complexity validation (8+ chars, special characters)"
(only if git diff shows this validation was added)
```

### Rule 4: Be Specific and Measurable

Vague entries don't help users understand impact.

**Vague:**
```markdown
✗ Improved performance
✗ Better error handling
✗ Enhanced user experience
✗ Fixed various bugs
```

**Specific:**
```markdown
✓ Reduced search time from 500ms to 50ms (90% improvement)
✓ Added specific error messages for missing config files
✓ Redesigned dashboard layout for faster navigation
✓ Fixed timeout bug in database queries
✓ Fixed crash when uploading files > 1GB
```

## Common Mistakes

### Mistake 1: Confusing "Changed" and "Fixed"

**Fixed** = restoring something that was broken
**Changed** = modifying something that already works

```markdown
✗ WRONG
### Fixed
- Changed error message format to be more helpful

✓ CORRECT
### Changed
- Improved error messages with actionable suggestions
```

### Mistake 2: Missing Impact Context

Don't assume users know what's important.

```markdown
✗ Minimal: "Updated dependency"
✓ Better: "Updated cryptographic library to address padding oracle vulnerability"

✗ Minimal: "Increased timeout"
✓ Better: "Increased request timeout from 5s to 10s to handle slow networks"
```

### Mistake 3: Mixing Internal and User-Facing Changes

```markdown
✗ WRONG
### Changed
- Refactored component architecture
- Improved error messages
- Reorganized source code
- Added JSON export

✓ CORRECT
### Changed
- Improved error messages

### Added
- JSON export
```

### Mistake 4: Using Vague or Marketing Language

```markdown
✗ "Revolutionary new capabilities"
✗ "Industry-leading improvements"
✗ "Next-generation features"

✓ "Added support for encrypted message transport"
✓ "Reduced memory usage by 40%"
✓ "New API v2 with GraphQL support"
```

### Mistake 5: Not Marking Breaking Changes Clearly

```markdown
✗ UNCLEAR
### Changed
- API endpoint changed from /users to /api/users

✓ CLEAR
### Changed
- **BREAKING**: API endpoint changed from /users to /api/users
- Migration guide: Update client code to use new endpoint path

### Removed
- Old /users endpoint (deprecated since v1.5, use /api/users instead)
```

## Examples

### Small Patch Release

```markdown
## [1.2.1] - 2026-01-21

### Fixed
- Fix typo in authentication documentation
- Fix timeout in database connection pool (was causing occasional 502 errors)
```

### Feature Release

```markdown
## [1.3.0] - 2026-01-22

### Added
- Support for encrypted message transport
- New `--dry-run` flag to preview changes before applying
- Export results to PDF format

### Changed
- Improved error messages with actionable suggestions
- Increased default timeout from 5s to 10s
```

### Major Breaking Release

```markdown
## [2.0.0] - 2026-01-23

### Added
- Migration guide in README.md
- New CLI command structure

### Changed
- **BREAKING**: Command renamed from `validate` to `verify`
- **BREAKING**: Config file format changed from YAML to JSON
- **BREAKING**: API endpoints require authentication token in header

### Removed
- Deprecated `validate` command (use `verify` instead)
- Support for YAML config files (use JSON instead)
- Legacy authentication method (use token-based auth instead)

### Fixed
- Fix handling of special characters in filenames
```

### Multi-Component Release

```markdown
## [1.2.0] - 2026-01-24

### Added (skill-a)
- New encryption algorithm support (AES-256)
- New parameter for custom processing rules

### Changed (skill-b)
- Improved error reporting with file line numbers

### Fixed (skill-c)
- Fix crash when processing empty files
- Fix memory leak in file watcher
```

## Multi-Component Changelogs

### Strategy 1: Unified CHANGELOG

Single `CHANGELOG.md` at project root documents all components:

```markdown
## [1.3.0] - 2026-01-24

### Added (skill-a)
- New encryption algorithm support

### Changed (skill-b)
- Improved error reporting

### Fixed (skill-c)
- Fix crash in file processing
```

**Pros:** Single source of truth
**Cons:** Can get long, harder to find component-specific changes

### Strategy 2: Per-Component CHANGELOG

Each component has its own `CHANGELOG.md`:

```
plugin/
├── CHANGELOG.md           (documents plugin changes)
├── skills/
│   ├── skill-a/
│   │   └── CHANGELOG.md   (documents skill-a changes)
│   ├── skill-b/
│   │   └── CHANGELOG.md   (documents skill-b changes)
```

**Pros:** Easy to find component-specific changes
**Cons:** Multiple files to maintain, harder to see full picture

**Recommendation:** Use per-component for large monorepos, unified for plugins with few skills.

## Best Practices Checklist

Before committing a release:

- [ ] CHANGELOG has new section with version and date
- [ ] All entries document user-facing changes only
- [ ] No version bump descriptions (no "Bumped to X.Y.Z")
- [ ] Entries are specific, not vague
- [ ] Entries match what's in `git diff`
- [ ] Breaking changes clearly marked with **BREAKING**
- [ ] Date is in ISO format (YYYY-MM-DD)
- [ ] Sections are in standard order: Added, Changed, Deprecated, Removed, Fixed, Security
- [ ] Each entry is a clear action (starts with verb: "Add", "Fix", "Improve", etc.)

## Pre-Release Versions

Use pre-release versions for testing before a stable release. Format: `X.Y.Z-IDENTIFIER`

### Pre-Release Identifiers

| Version | Purpose | When to Use |
|---------|---------|------------|
| `X.Y.Z-alpha.1` | Early testing, unstable | Internal testing, feature incomplete |
| `X.Y.Z-beta.1` | Stable testing, feature complete | Limited external testing, feedback gathering |
| `X.Y.Z-rc.1` | Release candidate, ready for production | Final testing before stable release |
| `X.Y.Z` | Stable release | Production deployment |

### Example Pre-Release Progression

```
2.0.0-alpha.1  → Early testing of breaking changes
2.0.0-beta.1   → More stable, migration guide ready
2.0.0-rc.1     → Final testing, deployment procedure verified
2.0.0          → Stable production release
```

### CHANGELOG for Pre-Releases

Document pre-releases the same way as stable releases:

```markdown
## [2.0.0-rc.1] - 2026-01-21

### Added
- Migration guide for users upgrading from v1.x

### Changed
- **BREAKING**: API endpoint structure reorganized
- **BREAKING**: Config format changed from YAML to JSON

### Removed
- Support for old YAML config format (use JSON instead)
```

### Rules for Pre-Release Versions

1. **Don't mix pre-release and stable** — Each pre-release is separate from final stable
2. **Increment pre-release identifier** — 2.0.0-alpha.1 → 2.0.0-alpha.2, not back to alpha.1
3. **Document same as stable** — Pre-releases still get CHANGELOG entries
4. **Test thoroughly before stable** — Pre-releases are for gathering feedback, not shipping
5. **Mark breaking changes clearly** — Use **BREAKING** even in pre-releases
