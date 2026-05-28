---
name: dependency-analyzer
description: Use this skill when you need to analyze project dependencies, detect outdated packages, identify breaking changes, and suggest safe update strategies to maintain dependency health and security.
---

# Skill body

## Step 1: Identify Dependency Files

Locate dependency files:

- `package.json` (Node.js)
- `requirements.txt` (Python)
- `go.mod` (Go)
- `Cargo.toml` (Rust)
- `pom.xml` (Java/Maven)

## Step 2: Analyze Dependencies

Examine dependencies:

- Read dependency files
- Check versions
- Identify outdated packages
- Note version constraints

## Step 3: Semantic Versioning Analysis

Analyze version numbers using semantic versioning (semver):

1. **Parse version numbers**:
   - Extract major.minor.patch from version strings
   - Handle version ranges (^, ~, >=, etc.)
   - Identify exact vs range versions

2. **Detect major version bumps**:
   - Compare current version with latest available
   - Identify major version changes (e.g., 1.x.x -> 2.x.x)
   - Flag major updates as potentially breaking

3. **Check changelogs for breaking changes**:
   - For major version updates, research breaking changes
   - Look for "BREAKING CHANGE" markers in changelogs
   - Check migration guides and review release notes for breaking changes
   - Document specific breaking changes found

4. **Semantic Versioning Rules**:
   - **Major version (X.0.0)**: Breaking changes likely, requires code changes
   - **Minor version (0.X.0)**: New features, backward compatible
   - **Patch version (0.0.X)**: Bug fixes, backward compatible

5. **Breaking Change Detection**:
   - Parse changelog entries for breaking change indicators
   - Identify deprecated APIs
   - Check for removal of features