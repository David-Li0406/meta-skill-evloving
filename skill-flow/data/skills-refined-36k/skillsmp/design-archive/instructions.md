# Design Archive Detailed Instructions

Complete step-by-step workflow for archiving design documentation.

## Detailed Workflow

### 1. Parse Parameters

Extract module, document, reason, and options from user request.

**Parameter parsing examples:**

- `/design-archive effect-type-registry old-cache.md` → module:
  `effect-type-registry`, doc: `old-cache.md`
- `/design-archive module doc.md --replacement=new.md` → reason: `superseded`,
  replacement: `new.md`
- `/design-archive module doc.md --move` → move to archive directory

**Default values:**

- `reason`: Prompt user if not provided
- `replacement`: null (required if reason is "superseded")
- `move`: false

### 2. Load Configuration

Read `.claude/design/design.config.json` to:

- Verify module exists
- Get design docs path
- Determine archive directory configuration

**Configuration structure:**

```json
{
  "modules": {
    "module-name": {
      "path": ".claude/design/module-name",
      "archiveDir": "_archive",
      "enabled": true
    }
  }
}
```

**Configuration validation:**

1. Read design.config.json
2. Check module exists in configuration
3. Get module path
4. Check for custom archive directory setting
5. Default to `_archive` if not configured

### 3. Validate Archival

Before archiving, validate all requirements.

**Document existence check:**

```bash
# Check if document exists
if [ ! -f ".claude/design/${module}/${doc}" ]; then
  ERROR: Document not found
fi
```

**Already archived check:**

Read document frontmatter to check current status:

```yaml
---
status: archived  # Already archived, skip
---
```

If already archived, report and exit (not an error).

**Archival reason validation:**

Valid reasons:

- `superseded`: Replaced by newer documentation
- `deprecated`: Feature/system deprecated
- `obsolete`: Information no longer accurate
- `completed`: Project finished

**Reason-specific requirements:**

For `superseded`:

```javascript
if (reason === 'superseded' && !replacement) {
  ERROR: "Replacement doc required for superseded reason"
}

if (replacement && !fileExists(replacementPath)) {
  ERROR: "Replacement doc not found: {replacementPath}"
}
```

For `deprecated`:

```javascript
// Optional: Check for deprecation timeline
if (!frontmatter.deprecation_timeline) {
  WARNING: "Consider adding deprecation timeline"
}
```

**Interactive reason prompt:**

If no reason provided, prompt user:

```text
Why is this document being archived?

1. superseded - Replaced by newer documentation
2. deprecated - Feature/system deprecated
3. obsolete - Information no longer accurate
4. completed - Project finished
5. other - Other reason

Select reason (1-5):
```

### 4. Update Document Frontmatter

Change status and add archival metadata based on reason.

**For superseded:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: superseded
  replacement: ./new-doc.md
  notes: "Brief explanation of what changed"
---
```

**For deprecated:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: deprecated
  deprecation_timeline:
    deprecated_date: 2025-12-01
    end_of_support: 2026-06-01
    removal_date: 2026-12-01
  replacement: ./v2-doc.md
  migration: ./migration-guide.md
---
```

**For obsolete:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: obsolete
  became_obsolete: 2026-01-01
  notes: "What became obsolete and why"
  current_docs: ./current-doc.md
---
```

**For completed:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: completed
  completion_date: 2026-01-15
  outcome: successfully_implemented
  final_docs: ../../docs/en/feature.md
---
```

**Frontmatter update algorithm:**

1. Read entire document
2. Extract frontmatter (first 30 lines between `---` markers)
3. Parse YAML
4. Update `status` to `archived`
5. Update `updated` date to today
6. Add `archived` object with appropriate fields
7. Reconstruct document with updated frontmatter
8. Write back to file

### 5. Add Archival Notice

Insert prominent notice after frontmatter.

**For superseded:**

```markdown
> **⚠️ ARCHIVED DOCUMENTATION**
>
> This design document was archived on {date}.
>
> **Reason:** This documentation has been superseded by newer design docs.
>
> **Replacement:** See [{replacement-name}](./{replacement-file}) for current
> documentation.
```

**For deprecated:**

```markdown
> **⚠️ ARCHIVED DOCUMENTATION**
>
> This design document was archived on {date}.
>
> **Reason:** The feature/system documented here has been deprecated.
>
> **Timeline:**
> - Deprecated: {deprecated_date}
> - End of support: {end_of_support}
> - Removal: {removal_date}
>
> **Migration:** See [{migration-name}](./{migration-file}) for upgrade path.
```

**For obsolete:**

```markdown
> **⚠️ ARCHIVED DOCUMENTATION**
>
> This design document was archived on {date}.
>
> **Reason:** This information is no longer accurate or relevant.
>
> **What changed:** {notes}
>
> **Current docs:** See [{current-name}](./{current-file}) for up-to-date
> information.
```

**For completed:**

