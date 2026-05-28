# Design Doc Validation Examples

Complete usage scenarios and example outputs for different validation states.

## Example 1: Validate single module

**User request:**

> Validate design docs for effect-type-registry

**Execution:**

1. Load config
2. Find module: `effect-type-registry`
3. Get design docs path: `.claude/design/effect-type-registry`
4. Find all `.md` files in path
5. Validate each file
6. Generate report

**Output:**

```markdown
# Design Doc Validation Report

**Module:** effect-type-registry
**Files validated:** 3
**Status:** ✅ PASS

## Summary

- Errors: 0
- Warnings: 1
- Info: 2

## Issues by File

### observability.md

**Status:** ✅ PASS

#### Warnings

- [Frontmatter] Status 'draft' with completeness 75 - consider changing to
  'current'

#### Info

- Consider adding more detail to Future Enhancements section

## Recommendations

1. Update observability.md status to 'current' to match completeness level
2. Add implementation timeline to Future Enhancements
```

## Example 2: Validate specific file with errors

**User request:**

> Validate cache-optimization.md in effect-type-registry

**Execution:**

1. Load config
2. Find module and file
3. Validate file
4. Generate report

**Output:**

```markdown
# Design Doc Validation Report

**Module:** effect-type-registry
**Files validated:** 1
**Status:** ❌ FAIL

## Summary

- Errors: 3
- Warnings: 1
- Info: 0

## Issues by File

### cache-optimization.md

**Status:** ❌ FAIL

#### Errors

- [Frontmatter] Missing required field: 'updated'
- [Frontmatter] Invalid category 'caching' - not in allowed list
  [architecture, observability, performance]
- [Line 45] Missing required section: Overview

#### Warnings

- [Frontmatter] Status 'stub' with completeness 0 - this is correct but needs
  content

## Recommendations

1. Add 'updated' field to frontmatter with current date
2. Change category to 'performance' (most appropriate for caching)
3. Add Overview section following template structure
4. Begin filling in content to move from stub to draft status
```

## Example 3: Strict validation of all modules

**User request:**

> Run strict validation on all design docs

**Execution:**

1. Load config
2. Get all modules
3. For each module, find design docs
4. Validate with strict checks enabled
5. Generate comprehensive report

**Output:**

```markdown
# Design Doc Validation Report

**Module:** all (3 modules)
**Files validated:** 15
**Status:** ⚠️  WARNINGS

## Summary

- Errors: 0
- Warnings: 8
- Info: 12

## Issues by Module

### effect-type-registry (3 files)

- ✅ observability.md - 1 warning, 2 info
- ✅ cache-optimization.md - 2 warnings, 1 info
- ✅ architecture.md - 0 warnings, 3 info

### rspress-plugin-api-extractor (5 files)

- ✅ type-loading-vfs.md - 1 warning, 1 info
- ✅ snapshot-tracking-system.md - 0 warnings, 2 info
- ⚠️  performance-observability.md - 2 warnings, 1 info
- ⚠️  error-observability.md - 1 warning, 0 info
- ✅ build-architecture.md - 0 warnings, 1 info

### design-doc-system (7 files)

- ✅ architecture.md - 1 warning, 1 info
- ✅ implementation-status.md - 0 warnings, 0 info
- [... more files ...]

## Top Recommendations

1. Update 5 files with status/completeness mismatches
2. Fill in placeholder sections in 3 stub documents
3. Add cross-references between related documents
4. Update last-synced dates for 8 files
```

## Special Cases

### New Files (Stub Status)

Stub files are expected to have many placeholders and low completeness:

- Don't warn about placeholders if status is "stub" and completeness < 20
- Do validate that frontmatter is complete
- Do validate that structure follows template

### Archived Documents

Archived documents may have outdated information:

- Require explanation in "Document Status" section at bottom
- Don't validate cross-references (may be to deleted files)
- Don't check completeness (frozen state)

### Module Without Design Docs

If module has no design docs yet:

```text
INFO: No design docs found for module '{module}'
- Design docs path: {path}
- This is normal for new modules
- Run /design-init to create your first design doc
```

### Invalid YAML

If frontmatter YAML is malformed:

```text
ERROR: Invalid YAML syntax in frontmatter
- Line: {line}
- Error: {yaml-error}
- Fix: Correct YAML syntax (check for: proper indentation, quotes, colons)
```

## Success Criteria

A design doc passes validation if:

- ✅ Valid YAML frontmatter with all required fields
- ✅ Field values meet validation rules
- ✅ Required sections present
- ✅ Cross-references exist
- ✅ Markdown linting passes
- ✅ Status matches completeness level

## Integration with CI/CD

This skill can be integrated into pre-commit hooks or CI pipelines:

```bash
# Pre-commit hook example
claude code --skill design-validate --args "all"

# CI pipeline example
- name: Validate design docs
  run: claude code --skill design-validate --args "all --strict"
```

Exit codes:

- 0: All validations pass
- 1: Warnings present
- 2: Errors found
