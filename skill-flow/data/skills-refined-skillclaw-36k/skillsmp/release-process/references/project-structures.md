# Project Structures

The release process works with any project structure. Find your pattern and apply the bracket system.

## Single-Component Project

Simple project with one versioned component.

### Structure

```
my-project/
├── package.json           ← Version: X.Y.Z
├── src/
├── CHANGELOG.md
└── README.md
```

### Version Files to Update

- `package.json` (or equivalent: `Cargo.toml`, `setup.py`, `pom.xml`, etc.)
- `CHANGELOG.md`

### Release Process

1. Assess scope (PATCH/MINOR/MAJOR)
2. Bump version in `package.json`
3. Update `CHANGELOG.md`
4. Commit: `git commit -m "Release version X.Y.Z"`
5. Tag: `git tag vX.Y.Z`

### Example: Rails App

```
rails-app/
├── package.json           (version: "1.2.3")
├── Gemfile
├── app/
├── spec/
├── CHANGELOG.md
└── README.md
```

## Multi-Component Project (Monorepo)

Multiple independent components in one repository, each with its own version.

### Structure

```
my-monorepo/
├── package.json           ← Parent version ≥ highest child
├── CHANGELOG.md           ← Documents parent + child changes
├── services/
│   ├── api/
│   │   ├── package.json   ← Independent version
│   │   └── CHANGELOG.md
│   └── worker/
│       ├── package.json   ← Independent version
│       └── CHANGELOG.md
└── README.md
```

### Version Strategy

- **Each component versions independently**
- **Parent version ≥ highest child version**
- If child is 1.1.0 and parent is 1.0.0 → bump parent to 1.1.0
- **Selective updates**: Only update components that changed

### Release Process

1. Identify which components changed
2. For each changed component:
   - Assess scope (PATCH/MINOR/MAJOR)
   - Bump version in component's version file
   - Update component's CHANGELOG.md
3. Bump parent version to ≥ highest child version
4. Update parent CHANGELOG.md
5. Commit all changes
6. Tag with parent version: `git tag vX.Y.Z`

### Example: Monorepo with Two Services

**Initial state:**
- Parent: 1.2.0
- API: 1.1.0
- Worker: 1.0.5

**Changes discovered:**
- API: Bug fix → 1.1.1 (patch)
- Worker: New feature → 1.1.0 (minor)
- Parent: Unchanged internally, but child is 1.1.0 → parent should be ≥ 1.1.0

