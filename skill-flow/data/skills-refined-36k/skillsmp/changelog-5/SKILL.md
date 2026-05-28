---
name: changelog
description: Generates changelog entries from commits since the last release. Use when the user wants to update CHANGELOG.md, add changelog entries, or document changes.
allowed-tools: [Bash, Read, Edit, Grep]
---

# Changelog Generation Skill

Analyzes commits since the last release and adds user-facing changes to CHANGELOG.md.

## Instructions

**IMPORTANT: When using this skill, announce to the user**: "Using changelog skill to generate changelog entries."

### 1. Get Last Release Tag

```bash
# Get the most recent release tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$LAST_TAG" ]; then
  echo "No previous release tag found. Will analyze all commits."
fi
```

### 2. Get Commits Since Last Release

```bash
# If tag exists
git log --format="%H %s" "$LAST_TAG"..HEAD

# If no tag, get recent commits
git log --format="%H %s" -50
```

### 3. Analyze Each Commit

For each commit, determine if it has user-facing impact:

**Include** (user-facing):
- New features (`:sparkles:`)
- Bug fixes (`:bug:`)
- Performance improvements (`:zap:`)
- Breaking changes (`:boom:`)
- Deprecations
- Security fixes (`:lock:`)

**Exclude** (internal):
- Refactoring (`:recycle:`) - unless it changes behavior
- Tests (`:white_check_mark:`)
- CI/CD changes (`:construction_worker:`)
- Documentation (`:memo:`) - unless user-facing docs
- Code style (`:art:`)
- Merge commits

### 4. Extract Issue References

Look for issue references in commit messages:
- `#123`
- `Fixes #123`
- `Closes #123`
- `Related to #123`

### 5. Categorize Changes

Group entries by category:

```markdown
### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Removed
- Removed features

### Deprecated
- Soon-to-be removed features

### Security
- Security fixes
```

### 6. Format Entries

Each entry should:
- Start with imperative verb (Add, Fix, Change, Remove)
- Be concise (one line)
- Include issue reference at end if available

Examples:
```markdown
- Add list formatting support (#42)
- Fix memory leak in data provider (#88)
- Change default locale to en-US
```

### 7. Determine Target Section

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Determine target section
if [[ "$BRANCH" =~ ^release-v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
  # On release branch → target is that version
  TARGET_SECTION="[${BASH_REMATCH[1]}]"
else
  # Not on release branch → target is Unreleased
  TARGET_SECTION="[Unreleased]"
fi
```

### 8. Update CHANGELOG.md

1. If target section doesn't exist, create it
2. Add/merge entries under the target section

**Creating new section if needed:**
- For `[Unreleased]`: Add after the header, before first version section
- For version `[X.Y.Z]`: Add after `[Unreleased]`, before previous versions

**Example structure:**
```markdown
## [Unreleased]

## [0.7.0] - 2024-01-15

### Added
- New feature description (#123)

## [0.6.0] - 2024-01-01
...
```

Use the Edit tool to update CHANGELOG.md.

## Workflow

1. Get last release tag
2. List commits since that tag
3. For each commit:
   - Read commit message
   - Determine if user-facing
   - Extract issue references
   - Categorize (Added/Changed/Fixed/etc.)
4. Determine target section:
   - On `release-vX.Y.Z` branch → `[X.Y.Z]`
   - Otherwise → `[Unreleased]`
5. Read current CHANGELOG.md
6. Create target section if it doesn't exist
7. Merge new entries with existing content in target section
8. Update CHANGELOG.md using Edit tool

## Guidelines

### Entry Writing
- Use imperative mood: "Add" not "Added" or "Adds"
- Be specific but concise
- Focus on user impact, not implementation details
- One logical change per entry

### Issue References
- Always include if available
- Format: `(#123)` at end of line
- Multiple issues: `(#123, #124)`

### Avoiding Duplicates
- Check existing [Unreleased] entries before adding
- Merge or update if similar entry exists

## Example Output

```markdown
## [Unreleased]

### Added
- Implement DecimalFormatter for number formatting (#42)
- Add locale fallback support

### Changed
- Update default collation strength to tertiary

### Fixed
- Fix crash when parsing invalid locale string (#55)
- Resolve memory leak in DataProvider (#58)
```

## Arguments

This skill takes no arguments. It always analyzes commits from the last release tag to HEAD.
