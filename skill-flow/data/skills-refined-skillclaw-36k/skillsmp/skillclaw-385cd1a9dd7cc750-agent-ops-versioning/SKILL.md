---
name: agent-ops-versioning
description: Use this skill when you need to manage semantic versioning, generate changelogs, and coordinate releases based on completed issues or git history.
---

# Versioning & Release Management

## Purpose
Manage semantic versioning, generate changelogs from completed issues or git history, and coordinate releases.

## Input Sources

Changelog entries can be generated from multiple sources:

| Source | Command | Best For |
|--------|---------|----------|
| **Issues** (default) | `/agent-version bump minor` | Teams using issue-first workflow |
| **Git diff** | `/agent-version bump minor --from main` | Teams not using AgentOps issues |
| **Git tags** | `/agent-version bump minor --from v2.0.0` | Compare against specific release |
| **Hybrid** | `/agent-version bump minor --include-git` | Catch commits without issues |

## Semantic Versioning Rules

Follow [SemVer 2.0.0](https://semver.org/):

| Bump | When | Example |
|------|------|---------|
| **MAJOR** | Breaking changes, incompatible API changes | 1.0.0 → 2.0.0 |
| **MINOR** | New features, backward compatible | 1.0.0 → 1.1.0 |
| **PATCH** | Bug fixes, backward compatible | 1.0.0 → 1.0.1 |

### Pre-release Tags
- `-alpha.1` — Early development, unstable
- `-beta.1` — Feature complete, testing
- `-rc.1` — Release candidate, final testing

### Build Metadata
- `+build.123` — CI build number
- `+20260115` — Build date

## Operations

### 1. Version Bump

```
/agent-version bump {major|minor|patch} [--prerelease {alpha|beta|rc}]
```

**Procedure:**
1. Read current version from README.md badge or package.json.
2. Calculate new version based on bump type.
3. Scan `issues/history.md` for issues since last version tag.
4. Generate changelog entries.
5. Update files:
   - CHANGELOG.md — Add new version section.
   - README.md — Update version badge and history table.
   - package.json (if exists) — Update version field.
6. Suggest git tag command (never auto-create).

**Output:**
```
📦 Version Bump: 2.0.0 → 2.1.0

Changes detected (12 issues):
- Added: 5 features
- Fixed: 4 bugs  
- Changed: 2 enhancements
- Security: 1 fix

Files to update:
- [x] CHANGELOG.md
- [x] README.md (badge + history)
- [ ] package.json (not found)

Preview CHANGELOG entry? [Y/n]
```

### 2. Changelog Generation

Auto-generate changelog entries from completed issues.

**Mapping issue types to changelog entries:**
- [Further details on mapping can be added here if necessary.]