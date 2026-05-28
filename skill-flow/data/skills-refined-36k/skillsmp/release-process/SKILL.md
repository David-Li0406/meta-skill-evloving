---
name: release-process
description: >-
  Plan and execute releases with semantic versioning and bracket-based freezing. Use when: "how do I release", "bump the version", "write the changelog", "what version comes next", "release the plugin", or managing scope creep in monorepos. Prevents version thrashing; supports single projects, monorepos, and multi-component systems.
version: 1.0.2
allowed-tools: Read,Write,Edit,Bash(git:*),Grep,Glob
---

# Release Process Guidance

Execute semantic versioning releases with bracket-based version freezing. This skill helps prevent version thrashing and coordinate releases across single projects, monorepos, plugins, and multi-component systems.

## Quick Start: 6-Step Release Process

Follow these steps in order. Use references for complex scenarios (scope creep, multi-component, breaking changes).

### Step 1: Determine Scope

What's changing? Pick ONE:

**PATCH** (bump Z: 1.0.2 → 1.0.3) — Fixes, clarifications, no user-facing additions
- Bug fixes in existing code
- Documentation updates or rewording
- Correcting typos and wording
- Better examples or explanations of existing features
- Improving performance (without API change)
- Adding warnings/guardrails to existing functionality
- Restructuring guides for clarity (same content)

**MINOR** (bump Y, reset Z: 1.0.5 → 1.1.0) — New capabilities, backward compatible
- New commands or features users can access
- New tool access or permissions
- New reference guides or entirely new sections
- Expanding existing API with new methods
- Adding completely new capabilities

**MAJOR** (bump X, reset Y,Z: 1.5.2 → 2.0.0) — Breaking changes
- Removing or renaming commands
- Changing behavior incompatibly
- Changing output format incompatibly
- Restructuring that requires user migration

⚠️ **Key distinction:** "Clarifying existing feature" (PATCH) ≠ "Adding new feature" (MINOR)

⚠️ **If uncertain:** Run `git diff` to see exact changes. Don't rely on memory.

### Step 2: Find Current Version

```bash
# Single-component (pick one):
grep '"version"' package.json
grep 'version:' SKILL.md frontmatter
grep 'version =' Cargo.toml

# Multi-component:
grep -r '"version"' .
```

### Step 3: Apply Bracket Rules

**Core principle:** Version freezes at scope level until commit. Can jump up, never down.

| If Currently At | And Discover | Do This | Example |
|---|---|---|---|
| 1.0.1 (fresh) | Patch work | Bump Z | 1.0.1 → 1.0.2 |
| 1.0.1 (fresh) | Minor work | Jump to Y+1, Z=0 | 1.0.1 → 1.1.0 |
| 1.0.1 (fresh) | Major work | Jump to X+1, Y=0, Z=0 | 1.0.1 → 2.0.0 |
| 1.0.2 (patch frozen) | Discover minor | Jump to minor | 1.0.2 → 1.1.0 |
| 1.1.0 (minor frozen) | Discover major | Jump to major | 1.1.0 → 2.0.0 |
| 2.0.0 (major frozen) | More work | **Don't bump again** | 2.0.0 (stays) |

**Why frozen?** Prevents version thrashing. One release = one version bump.

### Step 4: Update All Version Files

Find and update EVERY file containing the version:

**Common locations:**
- `package.json` (Node.js) — `"version": "X.Y.Z"`
- `Cargo.toml` (Rust) — `version = "X.Y.Z"`
- `SKILL.md` (Claude) — `version: X.Y.Z` in frontmatter
- Root `plugin.json` (plugins) — `"version": "X.Y.Z"`

Use Grep to search across all files:
1. Search for the old version number: `grep -r "X.Y.Z" .`
2. Review results to identify all version references
3. Update each file with the new version
4. Verify: Search for the old version again; should return zero results

**Multi-component rule:** If your project has children (skills, services), parent version ≥ highest child version.

⚠️ **Error prevention:** After updating, search again for the old version to catch any you missed.

### Step 5: Update CHANGELOG.md

Add entry at the TOP (under `## [Unreleased]`):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature users can access

### Changed
- Existing behavior modified (backward compatible)

### Fixed
- Bug that was broken

### Removed
- Feature that's gone
```

**Four critical rules (non-negotiable):**

1. ⚠️ **Only document changes users see** — Skip internal refactoring, code cleanup, optimization
2. ⚠️ **NEVER say "bumped version"** — NO "Bumped to 1.2.3", NO "Updated version", NO "skill-x: 1.0.0→1.0.1"
3. ⚠️ **Verify each change exists** — Run `git diff` and only document what's actually there
4. ⚠️ **Be specific** — "Reduced search from 500ms→50ms" not "Improved performance"

### Step 6: Commit and Tag

```bash
# Final verification
git status           # See what's staged
git diff             # See exact changes
head -20 CHANGELOG.md # Verify entries

