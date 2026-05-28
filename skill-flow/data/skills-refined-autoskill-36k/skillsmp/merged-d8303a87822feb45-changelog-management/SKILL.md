---
name: changelog-management
description: Use this skill to generate and update CHANGELOG.md files by analyzing git commit history, supporting both new changelogs and appending recent changes. Ideal for preparing release notes, documenting changes, and managing version history.
---

# Changelog Management

This skill generates and updates CHANGELOG.md files by analyzing git commit history, supporting conventional commits and semantic versioning. It can create new changelogs or append recent changes to existing ones.

## Auto-Invoke Triggers

This skill automatically activates when:

1. **Editing changelog files**: `CHANGELOG.md`, `CHANGELOG.txt`, `HISTORY.md`
2. **Mentioning keywords**: "changelog", "release notes", "version", "semantic versioning"
3. **Git tagging operations**: Creating or discussing version tags
4. **Release preparation**: Discussing release preparation or deployment

## What This Skill Delivers

When invoked, this skill provides:

### 1. Git History Analysis Report
- Commit range analysis (since last tag or specified range)
- Commit categorization by type (feat, fix, docs, etc.)
- Semantic version bump recommendation (MAJOR, MINOR, PATCH)
- Breaking changes detection
- Author and PR number extraction

### 2. Formatted Changelog
Choose from multiple formats:
- **Keep a Changelog** (default) - Industry standard, human-friendly
- **Conventional** - Follows Conventional Commits specification
- **GitHub** - GitHub-style release notes with PR links

### 3. Update Strategy
- Append to existing CHANGELOG.md (preserves history)
- Overwrite with fresh changelog
- Create new version section
- Merge with existing sections

## Common Use Cases

### Project Types
- **Microservices**: Track changes across multiple services
- **Frontend Applications**: UI updates and features
- **API Development**: REST API versioning and breaking changes
- **Infrastructure**: Deployment, CI/CD, DevOps updates
- **Documentation**: Technical docs, API docs, guides

## Workflow

### Preparing a Release
1. Analyze commits since last release.
2. Review and edit generated entries.
3. Use the update script to automatically insert a new version section.
4. Commit and tag the release.

### Daily Development (No Release Yet)
1. Analyze recent commits.
2. Review and edit generated entries.
3. Manually update the `[Unreleased]` section in CHANGELOG.md.

## Quick Start

Generate changelog for commits since last tag:

```bash
python scripts/analyze_commits.py --since-last-tag > new_entries.md
```

Or specify a commit range:

```bash
python scripts/analyze_commits.py --from=v1.0.0 --to=HEAD
```

## Commit Message Conventions

This skill expects **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Recognized types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions or changes
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Other changes

**Breaking changes**: Include `BREAKING CHANGE:` in commit footer or append an exclamation mark after the type (e.g., `feat!:`).

## Example Usage

### Preparing a Release
```bash
# Step 1: Analyze commits since last release
python scripts/analyze_commits.py --since-last-tag > /tmp/v2.1.0_entries.md

# Step 2: Review and edit /tmp/v2.1.0_entries.md

# Step 3: Use script to update CHANGELOG.md
python scripts/update_changelog.py 2.1.0 /tmp/v2.1.0_entries.md
```

### Daily Development
```bash
# Step 1: Analyze recent commits
python scripts/analyze_commits.py --from=HEAD~5 --to=HEAD > /tmp/recent_changes.md

# Step 2: Manually open CHANGELOG.md and edit [Unreleased] section
```

## Quality Standards

- **Conventional Commits**: 100% recognition of conventional commit format
- **Semantic Versioning**: Automatic MAJOR/MINOR/PATCH detection
- **Breaking Changes**: Clear highlighting of breaking changes
- **PR Linking**: Automatic GitHub PR number extraction
- **Date Formatting**: ISO 8601 dates (YYYY-MM-DD)
- **Markdown Formatting**: Valid markdown with proper headers

## Tips

- **Run analysis before creating tag**: Easier to identify the commit range.
- **Keep entries user-focused**: Rewrite technical commits for end-users.
- **Group related changes**: Combine multiple commits about the same feature.

## Version

1.0.0