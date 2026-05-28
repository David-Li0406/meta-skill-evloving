# Changelog Templates

Template variations for different initialization scenarios.

## Basic Template (No Existing Version)

Use when initializing a new project with no released versions:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
```

**When to use:**
- New projects with no releases
- Projects starting from version 0.1.0
- No git tags or package version found

---

## Template with Initial Version

Use when a version is detected from git tags or package files:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [VERSION] - YYYY-MM-DD

### Added
- Initial release
```

**Variable substitution:**
- `VERSION`: Detected version (e.g., "1.0.0", "0.1.0")
- `YYYY-MM-DD`: Current date in ISO 8601 format

**When to use:**
- Existing project with git tags
- Project has package.json, Cargo.toml, or pyproject.toml with version
- Retroactive changelog addition to versioned project

---

## Template with Links

Use when git repository is hosted on GitHub, GitLab, or similar:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [VERSION] - YYYY-MM-DD

### Added
- Initial release

[Unreleased]: REPO_URL/compare/vVERSION...HEAD
[VERSION]: REPO_URL/releases/tag/vVERSION
```

**Variable substitution:**
- `VERSION`: Detected version
- `YYYY-MM-DD`: Current date
- `REPO_URL`: Git remote URL (extract from git config)

**When to use:**
- Repository has remote configured
- Team prefers linked changelogs
- Integration with GitHub/GitLab releases

---

## Minimal Template

Use for lightweight projects or rapid prototyping:

```markdown
# Changelog

## [Unreleased]

### Added

### Fixed

## [VERSION] - YYYY-MM-DD
- Initial release
```

**When to use:**
- Small personal projects
- Prototypes or experiments
- Projects with infrequent changes

---

## Enterprise Template

Use for large projects requiring detailed change tracking:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
<!-- New features -->

### Changed
<!-- Changes in existing functionality -->

### Deprecated
<!-- Soon-to-be removed features -->

### Removed
<!-- Removed features -->

### Fixed
<!-- Bug fixes -->

### Security
<!-- Security vulnerability fixes -->

## [VERSION] - YYYY-MM-DD

### Added
- Initial release

---

## Guidelines

### Writing Changelog Entries

- Use clear, concise language
- Write for end users, not developers
- Include context when helpful
- Group related changes together
- Highlight breaking changes with **BREAKING**

### Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version: Incompatible API changes
- MINOR version: Backwards-compatible features
- PATCH version: Backwards-compatible bug fixes

### Contribution

When contributing, add your changes to the [Unreleased] section under the appropriate category.
```

**When to use:**
- Large team projects
- Projects requiring detailed documentation
- Enterprise or commercial software
- Projects with strict change management

---

## Template Selection Logic

### Decision Tree

```
Is there a detected version?
├─ Yes → Has remote repository?
│  ├─ Yes → Use "Template with Links"
│  └─ No → Use "Template with Initial Version"
└─ No → Is this an enterprise/large project?
   ├─ Yes → Use "Enterprise Template" (without version section)
   └─ No → Use "Basic Template (No Existing Version)"
```

### Detection Methods

**Version detection priority:**
1. Git tags matching semver pattern: `v?[0-9]+\.[0-9]+\.[0-9]+`
2. package.json `version` field
3. Cargo.toml `version` field
4. pyproject.toml `version` field
5. No version → Use basic template

**Remote repository detection:**
```bash
git remote get-url origin 2>/dev/null
```

If remote exists and matches known hosts:
- `github.com` → Use GitHub-style links
- `gitlab.com` → Use GitLab-style links
- Other → Generic version links

---

## Template Variables

### Standard Variables

| Variable | Description | Example | Source |
|----------|-------------|---------|--------|
| `VERSION` | Semver version number | "1.2.0" | Git tag, package file |
| `YYYY-MM-DD` | ISO date | "2025-01-15" | Current date |
| `REPO_URL` | Repository URL | "https://github.com/user/repo" | git remote |

### Variable Substitution Examples

**From git tag:**
```bash
# Input: git tag v1.2.0
# Template: ## [VERSION] - YYYY-MM-DD
# Output: ## [1.2.0] - 2025-01-15
```

**From package.json:**
```bash
# Input: "version": "0.5.3"
# Template: ## [VERSION] - YYYY-MM-DD
# Output: ## [0.5.3] - 2025-01-15
```

**Repository URL:**
```bash
# Input: git remote get-url origin
#        https://github.com/username/repo.git
# Template: [Unreleased]: REPO_URL/compare/vVERSION...HEAD
# Output: [Unreleased]: https://github.com/username/repo/compare/v1.2.0...HEAD
```

---

## Language-Specific Considerations

### JavaScript/Node.js

**Version source:** `package.json`
```json
{
  "version": "1.2.0"
}
```

**Additional context:** May include npm package link in header

### Rust

**Version source:** `Cargo.toml`
```toml
[package]
version = "1.2.0"
```

**Additional context:** May include crates.io link

### Python

**Version source:** `pyproject.toml`
```toml
[project]
version = "1.2.0"
```

**Additional context:** May include PyPI link

### Go

**Version source:** Git tags only (no package file convention)

**Additional context:** May include pkg.go.dev link

---

## Special Cases

### Pre-1.0 Projects

For projects in initial development (version < 1.0.0):

```markdown
## [0.3.0] - 2025-01-15

### Added
- Feature description

**Note:** This is a pre-1.0 release. The API is not yet stable and may change.
```

### Monorepo Projects

For monorepos tracking multiple packages:

```markdown
# Changelog

## [Unreleased]

### Package A
#### Added
- Feature in package A

### Package B
#### Fixed
- Bug fix in package B
```

Or use separate changelogs per package:
```
packages/
├── package-a/
│   └── CHANGELOG.md
└── package-b/
    └── CHANGELOG.md
```

### Library vs Application

**Library:** Emphasize API changes and compatibility
```markdown
### Changed
- **BREAKING**: Renamed `getData()` to `fetchData()` for clarity
- Modified return type of `processItems()` to include metadata
```

**Application:** Emphasize user-facing features
```markdown
### Added
- Dark mode toggle in settings
- Export reports to PDF format
```

---

## Validation Checklist

After template generation, verify:

- [ ] Header includes Keep a Changelog reference
- [ ] Header includes Semantic Versioning reference
- [ ] Unreleased section is present
- [ ] All six standard categories are present (Added, Changed, Deprecated, Removed, Fixed, Security)
- [ ] Date format is ISO 8601 (YYYY-MM-DD)
- [ ] Version format follows semver (if version present)
- [ ] Links are properly formatted (if links included)
- [ ] Template is valid markdown
- [ ] File encoding is UTF-8

---

## References

- Keep a Changelog: https://keepachangelog.com/
- Semantic Versioning: https://semver.org/
- ISO 8601 Date Format: https://www.iso.org/iso-8601-date-and-time-format.html
