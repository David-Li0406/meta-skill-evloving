---
name: dart-version-bumping
description: Bump lockstep versions for Dart and Flutter workspace packages based on the Unreleased section of the root CHANGELOG.md.
---

# Dart Version Bumping Skill

## When to use this skill

Use this skill when:

- You are asked to bump versions in a Dart or Flutter workspace / monorepo
- All packages share a single version
- Compatibility is guaranteed only for identical versions across packages
- Versions and releases are managed centrally
- CHANGELOG.md exists at the repository root

## Versioning Model

This repository uses **lockstep workspace versioning**:

- All packages share **one identical version**
- Every release publishes **all packages**
- Version equality guarantees compatibility across packages
- Compatibility across different versions is NOT guaranteed

Packages are distribution units, not independently versioned products.

## Source of Truth

The **only source of truth** for version decisions is:

/CHANGELOG.md → ## [Unreleased]

- There is exactly **one canonical CHANGELOG.md** at the repository root
- Package-level CHANGELOG.md files are **derived artifacts**
- Package CHANGELOG.md files must not be edited manually

Content outside `## [Unreleased]` must be ignored for version decisions.

## Semantic Versioning Rules

Versions follow:

MAJOR.MINOR.PATCH

Exactly **one** increment must be applied.

### Major Version Bump

Apply a **major bump** if and only if:

- A section named `### BREAKING` exists under `## [Unreleased]`
- Or any entry explicitly describes a breaking change

Result:

MAJOR = MAJOR + 1  
MINOR = 0  
PATCH = 0  

### Minor Version Bump

Apply a **minor bump** if and only if:

- No `### BREAKING` section exists
- New functionality is introduced via:
  - `### Added`
  - `### Features`
  - `### Changed` (non-breaking)

Result:

MINOR = MINOR + 1  
PATCH = 0  

### Patch Version Bump

Apply a **patch bump** if and only if:

- No breaking changes
- No new features
- Only fixes or maintenance work exist

Typical sections:
- `### Fixed`
- `### Refactored`
- `### Docs`
- `### Chore`

Result:

PATCH = PATCH + 1  

## Required Actions

### 1. Determine the Next Version

1. Read the current version from any `pubspec.yaml` (all versions are identical)
2. Parse `/CHANGELOG.md`
3. Extract `## [Unreleased]`
4. Determine the bump type using the rules above
5. Compute the next workspace version

### 2. Update pubspec.yaml Files

For **every package in the workspace**:

- Update the `version:` field to the new version
- Preserve formatting
- Do not modify dependencies
- Do not introduce per-package version differences

### 3. Update the Root CHANGELOG.md

- Rename `## [Unreleased]` to:

  ## [<new_version>] - <yyyy-MM-dd>

- Use the current date in `yyyy-MM-dd` format
- Insert a new empty `## [Unreleased]` section **above** it
- Preserve all existing content and ordering

### 4. Package CHANGELOG Handling (Important)

- Do NOT maintain or edit package-level `CHANGELOG.md` files
- During publishing, the root `CHANGELOG.md` is copied into each package directory
- This is a **publish-time operation only**
- Package CHANGELOG.md files are not authoritative

## Multi-Package Repositories

- Versioning is evaluated **once per workspace**
- All packages receive the same version
- Independent package versioning is explicitly forbidden
- Do not attempt to infer per-package changes

## Constraints

The agent must NOT:

- Evaluate packages independently
- Assign different versions to different packages
- Parse or interpret package-level CHANGELOG.md files
- Guess version numbers
- Skip versions
- Apply multiple version increments
- Bump versions if `## [Unreleased]` is empty
- Modify unrelated files

## Completion Criteria

The task is complete when:

- The root CHANGELOG.md is updated correctly
- All `pubspec.yaml` files contain the new identical version
- A fresh empty `## [Unreleased]` section exists
- No package-level changelog logic was introduced
- No unrelated changes exist
