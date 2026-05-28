---
name: export-findings
description: "Export Bosun findings to various formats. Use when exporting audit findings for stakeholders, generating reports from findings.json, creating CSV exports for tracking, or formatting findings for documentation. Also use when sharing findings outside Claude, creating executive summaries, generating HTML reports, or integrating findings with external systems. Guides transformation of findings into actionable outputs for different audiences."
---

# Export Findings

## Overview

Findings are only useful if they reach the right people in the right format. This skill guides export of Bosun findings to various formats for different audiences and integrations.

**Core principle:** Match the format to the audience. Developers want details, executives want summaries.

## The Export Process

### Phase 1: Load and Validate

Read and validate the findings:

1. **Load Findings**
   - Read `.bosun/findings.json`
   - Validate JSON structure
   - Check required fields present

2. **Validate Schema**
   - Each finding has: id, category, severity, title, description
   - Location has: file, line (optional: endLine)
   - SuggestedFix has: description, automated, effort

### Phase 2: Filter and Sort

Prepare findings for export:

1. **Filter Options**
   - By severity: critical, high, medium, low, info
   - By category: security, quality, architecture
   - By status: open, fixed, wontfix
   - By file pattern: `src/**/*.js`

2. **Sort Options**
   - By severity (critical first)
   - By file (group related findings)
   - By category (security first)

### Phase 3: Format and Output

Transform to target format:

1. **Markdown** - For documentation, PRs, wikis
2. **CSV** - For spreadsheets, tracking systems
3. **HTML** - For standalone reports
4. **Summary** - For executives, status updates

## Export Formats

### Markdown Format

```markdown
# Bosun Audit Findings

**Generated:** 2026-01-23
**Total Findings:** 11 (1 critical, 3 high, 5 medium, 2 low)

## Critical Findings

### SEC-001: Hardcoded API key in source
- **File:** src/config.js:15
- **Category:** Security
- **Severity:** Critical
- **Status:** Open

**Description:**
AWS API key found hardcoded in configuration file. This exposes
credentials in version control.

**Suggested Fix:**
Move API key to environment variable AWS_API_KEY

**Effort:** Trivial | **Automated:** Yes

---

## High Findings

### SEC-002: SQL injection vulnerability
...
```

### CSV Format

```csv
id,category,severity,title,file,line,status,effort,automated
SEC-001,security,critical,Hardcoded API key,src/config.js,15,open,trivial,true
SEC-002,security,high,SQL injection,src/db/users.js,42,open,minor,true
QUA-001,quality,medium,O(n²) algorithm,src/search.js,88,open,moderate,true
```

### HTML Format

```html
<!DOCTYPE html>
<html>
<head>
  <title>Bosun Audit Report</title>
  <style>
    .critical { background: #fee; border-left: 4px solid #c00; }
    .high { background: #fff3e0; border-left: 4px solid #f90; }
    .medium { background: #fff8e1; border-left: 4px solid #fc0; }
    .low { background: #e8f5e9; border-left: 4px solid #4c0; }
  </style>
</head>
<body>
  <h1>Bosun Audit Report</h1>
  <div class="summary">
    <p>Total: 11 findings</p>
    <ul>
      <li>Critical: 1</li>
      <li>High: 3</li>
      ...
    </ul>
  </div>
  <div class="findings">
    <div class="finding critical">
      <h3>SEC-001: Hardcoded API key</h3>
      <p>File: src/config.js:15</p>
      ...
    </div>
  </div>
</body>
</html>
```

### Summary Format

```
BOSUN AUDIT SUMMARY
===================
Date: 2026-01-23
Project: my-project

SEVERITY BREAKDOWN
  Critical: 1 ████████████████████
  High:     3 ████████████████
  Medium:   5 ████████████
  Low:      2 ████████

TOP ISSUES
1. [CRITICAL] Hardcoded API key in src/config.js
2. [HIGH] SQL injection in src/db/users.js
3. [HIGH] Missing auth on /api/admin

RECOMMENDED ACTIONS
1. Fix critical findings immediately
2. Schedule high findings for this sprint
3. Add medium findings to backlog

Full report: .bosun/findings.json
```

## Red Flags - STOP and Check

### Input Red Flags
```
- findings.json doesn't exist (run /audit first)
- Invalid JSON structure
- Missing required fields (id, severity, title)
- Empty findings array
```

### Output Red Flags
```
- Export loses important information
- Formatting breaks in target system
- Large exports without pagination
- Sensitive data in public exports
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "JSON is fine for everyone" | Match format to audience. |
| "We'll filter later" | Filter now. Noise hides signal. |
| "The summary is enough" | Details enable action. Include both. |
| "Executives don't need reports" | They need summaries. Generate them. |

## Export Checklist

Before exporting:

- [ ] findings.json exists and is valid
- [ ] Filter criteria appropriate for audience
- [ ] Sort order makes sense for format
- [ ] All required fields present in output
- [ ] Sensitive data handled appropriately
- [ ] Format renders correctly in target

## Quick Export Commands

```bash
# Check findings exist
cat .bosun/findings.json | jq '.findings | length'

# Count by severity
cat .bosun/findings.json | jq '.findings | group_by(.severity) | map({severity: .[0].severity, count: length})'

# Filter critical only
cat .bosun/findings.json | jq '.findings | map(select(.severity == "critical"))'

# Export to CSV (basic)
cat .bosun/findings.json | jq -r '.findings[] | [.id, .category, .severity, .title, .location.file, .location.line] | @csv'
```

## Findings Schema Reference

```json
{
  "version": "1.0",
  "generated": "2026-01-23T10:00:00Z",
  "summary": {
    "total": 11,
    "critical": 1,
    "high": 3,
    "medium": 5,
    "low": 2
  },
  "findings": [
    {
      "id": "SEC-001",
      "category": "security",
      "severity": "critical",
      "title": "Hardcoded API key in source",
      "description": "AWS API key found hardcoded...",
      "location": {
        "file": "src/config.js",
        "line": 15,
        "endLine": 15
      },
      "suggestedFix": {
        "description": "Move to environment variable",
        "automated": true,
        "effort": "trivial",
        "code": "const apiKey = process.env.AWS_API_KEY;"
      },
      "status": "open",
      "references": ["CWE-798"],
      "tags": ["secrets", "aws"]
    }
  ]
}
```

## References

- `.bosun/findings.json` for input schema
- CLAUDE.md for Bosun conventions
