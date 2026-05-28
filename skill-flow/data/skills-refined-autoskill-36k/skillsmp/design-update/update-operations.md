# Update Operations

All supported update operations for design documentation files.

## Frontmatter Updates

### Update Status

**Purpose:** Change document status to reflect current state

**Valid Values:**

- `stub` - Initial state, outline only (0-20% complete)
- `draft` - Work in progress (21-60% complete)
- `current` - Up-to-date documentation (61-100% complete)
- `needs-review` - Ready for review
- `archived` - No longer current, superseded or obsolete

**Validation:**

- New status must be valid value
- Status should match completeness level (warn if mismatch)
- For archived status, ensure document footer has archival reason

**Update:**

```yaml
status: {new-status}
updated: {current-date}
```

**Status-Completeness Matrix:**

| Completeness | Expected Status |
| :----------- | :-------------- |
| 0-20 | stub |
| 21-60 | draft |
| 61-90 | current, needs-review |
| 91-100 | current |

**Recommendation:** If status doesn't match completeness, suggest updating both.

### Update Completeness

**Purpose:** Update completion percentage to reflect progress

**Valid Values:** Integer 0-100

**Validation:**

- Value must be integer between 0-100
- Status should match completeness level
- Check against actual content (use smart estimation if available)

**Update:**

```yaml
completeness: {new-value}
updated: {current-date}
```

**Smart Validation:**
If completeness seems inaccurate based on content:

- Count filled vs placeholder sections
- Check section lengths
- Warn if declared completeness differs significantly from estimated

### Mark as Synced

**Purpose:** Indicate document has been verified against current codebase

**Update:**

```yaml
last-synced: {current-date}
updated: {current-date}
```

**Use Cases:**

- After running `/design-sync`
- After manually verifying accuracy
- After code changes that don't require doc changes

**Note:** Documents with `last-synced: never` should be synced periodically.

### Update Category

**Purpose:** Change document category

**Validation:**

- New category must be in module's allowed categories
- Check `.claude/design/design.config.json` for valid categories

**Update:**

```yaml
category: {new-category}
updated: {current-date}
```

**Common Categories:**

- architecture
- performance
- observability
- testing
- integration

### Update Related Docs

**Purpose:** Add or remove cross-references to related documentation

**Validation:**

- Paths must be valid and files must exist
- No duplicate entries
- Paths should be relative to `.claude/design/`

**Update:**

```yaml
related:
  - module-name/doc-name.md
  - another-module/another-doc.md
```

**Best Practices:**

- Add bidirectional references (if A relates to B, B should relate to A)
- Use module-relative paths
- Keep list alphabetically sorted

### Update Dependencies

**Purpose:** Track which docs this document depends on

**Validation:**

- Paths must be valid and files must exist
- No duplicate entries
- Check for circular dependencies (A → B → A)

**Update:**

```yaml
dependencies:
  - module-name/dependency-doc.md
```

**Use Cases:**

- Implementation docs depending on architecture docs
- Observability docs depending on architecture docs
- Performance docs depending on implementation docs

## Content Section Updates

### Update Specific Section

**Process:**

1. **Identify Section:**
   - Find section heading: `## {Section Name}`
   - Extract content between heading and next same-level heading

2. **Validate New Content:**
   - Content is valid markdown
   - Heading levels are appropriate
   - Code blocks have language identifiers
   - No broken internal links

3. **Replace Content:**
   - Keep section heading
   - Replace everything until next `##` heading
   - Preserve trailing newlines

**Common Sections:**

- Overview
- Current State
- Rationale
- Implementation Details
- Future Enhancements
- Related Documentation

### Add New Section

**Process:**

1. **Determine Insertion Point:**
   - After related sections
   - Before "Related Documentation" (footer section)
   - Follow template section order

2. **Create Section:**

```markdown
## {Section Name}

{Content}
```

1. **Update TOC:**
   - Add entry to table of contents if present
   - Link to new section

### Remove Section

**Process:**

1. **Identify Section:**
   - Find section heading
   - Find next same-level heading or end of file

2. **Validation:**
   - Not removing required section (Overview, Current State, Rationale)
   - Get user confirmation for non-placeholder sections

3. **Remove Content:**
   - Delete from heading to next heading
   - Update TOC

### Update Entire Document

**Purpose:** Replace entire document content (preserving frontmatter)

**Process:**

1. **Extract Frontmatter:**
   - Keep existing frontmatter
   - Update `updated` date
   - Optionally update completeness

2. **Replace Body:**
   - Replace everything after frontmatter
   - Validate new content is valid markdown

3. **Validation:**
   - Get user confirmation (destructive operation)
   - Verify new content has required sections

## Bulk Updates

### Update Multiple Fields at Once

**Purpose:** Make several frontmatter changes in one operation

**Example:**

```yaml
status: current
completeness: 85
last-synced: 2026-01-17
updated: 2026-01-17
```

**Process:**

1. Read current frontmatter
2. Apply all requested changes
3. Validate consistency (status ↔ completeness)
4. Write updated frontmatter
5. Update `updated` date

### Update Multiple Sections

**Purpose:** Update several content sections in one operation

**Process:**

1. Read current document
2. For each section update:
   - Validate section exists (or create if new)
   - Apply changes
3. Rebuild document
4. Update frontmatter `updated` date

## Validation After Updates

### Frontmatter Validation

After any frontmatter update, validate:

- ✅ All required fields present
- ✅ Field values have correct types
- ✅ Dates in correct format (YYYY-MM-DD)
- ✅ Dates in correct order (created ≤ updated ≤ last-synced)
- ✅ Status matches completeness
- ✅ Category is valid for module
- ✅ Related/dependency paths exist

### Content Validation

After content updates, validate:

- ✅ Valid markdown syntax
- ✅ Required sections present
- ✅ Heading levels consistent
- ✅ Code blocks have language identifiers
- ✅ Internal links are valid
- ✅ No duplicate section headings

### Recommendation Generation

After updates, provide recommendations:

**If status updated but not completeness:**

- Suggest updating completeness to match status
- Provide estimated completeness based on content

**If completeness updated but not status:**

- Suggest updating status to match completeness
- Show status-completeness matrix

**If content updated but not completeness:**

- Suggest updating completeness
- Provide smart estimate based on changes

**If synced:**

- Confirm last-synced date updated
- Note next sync recommendation (30-90 days)

## Update Output Format

After successful update, provide summary:

```markdown
## Changes Made

**File:** .claude/design/{module}/{doc}

**Frontmatter Changes:**
- status: {old} → {new}
- completeness: {old}% → {new}%
- last-synced: {old} → {new}
- updated: {new-date}

**Content Changes:**
- Updated section: {section-name}
- Added section: {new-section}
- Lines changed: ~{count}

## Validation

✅ All validations passed
⚠️ Status/completeness suggestion: Update status to 'current'

## Next Steps

1. Review changes in the file
2. Run `/design-validate {module}` to check for issues
3. Consider updating related documentation
4. If significant changes, update CLAUDE.md reference
```
