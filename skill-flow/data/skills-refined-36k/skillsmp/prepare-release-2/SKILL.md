---
name: prepare-release
description: Examine commits since the last tag, categorize changes by type (breaking/feature/fix), and recommend the appropriate semantic version bump
disable-model-invocation: true
---

# Prepare Release

Analyze the repository to prepare for a tagged release. Do NOT run git tag/push commands - only analyze, recommend, and provide commands for the user.

## Phase 0: Pre-flight Checks

**Branch**: Run `git branch --show-current`. **STOP** if not on `main`/`master`.

**Working Tree**: Run `git status --porcelain`. **WARN** if dirty (uncommitted changes excluded from analysis), but proceed.

**Remote Sync**: Run `git fetch origin` then `git rev-list --left-right --count origin/main...HEAD`.

- Behind remote: **STOP**
- Ahead of remote: **WARN** but proceed
- Diverged: **STOP**

## Phase 1: Repository State

1. **Latest semver tag**: `git tag --list --sort=-v:refname` - find latest vX.Y.Z or X.Y.Z (including pre-releases). Note if no tags exist.

2. **Version file(s)**: Check for `mix.exs`, `package.json`, `Cargo.toml`, `pyproject.toml`, `setup.py`, `pom.xml`, `build.gradle`, `*.csproj`, `*.gemspec`, `composer.json`, `Chart.yaml`, etc. Flag tag/file version mismatches.

3. **Changelog**: Check `CHANGELOG.md`, `HISTORY.md`, `NEWS.md`, `CHANGES.md`, `docs/CHANGELOG.md`. Note format.

## Phase 2: Change Analysis

Run `git log <last-tag>..HEAD --oneline` to collect commits.

**Classify each commit:**

| App Changes (normal semver)          | Non-App Changes (may not need bump)   |
| ------------------------------------ | ------------------------------------- |
| Source code (`src/`, `lib/`, `app/`) | Docs (`README.md`, `docs/`)           |
| API changes, features, bug fixes     | CI/CD (`.github/workflows/`, etc.)    |
| Breaking changes                     | Tests only (`test/`, `spec/`)         |
| Migrations, security patches         | Config (`.gitignore`, linting, IDE)   |
| Runtime dependency updates           | Build/container config (non-artifact) |

**Conventional commits mapping:**

- `feat:` -> MINOR, `fix:` -> PATCH
- `docs:`, `test:`, `ci:`, `chore:` -> Usually non-app
- `BREAKING CHANGE:` in body/footer or breaking marker (`feat!:`, `fix!:`) -> MAJOR

## Phase 3: Semver Decision

| Change Type     | Bump          | Result                     |
| --------------- | ------------- | -------------------------- |
| Breaking change | MAJOR         | X+1.0.0                    |
| New feature     | MINOR         | X.Y+1.0                    |
| Bug fix         | PATCH         | X.Y.Z+1                    |
| Non-app only    | PATCH or NONE | Consider if release needed |

**Special cases**: 0.x.x allows breaking in MINOR; pre-releases may bump to stable; first release starts at 0.1.0 or 1.0.0.

## Phase 4: Changelog

Draft entry if app changes exist or unreleased section is missing/incomplete. Follow project's existing format or Keep a Changelog (Added/Changed/Deprecated/Removed/Fixed/Security sections).

## Phase 5: Output Report

Provide:

1. **Current state**: Latest tag, version file(s) and values, alignment status, changelog location
2. **Changes summary**: Commit count, app vs non-app breakdown, breaking/features/fixes identified
3. **Recommendation**: Bump type, reasoning, new version number
4. **Required actions**: Checklist of files to update
5. **Draft changelog entry**
6. **Git commands** (copy-friendly block):

```bash
# Adjust based on what needs updating:
git add [version-file] CHANGELOG.md
git commit -m "chore: prepare release vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

## Constraints

1. **DO NOT** run git tag/push commands - provide them for user to run
2. **DO NOT** edit files - provide changes needed
3. **STOP** if not on main/master or if behind/diverged from remote
4. **Respect conventions** - match existing changelog format, commit style, version prefix (v or not)
5. **Be explicit** - explain version bump reasoning, flag uncertainties
6. **Use annotated tags** - always `git tag -a`, not lightweight
