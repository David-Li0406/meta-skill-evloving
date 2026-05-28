# Documentation Sync Examples

Real-world examples of syncing user documentation with design doc changes.

## Example 1: Simple README Sync After Feature Addition

Design doc updated with new caching feature. README is automatically updated
to reflect the new feature.

**Input:**

```bash
/docs-sync effect-type-registry
```

**Result:**

```text
Sync Report for effect-type-registry

Design docs changed: 1
- observability.md (updated: 2025-01-18)

User docs updated:
- README.md
  - Added feature: Automatic cache invalidation

Validation: ✅ All checks passed
```

## Example 2: Level-Specific Sync (README Only)

Sync only the README file, skipping repository and site documentation.

**Input:**

```bash
/docs-sync rspress-plugin-api-extractor --level=1
```

**Result:**

```text
Syncing Level 1 only (README)

Design docs checked: 5
Stale docs found: 0

README is up to date (last sync: 2025-01-17)
No changes needed
```

## Example 3: Dry-Run Preview

Preview what would change without actually writing files.

**Input:**

```bash
/docs-sync effect-type-registry --dry-run
```

**Result:**

```text
Dry-run mode: Preview of changes

Would update:

1. pkgs/effect-type-registry/README.md
   Changes:
   - Update features list (2 additions)
   - Refresh quick start example
   - Update API overview

2. pkgs/effect-type-registry/docs/caching.md
   Changes:
   - Update cache invalidation section
   - Add new TTL configuration example

No files written (dry-run mode)
To apply changes: /docs-sync effect-type-registry
```

## Example 4: Multiple Documentation Levels Updated

Architecture change affects README, repository guides, and site documentation.

**Input:**

```bash
/docs-sync rspress-plugin-api-extractor
```

**Result:**

```text
Sync Report for rspress-plugin-api-extractor

Design docs changed: 1
- type-loading-vfs.md (updated: 2025-01-18)

User docs updated:

Level 1 (README):
- Updated description
- Refreshed quick start example

Level 3 (Site docs):
- website/docs/en/packages/rspress-plugin-api-extractor/index.mdx
  - Updated architecture overview
- website/docs/en/packages/rspress-plugin-api-extractor/guides/vfs.mdx
  - Refreshed VFS integration guide

Validation: ✅ All checks passed
```

## Example 5: Custom Content Preservation

README has custom badges and examples that are preserved during sync.

**Before sync:**

```markdown
# effect-type-registry

![npm version](https://badge.fury.io/js/effect-type-registry.svg)

## Features

- Disk caching with TTL
- HTTP retry logic

## Advanced Examples

<!-- Custom section -->
Complex configuration example...
```

**After sync:**

```markdown
# effect-type-registry

![npm version](https://badge.fury.io/js/effect-type-registry.svg)

## Features

- Disk caching with TTL
- HTTP retry logic
- Automatic cache invalidation  <!-- NEW -->

## Advanced Examples

<!-- Custom section PRESERVED -->
Complex configuration example...
```

## Example 6: Conflict Detection and Resolution

User modified quick start example, but design doc also changed it.

**Input:**

```bash
/docs-sync effect-type-registry
```

**Result:**

```text
Warning: Sync conflicts detected

Conflicts:
1. README.md: Quick Start section
   - User modified example (2025-01-17)
   - Design doc updated example (2025-01-18)
   - Changes may conflict

Options:
1. Keep user version (skip update)
2. Use design doc version (replace user changes)
3. Manual merge required

Choose option [1-3]:
```

## Example 7: Breaking API Changes Detected

Design doc indicates breaking API changes that require manual review.

**Input:**

```bash
/docs-sync effect-type-registry
```

**Result:**

```text
⚠️  Breaking changes detected

Changes in observability.md:
- API signature changed: createRegistry()
- Removed export: TypeRegistry.make()
- New required parameter: config.cacheDir

Cannot auto-sync without manual review

Action required:
1. Review breaking changes in design doc
2. Update code examples manually
3. Add migration guide to README
4. Update version compatibility note
5. Re-run sync after manual updates
```

## Example 8: No Updates Needed

All documentation is already up to date.

**Input:**

```bash
/docs-sync website
```

**Result:**

```text
No changes detected

Design docs checked: 0 (module has no design docs)
User docs checked: 3

All user documentation is up to date
```

## Example 9: Repository Docs Only Sync

Update only repository documentation, skip README and site docs.

**Input:**

```bash
/docs-sync effect-type-registry --level=2
```

**Result:**

```text
Syncing Level 2 only (Repository docs)

Design docs changed: 1
- observability.md (updated: 2025-01-18)

Repository docs updated:
- docs/architecture/caching.md
  - Updated cache invalidation section
- docs/guides/configuration.md
  - Added TTL configuration options

Skipped:
- README (Level 1)
- Site docs (Level 3)

Validation: ✅ All checks passed
```

## Example 10: Full Multi-Level Sync After Major Updates

Sync all documentation levels after multiple design doc updates.

**Input:**

```bash
/docs-sync rspress-plugin-api-extractor
```

**Result:**

```text
Sync Report for rspress-plugin-api-extractor

Design docs changed: 3
- type-loading-vfs.md (updated: 2025-01-18)
- performance-observability.md (updated: 2025-01-18)
- error-observability.md (updated: 2025-01-17)

Level 1 (README):
✅ Updated features list
✅ Refreshed quick start example
✅ Updated API overview

Level 3 (Site docs):
✅ website/docs/en/packages/rspress-plugin-api-extractor/index.mdx
✅ website/docs/en/packages/rspress-plugin-api-extractor/guides/vfs.mdx
✅ website/docs/en/packages/rspress-plugin-api-extractor/guides/errors.mdx

Files updated: 4
Validation: ✅ All checks passed

Git status:
M pkgs/rspress-plugin-api-extractor/README.md
M website/docs/en/packages/rspress-plugin-api-extractor/index.mdx
M website/docs/en/packages/rspress-plugin-api-extractor/guides/vfs.mdx
M website/docs/en/packages/rspress-plugin-api-extractor/guides/errors.mdx
```
