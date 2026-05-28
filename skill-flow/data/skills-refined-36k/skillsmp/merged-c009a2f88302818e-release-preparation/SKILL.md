---
name: release-preparation
description: Use this skill when preparing a new version release, including changelog generation and version bumping.
---

# Release Preparation

This skill outlines the steps to prepare a new software release, including generating changelogs and determining version bumps based on commit analysis.

## Checklist

1. All tests pass
2. No Clippy warnings
3. Update version in `Cargo.toml`
4. Update `Cargo.lock`
5. Update `CHANGELOG.md`
6. Find and update version references in documentation
7. Commit changes (including `Cargo.lock`)
8. Create git tag

## Version Bump

Determine the appropriate version bump based on commit types:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat!:` or `BREAKING CHANGE:` | Major (1.0.0 → 2.0.0) | Breaking API change |
| `feat:` | Minor (1.0.0 → 1.1.0) | New feature |
| `fix:` | Patch (1.0.0 → 1.0.1) | Bug fix |
| `docs:`, `chore:`, `refactor:` | Patch | Maintenance |

Update version in `Cargo.toml`:

```toml
[package]
version = "X.Y.Z"
```

After updating `Cargo.toml`, run `cargo check` to update `Cargo.lock`:

```bash
cargo check
```

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Removed
- Removed features
```

## Update Version References in Documentation

Search for hardcoded version numbers in documentation and update them:

```bash
# Find version references (e.g., skilo@0.3.0, v0.3.0)
rg "skilo@\d+\.\d+\.\d+" --type md
rg "v\d+\.\d+\.\d+" README.md
```

Common locations:
- `README.md` - CI example (`cargo install skilo@X.Y.Z`)
- Installation instructions
- Badge URLs

## Release Commands

```bash
# Verify everything passes
cargo test && cargo clippy

# Commit release changes
git add -A
git commit -m "chore: release vX.Y.Z"

# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push with tags
git push && git push --tags
```

## Publishing to crates.io

```bash
# Dry run first
cargo publish --dry-run

# Publish
cargo publish
```

## Additional Notes

- Analyze commits since the last tag to generate release notes:

```bash
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```

- Check existing tags:

```bash
git tag --sort=-v:refname | head -5
```

- Use GitHub CLI for creating releases:

```bash
gh release create vX.Y.Z --generate-notes --title "vX.Y.Z"
```

## Ask Clarifying Questions If

- Versioning scheme is unclear (semver vs calver vs other)
- Pre-release versions are needed (alpha, beta, rc)
- Multiple release branches exist