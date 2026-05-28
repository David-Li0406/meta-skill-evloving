# Documentation Sync Instructions

Detailed step-by-step instructions for syncing user documentation with design
doc changes.

## Implementation Steps

### Step 1: Parse Parameters

```bash
# Parse command line arguments
# Usage: /docs-sync <module> [--level=<1|2|3>] [--dry-run]
```

Parameters:

- `module`: Module name (REQUIRED)
- `--level`: Sync specific level only (1=README, 2=repo, 3=site)
- `--dry-run`: Preview changes without writing files

### Step 2: Load Configuration

```bash
# Read design configuration
cat .claude/design/design.config.json
```

Extract for the specified module:

- Module path and package location
- Design docs path
- User docs configuration (readme, repoDocs, siteDocs)
- Quality standards for each level

### Step 3: Detect Changes

Compare timestamps between design docs and user docs:

**For design docs:**

```bash
# Find all design docs for module
find .claude/design/{module.designDocsPath} -name "*.md" -type f

# For each design doc, extract updated timestamp from frontmatter
grep -A 1 '^updated:' {design-doc-path}
```

**For user docs:**

```bash
# Get last modification time of README
stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" {module.path}/README.md

# Get last modification time of repo docs
find {module.userDocs.repoDocs} -name "*.md" -type f \
  -exec stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" {} \;

# Get last modification time of site docs
find {module.userDocs.siteDocs} -name "*.md" -o -name "*.mdx" \
  -type f -exec stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" {} \;
```

**Identify stale docs:**

- User doc is stale if design doc `updated` > user doc modification time
- Flag which user docs need updating

### Step 4: Analyze Impact

For each changed design doc, determine which user docs it affects:

**Level 1 (README) impact:**

- Overview changes → Update description
- New features → Update features list
- API changes → Update quick start and API overview
- Examples changes → Update usage examples

**Level 2 (Repository docs) impact:**

- Architecture changes → Update architecture guides
- Integration changes → Update integration guides
- New topics → Create new guide documents
- Removed topics → Archive or delete guides

**Level 3 (Site docs) impact:**

- Concept changes → Update concept documentation
- Tutorial changes → Update how-to guides
- API changes → Regenerate API reference
- Navigation changes → Update nav metadata

### Step 5: Determine Update Strategy

For each affected user doc:

**Full regeneration (recommended for):**

- README (Level 1) - small, quick to regenerate
- API reference docs - auto-generated from code
- Simple guides with no custom content

**Partial update (recommended for):**

- Repository guides with custom examples
- Site docs with custom components
- Docs with user-contributed content
- Heavily customized sections

**Manual review required (flag for):**

- Breaking changes in API
- Major architecture refactors
- Conflicting custom content
- Multiple design docs affecting same user doc

### Step 6: Update User Documentation

#### Level 1: Sync README

```bash
# Regenerate README using docs-generate-readme
# This is the simplest approach for READMEs
```

Steps:

1. Extract new content from design docs
2. Load existing README (if update mode)
3. Preserve custom sections (badges, screenshots)
4. Update standard sections (description, features, usage)
5. Write updated README
6. Update modification timestamp

#### Level 2: Sync Repository Docs

For each affected topic guide:

1. Identify which sections changed in design doc
2. Extract new content for those sections
3. Load existing guide
4. Update affected sections only
5. Preserve custom examples and notes
6. Write updated guide

#### Level 3: Sync Site Docs

For each affected site doc:

1. Identify content changes from design docs
2. Update concept docs with new information
3. Refresh how-to guides if steps changed
4. Regenerate API docs if API changed
5. Update navigation if structure changed

### Step 7: Preserve Custom Content

When updating docs, preserve:

**README custom sections:**

- Custom badges and shields
- Screenshots, GIFs, demos
- Additional examples beyond quick start
- Custom sections (Roadmap, FAQ, Contributors)
- Sponsor acknowledgments

**Repository docs custom content:**

