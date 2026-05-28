---
name: update-changelog
description: Use when completing features, fixes, or changes that should be recorded. Updates CHANGELOG.md with concise, searchable entries following Keep a Changelog format.
allowed-tools: [Read, Edit, Grep, Glob]
---

# CHANGELOG Update Skill

## Purpose

Maintain a clear, searchable record of changes. Entries should be concise enough to scan quickly but contain enough keywords to find via search.

## Trigger Conditions

Use this skill when:
- Completing a new feature
- Fixing a bug
- Making breaking changes
- Changing existing behavior
- Removing functionality
- Updating dependencies (if significant)

## CHANGELOG Format

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

### Section Types

| Section | Use When |
|---------|----------|
| `Added` | New feature or capability |
| `Changed` | Existing behavior modified |
| `Deprecated` | Feature will be removed |
| `Removed` | Feature was removed |
| `Fixed` | Bug fix |
| `Security` | Security vulnerability fix |

## Writing Good Entries

### Principles

1. **Searchable**: Include keywords users would search for
2. **Concise**: One line per change (2 max if complex)
3. **User-focused**: Describe the impact, not the implementation
4. **Specific**: Include command/option/config names

### Format

```markdown
### Added
- Feature name: brief description (`command` or `option` or `config`)
```

### Good Examples

```markdown
### Added
- Agent autonomous execution with `askUserAutoResponse` config option
- `--verbose` flag for CLI debugging output

### Changed
- Iterator agent now preserves session state across restarts with `--resume`

### Fixed
- Sandbox restriction error when agent uses `gh` commands

### Removed
- `climpt-code` domain (moved to separate repository)
```

### Bad Examples

```markdown
# Too vague - not searchable
### Added
- New feature for agents

# Too implementation-focused
### Changed
- Refactored runIteration to use async/await pattern

# Missing context
### Fixed
- Fixed the bug
```

## Process

### Step 1: Read Current CHANGELOG

```bash
head -50 CHANGELOG.md
```

### Step 2: Identify Change Category

| Question | Category |
|----------|----------|
| Is this entirely new? | Added |
| Does this modify existing behavior? | Changed |
| Does this remove something? | Removed |
| Does this fix a problem? | Fixed |
| Will this be removed later? | Deprecated |

### Step 3: Write Entry

Template:
```
<Feature/Fix name>: <impact description> (`<identifier>`)
```

Where `<identifier>` is:
- CLI option: `--option-name`
- Config field: `fieldName` in config
- Command: `command name`
- File/Path: path pattern if relevant

### Step 4: Place Entry

For unreleased changes:
```markdown
## [Unreleased]

### Added
- Your new entry here
```

For version-specific (during release):
```markdown
## [x.y.z] - YYYY-MM-DD

### Added
- Your new entry here
```

### Step 5: Verify

- Entry is under correct section
- Entry is searchable (try: "Would I find this if I searched for X?")
- Entry includes relevant identifiers

## Entry Templates

### New CLI Option
```markdown
- `--option-name` flag for <purpose>
```

### New Config Option
```markdown
- `configField` config option for <purpose>
```

### New Feature
```markdown
- <Feature name>: <what it does> (`command` or `option`)
```

### Behavior Change
```markdown
- <Component> now <new behavior> (previously <old behavior>)
```

### Bug Fix
```markdown
- Fixed <symptom> when <condition> (`affected component`)
```

### Breaking Change
```markdown
- **Breaking**: <what changed> (migration: <how to migrate>)
```

## Quick Reference

```
1. Determine category: Added/Changed/Removed/Fixed/Deprecated
2. Write one-line entry with:
   - What: Feature/fix name
   - Impact: User-visible effect
   - Identifier: `--option`, `config`, or `command`
3. Place under [Unreleased] or version section
4. Verify: "Can I find this by searching for the feature name?"

Entry formula:
  <What>: <Impact> (`identifier`)

Examples:
  - Agent auto-response: enables autonomous execution (`askUserAutoResponse`)
  - `--dry-run` flag for testing commands without execution
  - Fixed session state loss when using `--resume` with worktree
```

## Integration with Release

During release process:
1. Move entries from `[Unreleased]` to `[x.y.z] - YYYY-MM-DD`
2. Add new `[Unreleased]` section at top
3. Keep entries grouped by category

Example:
```markdown
## [Unreleased]

## [1.10.0] - 2025-01-24

### Added
- Entry moved from Unreleased

### Changed
- Another entry moved from Unreleased
```
