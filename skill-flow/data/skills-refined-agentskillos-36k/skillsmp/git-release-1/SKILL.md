---
name: git-release
description: Git release workflow with semantic versioning and changelogs
license: MIT
---

# Git Release Skill

Use this skill when preparing releases, managing versions, and generating changelogs.

## When to Use

- Preparing a new release
- Updating version numbers
- Generating changelogs
- Creating release tags
- Publishing to npm/package registries

## Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── Bug fixes (backwards compatible)
  │     └──────── New features (backwards compatible)
  └────────────── Breaking changes
```

### Version Bump Rules

| Change Type | Example | Version Bump |
|-------------|---------|--------------|
| Breaking API change | Remove function | MAJOR (1.0.0 → 2.0.0) |
| New feature | Add endpoint | MINOR (1.0.0 → 1.1.0) |
| Bug fix | Fix crash | PATCH (1.0.0 → 1.0.1) |
| Documentation | Update README | PATCH (optional) |
| Refactor (no API change) | Internal cleanup | PATCH (optional) |

### Pre-release Versions

```
1.0.0-alpha.1   # Alpha release
1.0.0-beta.1    # Beta release
1.0.0-rc.1      # Release candidate
```

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation | None |
| `style` | Formatting | None |
| `refactor` | Code restructure | None |
| `perf` | Performance | PATCH |
| `test` | Tests | None |
| `chore` | Maintenance | None |
| `BREAKING CHANGE` | Breaking change | MAJOR |

### Examples

```bash
# Feature
git commit -m "feat(auth): add OAuth2 login support"

# Bug fix
git commit -m "fix(api): handle null response from payment provider"

# Breaking change
git commit -m "feat(api)!: change user endpoint response format

BREAKING CHANGE: User endpoint now returns nested profile object"

# With scope
git commit -m "fix(ui): correct button alignment on mobile"

# With body
git commit -m "refactor(database): migrate to connection pooling

- Replace individual connections with pool
- Add connection timeout handling
- Update all database queries to use pool"
```

## Release Workflow

### 1. Pre-Release Checks

```bash
# Ensure clean working directory
git status

# Ensure on correct branch
git branch --show-current

# Pull latest changes
git pull origin main

# Run tests
npm test

# Run build
npm run build

# Check for vulnerabilities
npm audit
```

### 2. Version Bump

```bash
# Using npm (updates package.json and creates commit)
npm version patch  # 1.0.0 → 1.0.1
npm version minor  # 1.0.0 → 1.1.0
npm version major  # 1.0.0 → 2.0.0

# Pre-release versions
npm version prerelease --preid=alpha  # 1.0.0 → 1.0.1-alpha.0
npm version prerelease --preid=beta   # 1.0.0 → 1.0.1-beta.0
npm version prerelease --preid=rc     # 1.0.0 → 1.0.1-rc.0
```

### 3. Generate Changelog

```bash
# Using conventional-changelog
npx conventional-changelog -p angular -i CHANGELOG.md -s

# Or with standard-version (automates version + changelog)
npx standard-version
npx standard-version --release-as minor
npx standard-version --prerelease alpha
```

### 4. Create Tag and Push

```bash
# Tag is usually created by npm version or standard-version
# If manual:
git tag -a v1.2.0 -m "Release v1.2.0"

# Push with tags
git push origin main --follow-tags
```

### 5. Create GitHub Release

```bash
# Using GitHub CLI
gh release create v1.2.0 \
  --title "v1.2.0" \
  --notes-file RELEASE_NOTES.md

# With auto-generated notes
gh release create v1.2.0 --generate-notes

# Draft release for review
gh release create v1.2.0 --draft
```

### 6. Publish (if applicable)

```bash
# npm
npm publish

# npm with tag (for pre-releases)
npm publish --tag next
npm publish --tag beta
```

## Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2024-01-15

### Added
- OAuth2 login support for Google and GitHub (#123)
- Dark mode toggle in settings (#145)

### Changed
- Improved loading performance for dashboard (#156)
- Updated dependencies to latest versions

### Fixed
- Fixed button alignment on mobile devices (#167)
- Corrected timezone handling in date picker (#172)

### Security
- Updated jsonwebtoken to fix CVE-2023-XXXXX

## [1.1.0] - 2024-01-01

### Added
- Initial release with core features
```

## GitHub Actions for Releases

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - run: npm ci
      - run: npm test
      - run: npm run build

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Release Checklist

### Before Release
- [ ] All tests pass
- [ ] Build succeeds
- [ ] No security vulnerabilities
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped

### Release
- [ ] Tag created
- [ ] Pushed to remote
- [ ] GitHub release created
- [ ] Package published (if applicable)

### After Release
- [ ] Verify installation works
- [ ] Announce release (if applicable)
- [ ] Monitor for issues

## Hotfix Process

```bash
# Create hotfix branch from release tag
git checkout -b hotfix/1.2.1 v1.2.0

# Make fix
# ... commit changes ...
git commit -m "fix(critical): resolve payment processing error"

# Bump patch version
npm version patch

# Push and create PR to main
git push origin hotfix/1.2.1

# After merge, tag and release
git checkout main
git pull
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git push origin v1.2.1
```

## Rollback Process

```bash
# Revert to previous version
git revert HEAD  # If single commit

# Or reset to tag
git checkout v1.1.0

# Create new patch release
npm version patch
git push origin main --follow-tags
```
