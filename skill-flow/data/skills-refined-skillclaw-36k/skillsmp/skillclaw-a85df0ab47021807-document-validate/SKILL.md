---
name: document-validate
description: Use this skill to validate the structure and frontmatter of design and plan documents, ensuring compliance and proper formatting before commits.
---

# Document Validation

Validates design and plan documentation files for structure, frontmatter, and quality compliance.

## Overview

This skill validates documentation by:

1. Reading the configuration from `design.config.json`
2. Finding documents for the specified module or plan
3. Validating YAML frontmatter structure and values
4. Checking for required sections and fields
5. Validating cross-references and links
6. Reporting issues with severity levels
7. Providing actionable fix recommendations

## Quick Start

**Basic validation for a design document:**

```bash
/document-validate design effect-type-registry
```

**Basic validation for a plan document:**

```bash
/document-validate plan plan-design-linking-phase-1
```

**Validate all documents:**

```bash
/document-validate all
```

**Strict mode (additional quality checks):**

```bash
/document-validate all --strict
```

## How It Works

### 1. Parse Parameters

- `type`: Document type to validate (`design` or `plan`) [REQUIRED]
- `name`: Document name to validate (or "all" for all documents)
- `--strict`: Enable strict mode with additional checks (default: false)

### 2. Load Configuration

Read `.claude/design/design.config.json` to get:

- Module and plan configuration and paths
- Quality standards
- Required frontmatter fields
- Minimum section requirements

### 3. Find and Validate Documents

Use Glob to find documents, then for each file:

**Frontmatter Validation:**

- Validate YAML syntax
- Check all required fields exist
- Verify field values are correct type and format
- Validate dates are in order (created ≤ updated ≤ last-synced)
- Check status matches completeness level

**Structure Validation:**

- Verify required sections exist
- Check TOC matches headings (if required)
- Validate document title

**Cross-Reference Validation:**

- Check paths in `related` and `dependencies` arrays exist
- Validate bidirectional links and internal markdown links

**Quality Checks (strict mode only):**

- Completeness accuracy
- Status appropriateness
- Documentation quality (section length, content depth)

### 4. Report Results

Generate a validation report with issues categorized by severity:

- **ERROR**: Must be fixed (blocks)
- **WARNING**: Should be fixed
- **INFO**: Suggestions for improvement