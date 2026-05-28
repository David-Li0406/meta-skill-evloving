---
name: prepare-release
description: Prepare a new version release with changelog and version bumps
license: MIT OR Apache-2.0
---

# Prepare Release

Steps to prepare a new skilo release.

## Checklist

1. All tests pass
2. No Clippy warnings
3. Update version in `Cargo.toml`
4. Update `Cargo.lock`
5. Update `CHANGELOG.md`
6. Find and update version references in docs
7. Commit changes (including `Cargo.lock`)
8. Create git tag

## Version Bump

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
```

## Update Version References in Docs

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
