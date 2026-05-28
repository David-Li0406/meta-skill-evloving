---
name: context-audit-review
description: Use this skill for comprehensive quality audits and reviews of CLAUDE.md context files to ensure efficiency, structure, and compliance with design standards.
---

# LLM Context Audit and Review

This skill performs thorough audits and reviews of CLAUDE.md context files, checking for quality, efficiency, structure, and compliance with design documentation standards.

## Overview

The skill combines auditing and reviewing processes to ensure CLAUDE.md files provide efficient context for AI assistants without unnecessary token usage. It analyzes files against defined quality standards, checks line counts, verifies design document references, and generates detailed reports with prioritized recommendations.

## Instructions

### 1. Locate Configuration

Read `.claude/design/design.config.json` to understand quality standards:

- Root CLAUDE.md max lines (default: 500)
- Child CLAUDE.md max lines (default: 300)
- Required design doc pointers setting
- Module structure for monorepos

### 2. Find CLAUDE.md Files

Search for CLAUDE.md files in the repository:

- Root: `CLAUDE.md` or `CLAUDE.local.md`
- Children: `{module}/CLAUDE.md` for each module
- Monorepo packages: Check each package directory

### 3. Analyze Each File

For each CLAUDE.md file found:

**Line Count Check:**

- Count total lines (excluding blank lines)
- Compare against limits (root: 500, child: 300)
- Flag files exceeding limits

**Content Structure Check:**

- Verify high-level imperative instructions (not details)
- Check for design doc pointers using @ syntax or links
- Identify overly detailed sections (candidates for design docs)
- Look for duplicated information between files

**Design Doc Pointer Check:**

- Find references to design documentation
- Verify @ syntax is used correctly: `@./.claude/design/module/doc.md`
- Ensure pointers include guidance on when to load context
- Check that docs being pointed to actually exist

**Hierarchy Check:**

- Verify child CLAUDE.md files exist where appropriate
- Check for modules with complex docs that should have children
- Identify opportunities to split large root files

### 4. Generate Report

Create a comprehensive audit and review report with:

**Summary:**

- Total CLAUDE.md files found
- Average line count
- Files over limit count
- Overall health score (0-100)

**Issues by Severity:**

Group by severity (critical, high, medium, low):

- **Critical:** Files exceeding line limits by >20%
- **High:** Missing design doc pointers when design docs exist
- **Medium:** Files approaching line limits (>80%)
- **Low:** Minor structure improvements

**Recommendations:**

Actionable suggestions:

1. Which sections to move to design docs
2. Where to create child CLAUDE.md files
3. How to improve @ syntax pointer clarity
4. What duplicated content to consolidate

### 5. Quality Metrics

Calculate and report:

- **Efficiency Score:** Percentage of files within limits
- **Pointer Coverage:** Percentage of design docs with CLAUDE.md pointers
- **Hierarchy Health:** Appropriate child files for module complexity
- **Duplication Level:** Amount of repeated content across files

## Output Format

Generate markdown report with structure:

```markdown
# CLAUDE.md Audit and Review Report

**Date:** YYYY-MM-DD
**Repository:** {name}
**Type:** {monorepo|single-package}

## Summary

- CLAUDE.md files: X
- Average line count: Y
- Files over limit: Z
- Overall efficiency: N%

## Issues Found

### Critical
[List of critical issues with file locations and recommendations]

### High Priority
[List of high-priority issues]

### Medium Priority
[List of medium-priority issues]

### Low Priority
[List of low-priority issues]

## Recommendations

1. [Specific actionable recommendation]
2. [Specific actionable recommendation]
...

## Quality Metrics

- Efficiency Score: X%
- Pointer Coverage: Y%
- Hierarchy Health: Z%
- Duplication Level: N%

## Next Steps

[Suggested order of operations to address issues]
```

## Special Cases

**Monorepo:**

Review both root CLAUDE.md and package-level files. Check for appropriate delegation between root and children.

**No design docs yet:**

If `.claude/design/` doesn't exist, note that design documentation system should be set up first.

**CLAUDE.local.md:**

These override CLAUDE.md and should follow same standards. Review both if present, noting which takes precedence.

## Success Criteria

A successful audit and review report:

- Identifies specific line numbers for problematic sections
- Provides concrete recommendations, not vague suggestions
- Prioritizes issues by impact on context efficiency
- Includes actionable next steps in recommended order

## Related Skills

- `/context-validate` - Basic structure and formatting validation
- `/context-update` - Update context files based on audit findings
- `/context-split` - Split large files that exceed limits
- `/design-audit` - Similar comprehensive audit for design docs