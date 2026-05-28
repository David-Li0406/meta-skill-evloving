# Rust Projects with release-plz

Reference guide for semantic versioning and release automation in Rust workspaces using release-plz.

## Overview

release-plz is a Rust-native release automation tool that:
- Analyzes conventional commits since last tag
- Runs cargo-semver-checks for API compatibility validation
- Determines version bump (MAJOR/MINOR/PATCH)
- Updates CHANGELOG.md via git-cliff integration
- Creates git tags and GitHub releases
- Publishes to crates.io in dependency order

**Key Difference from Node.js semantic-release**: release-plz is SSoT-native - version lives only in `Cargo.toml`.

## Installation

```bash
cargo install release-plz
cargo install cargo-rdme  # For README SSoT
```

## Configuration Files

### release-plz.toml

```toml
[workspace]
# Changelog generation via git-cliff
changelog_config = "cliff.toml"
changelog_update = true

# Git operations
git_tag_enable = true
git_release_enable = true

# API compatibility validation
semver_check = true

# Publishing
publish = true
allow_dirty = false
dependencies_update = true

# README SSoT: Generate from lib.rs before release
pre_release_hook = "cargo rdme --workspace-project <crate-name> --readme-path README.md"

# Tag format
git_tag_name = "v{{ version }}"
git_release_name = "Project v{{ version }}"
```

### Cargo.toml (Workspace)

```toml
[workspace]
resolver = "2"
members = ["crates/*"]

[workspace.package]
version = "1.0.0"  # SSoT for version
edition = "2024"
license = "MIT"
repository = "https://github.com/user/project"

[workspace.dependencies]
# Shared dependencies here
```

### Per-Crate Cargo.toml

```toml
[package]
name = "my-crate"
version.workspace = true  # Inherit from workspace
edition.workspace = true
license.workspace = true
```

## README SSoT Architecture

The Single Source of Truth (SSoT) chain:

```
lib.rs doc comments → cargo-rdme → README.md → crates.io
```

### Setup

1. **Add markers to README.md**:
```markdown
# Project Name

[![Crates.io](https://img.shields.io/crates/v/crate.svg)](https://crates.io/crates/crate)

<!-- cargo-rdme start -->
<!-- cargo-rdme end -->

## License
```

2. **Write documentation in lib.rs**:
```rust
//! Project description.
//!
//! [![Crates.io](https://img.shields.io/crates/v/crate.svg)](https://crates.io/crates/crate)
//!
//! ## Installation
//!
//! ```toml
//! [dependencies]
//! crate = "1.0"
//! ```
//!
//! ## Usage
//!
//! ```rust
//! use crate::Thing;
//! let thing = Thing::new();
//! ```
```

3. **Configure pre_release_hook** in release-plz.toml:
```toml
pre_release_hook = "cargo rdme --workspace-project my-crate --readme-path README.md"
```

4. **Add version-sync validation**:
```toml
# Cargo.toml [dev-dependencies]
version-sync = "0.9"
```

```rust
// tests/version_sync.rs
#[test]
fn test_readme_version_matches_cargo_toml() {
    version_sync::assert_markdown_deps_updated!("README.md");
}
```

## Workflow Commands

### Preview Release

```bash
/usr/bin/env bash << 'GIT_EOF'
release-plz release --dry-run --git-token "$(gh auth token)"
GIT_EOF
```

### Execute Release

```bash
/usr/bin/env bash << 'RELEASE_EOF'
export CARGO_REGISTRY_TOKEN=$(doppler secrets get CRATES_IO_TOKEN --project myproject --config prod --plain)
release-plz release --git-token "$(gh auth token)"
RELEASE_EOF
```

### Verify Release

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# Check tags
git tag -l --sort=-version:refname | head -3

# Check GitHub release
gh release view $(git describe --tags --abbrev=0)

# Check crates.io
cargo search my-crate
PREFLIGHT_EOF
```

## Version Determination

release-plz analyzes commits since last tag:

| Commit Type | Version Bump |
|-------------|--------------|
| `feat:` or `feat!:` | MINOR |
| `fix:` | PATCH |
| `BREAKING CHANGE:` in body | MAJOR |
| `chore:`, `docs:`, `refactor:` | No bump |

cargo-semver-checks additionally validates:
- Public API changes match commit types
- Breaking changes have `BREAKING CHANGE:` or `!` in commit

## Multi-Crate Workspace

release-plz automatically publishes in dependency order. For a workspace with:
- `core` (no deps)
- `providers` (depends on core)
- `cli` (depends on providers)

Publishing order: core → providers → cli

### Partial Release Recovery

If release fails midway:

```bash
/usr/bin/env bash << 'RECOVER_EOF'
export CARGO_REGISTRY_TOKEN=$(doppler secrets get CRATES_IO_TOKEN --project myproject --config prod --plain)

# Check which crates need publishing
cargo search my-crate --limit 10

# Publish remaining crates in order
for crate in providers cli; do
  cargo publish -p $crate --allow-dirty
  sleep 10
done
RECOVER_EOF
```

## Troubleshooting

### "can't determine registry indexes"

```bash
rm -rf ~/.cargo/registry/index/github.com-*
```

### "already published"

Crates are on crates.io but tag doesn't exist:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --generate-notes
```

### cargo-rdme not found

```bash
cargo install cargo-rdme
```

### README out of sync

```bash
cargo rdme --workspace-project my-crate --readme-path README.md --check
# If fails:
cargo rdme --workspace-project my-crate --readme-path README.md
```

## Best Practices

1. **Use workspace version inheritance** - Single version in workspace Cargo.toml
2. **Configure pre_release_hook** - Automate README generation
3. **Add version-sync test** - Catch stale docs before release
4. **Use Doppler for tokens** - Secure credential management
5. **Conventional commits** - Enables automatic version determination
6. **cargo-semver-checks** - Validates API compatibility claims

## Links

- [release-plz Documentation](https://release-plz.ieni.dev/)
- [cargo-rdme](https://github.com/orium/cargo-rdme)
- [cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks)
- [version-sync](https://github.com/mgeisler/version-sync)
- [git-cliff](https://git-cliff.org/)
