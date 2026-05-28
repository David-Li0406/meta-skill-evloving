---
name: analyze
description: Analyze codebase for bugs, debt, documentation, security, or style issues
argument-hint: <type> [paths...]
---

# Analyze Codebase

## Overview

Analyze codebase for issues across multiple domains: bugs, technical debt, documentation, security vulnerabilities, or style inconsistencies. Categorizes findings by severity with specific file locations and actionable fix suggestions. Returns structured JSON for workflow integration and generates a markdown report.

## Arguments

### Definitions

- **`<type>`** (required): Analysis type to perform. Must be one of:
  - `bug` - Logic errors, runtime errors, and edge cases
  - `debt` - Technical debt, architecture, and performance issues
  - `doc` - Documentation accuracy and completeness
  - `security` - Vulnerabilities, unsafe patterns, and dependency issues
  - `style` - Code style, consistency, and best practices
- **`[paths...]`** (optional): Space-separated list of files or directories to analyze. When provided, only these paths are analyzed. Otherwise, the entire codebase is analyzed.

### Values

\$ARGUMENTS

## Additional Resources

Load ONE of these based on the `<type>` argument:

- For bug analysis, see [references/bug.md](references/bug.md)
- For debt analysis, see [references/debt.md](references/debt.md)
- For doc analysis, see [references/doc.md](references/doc.md)
- For security analysis, see [references/security.md](references/security.md)
- For style analysis, see [references/style.md](references/style.md)

## Core Principles

- Only report REAL issues - quality over quantity
- Only report UNFIXED issues - if resolved, do not include it
- Be specific with exact file and line numbers
- Understand project patterns before flagging issues
- Consider framework conventions and intentional design choices
- Check if apparent issues are handled elsewhere before flagging
- Recognize test-specific patterns and legitimate edge cases
- If no issues found, return success with zero counts

## Instructions

1. **Validate Type Argument**
   - Check that `<type>` argument is provided
   - Verify it is one of: `bug`, `debt`, `doc`, `security`, `style`
   - If missing or invalid, stop execution and return error:

     ```json
     {
       "success": false,
       "error": "Invalid or missing type argument. Must be one of: bug, debt, doc, security, style"
     }
     ```

2. **Load Type-Specific Guidelines**
   Based on the `<type>` argument, load the corresponding reference file:
   - `bug` -> Read [references/bug.md](references/bug.md)
   - `debt` -> Read [references/debt.md](references/debt.md)
   - `doc` -> Read [references/doc.md](references/doc.md)
   - `security` -> Read [references/security.md](references/security.md)
   - `style` -> Read [references/style.md](references/style.md)

3. **Determine Scope**
   - If `[paths]` are provided, focus only on those files/directories
   - Otherwise, analyze the entire codebase
   - Exclude test files, node_modules, build outputs, and vendor directories
   - For `doc` type: find all documentation files (README, docs/, \*.md)

4. **Understand Project Context**
   - Check for linter configs (ESLint, Prettier, Ruff)
   - Read CLAUDE.md for project-specific guidelines
   - Analyze existing code patterns to understand conventions

5. **Analyze for Issues**
   - Apply type-specific analysis criteria from the loaded reference file
   - Verify each finding is a real issue, not a false positive
   - Check if apparent issues are handled elsewhere

6. **Categorize Findings**
   Rate each finding by severity (all types use this scale):
   - **Critical**: Severe impact - crashes, data loss, security breaches, misleading docs
   - **High**: Significant impact - functional bugs, major gaps, exploitable with conditions
   - **Medium**: Moderate impact - edge cases, minor issues, incomplete coverage
   - **Low**: Minimal impact - best practice violations, minor improvements

7. **Generate Report**
   - Save to `agentic/analysis/<type>.md`
   - Include date in report header
   - Group findings by severity

8. **Return JSON Output**
   - Return structured JSON matching the output schema
   - Use the unified finding schema for all types
   - Include notes only when meaningful (see type-specific reference for guidance)

