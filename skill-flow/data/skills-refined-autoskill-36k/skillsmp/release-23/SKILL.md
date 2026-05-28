---
name: release
description: This skill should be used when the user asks to "release a project", "create a release", "bump version", "publish to GitHub", "prepare a release", "run release validation", or needs to perform SDLC-compliant releases for Claude Code plugins, Python, Node.js, Go, or Rust projects. Provides comprehensive pre-release validation including tests, lint, coverage, and security checks.
allowed-tools: Bash(*), Read, Write, Glob, Grep, AskUserQuestion
---

# Universal Release Skill

This skill executes comprehensive release workflows with SDLC validation for multiple project types. It prevents broken, untested, or insecure code from being released.

## Supported Project Types

| Type | Detection | Version Tool | Validators |
|------|-----------|--------------|------------|
| Claude Plugin | `.claude-plugin/plugin.json` | bump-my-version | plugin.json, agents, skills, commands |
| Python | `pyproject.toml`, `setup.py` | bump-my-version | pytest, ruff, mypy, bandit, pip-audit |
| Node.js | `package.json` | npm version | npm test, eslint, npm audit |
| Go | `go.mod` | manual | go test, golangci-lint, go vet |
| Rust | `Cargo.toml` | cargo-bump | cargo test, clippy, cargo audit, cargo fmt |

## Quick Reference

```bash
# Interactive release (prompts for type)
/agents:release

# Specific release types
/agents:release patch      # Bug fixes (0.7.1 → 0.7.2)
/agents:release minor      # New features (0.7.1 → 0.8.0)
/agents:release major      # Breaking changes (0.7.1 → 1.0.0)

# Options
/agents:release --dry-run          # Preview without changes
/agents:release --pr               # Create PR instead of push
/agents:release --force            # Continue despite warnings
/agents:release --coverage=80      # Override coverage threshold
```

## Release Workflow

Execute these phases in order:

### Phase 1: Project Detection

Detect project type using cascade detection:

```bash
if [ -f ".claude-plugin/plugin.json" ] || [ -f "plugin.json" ]; then
    PROJECT_TYPE="claude-plugin"
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    PROJECT_TYPE="python"
elif [ -f "package.json" ]; then
    PROJECT_TYPE="nodejs"
elif [ -f "go.mod" ]; then
    PROJECT_TYPE="go"
elif [ -f "Cargo.toml" ]; then
    PROJECT_TYPE="rust"
else
    PROJECT_TYPE="generic"
fi
```

### Phase 2: Git Status Check

Verify repository state:

```bash
echo "Branch: $(git branch --show-current)"
git status --porcelain
git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline -5
```

### Phase 3: SDLC Validation

**CRITICAL**: Run comprehensive validation before any release.

Use the release validator script:

```bash
VALIDATOR="${SKILL_DIR}/scripts/release_validator.py"
python3 "$VALIDATOR" . --coverage-threshold=${COVERAGE:-95} --verbose
```

The validator checks:
- **Tests**: Run test suite, verify passing
- **Coverage**: Enforce 95% minimum (configurable)
- **Lint**: Check code style and formatting
- **Security**: Scan for vulnerabilities
- **CHANGELOG**: Verify [Unreleased] section exists
- **Breaking changes**: Detect deleted/renamed files
- **CI config**: Verify workflows exist

If validation fails without `--force`, prompt:

```
AskUserQuestion:
- question: "Validation found issues. How to proceed?"
- options:
  - "Fix issues first (Recommended)"
  - "Continue anyway"
  - "Abort release"
```

### Phase 4: Uncommitted Changes

If uncommitted changes exist:

1. Show changes: `git diff --stat`
2. Prompt for action: commit all, commit staged, skip, or abort
3. Generate conventional commit message based on project type:
   - Claude plugins: `feat(agents):`, `feat(skills):`, `fix(commands):`
   - General: `feat:`, `fix:`, `refactor:`, `docs:`

**Never commit sensitive files**: `.env*`, `*.key`, `*.pem`, `*credentials*`

### Phase 5: Version Bump

Execute version bump using appropriate tool:

| Project | Tool | Command |
|---------|------|---------|
| Claude Plugin | bump-my-version | `bump-my-version bump $TYPE` |
| Python | bump-my-version | `bump-my-version bump $TYPE` |
| Node.js | npm | `npm version $TYPE` |
| Go | manual | Edit go.mod |
| Rust | cargo-bump | `cargo bump $TYPE` |

For `--dry-run`, show preview without executing.

### Phase 6: Push Release

**Default (no --pr)**:
```bash
git push --follow-tags
```

**With --pr flag**:
```bash
BRANCH="release/$(date +%Y%m%d)-v${NEW_VERSION}"
git checkout -b "$BRANCH"
git push -u origin "$BRANCH"
gh pr create --title "chore(release): v${NEW_VERSION}" --body "..."
```

### Phase 7: Summary

Display release summary:
- Project type and path
- Version change (old → new)
- Validation results
- Git status (branch, tags, remote)

## Semver Recommendation Logic

The validator recommends version type based on changes:

| Detected | Recommendation |
|----------|---------------|
| Breaking changes (deleted/renamed files) | `major` |
| New features, significant additions | `minor` |
| Bug fixes, docs, maintenance | `patch` |

Breaking change detection analyzes git diff since last tag for:
- Deleted files (excluding tests, dotfiles)
- Renamed files (public API changes)

## Coverage Threshold

Default: **95%** coverage required.

Override methods:
1. Command flag: `--coverage=80`
2. Project config (pyproject.toml, package.json)
3. Environment: `COVERAGE_THRESHOLD=80`

## Error Handling

### Validation Failure
1. Display specific failing checks
2. Show remediation steps
3. Offer `--force` to continue or abort

### Push Failure
1. Fetch and check for conflicts
2. Attempt rebase: `git pull --rebase`
3. Retry push
4. Fallback: offer PR creation

### Version Bump Failure
1. Check for uncommitted version files
2. Verify .bumpversion.toml exists
3. Offer manual version instructions

## Safety Rules

- Never force push
- Never skip validation without explicit confirmation
- Always run full validation before release
- Preserve all git history
- Require coverage threshold by default
- Warn on breaking changes

## Additional Resources

### Scripts
- **`scripts/release_validator.py`** - Comprehensive SDLC validation script

### References
- **`references/sdlc-requirements.md`** - Detailed validation requirements per project type
- **`references/version-management.md`** - Version bump tool configurations

### Examples
- **`examples/plugin-release.md`** - Example Claude plugin release output
- **`examples/python-release.md`** - Example Python package release output