- User-contributed examples
- Additional troubleshooting tips
- Custom diagrams and visualizations
- Community resources and links

**Site docs custom content:**

- Interactive components
- Custom MDX elements
- Additional tutorials
- Community-contributed guides

**Detection strategy:**

1. Parse existing doc into sections
2. Mark sections as "standard" or "custom"
3. Standard sections: defined in template
4. Custom sections: everything else
5. Only update standard sections during sync

### Step 8: Update Timestamps

After successful sync:

**User doc metadata:**

- Update file modification time
- Add sync timestamp to frontmatter (if applicable)
- Record which design docs triggered the sync

**Sync log:**

Create or update `.claude/.sync-log.json`:

```json
{
  "lastSync": "2025-01-18T12:00:00Z",
  "syncs": [
    {
      "timestamp": "2025-01-18T12:00:00Z",
      "module": "effect-type-registry",
      "level": "all",
      "designDocs": [
        ".claude/design/effect-type-registry/observability.md"
      ],
      "userDocs": [
        "pkgs/effect-type-registry/README.md"
      ],
      "changes": [
        "Updated features list",
        "Refreshed quick start example"
      ]
    }
  ]
}
```

### Step 9: Validate Updates

Run validation on updated docs:

**README validation:**

```bash
# Check word count
wc -w {module.path}/README.md

# Validate markdown
markdownlint {module.path}/README.md

# Check for broken links
grep -o '\[.*\](.*\.md)' {module.path}/README.md
```

**Repository docs validation:**

```bash
# Validate all repo docs
find {module.userDocs.repoDocs} -name "*.md" -exec markdownlint {} \;

# Check cross-references
grep -r '\[.*\](.*\.md)' {module.userDocs.repoDocs}
```

**Site docs validation:**

```bash
# Validate MDX syntax
# Check navigation metadata
cat {module.userDocs.siteDocs}/_meta.json

# Validate frontmatter
find {module.userDocs.siteDocs} -name "*.mdx" -exec grep -A 5 '^---' {} \;
```

### Step 10: Generate Sync Report

Create summary of changes:

```text
Sync Report for effect-type-registry
=====================================

Design docs changed since last sync: 1
- observability.md (updated: 2025-01-18)

User docs updated:
- README.md (Level 1)
  - Updated features list
  - Refreshed quick start example
  - Updated API overview

Validation:
- ✅ README word count: 387 (target: 200-500)
- ✅ Markdown linting: passed
- ✅ No broken links
- ✅ Code examples valid

Next steps:
- Review changes in git diff
- Test code examples
- Commit updated documentation
```

## Sync Strategies by Level

### Level 1: README

#### Strategy: Full regeneration

Reason: READMEs are short and standardized, full regen is fast and consistent

Process:

1. Detect changes in design docs
2. Regenerate README using docs-generate-readme
3. Preserve custom badges and screenshots
4. Validate output
5. Update timestamp

### Level 2: Repository Docs

#### Strategy: Selective update

Reason: Repo docs may have custom examples and manual enhancements

Process:

1. Identify affected topic guides
2. Parse each guide into sections
3. Update only sections affected by design doc changes
4. Preserve custom content
5. Validate cross-references
6. Update timestamps

### Level 3: Site Docs

#### Strategy: Hybrid approach

Reason: Mix of auto-generated (API) and manual (guides) content

Process:

1. Auto-regenerate API reference docs
2. Selectively update concept docs
3. Flag guides that need manual review
4. Update navigation if structure changed
5. Validate framework syntax
6. Update timestamps

## Change Detection Algorithms

### Timestamp Comparison

```javascript
// Pseudo-code for change detection
function isStale(designDoc, userDoc) {
  const designUpdated = designDoc.frontmatter.updated;
  const userModified = userDoc.stats.mtime;
  return designUpdated > userModified;
}
```

### Content Hash Comparison

For more accurate detection:

