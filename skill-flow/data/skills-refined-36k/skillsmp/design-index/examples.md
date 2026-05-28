# Design Index Examples

Usage examples for generating design documentation indexes.

## Example 1: Generate Module Index

**User request:**

> Generate index for effect-type-registry

**Execution:**

1. Load config
2. Find all docs (4 found)
3. Extract metadata and headings
4. Group by category
5. Generate markdown index
6. Write to INDEX.md

**Output:**

```markdown
# Index Generated

**Module:** effect-type-registry
**Documents indexed:** 4
**Output:** .claude/design/effect-type-registry/INDEX.md
```

## Example 2: HTML Navigation for All Modules

**User request:**

> Create HTML navigation for all design docs

**Execution:**

1. Load all modules
2. Scan all design docs (12 total)
3. Group by module and category
4. Generate HTML with navigation
5. Write to index.html

**Output:**

```markdown
# Index Generated

**Scope:** All modules
**Format:** HTML
**Documents:** 12
**Output:** .claude/design/index.html
```

## Example 3: JSON Index by Status

**User request:**

> Generate JSON index organized by status

**Execution:**

1. Scan docs
2. Group by status
3. Include full metadata
4. Generate JSON
5. Output to stdout

**Output:** JSON structure printed to terminal

## Example 4: Index with Sections

**User request:**

> Generate index for rspress-plugin with sections included

**Parameters:**

- module: `rspress-plugin-api-extractor`
- include-sections: `true`
- depth: `3`

**Output:**

Detailed index showing document structure with all sections and subsections.

## Example 5: Alphabetical Index

**User request:**

> Create alphabetical index for all modules

**Parameters:**

- module: `all`
- organize-by: `alphabetical`

**Output:**

Documents sorted A-Z across all modules.

## Example 6: Recent Updates Index

**User request:**

> Show recently updated design docs

**Parameters:**

- module: `all`
- organize-by: `date`

**Output:**

Documents grouped by update recency (This Week, This Month, Older).

## Error Scenarios

### No Documents Found

**Input:**

```bash
/design-index new-module
```

**Output:**

```text
INFO: No design documents found

Module: new-module
Path: .claude/design/new-module

This module has no design documentation yet.
Run /design-init to create your first design doc.
```

### Invalid Organization Method

**Input:**

```bash
/design-index module --organize-by=invalid
```

**Output:**

```text
ERROR: Invalid organization method

Provided: invalid
Valid options: category, status, alphabetical, date

Example: /design-index effect-type-registry --organize-by=category
```
