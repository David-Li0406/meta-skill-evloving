# Semantic Versioning Guide

## Overview

Semantic Versioning (SemVer) is a versioning scheme that conveys meaning about the underlying changes. Version numbers follow the format `MAJOR.MINOR.PATCH`.

---

## Version Format

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── Patch: Bug fixes, no new features
  │     └──────── Minor: New features, backwards compatible
  └────────────── Major: Breaking changes
```

### Examples

| Version | Change Type |
|---------|-------------|
| 1.0.0 → 1.0.1 | Patch: Bug fix |
| 1.0.1 → 1.1.0 | Minor: New feature |
| 1.1.0 → 2.0.0 | Major: Breaking change |

---

## When to Bump Each Number

### MAJOR (X.0.0)

Bump when you make **breaking changes** that require users to modify their code or behavior.

**Examples:**
- Remove or rename a public function
- Change function signature (required parameters)
- Remove or rename CLI commands
- Change file/folder structure
- Change data format (incompatible with old format)
- Remove deprecated features
- Change authentication mechanism

```
# Before (v1.x)
def calculate_total(items, tax_rate):
    ...

# After (v2.0.0) - Breaking: parameter renamed
def calculate_total(items, tax_percentage):  # BREAKING
    ...
```

### MINOR (0.X.0)

Bump when you add **new features** in a backwards-compatible manner.

**Examples:**
- Add new function or method
- Add new optional parameter
- Add new CLI command
- Add new configuration option
- Add new file type support
- Deprecate a feature (without removing)

```
# v1.0.0
def calculate_total(items, tax_rate):
    ...

# v1.1.0 - New optional parameter (backwards compatible)
def calculate_total(items, tax_rate, discount=0):  # NEW
    ...
```

### PATCH (0.0.X)

Bump when you make **backwards-compatible bug fixes**.

**Examples:**
- Fix a bug
- Fix typo in output
- Improve error messages
- Performance improvement
- Documentation fix
- Fix edge case handling

```
# v1.0.0 - Bug: doesn't handle empty list
def calculate_total(items, tax_rate):
    total = sum(item.price for item in items)
    return total * (1 + tax_rate)

# v1.0.1 - Fixed empty list handling
def calculate_total(items, tax_rate):
    if not items:
        return 0  # FIX
    total = sum(item.price for item in items)
    return total * (1 + tax_rate)
```

---

## Starting Versions

### 0.x.x (Development Phase)

- Version `0.x.x` indicates initial development
- The public API should not be considered stable
- Breaking changes can happen in minor versions
- Common to start at `0.1.0`

### 1.0.0 (First Stable Release)

- Signals that the public API is stable
- Users can rely on backwards compatibility
- Commit to following SemVer rules strictly

**When to release 1.0.0:**
- Public API is defined and documented
- Core features are complete and tested
- Ready for production use

---

## Release Naming Convention

### Format

```
vX.Y.Z — [Program] / [Module]: [Feature]
```

### Components

| Part | Type | Description | Examples |
|------|------|-------------|----------|
| `vX.Y.Z` | Version | SemVer number | v0.2.0, v1.0.0 |
| `Program` | Noun | Major domain | Kitchen, Garden, Auth |
| `Module` | Noun-phrase | Capability area | Planning, Tasks, Users |
| `Feature` | Verb/Noun | Specific action | Create meal plan, Login |

### Examples

```
v0.1.0 — Project / Setup: Initial scaffolding
v0.2.0 — Kitchen / Planning: Create weekly meal plan
v0.3.0 — Garden / Tasks: Track watering routine
v0.3.1 — Garden / Tasks: Fix notification timing
v0.4.0 — Kitchen / Inventory: Track pantry items
v1.0.0 — MVP Release: Full Kitchen and Garden support
```

---

## Scope Tags

Machine-readable tags for commits and release notes.

### Format

```
scope: program.module.feature
```

All lowercase, kebab-case for multi-word names.

### Examples

```
scope: kitchen.planning.create-meal-plan
scope: garden.tasks.track-watering
scope: auth.users.password-reset
```

### Usage in Commits

```
feat(kitchen.planning): Add weekly meal plan generation

scope: kitchen.planning.create-meal-plan

- Added meal plan generation algorithm
- Created planning UI components
- Integrated with recipe database
```

---

## Pre-Release Versions

For testing before official release.

### Formats

| Type | Format | Use Case |
|------|--------|----------|
| Alpha | `1.0.0-alpha.1` | Internal testing, unstable |
| Beta | `1.0.0-beta.1` | External testing, feature complete |
| RC | `1.0.0-rc.1` | Release candidate, only blockers fixed |

### Rules

- Pre-release versions have lower precedence: `1.0.0-alpha.1 < 1.0.0`
- Use only for significant releases (e.g., v1.0.0)
- Increment the pre-release number: `alpha.1`, `alpha.2`, etc.

---

## Version Precedence

Versions are compared left to right:

```
1.0.0 < 2.0.0 < 2.1.0 < 2.1.1

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0 < 1.0.1
```

---

## Common Mistakes

### Mistake 1: Breaking changes in MINOR

```
# v1.0.0
def get_user(id):
    return user

# v1.1.0 - WRONG! This is breaking (changed return type)
def get_user(id):
    return {"user": user, "metadata": {...}}

# Should be v2.0.0
```

### Mistake 2: New features in PATCH

```
# v1.0.0
class User:
    def __init__(self, name):
        self.name = name

# v1.0.1 - WRONG! New feature should be MINOR
class User:
    def __init__(self, name, email=None):  # New feature
        self.name = name
        self.email = email

# Should be v1.1.0
```

### Mistake 3: Skipping versions

```
# Don't do this:
v1.0.0 → v1.0.5 (skipped 1-4)

# Do this:
v1.0.0 → v1.0.1 → v1.0.2 (sequential)
```

---

## Checklist

Before releasing:

- [ ] Version number follows SemVer
- [ ] CHANGELOG updated with all changes
- [ ] Release name follows convention
- [ ] Breaking changes documented (if MAJOR)
- [ ] Migration guide provided (if MAJOR)
- [ ] All tests pass
- [ ] Documentation updated