## Output Guidance

Return a JSON object AND save a detailed markdown report.

### JSON Output Schema

```json
{
  "success": true,
  "analysis_type": "{{type}}",
  "findings_count": {
    "critical": "{{critical_count}}",
    "high": "{{high_count}}",
    "medium": "{{medium_count}}",
    "low": "{{low_count}}",
    "total": "{{total_count}}"
  },
  "findings": ["{{findings_array}}"],
  "document_path": "agentic/analysis/{{type}}.md"
}
```

<!--
Placeholders:
- {{type}}: Analysis type (bug, debt, doc, security, style)
- {{critical_count}}, {{high_count}}, {{medium_count}}, {{low_count}}: Integer counts per severity
- {{total_count}}: Sum of all findings
- {{findings_array}}: Array of finding objects using the Finding Schema below
-->

### Finding Schema

All analysis types use this unified finding structure:

```json
{
  "id": "{{id_prefix}}-{{sequence}}",
  "severity": "{{severity}}",
  "title": "{{title}}",
  "file": "{{file}}",
  "line": "{{line}}",
  "description": "{{description}}",
  "fix": "{{fix}}",
  "notes": "{{notes}}"
}
```

<!--
Placeholders:
- {{id_prefix}}: Type-based prefix (BUG, DEBT, DOC, SEC, STYLE)
- {{sequence}}: Sequential number starting at 001
- {{severity}}: One of critical, high, medium, low
- {{title}}: Brief descriptive title of the issue
- {{file}}: Path to the affected file
- {{line}}: Line number where issue occurs
- {{description}}: What is wrong and why it's a problem
- {{fix}}: How to fix the issue
- {{notes}}: Optional additional context (omit key if empty)

ID Prefixes by type:
- bug -> BUG-001, BUG-002, ...
- debt -> DEBT-001, DEBT-002, ...
- doc -> DOC-001, DOC-002, ...
- security -> SEC-001, SEC-002, ...
- style -> STYLE-001, STYLE-002, ...

Notes field: Optional. Only include when there is meaningful additional context.
See the type-specific reference file for guidance on what to include.
-->

## Templates

### Markdown Report Template

Save to `agentic/analysis/<type>.md`:

```markdown
# {{type_title}} Analysis Report

**Date**: {{date}}
**Scope**: {{scope}}

## Summary

| Severity | Count              |
| -------- | ------------------ |
| Critical | {{critical_count}} |
| High     | {{high_count}}     |
| Medium   | {{medium_count}}   |
| Low      | {{low_count}}      |

## Critical

### {{id}}: {{title}}

**File:** {{file}}
**Line:** {{line}}
**Description:** {{description}}
**Fix:** {{fix}}
**Notes:** {{notes}}

---

## High

[Repeat finding format for each high severity issue]

## Medium

[Repeat finding format for each medium severity issue]

## Low

[Repeat finding format for each low severity issue]
```

<!--
Placeholders:
- {{type}}: Analysis type in lowercase (bug, debt, doc, security, style)
- {{type_title}}: Analysis type capitalized for title (Bug, Debt, Doc, Security, Style)
- {{date}}: Current date in YYYY-MM-DD format
- {{scope}}: "Entire codebase" or comma-separated list of analyzed paths
- {{critical_count}}, {{high_count}}, {{medium_count}}, {{low_count}}: Integer counts
- {{id}}: Finding ID with prefix (e.g., BUG-001, SEC-003)
- {{title}}: Brief descriptive title
- {{file}}: Path to the affected file
- {{line}}: Line number where issue occurs
- {{description}}: What is wrong and why it's a problem
- {{fix}}: How to fix the issue
- {{notes}}: Optional additional context (omit line if empty)

Structure:
- Group findings by severity section (Critical, High, Medium, Low)
- Within each section, list findings in ID order
- Add horizontal rule (---) between findings
- Omit empty severity sections
-->
