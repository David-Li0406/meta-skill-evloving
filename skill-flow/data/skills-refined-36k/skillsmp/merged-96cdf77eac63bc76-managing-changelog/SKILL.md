---
name: managing-changelog
description: Use this skill to create, update, and maintain CHANGELOG.md files following Common Changelog and Keep a Changelog standards, ensuring clear documentation of version changes and release notes.
---

# Managing Changelog

Create and maintain CHANGELOG.md files following standard formats (Common Changelog + Keep a Changelog).

## When to Use

Activate when:
- Creating a new CHANGELOG.md
- Adding a release entry
- Updating the Unreleased section
- Validating changelog format
- User mentions "changelog", "release notes", "version history", "add to changelog", "update changelog", "create changelog", "change log format", or needs to document version changes.

## Core Workflows

| ID | Purpose | Trigger |
|----|---------|---------|
| WF1 | Create CHANGELOG.md | Initial setup |
| WF2 | Add Release Entry | New version |
| WF3 | Update Unreleased | Pre-release changes |
| WF4 | Validate Format | Quality check |
| WF5 | Promote Prerelease | Stabilize alpha/beta/rc |

### WF1: Create CHANGELOG.md

**Purpose**: Initialize a new changelog file.

**When**: No CHANGELOG.md exists, explicit request.

**Steps**:

1. **Choose format**: Ask user for Common Changelog or Keep a Changelog. Default to Common Changelog.
2. **Write initial structure**:
   ```markdown
   # Changelog

   All notable changes documented here.
   Format: [Common Changelog](https://common-changelog.org) / [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
   Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

   ## [Unreleased]

   [unreleased]: https://github.com/owner/repo/compare/vX.X.X...HEAD
   ```
3. **Confirm creation**.

### WF2: Add Release Entry

**Purpose**: Add a new version entry.

**When**: New release, version bump, explicit request.

**Execution**:

1. **Gather info**: Version (semver-valid), Date (YYYY-MM-DD), Changes (from git log, HISTORY.md, or user input).
2. **Process changes**: Improve quality by removing noise, rephrasing, merging related changes, and keeping brief.
3. **Categorize changes**: Use Common Changelog or Keep a Changelog categories.
4. **Format entry**:
   ```markdown
   ## [1.2.3] - 2025-11-26

   ### Changed
   - **Breaking:** refactor API to use async/await ([#45](url)) (Author)

   ### Added
   - Add support for JSON export ([#42](url), [#43](url))

   ### Fixed
   - Fix memory leak in cache ([#44](url)) (Author)

   [1.2.3]: https://github.com/owner/repo/releases/tag/v1.2.3
   ```
5. **Add notice** if needed.
6. **Insert entry** after `## [Unreleased]` section.
7. **Move unreleased content** if exists.

### WF3: Update Unreleased

**Purpose**: Add changes to the Unreleased section.

**When**: Pre-release changes, ongoing work.

**Steps**:

1. **Read current CHANGELOG.md**.
2. **Add to Unreleased** (if section exists, else create).

### WF4: Validate Format

**Purpose**: Check changelog follows standards.

**When**: Before release, quality check, explicit request.

**Checks**: Ensure structure, categories, and content follow guidelines.

### WF5: Promote Prerelease

**Purpose**: Convert prerelease to stable release.

**When**: Promoting alpha/beta/rc to stable.

**Approaches**: Copy content, skip entry, or refer to prerelease.

## Format Reference

### Common Changelog Format

**Heading**:
```markdown
## [X.Y.Z] - YYYY-MM-DD
```

**Categories**: Changed, Added, Removed, Fixed.

### Keep a Changelog Format

**Heading**: Same as Common Changelog.

**Categories**: Added, Changed, Deprecated, Removed, Fixed, Security.

## Guiding Principles

- Changelogs for humans, communicate impact of changes, sort by importance, and link changes to further info.

## Anti-patterns

**Avoid**: Verbatim git log dumps, vague descriptions, missing dates, inconsistent categories, and security violations.

## Tool Usage

**Read**: Load existing CHANGELOG.md or HISTORY.md.  
**Write**: Create new CHANGELOG.md.  
**Edit**: Update existing changelog (add entries, update sections).

## Examples

**Common Changelog**:
```markdown
# Changelog

## [2.1.0] - 2025-11-26

### Changed
- **Breaking:** refactor config to use YAML ([#45](url)) (Alice)

### Added
- Add dark mode support ([#42](url), [#43](url))

### Fixed
- Fix memory leak in parser ([abc123](url))

[2.1.0]: https://github.com/owner/repo/releases/tag/v2.1.0
```

**Keep a Changelog**:
```markdown
# Changelog

## [2.1.0] - 2025-11-26

### Added
- Dark mode support for UI

### Changed
- Config now uses YAML instead of JSON (breaking change)

### Fixed
- Memory leak in parser

[2.1.0]: https://github.com/owner/repo/releases/tag/v2.1.0
```