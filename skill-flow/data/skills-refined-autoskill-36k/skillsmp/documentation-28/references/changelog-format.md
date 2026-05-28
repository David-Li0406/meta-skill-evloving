# Changelog Format Guide

## Overview

This guide follows [Keep a Changelog](https://keepachangelog.com/) format, a human-readable standard for documenting project changes.

---

## Why Keep a Changelog?

- **For humans:** Easier to read than git log
- **For automation:** Structured format enables tooling
- **For decisions:** Helps users decide to upgrade
- **For debugging:** Trace when changes were introduced

---

## File Structure

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New features not yet released

---

## [1.0.0] — 2026-01-20 — Program / Module: Feature

### Added
- Feature description

### Changed
- Change description

### Fixed
- Fix description

---

## [0.1.0] — 2026-01-01 — Initial Release

### Added
- Initial project scaffolding
```

---

## Change Types

Use these categories in order:

| Type | Description | Example |
|------|-------------|---------|
| **Added** | New features | "Added user authentication" |
| **Changed** | Changes in existing functionality | "Updated API response format" |
| **Deprecated** | Soon-to-be removed features | "Deprecated old auth method" |
| **Removed** | Now removed features | "Removed legacy endpoint" |
| **Fixed** | Bug fixes | "Fixed login redirect loop" |
| **Security** | Vulnerability fixes | "Fixed XSS vulnerability" |

### Order Rule

Always list changes in this order: Added → Changed → Deprecated → Removed → Fixed → Security

---

## Entry Format

### Version Header

```markdown
## [VERSION] — YYYY-MM-DD — Program / Module: Feature
```

Components:
- `[VERSION]`: SemVer version in brackets
- `YYYY-MM-DD`: ISO 8601 date format
- `Program / Module: Feature`: Human-readable release name

### Change Entry

```markdown
### Added
- Added feature X that allows users to do Y
- Added new CLI command `foo` for Z
```

Each entry:
- Starts with a hyphen `-`
- Uses active voice
- Explains what changed and optionally why
- Links to issues/PRs when helpful: `([#123](link))`

---

## Writing Good Entries

### Do This

```markdown
### Added
- Added export to CSV feature for reports
- Added dark mode support with system preference detection

### Changed
- Improved search performance by 40% through query optimization
- Updated error messages to be more actionable

### Fixed
- Fixed crash when uploading files larger than 10MB
- Fixed incorrect total calculation in shopping cart
```

### Don't Do This

```markdown
### Added
- Added stuff
- New feature
- CSV

### Fixed
- Fixed bug
- Fixed issue #123
- Misc fixes
```

### Entry Checklist

- [ ] Describes what changed (not just "fixed bug")
- [ ] Uses active voice ("Added" not "Addition of")
- [ ] Is user-focused (what does this mean for them?)
- [ ] Links to issue/PR if relevant
- [ ] Is concise but complete

---

## The Unreleased Section

Always maintain an `[Unreleased]` section at the top for changes not yet released.

```markdown
## [Unreleased]

### Added
- Added feature X (in development)
- Added feature Y (in testing)

### Fixed
- Fixed issue Z
```

When releasing:
1. Move entries from `[Unreleased]` to new version section
2. Add version number and date
3. Keep empty `[Unreleased]` section for future changes

---

## Linking Versions

At the bottom of the changelog, add comparison links:

```markdown
[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/user/repo/releases/tag/v0.1.0
```

This allows readers to see the full diff between versions.

---

## Complete Example

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Added keyboard shortcuts for common actions

---

## [0.3.0] — 2026-01-15 — Kitchen / Planning: Generate shopping list

### Added
- Added automatic shopping list generation from meal plans
- Added ingredient quantity aggregation
- Added store section organization for lists

### Changed
- Improved meal plan algorithm to consider dietary restrictions

### Fixed
- Fixed duplicate ingredients in shopping list
- Fixed incorrect unit conversions for some ingredients

---

## [0.2.0] — 2026-01-08 — Kitchen / Planning: Create weekly meal plan

### Added
- Added weekly meal planning interface
- Added recipe suggestions based on preferences
- Added meal plan templates for quick setup

### Changed
- Updated recipe database with 50 new recipes

---

## [0.1.0] — 2026-01-01 — Initial Release

### Added
- Initial project structure and configuration
- Basic recipe storage and retrieval
- Simple search functionality


[Unreleased]: https://github.com/user/project/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/user/project/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/user/project/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/user/project/releases/tag/v0.1.0
```

---

## Changelog Anti-Patterns

### Don't Do

| Anti-Pattern | Problem |
|--------------|---------|
| `- Fixed bugs` | Too vague, unhelpful |
| `- Updated dependencies` | Unless security-relevant, omit |
| `- Refactored code` | Internal changes don't belong |
| `- Misc improvements` | Be specific or omit |
| Missing dates | Readers can't track timing |
| No version links | Can't see actual changes |

### Do Instead

| Instead Of | Write |
|------------|-------|
| Fixed bugs | Fixed crash when submitting empty form |
| Updated deps | Updated lodash to fix prototype pollution (CVE-XXXX) |
| Refactored | (Don't include unless it affects users) |
| Misc | Be specific about each improvement |

---

## Automation Tips

### Generate from Git

```bash
# Get commits since last tag
git log v0.2.0..HEAD --oneline

# Get commits with conventional commit format
git log v0.2.0..HEAD --format="%s" | grep -E "^(feat|fix|docs):"
```

### Validate Format

```python
# Check changelog has required sections
def validate_changelog(content):
    required = ["## [Unreleased]", "### Added", "### Changed", "### Fixed"]
    for section in required:
        if section not in content:
            print(f"Missing: {section}")
```