# Stage only version files and changelog
git add package.json Cargo.toml SKILL.md plugin.json CHANGELOG.md

# Commit (DO NOT use --amend unless asked)
git commit -m "Release version X.Y.Z

- Added: What users can now do
- Fixed: What was broken and is fixed
- Changed: What works differently
"

# Tag and push
git tag vX.Y.Z
git push origin vX.Y.Z  # if using remote
```

⚠️ **Error prevention:** If you realize you forgot a file AFTER committing, create a NEW commit (don't amend).

## Multi-Component Projects (Monorepos, Plugins)

**Key rule:** Parent version ≥ highest child version. Only bump components that changed.

**Example:** If plugin is 1.2.0 and skill-a gets a minor bump to 1.1.0, plugin must jump to 1.3.0 (stays ≥ 1.1.0).

**Detect changed components:**
```bash
git diff HEAD~1 --name-only  # See all changed files since last commit
```

Version only the components in that list. See `references/project-structures.md` for detailed examples.

## Common Release Patterns

### Pattern 1: Patch Release (Bug Fix + Docs)

```
Current: 1.2.3 → New: 1.2.4
Changes: Fix bug, update docs
Type: Patch (Z only)

CHANGELOG:
## [1.2.4] - 2026-01-21
### Fixed
- Fix timeout in database queries
- Fix typo in README
```

### Pattern 2: Feature Release (New Capability)

```
Current: 1.2.3 → New: 1.3.0
Changes: New encryption support
Type: Minor (Y+1, Z→0)

CHANGELOG:
## [1.3.0] - 2026-01-22
### Added
- Support for encrypted documents
```

### Pattern 3: Breaking Release (API Change)

```
Current: 1.5.2 → New: 2.0.0
Changes: Rename command (breaking)
Type: Major (X+1, Y→0, Z→0)

CHANGELOG:
## [2.0.0] - 2026-01-23
### Changed
- **BREAKING**: Renamed 'validate' to 'verify'
### Removed
- Old 'validate' command (use 'verify')
```

### Pattern 4: Scope Creep (Multiple Jumps)

```
Discoveries:
1. Bug fix detected → 1.2.1 (patch frozen)
2. Need new feature → 1.3.0 (jump to minor)
3. Need breaking change → 2.0.0 (jump to major)
4. Find another bug → 2.0.0 (stay major)

Final: 2.0.0 with all changes documented
See references/workflows.md for details
```

## ⚠️ Critical Rules (Don't Violate These)

**Violating these rules breaks team coordination and creates confusing git history. Follow them strictly.**

### Rule 1: One Version Bump Per Release Cycle

**What:** Bump once, commit once. Don't chain bumps (1.0.1 → 1.0.2 → 1.1.0).

**Why:** Prevents version thrashing. One release = one version = one git commit.

**Consequence:** Multiple bumps create confusing git history and version confusion. Teams don't know which version is deployed.

---

### Rule 2: Never Amend Releases After Commit

**What:** If you realize you missed a file AFTER committing, create a NEW commit (never use `git commit --amend`).

**Why:** Clear git history for teams. Amended commits are confusing in shared repositories.

**Consequence:** Amended releases hide what actually happened. Other team members pull old versions. Deploy failures.

---

### Rule 3: Never Document Version Bumps in CHANGELOG

**What:** CHANGELOG documents changes to users, not version management.

**Why:** Changelogs are for users to understand impact. Version numbers are metadata.

**Consequence:** Confusing changelogs that waste users' time. Example of what NOT to write:
- ❌ "Bumped to 1.2.3"
- ❌ "Updated version from 1.0.0 to 1.1.0"
- ❌ "skill-x: 1.0.0 → 1.0.1"

**Write instead:**
- ✅ "Fixed timeout bug in API requests"
- ✅ "Added support for encrypted documents"

---

### Rule 4: Verify Changes Against git diff

**What:** Don't document from memory. Run `git diff` and only document what's actually there.

**Why:** Prevents documenting changes that don't exist or forgetting actual changes.

**Consequence:** Users read about changes that don't exist in their code. Credibility destroyed.

---

### Rule 5: Parent Version ≥ Highest Child Version

**What:** In multi-component projects, parent version must be ≥ every child version.

**Why:** Prevents version confusion. If parent is 1.2.0 but child is 1.3.0, nobody knows which version controls what.

**Consequence:** Version confusion across teams. Deployments fail. Coordination breaks down.

## When to Use References

- **Bracket System Deep Dive:** `references/bracket-system.md` — Understand state transitions and scope creep
- **Changelog Best Practices:** `references/changelog-guidelines.md` — Learn all sections and common mistakes
- **Project Patterns:** `references/project-structures.md` — Single-component to complex monorepos
- **Step-by-Step Workflows:** `references/workflows.md` — Detailed procedures for all scenarios
