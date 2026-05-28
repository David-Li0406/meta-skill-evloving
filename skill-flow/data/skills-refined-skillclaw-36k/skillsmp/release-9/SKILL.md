---
name: release
description: Release a Lean project with tier-aware dependency ordering. Use when releasing, versioning, tagging, or publishing a project in the workspace.
---

# Release Workflow

Guide the release process for Lean projects with dependency tier awareness.

## Quick Start

1. Identify project to release
2. Check tier ordering (can't release before dependencies)
3. Build and test
4. Commit, tag, and push
5. List downstream projects needing updates

## Dependency Tiers (release in order)

| Tier | Projects |
|------|----------|
| 0 | crucible, staple, cellar, assimptor, raster |
| 1 | herald, trellis, collimator, protolean, scribe, chronicle, terminus, fugue, linalg, chronos, measures, rune, tincture, wisp, chisel, ledger, quarry, convergent, reactive, tabular, entity, totem, conduit, tracer, smalltalk |
| 2 | citadel, legate, oracle, parlance, arbor, blockfall, twenty48, minefield, solitaire, stencil |
| 3 | loom, afferent, canopy, ask, lighthouse, enchiridion, docgen |
| 4 | todo-app, homebase-app, chroma, vane, worldmap, grove, cairn, afferent-demos |

## Release Process

### Step 1: Pre-flight Checks

```bash
cd <category>/<project>

# Check current version
git describe --tags --abbrev=0 2>/dev/null || echo "No tags yet"

# Check for uncommitted changes
git status

# Ensure dependencies are released
# (check lakefile.lean for require statements)
```

### Step 2: Build and Test

```bash
# For FFI projects
./build.sh

# For standard projects
lake build && lake test
```

### Step 3: Commit and Tag

```bash
git add -A
git commit -m "Description of changes"
git push origin master

# Determine next version
git tag -l "v*" | sort -V | tail -1  # See latest

# Create new tag
git tag v0.0.X
git push origin v0.0.X
```

### Step 4: Update Downstream Projects

After releasing, these projects may need lakefile updates:

**Tier 0 → Tier 1+**: Almost all projects depend on tier 0
**Key dependencies:**
- crucible: All projects with tests
- collimator: afferent, and projects using optics
- terminus: blockfall, twenty48, minefield, lighthouse, enchiridion
- herald: citadel, loom
- arbor: afferent, canopy
- wisp: oracle, afferent, loom

## Version Tag Format

Always use semantic versioning: `v0.0.1`, `v0.1.0`, `v1.0.0`

## GitHub Note

Repository name for `chronos` is `nathanial/chronos-lean` (all others match directory name).
