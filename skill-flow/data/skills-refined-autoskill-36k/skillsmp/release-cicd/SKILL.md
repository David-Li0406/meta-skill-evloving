---
name: release-cicd
description: Knowledge about the project's CI/CD pipeline, Semantic Versioning with Conventional Commits, release-please automation, and GoReleaser. Use when working with releases, commits, or CI workflows.
---

# Release & CI/CD

This skill covers the automated release pipeline for Drime Shell.

## Semantic Versioning (SemVer)

The project uses [Semantic Versioning](https://semver.org/) with [Conventional Commits](https://www.conventionalcommits.org/).

### Version Format

```
v{MAJOR}.{MINOR}.{PATCH}[-{PRERELEASE}]

Examples:
- v1.0.0        # Stable release
- v1.0.0-beta.1 # Beta pre-release (current phase)
```

### Commit Types → Version Bumps

| Commit Type | Example | Version Bump |
|-------------|---------|--------------|
| `feat:` | `feat: add vault lock command` | Minor (1.0.0 → 1.1.0) |
| `fix:` | `fix: handle empty folder in ls` | Patch (1.0.0 → 1.0.1) |
| `feat!:` or `BREAKING CHANGE:` | `feat!: change API response format` | Major (1.0.0 → 2.0.0) |
| `docs:`, `chore:`, `test:`, `ci:` | `docs: update README` | No release |

### Commit Message Format

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

**Examples:**
```bash
# Feature (minor bump)
feat(vault): add automatic lock timeout

# Bug fix (patch bump)
fix(upload): retry on SSL EOF errors

# Breaking change (major bump)
feat(api)!: require workspaceId on all endpoints

BREAKING CHANGE: workspaceId is now mandatory

# No release
docs: fix typo in README
chore: update dependencies
test: add coverage for edge cases
```

## CI/CD Pipeline

### Workflow Overview

```
Push to main ──► Lint (fast)
     │
     └──► release-please creates/updates Release PR

PR opened ──► Lint + Test + Coverage

Release PR merged ──► Tag created (v1.0.0-beta.X)
     │
     └──► GoReleaser builds binaries ──► GitHub Release
```

### GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push/PR to main | Lint, test, coverage |
| `release-please.yml` | Push to main | Manage Release PR |
| `release.yml` | Tag `v*` | Build & publish binaries |
| `codeql.yml` | PR/push/weekly | Security scanning |
| `dependabot-auto-merge.yml` | Dependabot PR | Auto-merge dep updates |

### CI Checks (ci.yml)

**On every push to main:**
- Fast lint with `golangci-lint`

**On PRs:**
- Lint + `go mod tidy` check
- Tests with race detector and coverage
- Coverage uploaded to Codecov

**On Release PRs (`release-please--*`):**
- Full lint
- Cross-compilation for all targets (linux/darwin/windows × amd64/arm64)
- Tests with race detector

## Release Process

### Automated via release-please

1. **Commits accumulate** on `main` with conventional commit messages
2. **release-please** creates/updates a Release PR with:
   - Version bump based on commit types
   - Auto-generated CHANGELOG
3. **Merge the Release PR** → triggers tag creation
4. **GoReleaser** builds binaries for all platforms
5. **GitHub Release** created with binaries attached

### Configuration Files

| File | Purpose |
|------|---------|
| `release-please-config.json` | Release-please settings (`prerelease: true` for beta) |
| `.release-please-manifest.json` | Current version (`"1.0.0-beta.0"`) |
| `.goreleaser.yaml` | Build matrix, binary naming, changelog |

### Build Targets

```yaml
# .goreleaser.yaml builds for:
- linux/amd64, linux/arm64
- darwin/amd64, darwin/arm64 (macOS)
- windows/amd64, windows/arm64
```

### Version Injection

GoReleaser injects version info via ldflags:

```go
// internal/build/info.go
var (
    Version = "dev"      // Set by -ldflags
    Commit  = "unknown"
    Date    = "unknown"
)
```

## Local Development Commands

```bash
# Run all checks (what CI does)
make check           # fmt + lint + test

# Individual checks
make lint            # Run golangci-lint
make test            # Run tests
make test-race       # Tests with race detector
make test-cover      # Tests with coverage report

# Local release testing
make release-dry     # GoReleaser dry-run (no publish)
```

## Graduating from Beta

To switch from beta to stable releases:

1. Edit `release-please-config.json`
2. Remove `"prerelease": true`
3. Next release will be `v1.0.0` (or appropriate version)

## Dependabot

Automated dependency updates:
- **Go modules**: Weekly checks
- **GitHub Actions**: Weekly checks
- **Auto-merge**: Enabled for passing Dependabot PRs
