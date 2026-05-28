---
name: changelog-management
description: Use this skill to generate and update user-friendly changelogs from git commits for any project type, ensuring accurate documentation of changes for releases.
---

# Changelog Management

This skill automates the generation and updating of changelog entries from git commit history, categorizing changes into Added, Changed, Fixed, and Breaking sections. It follows a user-friendly format suitable for release notes and public changelogs.

## When to Use

- Preparing release notes for a new version.
- Creating weekly/monthly product update summaries.
- Writing changelog entries for app stores.
- Generating customer-facing update notifications.
- Maintaining a public changelog page.

## Core Principles

1. **Commit Analysis**: Parse conventional commit messages to understand change types.
2. **Accurate Categorization**: Correctly categorize changes as Added, Changed, Fixed, or Breaking.
3. **Comprehensive Coverage**: Include all meaningful commits in the changelog.
4. **User-Friendly Language**: Translate technical commit messages into clear, descriptive entries.

## Instructions

### Activation Triggers

Invoke this skill when:
- Preparing to create a Pull Request.
- Explicitly asked to update the changelog from commits.
- Multiple commits exist that aren't reflected in the changelog.
- Before merging a feature branch to main.

### Workflow Steps

#### Step 1: Identify Base Branch and Target

1. **Check current branch:**
   ```bash
   git branch --show-current
   ```

2. **Find base branch (usually main):**
   ```bash
   git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | cut -d'/' -f2 || echo "main"
   ```

3. **Find merge base (where branch diverged):**
   ```bash
   git merge-base HEAD origin/main
   ```

#### Step 2: Gather Commits

**Get all commits since divergence:**
```bash
git log origin/main..HEAD --pretty=format:"%h|%s"
```

#### Step 3: Categorize Changes

| Category          | Commit Prefixes         | Emoji |
|-------------------|-------------------------|-------|
| New Features      | feat, add               | ✨     |
| Improvements      | improve, enhance, update| 🔧     |
| Bug Fixes         | fix, resolve, patch     | 🐛     |
| Breaking Changes   | breaking, !:            | 💥     |
| Security          | security, vuln          | 🔒     |
| Performance       | perf, optimize          | ⚡     |

#### Step 4: Format Changelog Entry

Generate entries following this format:
```markdown
## Version {version} - {date}

### Breaking Changes
- Description of breaking change 1

### Added
- New feature description 1

### Changed
- Change description 1

### Fixed
- Bug fix description 1
```

#### Step 5: Update Changelog

1. **Read the current changelog:**
   ```bash
   cat CHANGELOG.md
   ```

2. **Insert new entries under appropriate subsections:**
   - Maintain existing entries unchanged.
   - Ensure consistent formatting.

#### Step 6: Validate and Report

1. **Check markdown syntax:**
   ```bash
   mkdocs build --strict 2>&1 | grep -i "changelog"
   ```

2. **Report the changes made:**
```markdown
## ✅ Changelog Updated from Commits

**Analyzed:**
- Commit range: `origin/main..HEAD`
- Total commits: X
- Commits processed: Y

**Generated entries:**
- Added: A entries
- Changed: B entries
- Fixed: C entries
- Security: D entries

**Files updated:**
- `CHANGELOG.md` - Added new entries under [Unreleased]

**Validation:**
✅ Markdown syntax valid
✅ No duplicate entries
✅ All meaningful commits covered

**Status:** Ready for commit
```

## Constraints and Safety

### DO NOT

1. Modify code files - only update `CHANGELOG.md`.
2. Delete existing changelog entries - only add new ones.
3. Change the changelog format - maintain a consistent structure.
4. Skip security-related commits - always include in the Security section.
5. Add entries for merge commits - use actual commits instead.
6. Fabricate entries - only create entries from actual commits.

### ALWAYS

1. Read the changelog before editing.
2. Parse commit messages carefully.
3. Include file references when relevant.
4. Group related changes together.
5. Validate after update.

## Examples

### Example 1: Feature Branch Ready for PR

**Trigger:** User says "Update changelog before PR"

**Actions:**
1. Check current branch and find commits.
2. Analyze commits and categorize them.
3. Read and edit the changelog to add new entries.
4. Validate and report completion.

### Example 2: Bug Fix Branch

**Trigger:** User says "Generate changelog from commits"

**Actions:**
1. Check branch and find commits.
2. Categorize and analyze commits.
3. Read and edit the changelog.
4. Validate and report.

## Integration with CI

This skill complements CI workflows by ensuring that changelogs are updated before creating pull requests, thus maintaining accurate documentation of changes.

## Troubleshooting

### Issue: Commits don't follow conventional format

**Solution:**
1. Analyze commit diff to understand change type.
2. Default to **Changed** if unclear.

### Issue: Too many small commits

**Solution:**
1. Group trivial commits by theme.
2. Create a single changelog entry summarizing all.

## Success Metrics

This skill is successful when:
- All commits are reflected in the changelog before PR.
- Changelog entries are accurate and descriptive.
- Proper categorization is maintained.
- No manual changelog editing is needed.