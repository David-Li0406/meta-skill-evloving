---
name: review-report
description: "A universal report skill for saving code review and security review results as Markdown files with checklist-based progress tracking. Differentiates review types by directory (docs/reports/code-review/, docs/reports/security-review/). Generates Markdown files via automatic script invocation. Used by code-reviewer and security-reviewer agents after review completion."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Review Report

A universal skill for saving review results as structured Markdown files with fix checklists for progress tracking.

## Core Features

1. **Markdown format report generation**: Saves structured issue lists with visual formatting
2. **Directory-based classification**: Automatic classification by review type
3. **Automatic script invocation**: Uses Python script for token efficiency
4. **Fix checklist generation**: Enables progress tracking for issue resolution

---

## Report Generation Procedure

Follow these steps to generate a report using this skill:

### Step 1: Organize Issue Data

Organize discovered issues as a JSON array:

```json
[
  {
    "file": "app/components/example.tsx",
    "location": "23:5",
    "severity": "high",
    "category": "type-safety",
    "problem": "Type safety violation due to any type usage",
    "suggestion": "Change to unknown type and apply Type Guard"
  }
]
```

### Step 2: Execute Script

Execute the following command using the Bash tool:

```bash
python .claude/skills/review-report/scripts/generate_report.py \
  --output <directory> \
  --issues '<JSON array>'
```

**Output directories:**
- Code review: `docs/reports/code-review`
- Security review: `docs/reports/security-review`

**Example (code review):**
```bash
python .claude/skills/review-report/scripts/generate_report.py \
  --output docs/reports/code-review \
  --issues '[{"file":"app/components/Button.tsx","location":"15:3","severity":"high","category":"type-safety","problem":"any type usage","suggestion":"Use unknown instead"}]'
```

**If no issues found:**
```bash
python .claude/skills/review-report/scripts/generate_report.py \
  --output docs/reports/code-review \
  --issues '[]'
```

### Step 3: Verify Results

After execution, confirm the "리포트 생성 완료" message and file path.

Additionally, verify file creation:
```bash
ls -la docs/reports/code-review/*.md | tail -1
```

### Step 4: Track Fixes via Checklist

**⚠️ MANDATORY**: After fixing issues, agents MUST update the report checkboxes.

The generated Markdown report includes a **Fix Checklist** section:

```markdown
## ✅ Fix Checklist

**⚠️ MANDATORY**: Check each box (`- [x]`) immediately after fixing the issue.

Track your progress by checking off fixed issues:

- [ ] #1 [Critical] path/to/file.ts:23 - Brief problem description
```

**Checklist Update Protocol**:
1. **Fix the issue** in source code
2. **Open the generated `.md` report file** using Read tool
3. **Change checkbox**: `- [ ]` → `- [x]` for the fixed issue
4. **Save changes** using Edit tool
5. Track overall progress by reviewing completed items
6. When all items are checked, update report status to `✅ Complete`

⛔ **CRITICAL**: Checkboxes MUST be checked immediately after each fix. Do NOT batch checkbox updates.

---

## Issue Field Description

| Field | Required | Description |
|-------|----------|-------------|
| file | O | File path |
| location | O | Line:column (e.g., "23:5") |
| severity | O | critical / high / medium / low |
| category | O | Issue classification (type-safety, convention, security, etc.) |
| problem | O | Detailed problem description |
| suggestion | O | Fix suggestion |
| references | X | Array of referenced document paths (optional) |

---

## Severity Criteria

- **critical**: Runtime errors, security vulnerabilities (immediate fix required)
- **high**: Type safety, major convention violations
- **medium**: Code quality, performance improvement recommendations
- **low**: Style, documentation recommendations

---

## Categories by Review Type

### Code Review (docs/reports/code-review/)

- `type-safety`: Type safety (any usage, missing generic constraints, etc.)
- `convention`: Code conventions (function declaration style, naming, etc.)
- `react19`: React 19 optimization rules (unnecessary memoization, etc.)
- `deprecated-api`: Deprecated APIs
- `code-quality`: Code quality (duplication, complexity, etc.)

### Security Review (docs/reports/security-review/)

- `injection`: Injection vulnerabilities (SQL, XSS, Command, etc.)
- `access-control`: Access control issues
- `auth-failure`: Authentication/session management issues
- `crypto-failure`: Cryptography-related issues
- `security-misconfig`: Security configuration errors

---

## Filename Convention

`{8-char_random_hash}_{YYYYMMDD}.md`

Example: `a1b2c3d4_20260119.md`

---

## Generated Report Structure

The generated Markdown report includes:

1. **Header**: Review type, status, generation timestamp, total issues
2. **Summary Table**: Issue count by severity with visual indicators
3. **Issues Section**: Organized by severity (Critical → Low) with detailed tables
4. **Fix Checklist**: Checkbox items for tracking progress
5. **Notes Section**: Additional context and recommendations

Example output:
```markdown
# Code Review Report

**Status**: 🔄 In Progress
**Generated**: 2026-01-22 10:30:00 (UTC)
**Total Issues**: 5

---

## 📊 Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 High | 2 |
| 🟡 Medium | 1 |
| 🟢 Low | 1 |

---

## 🔍 Issues

### 🔴 Critical Issues

| # | File | Location | Category | Problem | Suggestion |
|---|------|----------|----------|---------|------------|
| 1 | ... | ... | ... | ... | ... |

---

## ✅ Fix Checklist

- [ ] #1 [Critical] file.ts:10 - Problem description
- [ ] #2 [High] file.ts:20 - Problem description
...
```

---

## JSON Escape Notes

- Single quotes (') inside JSON should be escaped as `'\''`
- Double quotes (") are JSON standard, use as-is
- Korean characters can be used directly

---

## References

- Markdown template details: `references/report-template.md`
- Security review reference: `.claude/skills/owasp-top10-2025/references/`
