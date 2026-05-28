# Version Management with Changesets

## Overview

**Changesets** is a tool for managing versions and changelogs in monorepos and single packages.

**Key Features:**
- Semantic versioning automation
- Changelog generation
- Monorepo-friendly
- Works across npm, pnpm, yarn
- GitHub integration

**Workflow:**
1. Developer adds changeset describing changes
2. CI checks for changesets on PRs
3. Changesets generates version bumps and changelog
4. Publish packages with updated versions

---

## Installation

**In monorepo root:**
```bash
pnpm add -D @changesets/cli
```

**Initialize:**
```bash
pnpm changeset init
```

This creates `.changeset/config.json` and `.changeset/README.md`.

---

## Configuration

**.changeset/config.json:**
```json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": [],
  "___experimentalUnsafeOptions_WILL_CHANGE_IN_PATCH": {
    "onlyUpdatePeerDependentsWhenOutOfRange": true
  }
}
```

**Key options:**
- `changelog` - How to generate changelogs
- `commit` - Auto-commit version changes
- `fixed` - Packages versioned together
- `linked` - Packages that should have same version
- `access` - Public or restricted npm packages
- `baseBranch` - Main branch name
- `updateInternalDependencies` - How to bump internal deps

---

## Creating Changesets

### Add Changeset

**Interactive:**
```bash
pnpm changeset
```

This prompts:
1. Which packages changed?
2. What type of change? (major/minor/patch)
3. Summary of changes

**Creates file:** `.changeset/random-words-here.md`

**Example changeset file:**
```md
---
"@repo/package-a": minor
"@repo/package-b": patch
---

Add new feature to package-a and fix bug in package-b
```

### Changeset Types

**Patch (0.0.X)** - Bug fixes
```bash
pnpm changeset
# Select: patch
```

**Minor (0.X.0)** - New features (backwards compatible)
```bash
pnpm changeset
# Select: minor
```

**Major (X.0.0)** - Breaking changes
```bash
pnpm changeset
# Select: major
```

### Multiple Packages

**Single changeset for multiple packages:**
```md
---
"@repo/ui": minor
"@repo/utils": patch
"@repo/types": minor
---

- Add Button component to ui
- Fix date utility in utils
- Add new types for Button
```

---

## Versioning Packages

### Version Command

**Preview version bumps:**
```bash
pnpm changeset version
```

This:
1. Reads all changesets
2. Determines version bumps
3. Updates package.json versions
4. Generates CHANGELOG.md
5. Deletes consumed changesets

**What gets updated:**
- `package.json` version fields
- `CHANGELOG.md` files
- Internal dependencies

**Example CHANGELOG.md:**
```md
# @repo/ui

## 1.2.0

### Minor Changes

- abc123: Add Button component

### Patch Changes

- Updated dependencies
  - @repo/types@1.1.0
```

### Publishing

**Publish all updated packages:**
```bash
pnpm changeset publish
```

This:
1. Builds packages
2. Runs tests
3. Publishes to npm
4. Creates git tags

**Then push:**
```bash
git push --follow-tags
```

---

## Monorepo Workflows

### Fixed Versioning

**All packages same version:**
```json
{
  "fixed": [
    ["@repo/ui", "@repo/utils", "@repo/types"]
  ]
}
```

When one package bumps to 2.0.0, all bump to 2.0.0.

### Linked Versioning

**Packages increment together:**
```json
{
  "linked": [
    ["@repo/ui", "@repo/utils"]
  ]
}
```

If ui bumps minor, utils bumps minor too (but can have different major versions).

### Internal Dependencies

**When @repo/ui depends on @repo/utils:**

**.changeset/config.json:**
```json
{
  "updateInternalDependencies": "patch"
}
```

Options:
- `"patch"` - Always bump dependents as patch
- `"minor"` - Bump dependents as minor

**Example:**
- utils: 1.0.0 → 1.1.0 (minor)
- ui depends on utils
- ui: 1.0.0 → 1.0.1 (patch bump for dependency update)

---

## GitHub Integration

### PR Changeset Check

**.github/workflows/changeset-check.yml:**
```yaml
name: Changeset Check

on:
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Check for changesets
        run: pnpm changeset status --since=origin/main
```

### Automated Release PR

