---
name: conventional-commits-release
description: Enforces conventional commit format for PR titles and commit messages, automating semantic versioning and GitHub releases. Use this skill when writing commit messages, creating PR titles, understanding version bumps, configuring release automation, or troubleshooting commitlint failures.
version: 1.0.0
tags:
  - git
  - ci-cd
  - semantic-versioning
  - github-actions
  - automation
---

# Conventional Commits & Release Automation

## Overview

This project uses a fully automated release pipeline built on conventional commits. Every PR title is validated by commitlint to ensure it follows the format `type(scope): description`. When PRs are squash-merged to main, semantic-release analyzes commit messages to automatically determine version bumps and create GitHub releases.

## Commit Format

### Structure

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Rules**:
- Type is required (must be lowercase)
- Scope is optional but recommended (must be lowercase)
- Description must be lowercase and under 100 characters
- Breaking changes use `!` after type/scope or `BREAKING CHANGE:` footer

### Allowed Types

| Type | Version Bump | Purpose |
|------|-------------|----------|
| `feat` | Minor (0.X.0) | New feature |
| `fix` | Patch (0.0.X) | Bug fix |
| `perf` | Patch (0.0.X) | Performance improvement |
| `docs` | None | Documentation only |
| `style` | None | Code formatting |
| `refactor` | None | Code change, no feature/fix |
| `test` | None | Adding/updating tests |
| `build` | None | Build system or dependencies |
| `ci` | None | CI/CD configuration |
| `chore` | None | Maintenance tasks |
| `revert` | Varies | Revert previous commit |

### Project Scopes

| Scope | Area |
|-------|------|
| `cli` | CLI commands and interface |
| `primitives` | Core domain models |
| `services` | Business logic services |
| `storage` | Storage abstractions |
| `agents` | Agent definitions |
| `templates` | Template files |
| `docs` | Documentation |
| `ci` | CI/CD |
| `release` | Release process |
| `baseline` | Baseline command |
| `skill` | Skill management |
| `mcp` | MCP server integration |
| `oauth` | OAuth authentication |

## PR Title Examples

### Valid Titles

```bash
# Feature additions
feat(cli): add mcp server list command
feat(oauth): implement PKCE flow for authentication
feat!: redesign session management format

# Bug fixes
fix(services): handle empty config gracefully
fix(storage): resolve file lock race condition

# Breaking changes (triggers major version bump)
feat(cli)!: change default output format to json
fix!: rename Config to HarnessConfig

# Other types
docs: update installation guide
refactor(primitives): extract validation logic
test(services): add coverage for edge cases
ci: add python 3.13 to test matrix
chore(deps): update rich to v14
```

### Invalid Titles (Will Fail CI)

```bash
Add new feature              # Missing type
Feat: add feature           # Type must be lowercase
feat: Add Feature           # Description must be lowercase
feat(CLI): add command      # Scope must be lowercase
feat(unknown): add thing    # Scope warning (allowed but flagged)
```

## Release Automation

### How It Works

1. Developer creates PR with conventional commit title
2. CI validates PR title format using commitlint
3. PR is squash-merged to main (PR title becomes commit message)
4. semantic-release analyzes commits since last release
5. If release-worthy commits exist, semantic-release:
   - Calculates next version based on commit types
   - Generates release notes from commit messages
   - Creates GitHub release with tag

### Version Bump Rules

```
fix:  → Patch (1.0.0 → 1.0.1)
perf: → Patch (1.0.0 → 1.0.1)
feat: → Minor (1.0.0 → 1.1.0)
!:    → Major (1.0.0 → 2.0.0)
BREAKING CHANGE: → Major (1.0.0 → 2.0.0)
```

### semantic-release Configuration

From `package.json`:

```json
{
  "release": {
    "branches": ["main"],
    "plugins": [
      "@semantic-release/commit-analyzer",
      "@semantic-release/release-notes-generator",
      "@semantic-release/github"
    ]
  }
}
```

### Python Package Versioning

The Python package version is sourced from Git tags via hatch-vcs:

```toml
# pyproject.toml
[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
fallback_version = "0.0.0+unknown"
```

This ensures `context-harness --version` matches the latest GitHub release.

## Local Testing

### Test PR Title Before Push

```bash
# Install dependencies (first time only)
npm install

# Test a commit message
echo "feat(cli): add new command" | npx commitlint

# Test with verbose output
echo "fix(oauth): handle token expiry" | npx commitlint --verbose

# Test breaking change
echo "feat!: redesign api" | npx commitlint --verbose
```

### Validate Recent Commits