```javascript
// Calculate hash of relevant sections
function hasContentChanged(designDoc, lastSync) {
  const currentHash = hash(designDoc.content);
  const previousHash = lastSync.contentHash;
  return currentHash !== previousHash;
}
```

### Semantic Change Detection

Check for significant changes:

- New sections added
- Sections removed
- API signatures changed
- Code examples modified
- Major rewording (>30% text change)

Ignore minor changes:

- Typo fixes
- Formatting tweaks
- Comment updates
- Whitespace changes

## Conflict Resolution

### Scenario: Custom Features List

If user added custom features to README:

#### Option 1: Preserve custom, skip update

```text
Warning: Custom features section detected
Skipping features update to preserve user content
Manual review recommended
```

#### Option 2: Merge both

```text
Features from design docs:
- Feature A (from design)
- Feature B (from design)

Custom features in README:
- Feature X (custom)
- Feature Y (custom)

Merged features:
- Feature A
- Feature B
- Feature X (custom)
- Feature Y (custom)
```

#### Option 3: Replace with generated

```text
Warning: Replacing custom features with generated content
Custom features will be lost
Backup created: README.md.backup
```

### Scenario: Modified Examples

If user enhanced quick start example:

**Detection:**

```bash
# Compare example code
diff <(grep -A 10 '```typescript' .claude/design/module/main.md) \
     <(grep -A 10 '```typescript' pkgs/module/README.md)
```

**Resolution:**

- Preserve user enhancements if they extend example
- Replace if example is outdated or incorrect
- Flag for manual review if conflicting

### Scenario: Breaking Changes

If design doc indicates breaking API changes:

**Flag for manual review:**

```text
⚠️  Breaking changes detected in design docs
Cannot auto-sync without manual review

Changes:
- API signature changed: getTypeDefinitions()
- Removed exports: TypeRegistry.create()
- New required parameters: cacheDir

Action required:
1. Review breaking changes
2. Update code examples manually
3. Add migration guide to README
4. Update version compatibility note
```

## Dry-Run Mode

When `--dry-run` flag is provided:

1. Run all detection and analysis
2. Determine what would be updated
3. Generate preview of changes
4. Don't write any files

**Output format:**

```text
Dry-run mode: Preview of changes
=================================

Would update the following files:

1. pkgs/effect-type-registry/README.md
   - Update features list (3 additions, 1 removal)
   - Refresh quick start example
   - Update API overview

2. pkgs/effect-type-registry/docs/architecture.md
   - Update caching section
   - Add new diagram reference

No files written (dry-run mode)
To apply changes, run: /docs-sync effect-type-registry
```

## Error Handling

### Missing Configuration

```text
Error: Module 'xyz' not found in design.config.json
Available modules: effect-type-registry, rspress-plugin-api-extractor, website
```

### No Changes Detected

```text
No changes detected since last sync
All user documentation is up to date

Last sync: 2025-01-17 15:30:00
Design docs checked: 3
User docs checked: 5
```

### Sync Conflicts

```text
Error: Sync conflicts detected

Conflicts:
1. README.md: Custom features section conflicts with generated content
2. docs/architecture.md: File modified after design doc update

Run with --force to override, or resolve manually
```

### Validation Failures

```text
Warning: Updated docs have validation errors

Errors:
- README.md: Line 45 exceeds 80 characters
- docs/api.md: Broken link to ./examples.md

Fix errors before committing
```

## Integration Points

- Uses `.claude/design/design.config.json` for configuration
- Reads design docs from `designDocsPath`
- Updates files in `userDocs` paths
- May invoke `docs-generate-readme` for full README regeneration
- May invoke `docs-review` for validation
- Respects quality standards for each level

## Related Skills

- `/docs-generate-readme` - Full README regeneration
- `/docs-generate-repo` - Full repo docs regeneration
- `/docs-generate-site` - Full site docs regeneration
- `/docs-review` - Validate sync quality
- `/design-sync` - Sync design docs with code (reverse direction)
