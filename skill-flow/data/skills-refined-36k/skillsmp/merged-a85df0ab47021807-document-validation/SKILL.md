---
name: document-validation
description: Use this skill when validating design and plan documents for compliance, ensuring proper formatting, and verifying metadata before commits.
---

# Document Validation

Validates design and plan documentation files for structure, frontmatter, and quality compliance.

## Overview

This skill validates both design and plan documentation by:

1. Reading the configuration from `design.config.json`
2. Finding relevant documentation files for validation
3. Validating YAML frontmatter structure and values
4. Checking for required fields and data types
5. Validating status-progress alignment and date relationships
6. Reporting issues with severity levels and actionable recommendations

## Quick Start

**Validate a specific design document:**

```bash
/design-validate <module-name> <file-name>
```

**Validate all design documents:**

```bash
/design-validate <module-name> --all
```

**Validate a specific plan:**

```bash
/plan-validate <plan-name>
```

**Validate all plans:**

```bash
/plan-validate --all
```

**Strict mode for additional quality checks:**

```bash
/design-validate <module-name> --strict
/plan-validate <plan-name> --strict
```

## How It Works

### 1. Parse Parameters

- For design validation:
  - `module`: Module name to validate (or "all" for all modules) [REQUIRED]
  - `file`: Specific file to validate (default: all files in module)
  - `strict`: Enable strict mode with additional checks (default: false)

- For plan validation:
  - `plan-name`: Plan name/ID to validate (or --all for all plans) [REQUIRED]
  - `--strict`: Enable strict mode with additional quality checks
  - `--fix`: Auto-fix issues when possible

### 2. Load Configuration

Read `.claude/design/design.config.json` to get:

- Module and plan paths
- Quality standards
- Required frontmatter fields
- Valid status values and progress limits

### 3. Locate and Validate Documents

Use Glob to find design docs or locate plan files based on the provided name. For each file:

**Frontmatter Validation:**

- Validate YAML syntax
- Check all required fields exist
- Verify field values are correct type and format
- Validate dates are in order (created ≤ updated ≤ last-synced for design docs; created ≤ updated for plans)
- Check status matches completeness level

**Structure Validation:**

- Verify required sections exist for design docs
- Check TOC matches headings (if required)

**Cross-Reference Validation:**

- Check paths in `related`, `dependencies`, and `implementation-plans` arrays for design docs
- Validate bidirectional links between plans and design docs

### 4. Report Results

Generate a validation report with issues categorized by severity:

- **ERROR**: Must be fixed (blocks)
- **WARNING**: Should be fixed
- **INFO**: Nice to have

## Exit Codes

- ✅ **PASS**: No errors found
- ⚠️  **WARNINGS**: Warnings but no errors
- ❌ **FAIL**: Errors found, must fix

## Success Criteria

A document passes validation if:

- ✅ Valid YAML frontmatter with all required fields
- ✅ Field values meet validation rules
- ✅ Required sections present (for design docs)
- ✅ Cross-references exist (related, dependencies, plans)
- ✅ Status matches completeness level
- ✅ Markdown linting passes

## Related Skills

- `plan-create` - Create new plans
- `plan-update` - Update plan status/progress
- `plan-list` - List all plans
- `design-init` - Validate newly created docs
- `design-update` - Validate after updates
- `design-sync` - Validate after syncing with code