```bash
# Check last commit
npx commitlint --from HEAD~1 --to HEAD

# Check last 5 commits
npx commitlint --from HEAD~5 --to HEAD

# Check all commits since a tag
npx commitlint --from v1.0.0 --to HEAD
```

### Interactive Commit with Commitizen (Optional)

```bash
# Install commitizen globally
npm install -g commitizen

# Use interactive commit
npx cz
```

## CI/CD Workflows

### PR Title Validation (ci.yml)

```yaml
lint-pr-title:
  if: github.event_name == 'pull_request'
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 'lts/*'
    - run: npm clean-install
    - name: Validate PR title
      env:
        PR_TITLE: ${{ github.event.pull_request.title }}
      run: echo "$PR_TITLE" | npx commitlint --verbose
```

### Release Workflow (release.yml)

```yaml
release:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        persist-credentials: false
    - uses: actions/setup-node@v4
      with:
        node-version: 'lts/*'
    - run: npm clean-install
    - name: Release
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: npx semantic-release
```

## Troubleshooting

### CI Failure: "subject must be lower-case"

**Problem**: PR title has uppercase letters in description.

```bash
# Wrong
feat(cli): Add new MCP command

# Correct
feat(cli): add new mcp command
```

### CI Failure: "type must be lower-case"

**Problem**: Type prefix is capitalized.

```bash
# Wrong
Feat(cli): add command

# Correct
feat(cli): add command
```

### CI Failure: "type must be one of..."

**Problem**: Using an invalid type.

```bash
# Wrong
feature(cli): add command

# Correct
feat(cli): add command
```

**Valid types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### CI Failure: "header must not be longer than 100 characters"

**Problem**: PR title exceeds 100 characters.

**Solution**: Shorten the description. Use the PR body for details.

### No Release Created After Merge

**Possible causes**:

1. **No release-worthy commits**: Only `feat`, `fix`, `perf`, or breaking changes trigger releases
   ```bash
   # These DO NOT trigger releases
   docs: update readme
   chore: update dependencies
   refactor: clean up code
   test: add unit tests
   ```

2. **Wrong branch**: Releases only occur on `main` branch

3. **semantic-release dry run**: Check Actions logs for "no release" message

### Version Mismatch

**Problem**: `context-harness --version` shows wrong version.

**Solutions**:
1. Ensure you're on a tagged commit or have tags fetched: `git fetch --tags`
2. Reinstall package: `uv pip install -e .`
3. Check hatch-vcs is working: `uv run python -c "from context_harness import __version__; print(__version__)"`

## Hotfix Releases

For urgent fixes that need immediate release:

1. Create branch from main: `git checkout -b hotfix/critical-bug main`
2. Make fix with proper commit: `fix(scope): critical bug description`
3. Create PR with same title
4. Get expedited review and merge
5. Release triggers automatically

**Note**: Hotfixes follow normal semantic versioning. Use `fix:` for patch releases.

## Reverting Releases

### Revert a Commit

```bash
# Create revert commit
git revert <commit-sha>

# PR title should be
revert: <original commit message>

# Or with reference
revert: feat(cli): add command

Refs: abc1234
```

### Revert Behavior

- Reverting a `feat` commit creates a `revert` commit (triggers patch by default)
- To force a minor/major version bump on revert, use breaking change syntax
- The reverted functionality will be noted in release notes

### Emergency Rollback

If a release causes critical issues:

1. Revert the problematic commit(s)
2. Create PR with `fix!: revert breaking change` if needed
3. Merge triggers new release with incremented version

## Related Files

| File | Purpose |
|------|---------|
| `commitlint.config.js` | Type and scope validation rules |
| `package.json` | semantic-release plugin configuration |
| `.github/workflows/ci.yml` | PR title validation workflow |
| `.github/workflows/release.yml` | Automated release workflow |
| `pyproject.toml` | hatch-vcs Git tag versioning |

## Quick Reference

### Commit Message Cheatsheet

```bash
# New feature (minor bump)
feat(scope): add something new

# Bug fix (patch bump)
fix(scope): fix something broken

# Breaking change (major bump)
feat(scope)!: change api signature

# No version bump
docs: update documentation
chore: routine maintenance
refactor: code improvement
test: add tests
ci: update workflows
```

### Before Creating PR

1. Write descriptive, lowercase title
2. Use appropriate type and scope
3. Keep under 100 characters
4. Test locally if unsure: `echo "your title" | npx commitlint`

---

_Skill: conventional-commits-release v1.0.0 | Last updated: 2025-12-31_