**.github/workflows/release.yml:**
```yaml
name: Release

on:
  push:
    branches:
      - main

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    runs-on: ubuntu-latest

    permissions:
      contents: write
      pull-requests: write
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Create Release PR or Publish
        uses: changesets/action@v1
        with:
          version: pnpm changeset version
          publish: pnpm changeset publish
          commit: 'chore: version packages'
          title: 'chore: version packages'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**How it works:**
1. When changesets exist, creates/updates "Version Packages" PR
2. PR shows version bumps and changelog
3. When PR merged, publishes packages
4. Creates git tags

---

## Snapshot Releases

**For testing before official release:**

```bash
pnpm changeset version --snapshot beta
pnpm changeset publish --tag beta
```

This publishes:
- `@repo/ui@1.2.0-beta-20240101120000`

Install with:
```bash
npm install @repo/ui@beta
```

---

## Pre-releases

### Enter Pre-release Mode

```bash
pnpm changeset pre enter next
```

Now all changesets create pre-release versions:
- `1.0.0` → `1.0.1-next.0`
- `1.0.1-next.0` → `1.0.1-next.1`

### Exit Pre-release Mode

```bash
pnpm changeset pre exit
```

Next version command creates normal release:
- `1.0.1-next.1` → `1.0.1`

### Publishing Pre-releases

```bash
pnpm changeset publish --tag next
```

Users install with:
```bash
npm install @repo/ui@next
```

---

## Best Practices

1. **Add changeset in PR** - Part of development workflow
2. **Descriptive summaries** - Explain why, not just what
3. **Check changeset status** - Before merging PR
4. **Automated releases** - Use GitHub Action
5. **Protect main** - Require changeset check
6. **Test snapshots** - Before official release
7. **Pre-releases** - For beta testing
8. **Internal deps** - Configure updateInternalDependencies
9. **CHANGELOG** - Review before publishing
10. **Git tags** - Always push tags after publish

---

## Common Workflows

### Feature Development

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes
# ...

# 3. Add changeset
pnpm changeset
# Choose: minor
# Summary: Add new feature

# 4. Commit changeset
git add .changeset/
git commit -m "feat: add new feature"

# 5. Push and create PR
git push

# 6. PR checks pass (including changeset check)
# 7. Merge PR
# 8. Automated release PR created
# 9. Review and merge release PR
# 10. Packages published automatically
```

### Bug Fix

```bash
# Add changeset
pnpm changeset
# Choose: patch
# Summary: Fix bug in validation

git add .changeset/
git commit -m "fix: validation bug"
```

### Breaking Change

```bash
# Add changeset
pnpm changeset
# Choose: major
# Summary: Remove deprecated API

git add .changeset/
git commit -m "feat!: remove deprecated API"
```

---

## Troubleshooting

### No Changesets Found

**If PR has no changes to packages:**
```bash
# Add empty changeset
pnpm changeset --empty
```

**Or skip changeset check for docs-only changes:**
```yaml
# In GitHub Action
if: contains(github.event.pull_request.labels.*.name, 'no-changeset') == false
```

### Version Not Updating

**Check changeset files exist:**
```bash
ls .changeset/*.md
```

**Check config:**
```bash
cat .changeset/config.json
```

**Manually run:**
```bash
pnpm changeset version --verbose
```

### Publish Fails

**Check npm credentials:**
```bash
npm whoami
```

**Check package.json:**
- `name` is correct
- `version` is valid
- `publishConfig` is set

**Dry run:**
```bash
npm publish --dry-run
```

---

## Alternatives

**semantic-release:**
- Fully automated based on commits
- No manual changeset files
- Good for single packages
- Steeper learning curve

**release-please:**
- Google's tool
- Creates release PRs
- Supports multiple languages
- Less monorepo-focused

**Manual versioning:**
- Full control
- More error-prone
- Good for simple projects
- Less automation

**When to use Changesets:**
- Monorepos with multiple packages
- Want control over version bumps
- Need good changelog
- Publishing to npm

---

## Quick Reference

**Setup:**
```bash
pnpm add -D @changesets/cli
pnpm changeset init
```

**Add changeset:**
```bash
pnpm changeset
```

**Version:**
```bash
pnpm changeset version
```

**Publish:**
```bash
pnpm changeset publish
git push --follow-tags
```

**Check status:**
```bash
pnpm changeset status
```

**Pre-release:**
```bash
pnpm changeset pre enter next
pnpm changeset publish --tag next
pnpm changeset pre exit
```

**Snapshot:**
```bash
pnpm changeset version --snapshot beta
pnpm changeset publish --tag beta
```