**Final state:**
- Parent: 1.2.0 → 1.3.0 (to match worker's capability level)
- API: 1.1.0 → 1.1.1
- Worker: 1.0.5 → 1.1.0

**Commit:**
```bash
git add services/api/package.json services/api/CHANGELOG.md \
        services/worker/package.json services/worker/CHANGELOG.md \
        package.json CHANGELOG.md
git commit -m "Release version 1.3.0

- api: Fixed bug in request handling
- worker: Added new processing capability
"
git tag v1.3.0
```

## Claude Plugin with Bundled Skills

Plugin with bundled skills, each versioning independently.

### Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json        ← Plugin version: X.Y.Z
├── CHANGELOG.md           ← Documents all changes
├── skills/
│   ├── skill-a/
│   │   ├── SKILL.md       ← Independent version
│   │   └── references/
│   ├── skill-b/
│   │   ├── SKILL.md       ← Independent version
│   │   └── references/
│   └── skill-c/
│       ├── SKILL.md       ← Independent version
│       └── references/
└── README.md
```

### Version Strategy

- **Plugin version ≥ highest skill version**
- Each skill versions independently
- Only update skills that changed
- If skill is 1.1.0 and plugin is 1.0.0 → bump plugin to 1.1.0

### Release Process

1. Identify which skills changed
2. For each changed skill:
   - Assess scope (PATCH/MINOR/MAJOR)
   - Bump version in skill's SKILL.md frontmatter
   - Update skill's CHANGELOG.md (optional, can use plugin's CHANGELOG)
3. Bump plugin version to ≥ highest skill version
4. Update plugin's CHANGELOG.md with all changes
5. Commit all changes
6. Tag with plugin version: `git tag vX.Y.Z`

### Example: Plugin with Three Skills

**Initial state:**
- Plugin: 1.2.0
- Skill-a: 1.0.0
- Skill-b: 1.0.0
- Skill-c: 1.0.0

**Changes discovered:**
- Skill-a: New feature → 1.1.0 (minor)
- Skill-b: Bug fix → 1.0.1 (patch)
- Skill-c: No changes → stays 1.0.0

**Final state:**
- Plugin: 1.2.0 → 1.3.0 (to match skill-a)
- Skill-a: 1.0.0 → 1.1.0
- Skill-b: 1.0.0 → 1.0.1
- Skill-c: 1.0.0 (unchanged)

**CHANGELOG.md:**
```markdown
## [1.3.0] - 2026-01-21

### Added (skill-a)
- New encryption support for sensitive data
- New parameter for custom validation rules

### Fixed (skill-b)
- Fix timeout in request handling
```

## Single Skill (Standalone)

A skill released independently as a package.

### Structure

```
my-skill/
├── SKILL.md               ← Version in frontmatter
├── CHANGELOG.md
├── references/
│   ├── guide.md
│   └── examples.md
└── README.md
```

### SKILL.md Frontmatter

```yaml
---
name: my-skill
description: What this skill does
version: 1.0.0
---
```

### Version Files to Update

- `SKILL.md` frontmatter `version:` field
- `CHANGELOG.md`

### Release Process

1. Assess scope (PATCH/MINOR/MAJOR)
2. Update version in `SKILL.md` frontmatter
3. Update `CHANGELOG.md`
4. Commit: `git commit -m "Release version X.Y.Z"`
5. Tag: `git tag vX.Y.Z`

### Example

```yaml
---
name: release-process
description: Guide semantic versioning releases using bracket-based freezing
version: 1.1.0
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
---
```

## Node.js Project (package.json)

### Version Location

```json
{
  "name": "my-project",
  "version": "1.2.3",
  "description": "..."
}
```

### Update Command

```bash
npm version patch    # Bumps Z (1.2.3 → 1.2.4)
npm version minor    # Bumps Y, resets Z (1.2.3 → 1.3.0)
npm version major    # Bumps X, resets Y,Z (1.2.3 → 2.0.0)
```

## Rust Project (Cargo.toml)

### Version Location

```toml
[package]
name = "my-project"
version = "1.2.3"
```

### Update Method

```bash
# Manual edit required, no automatic tool
# Edit Cargo.toml: version = "1.2.3"
```

## Python Project (pyproject.toml)

### Version Location

```toml
[project]
name = "my-project"
version = "1.2.3"
```

## Java Project (pom.xml)

### Version Location

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-project</artifactId>
    <version>1.2.3</version>
</project>
```

## Ruby Project (.gemspec)

### Version Location

```ruby
Gem::Specification.new do |s|
  s.name        = "my-project"
  s.version     = "1.2.3"
end
```

## Go Project (no built-in version)

### Strategy

- Use git tags for versioning: `v1.2.3`
- Optionally maintain version in:
  - `version/version.go` constant
  - `main.go` const
  - `.version` file

### Example (version/version.go)

```go
package version

const Version = "1.2.3"
```

## Finding All Version References

Before releasing, find every place version appears:

```bash
# Search for version strings
grep -r '"version"' .
grep -r "version =" .
grep -r "version:" .
grep -r "Version =" .
grep -r "__version__" .

# Exclude common directories
grep -r '"version"' . --exclude-dir=node_modules --exclude-dir=.git
```

## Version Bumping Across Multiple Files

For projects with version in multiple places:

```bash
# Find all occurrences
grep -r "1.2.3" .

# Create a checklist
# 1. package.json version
# 2. SKILL.md version
# 3. MyProject.ts version const
# 4. Any other files...

# Update each one
# Use Edit tool: systematic, no mistakes
# Commit once with all files updated
```

## Parent Version Rules (Multi-Component)

When a project has multiple versioned components:

**Rule: Parent version ≥ highest child version**

### Examples

| Scenario | Child Versions | Parent Should Be | Reason |
|----------|----------------|------------------|--------|
| All at same version | All 1.0.0 | 1.0.0 | Match |
| One child bumped | 1.1.0, 1.0.0, 1.0.0 | 1.1.0 or higher | Parent ≥ highest |
| Multiple children bumped | 1.1.0, 1.2.0, 1.0.0 | 1.2.0 or higher | Parent ≥ highest |
| Parent needs bump | Parent 1.0.0, Child 1.1.0 | 1.1.0 | Update parent |

### Real Example

**Before release:**
- Plugin: 1.5.0
- Skill-A: 1.2.0
- Skill-B: 1.1.0

**After changes:**
- Plugin: Should be bumped (changes were made)
- Skill-A: New feature discovered → 1.3.0
- Skill-B: No changes → stays 1.1.0

**Final state:**
- Plugin: 1.5.0 → 1.6.0 (parent ≥ 1.3.0, so bump to 1.6.0 if parent also has changes, or 1.3.0 if parent only coordinates)

**Most common:** Parent gets MINOR bump to match highest child capability