```markdown
> **⚠️ ARCHIVED DOCUMENTATION**
>
> This design document was archived on {date}.
>
> **Reason:** This project has been completed.
>
> **Outcome:** {outcome}
>
> **Final documentation:** See [{final-name}]({final-path})
```

**Notice insertion algorithm:**

1. Read document content
2. Find end of frontmatter (second `---` marker)
3. Insert notice immediately after frontmatter
4. Add blank line after notice
5. Preserve rest of document content
6. Write back to file

### 6. Update Cross-References

Find and update all references to the archived document.

**Finding references:**

Search in multiple locations:

```bash
# Design docs
grep -r "archived-doc.md" .claude/design/ --include="*.md"

# CLAUDE.md files
grep -r "archived-doc.md" CLAUDE.md
grep -r "archived-doc.md" pkgs/*/CLAUDE.md

# Indirect references (by title/name)
grep -r "Old Design Name" .claude/design/ --include="*.md"
```

**Reference types:**

1. **Frontmatter references:**

```yaml
related:
  - ./archived-doc.md  # Update to replacement or remove
dependencies:
  - ./archived-doc.md  # Update to replacement or remove
```

1. **Content links:**

```markdown
See [archived doc](./archived-doc.md) for details.
# Update to:
See [new doc](./new-doc.md) for details.
```

1. **CLAUDE.md pointers:**

```markdown
Design docs: .claude/design/module/archived-doc.md
# Update or remove
```

**Update strategies:**

For each reference found:

- If `superseded`: Replace with replacement doc path
- If `deprecated`: Add deprecation note, keep link with archive warning
- If `obsolete`: Remove or replace with current docs
- If `completed`: Remove or replace with final docs

**Batch update procedure:**

1. Collect all files with references
2. For each file:
   - Read content
   - Find all references to archived doc
   - Apply appropriate update strategy
   - Write updated content
   - Track changes for summary

### 7. Optional: Move to Archive Directory

If `--move` parameter specified, physically move the file.

**Archive directory structure:**

```text
.claude/design/{module}/
├── _archive/
│   ├── 2026/
│   │   └── archived-doc.md
│   └── README.md  (explains archive)
└── current-docs.md
```

**Move procedure:**

1. Create `_archive/` directory if it doesn't exist
2. Optionally create year subdirectory: `_archive/{year}/`
3. Move document to archive directory
4. Update all references to new path
5. Optionally create redirect stub at original location

**Redirect stub (optional):**

```markdown
# {Original Title}

This document has been archived.

See [`_archive/{year}/{doc}`](./_archive/{year}/{doc})
```

**Reference path updates:**

When moving to archive directory, update all references:

- Old: `./archived-doc.md`
- New: `./_archive/2026/archived-doc.md`

### 8. Report Archival Summary

Provide comprehensive summary of all actions taken.

**Summary format:**

```markdown
# Archival Summary

## Document Archived

**File:** .claude/design/{module}/{doc}
**Status:** archived
**Reason:** {reason}
**Date:** {date}

## Changes Made

### Document Updates
- ✅ Status changed to "archived"
- ✅ Archival metadata added
- ✅ Archive notice inserted

### Cross-Reference Updates

**Files modified:** {count}

1. {file-path}
   - Updated frontmatter reference
2. {file-path}
   - Updated content link

### Additional Actions

{if moved}
- ✅ Moved to _archive/{year}/
- ✅ Updated {count} path references
{endif}

## Validation

- ✅ Replacement exists and is adequate
- ✅ All references updated
- ✅ CLAUDE.md files updated

## Next Steps

{if superseded}
1. Review replacement doc for completeness
2. Consider adding migration guide
{endif}

{if deprecated}
1. Update deprecation timeline in code comments
2. Add deprecation warnings to affected APIs
{endif}
```

## Advanced Features

### Batch Archival

Archive multiple related documents:

```javascript
function batchArchive(docs, reason, replacement) {
  for (doc of docs) {
    // Validate all docs first
    validateArchival(doc)
  }

  // Archive all docs
  for (doc of docs) {
    archiveDocument(doc, reason, replacement)
  }

  // Update cross-references once at the end
  updateAllReferences(docs, replacement)
}
```

### Archive Audit

Review all archived documents:

```javascript
function auditArchive(module) {
  const archivedDocs = findArchivedDocs(module)

  for (doc of archivedDocs) {
    // Check replacement still exists
    if (doc.archived.replacement) {
      if (!fileExists(doc.archived.replacement)) {
        WARNING: "Broken replacement link"
      }
    }

    // Check if too old to keep
    const age = today - doc.archived.date
    if (age > 365 && doc.archived.reason === 'obsolete') {
      SUGGEST: "Consider permanent removal"
    }
  }
}
```

### Restoration

Unarchive a document:

```javascript
function restoreDocument(module, doc, reason) {
  // Remove archive status
  // Remove archive notice
  // Update cross-references back
  // Optionally move from _archive directory
}
```
