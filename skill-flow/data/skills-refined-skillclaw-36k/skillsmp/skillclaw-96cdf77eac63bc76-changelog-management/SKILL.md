---
name: changelog-management
description: Use this skill when creating, updating, or maintaining CHANGELOG.md files to document project changes clearly and consistently.
---

# Changelog Management

This skill helps you create and maintain CHANGELOG.md files following the Keep a Changelog and Common Changelog formats, ensuring clear communication of changes to users.

## When to Use

Activate this skill when:
- Creating a new CHANGELOG.md
- Adding a release entry
- Updating the unreleased section
- Validating the changelog format
- You need to document version changes or respond to requests related to changelogs, release notes, or version history.

## Core Workflows

### Workflow 1: Create CHANGELOG.md

**Purpose**: Initialize a new changelog file.

**Steps**:
1. **Choose format**: Ask the user to select between Common Changelog or Keep a Changelog. Default to Common Changelog.
2. **Write initial structure**:
   ```markdown
   # Changelog

   All notable changes to this project will be documented in this file.
   The format is based on [Common Changelog](https://common-changelog.org) / [Keep a Changelog](https://keepachangelog.com/).
   This project adheres to [Semantic Versioning](https://semver.org/).

   ## [Unreleased]

   [Unreleased]: https://github.com/owner/repo/compare/vX.X.X...HEAD
   ```
3. **Confirm creation**.

### Workflow 2: Add Release Entry

**Purpose**: Add a new version entry.

**Steps**:
1. **Gather information**:
   - Version: Ensure it is semver-valid (e.g., 1.2.3).
   - Date: Use the format YYYY-MM-DD (ISO 8601).
   - Changes: Collect from git log, HISTORY.md, or user input.
2. **Process changes**:
   - **Remove noise**: Exclude irrelevant changes (e.g., dotfiles, dev dependencies).
   - **Rephrase**: Align terminology and add missing details.
   - **Merge related changes**: Combine related commits for clarity.

### Change Categories

| Category | When to Use | Example |
|----------|-------------|---------|
| **Added** | New features | Add dark mode support |
| **Changed** | Modifications to existing features | Improve search performance by 50% |
| **Deprecated** | Features to be removed | Deprecate legacyParse() |
| **Removed** | Removed features | Remove Node.js 14 support |
| **Fixed** | Bug fixes | Fix login timeout issue |
| **Security** | Security patches | Fix XSS vulnerability |

### Commit Type to Changelog Mapping

| Commit Type | Changelog Category | Notes |
|-------------|-------------------|-------|
| `feat` | **Added** | New features |
| `fix` | **Fixed** | Bug fixes |
| `perf` | **Changed** | Performance improvements |
| `security` | **Security** | Security patches |
| `BREAKING CHANGE` | **Changed** or **Removed** | With **BREAKING** prefix |
| `refactor`, `docs`, `style`, `test`, `chore` | *(usually omit)* | No user impact |

## Entry Format

### Standard Format

```markdown
- [Action verb] [what changed] ([reference])
```

### Examples

```markdown
### Added
- Add user dashboard with customizable widgets (#123)
- Add support for PostgreSQL 15 (PR #456)

### Changed
- **BREAKING**: Change API response format from XML to JSON (#789)
- Update minimum Node.js version to 1
```