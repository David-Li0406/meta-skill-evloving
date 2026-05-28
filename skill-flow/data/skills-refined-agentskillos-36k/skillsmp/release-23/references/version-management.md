# Version Management Configuration

Configuration guides for version bump tools across project types.

## bump-my-version (Python, Claude Plugins)

### Installation
```bash
pip install bump-my-version
```

### Configuration (.bumpversion.toml)

```toml
[tool.bumpversion]
current_version = "0.7.1"
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
commit = true
tag = true
tag_name = "v{new_version}"
tag_message = "Release v{new_version}"
message = "chore(release): bump version to {new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = "version = \"{current_version}\""
replace = "version = \"{new_version}\""

[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "## [Unreleased]"
replace = "## [Unreleased]\n\n## [{new_version}] - {now:%Y-%m-%d}"
```

### Claude Plugin Configuration

```toml
[tool.bumpversion]
current_version = "0.7.1"
commit = true
tag = true
tag_name = "plugin-v{new_version}"
message = "chore(plugin): bump version to {new_version}"

[[tool.bumpversion.files]]
filename = ".claude-plugin/plugin.json"
search = "\"version\": \"{current_version}\""
replace = "\"version\": \"{new_version}\""

[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "## [Unreleased]"
replace = "## [Unreleased]\n\n## [{new_version}] - {now:%Y-%m-%d}"
```

### Commands
```bash
# Dry run (preview)
bump-my-version bump patch --dry-run --verbose

# Execute bump
bump-my-version bump patch   # 0.7.1 → 0.7.2
bump-my-version bump minor   # 0.7.1 → 0.8.0
bump-my-version bump major   # 0.7.1 → 1.0.0

# Specific version
bump-my-version bump --new-version 1.0.0
```

## npm version (Node.js)

### Configuration (package.json)

```json
{
  "name": "my-package",
  "version": "1.0.0",
  "scripts": {
    "preversion": "npm test",
    "version": "npm run build && git add -A",
    "postversion": "git push && git push --tags"
  }
}
```

### Commands
```bash
# Bump version (auto-commits and tags)
npm version patch   # 1.0.0 → 1.0.1
npm version minor   # 1.0.0 → 1.1.0
npm version major   # 1.0.0 → 2.0.0

# With message
npm version patch -m "Release %s"

# Without git operations
npm version patch --no-git-tag-version
```

### Pre/Post Hooks
- `preversion`: Runs before version bump (e.g., tests)
- `version`: Runs after bump, before commit (e.g., build)
- `postversion`: Runs after commit (e.g., push)

## cargo-bump (Rust)

### Installation
```bash
cargo install cargo-bump
```

### Commands
```bash
cargo bump patch   # 0.1.0 → 0.1.1
cargo bump minor   # 0.1.0 → 0.2.0
cargo bump major   # 0.1.0 → 1.0.0
```

### Manual Alternative
Edit `Cargo.toml` directly:
```toml
[package]
name = "my-crate"
version = "1.0.0"
```

Then commit and tag:
```bash
git add Cargo.toml Cargo.lock
git commit -m "chore(release): bump version to 1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"
```

## Go Modules

Go modules don't have built-in version management. Use git tags:

### Tagging Convention
```bash
# For module at repo root
git tag v1.0.0

# For submodule at path/to/module
git tag path/to/module/v1.0.0
```

### Version in go.mod
The version is determined by git tags, not go.mod content:
```
module github.com/user/repo

go 1.21
```

### Release Process
```bash
# Ensure module is tidy
go mod tidy

# Commit changes
git add go.mod go.sum
git commit -m "chore(release): prepare v1.0.0"

# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Push with tags
git push --follow-tags
```

## Semantic Versioning Reference

### Version Format
```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
1.0.0
1.0.0-alpha.1
1.0.0-beta.2+build.123
```

### When to Bump

| Change Type | Version | Example |
|-------------|---------|---------|
| Breaking API change | MAJOR | Remove public function |
| New feature (backward compatible) | MINOR | Add new endpoint |
| Bug fix (backward compatible) | PATCH | Fix null pointer |
| Documentation only | PATCH | Update README |
| Internal refactor (no API change) | PATCH | Optimize algorithm |

### Pre-release Versions
```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

## Tag Naming Conventions

| Project Type | Tag Format | Example |
|--------------|------------|---------|
| Generic | `v{version}` | v1.0.0 |
| Claude Plugin | `plugin-v{version}` | plugin-v0.7.1 |
| Monorepo | `{package}-v{version}` | api-v1.0.0 |
| Go submodule | `{path}/v{version}` | pkg/utils/v1.0.0 |

## CHANGELOG Integration

### Keep a Changelog Format
```markdown
# Changelog

## [Unreleased]

## [1.0.0] - 2024-01-15

### Added
- New feature X

### Changed
- Updated behavior Y

### Fixed
- Bug fix Z

### Removed
- Deprecated feature W
```

### Auto-update with bump-my-version
The `[[tool.bumpversion.files]]` entry for CHANGELOG.md automatically:
1. Keeps `## [Unreleased]` header
2. Inserts new version section with date
3. Preserves existing changelog entries
