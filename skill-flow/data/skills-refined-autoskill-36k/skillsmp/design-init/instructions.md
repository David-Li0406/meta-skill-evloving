# Detailed Instructions

Complete step-by-step instructions for initializing design documentation.

## Workflow

### 1. Parse Parameters

Extract parameters from the user's request:

**Required:**

- `module`: Module name (must exist in config)
- `topic`: Topic/filename for the document (kebab-case)

**Optional:**

- `category`: Design doc category (default: infer from topic or use default)
- `template`: Specific template to use (default: auto-select)

**Examples:**

- "Create a design doc for type-loading in rspress-plugin-api-extractor"
  - module: `rspress-plugin-api-extractor`
  - topic: `type-loading`
  - category: auto-detect or ask

- "Initialize architecture doc for my-package called api-design"
  - module: `my-package`
  - topic: `api-design`
  - category: `architecture`

### 2. Load Configuration

Read `.claude/design/design.config.json` to understand:

- Module configuration and paths
- Available categories for the module
- Design docs path for the module
- Template locations

**Validation:**

- Verify module exists in config
- Check if module has `designDocsPath` configured
- Validate category is appropriate for module

**Example config structure:**

```json
{
  "modules": {
    "my-package": {
      "path": "packages/my-package",
      "designDocsPath": ".claude/design/my-package",
      "categories": ["architecture", "performance", "observability"]
    }
  }
}
```

### 3. Determine Category and Template

If category not provided, infer from topic name or ask user.

**Category inference patterns:**

- Topics containing "architecture", "structure", "design" → `architecture`
- Topics containing "performance", "optimization", "benchmark" →
  `performance`
- Topics containing "observability", "logging", "metrics", "events" →
  `observability`
- Topics containing "test", "testing" → `testing`
- Topics containing "integration", "api" → `integration`
- Otherwise → ask user or use `default`

See [category-templates.md](category-templates.md) for complete inference
patterns.

**Template selection:**

1. Check for category-specific template:
   `.claude/skills/design-init/templates/{category}.template.md`
2. Fall back to default:
   `.claude/skills/design-init/templates/design-doc.template.md`

**Ask user if ambiguous:**

If category cannot be confidently inferred, ask:

```text
Which category best fits this design doc?

1. architecture - System/component architecture
2. performance - Performance characteristics and optimization
3. observability - Logging, metrics, error tracking
4. testing - Testing strategy and implementation
5. integration - Integration patterns and APIs
6. other - General design documentation
```

### 4. Read Template

Read the selected template file.

**Handle missing template:**

If category-specific template doesn't exist, fall back to default template.

**Template variables to replace:**

- `{module-name}` → actual module name
- `{Document Title}` → formatted topic (Title Case)
- `YYYY-MM-DD` → current date
- `stub` → initial status
- `0` → initial completeness
- Other placeholders as appropriate

### 5. Populate Frontmatter

Replace frontmatter placeholders with actual values:

```yaml
---
status: stub
module: {actual-module-name}
category: {selected-category}
created: {current-date}
updated: {current-date}
last-synced: never
completeness: 0
related: []
dependencies: []
---
```

**Current date format:** `YYYY-MM-DD` (e.g., `2026-01-17`)

### 6. Populate Document Body

Replace template placeholders:

- `{Document Title}` → Topic in Title Case (e.g., `type-loading` →
  `Type Loading`)
- `{System/Feature Name}` → Same as document title
- `{module-name}` in text → actual module name
- Keep other `{Placeholder}` markers for user to fill in

**Title case conversion:**

```text
type-loading → Type Loading
api-design → API Design
error-handling-system → Error Handling System
```

### 7. Determine Output Path

Construct the output file path:

```text
{designDocsPath}/{topic}.md
```

**Example:**

- Module: `rspress-plugin-api-extractor`
- Topic: `type-loading`
- Design docs path: `.claude/design/rspress-plugin-api-extractor`
- Output: `.claude/design/rspress-plugin-api-extractor/type-loading.md`

**Validation:**

- Check if file already exists
- If exists, ask user: "File already exists. Overwrite? (y/n)"
- Ensure parent directory exists

### 8. Create File

Write the populated template to the output path.

**Create directory if needed:**

If the design docs directory doesn't exist, create it first.

### 9. Report Success

Provide a summary of what was created:

```markdown
# Design Document Created

**File:** `.claude/design/{module}/{topic}.md`
**Module:** {module}
**Category:** {category}
**Template:** {template-used}
**Status:** stub

## Next Steps

1. Fill in the placeholders marked with `{...}`
2. Add overview and rationale sections
3. Document current state
4. Update completeness score (0-100)
5. Change status from `stub` to `draft` when partially complete
6. Run `/design-validate {module}` to check for issues

## Related Documentation

To reference this in CLAUDE.md:

\`\`\`markdown
**For {topic} details:**
→ `@./.claude/design/{module}/{topic}.md`

Load when working on {topic} or related functionality.
\`\`\`
```

## Validation Rules

Before creating the file, validate:

- ✅ Module exists in config
- ✅ Module has `designDocsPath` configured
- ✅ Category is valid
- ✅ Topic is kebab-case (lowercase with hyphens)
- ✅ Template file exists
- ✅ Output path is valid
- ✅ File doesn't already exist (or user confirmed overwrite)

## Special Cases

### New module without design docs

If module exists in config but has no `designDocsPath`:

1. Suggest path: `.claude/design/{module}`
2. Ask user to confirm or provide alternative
3. Create directory
4. Proceed with file creation

### Topic with spaces or special characters

Convert to kebab-case automatically:

- "Type Loading System" → `type-loading-system`
- "API_Design" → `api-design`
- "Error Handling (v2)" → `error-handling-v2`

### Very long topics

If topic is >50 characters, suggest abbreviation:

```text
Warning: Topic name is quite long (65 characters).
Consider a shorter name for the file:

Current: advanced-performance-optimization-strategies-for-large-datasets
Suggested: performance-large-datasets

Use suggested name? (y/n)
```

## Success Criteria

A successful initialization:

- ✅ Creates valid markdown file
- ✅ Frontmatter has all required fields
- ✅ Frontmatter values are populated (not placeholders)
- ✅ Document title matches topic
- ✅ File is in correct location
- ✅ File passes markdown linting
- ✅ User receives clear next steps
