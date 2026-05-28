---
name: sdlc-review
description: Review implementation quality and plan compliance
argument-hint: <workflow-id> [plan] [output_dir] [severity]
---

# SDLC Review

## Overview

Review the implementation against quality standards and optionally against a plan. When a plan is provided, the review verifies plan compliance. Creates a review.md file in the specified output directory. When no plan is provided, the review examines the diff compared to the remote main branch.

## Arguments

### Definitions

- **`<workflow-id>`** (required): The workflow identifier for output organization.
- **`[plan]`** (optional): Path to plan document. When provided, review checks plan compliance.
- **`[output_dir]`** (optional): Directory to write review.md file (default to `agentic/outputs/<workflow-id>`).
- **`[severity]`** (optional): Minimum severity to report. Values: `minor`, `major`, `critical`. Defaults to `minor`.

### Values

\$ARGUMENTS

## Core Principles

- Review all changes thoroughly before reporting
- When no plan is provided, review the diff against `origin/main` (or `origin/master` as fallback)
- When a plan is provided, verify all milestones and tasks are completed
- Report issues with accurate severity levels
- Tests, lint, types, and build must pass for a successful review
- Always create a review.md file in the output directory

## Instructions

1. **Parse Arguments**
   - Extract workflow-id, plan, output_dir, and severity from arguments
   - Default output_dir to `agentic/outputs/<workflow-id>` if not specified
   - Default severity to `minor` if not specified

2. **Determine Review Scope**
   - If plan is provided: Load and parse the plan document
   - If no plan: Fetch latest remote main branch and get diff

3. **Run Quality Checks**
   - **Test Suite**: Run all tests, verify coverage
   - **Linter**: Check for linting errors
   - **Type Checker**: Verify type correctness
   - **Build**: Ensure project builds successfully

4. **Review Changes**
   - If plan provided:
     - Verify all milestones completed
     - Verify all tasks marked done
     - Check for scope creep (unplanned changes)
   - If no plan:
     - Review all changed files in the diff
     - Check for code quality issues
     - Identify potential bugs or regressions

5. **Generate Review Output**
   - Aggregate all check results
   - Filter issues by severity threshold
   - Generate summary

6. **Write Outputs**
   - Create `review.md` file in the output_dir
   - Return JSON output

## Output Guidance

### JSON Output

Return JSON with review details:

```json
{
  "success": true,
  "review_passed": {{review_passed}},
  "checks": {
    "plan_compliance": {
      "passed": {{plan_compliance_passed}},
      "milestones_complete": {{milestones_complete}},
      "milestones_total": {{milestones_total}}
    },
    "tests": {
      "passed": {{tests_passed}},
      "total": {{tests_total}},
      "passing": {{tests_passing}},
      "failing": {{tests_failing}},
      "coverage": {{coverage_percent}}
    },
    "lint": {
      "passed": {{lint_passed}},
      "errors": {{lint_errors}},
      "warnings": {{lint_warnings}}
    },
    "types": {
      "passed": {{types_passed}},
      "errors": {{type_errors}}
    },
    "build": {
      "passed": {{build_passed}}
    }
  },
  "issues": [{{issues_array}}],
  "summary": "{{summary}}",
  "document_path": "{{document_path}}"
}
```

<!--
Placeholders:
- {{review_passed}}: Boolean indicating if review passed (true/false)
- {{plan_compliance_passed}}: Boolean for plan compliance check (true/false/null if no plan)
- {{milestones_complete}}, {{milestones_total}}: Integer counts for plan compliance (null if no plan)
- {{tests_passed}}: Boolean for tests passing (true/false)
- {{tests_total}}, {{tests_passing}}, {{tests_failing}}: Integer counts for test results
- {{coverage_percent}}: Code coverage percentage (e.g., 82.5)
- {{lint_passed}}: Boolean for lint check passing (true/false)
- {{lint_errors}}, {{lint_warnings}}: Integer counts for lint results
- {{types_passed}}: Boolean for type check passing (true/false)
- {{type_errors}}: Integer count for type check errors
- {{build_passed}}: Boolean for build passing (true/false)
- {{issues_array}}: Array of issue objects with severity, category, message, file, line
- {{summary}}: Human-readable summary of review results
- {{document_path}}: Path to generated review.md file
-->

### Issue Schema

```json
{
  "severity": "{{severity}}",
  "category": "{{category}}",
  "message": "{{message}}",
  "file": "{{file}}",
  "line": {{line}}
}
```

<!--
Placeholders:
- {{severity}}: One of minor, major, critical
- {{category}}: Check category (tests, lint, types, build, plan_compliance, code_quality)
- {{message}}: Description of the issue
- {{file}}: Path to the affected file (null if not applicable)
- {{line}}: Line number where issue occurs (null if not applicable)
-->

### Review Document

Create a `review.md` file in the output_dir with the following format:

```markdown
# Review

**Status**: {{review_status}}
**Date**: {{review_date}}

## Progress

- [ ] All issues resolved
- [ ] Tests passing
- [ ] Lint passing
- [ ] Types passing
- [ ] Build passing

## Summary

{{summary}}

## Checks

| Check           | Status                     | Details                                                                    |
| --------------- | -------------------------- | -------------------------------------------------------------------------- |
| Plan Compliance | {{plan_compliance_status}} | {{milestones_complete}}/{{milestones_total}} milestones                    |
| Tests           | {{tests_status}}           | {{tests_passing}}/{{tests_total}} passing ({{coverage_percent}}% coverage) |
| Lint            | {{lint_status}}            | {{lint_errors}} errors, {{lint_warnings}} warnings                         |
| Types           | {{types_status}}           | {{type_errors}} errors                                                     |
| Build           | {{build_status}}           | {{build_details}}                                                          |

## Issues

{{#if issues_exist}}
| Severity | Category | File | Line | Message |
|----------|----------|------|------|---------|
{{#each issues}}
| {{severity}} | {{category}} | {{file}} | {{line}} | {{message}} |
{{/each}}
{{else}}
No issues found.
{{/if}}
```

<!--
Placeholders:
- {{review_status}}: PASSED or FAILED
- {{review_date}}: ISO 8601 date (YYYY-MM-DD)
- {{summary}}: Human-readable summary of review results
- {{plan_compliance_status}}: Checkmark or X emoji based on passed status
- {{milestones_complete}}, {{milestones_total}}: Integer counts
- {{tests_status}}: Checkmark or X emoji based on passed status
- {{tests_passing}}, {{tests_total}}: Integer counts
- {{coverage_percent}}: Code coverage percentage
- {{lint_status}}: Checkmark or X emoji based on passed status
- {{lint_errors}}, {{lint_warnings}}: Integer counts
- {{types_status}}: Checkmark or X emoji based on passed status
- {{type_errors}}: Integer count
- {{build_status}}: Checkmark or X emoji based on passed status
- {{build_details}}: Brief description of build result
- {{issues_exist}}: Boolean indicating if there are issues to display
- {{issues}}: Array of issue objects (severity, category, file, line, message)
-->
