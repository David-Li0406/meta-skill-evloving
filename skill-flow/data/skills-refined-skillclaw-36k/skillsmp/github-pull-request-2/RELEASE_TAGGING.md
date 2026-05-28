# Release Tagging Guide

Complete guide for using the automated PR merge and release tagging workflow.

## Quick Start

After a PR is approved and ready to merge:

```bash
# Merge PR #42 and create release v1.2.0
./scripts/merge-and-release.sh 42

# Or from skill directory:
./.github/skills/github-pull-request/scripts/merge-and-release.sh 42
```

## Options

### Preview mode (`--dry-run`)

See what would happen without making any changes:

```bash
./scripts/merge-and-release.sh 42 --dry-run
```

### Merge without release (`--no-tag`)

Just merge the PR, skip release tag creation:

```bash
./scripts/merge-and-release.sh 42 --no-tag
```

### Verbose output (`--verbose`)

Show detailed execution steps:

```bash
./scripts/merge-and-release.sh 42 --verbose
```

## How It Works

The script performs these steps automatically:

1. **Verify PR is valid** - Checks PR exists and is OPEN
2. **Check merge compatibility** - Ensures no conflicts, all checks pass
3. **Fetch PR details** - Gets title, branch, metadata
4. **Calculate version** - Uses Conventional Commits (feat/fix/docs)
5. **Merge PR** - Squashes commits, removes remote branch
6. **Create git tag** - Creates annotated tag with release notes
7. **Push tag** - Pushes tag to GitHub
8. **Create GitHub release** - Generates release page

## Semantic Versioning

Version bumps are determined automatically from PR title:

| PR Type      | Example             | Version Bump                |
| ------------ | ------------------- | --------------------------- |
| **feat**     | `feat: add feature` | **MINOR** (v1.0.0 → v1.1.0) |
| **fix**      | `fix: resolve bug`  | **PATCH** (v1.0.0 → v1.0.1) |
| **docs**     | `docs: update docs` | **PATCH** (v1.0.0 → v1.0.1) |
| **refactor** | `refactor: code`    | **PATCH** (v1.0.0 → v1.0.1) |
| **chore**    | `chore: deps`       | **PATCH** (v1.0.0 → v1.0.1) |

## Troubleshooting

### "PR not found or inaccessible"

```bash
# Verify authentication
gh auth status

# Check PR exists
gh pr view <number>
```

### "PR is not OPEN"

PR might already be merged. Check PR status:

```bash
gh pr view <number>
```

### "PR is not mergeable"

Resolve conflicts and ensure all checks pass:

```bash
# Update from main
git fetch origin main
git merge origin/main

# Fix conflicts manually, then push
git add .
git commit -m "fix: resolve merge conflicts"
git push
```

### "Failed to create git tag"

Tag might already exist:

```bash
git tag -l | grep "^v"
git describe --tags --abbrev=0
```

## Manual Workflow

If you need to merge and tag manually:

```bash
# 1. Merge PR
gh pr merge <number> --squash --delete-branch

# 2. Get current version
CURRENT_TAG=$(git describe --tags --abbrev=0)

# 3. Calculate next version
NEXT_VERSION="v1.3.0"

# 4. Create tag
git tag -a "$NEXT_VERSION" -m "Release $NEXT_VERSION"

# 5. Push tag
git push origin "$NEXT_VERSION"

# 6. Create release
gh release create "$NEXT_VERSION" --title "Release $NEXT_VERSION"
```

## Integration with CI/CD

Use in GitHub Actions:

```yaml
- name: Merge and Release PR
  run: |
    ./.github/skills/github-pull-request/scripts/merge-and-release.sh ${{ github.event.pull_request.number }}
  if: github.event.pull_request.merged == true
```

## Version Format

Releases follow Semantic Versioning:

```
vMAJOR.MINOR.PATCH

Examples:
v1.0.0   # Initial release
v1.1.0   # New features
v1.1.1   # Bug fix
v2.0.0   # Breaking changes
```

Each tag includes:

- Release title
- PR reference
- Merge commit hash
- Release date

View all releases: https://github.com/JordiNodeJS/thesimpsonsapi/releases

## Related Documentation

- [GitHub PR Skill](./SKILL.md) - Full skill documentation
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub CLI Reference](https://cli.github.com/manual/)
