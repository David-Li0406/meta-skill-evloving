---
title: {{TITLE}}
category: analysis
type: {{code|performance|security|dependency|other}}
status: in-progress
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
author: Claude
tags: []
scope: {{files or directories analyzed}}
---

# {{TITLE}}

## Scope

{{What code/system/area was analyzed?}}

**Files analyzed:**
- `{{path/to/file1.rb}}`
- `{{path/to/file2.rb}}`
- `{{path/to/directory/}}`

**Analysis type:** {{code quality | performance | security | dependency | other}}

## Executive Summary

{{One paragraph summary of the most important findings and recommendations.}}

## Methodology

{{How was this analysis conducted?}}

- Static code analysis
- Performance profiling
- Manual code review
- Automated scanning tools

## Findings

### Critical Issues

| Issue | Location | Impact | Recommendation |
|-------|----------|--------|----------------|
| {{Issue description}} | `{{file:line}}` | {{Impact description}} | {{Fix recommendation}} |

### Warnings

| Issue | Location | Impact | Recommendation |
|-------|----------|--------|----------------|
| {{Issue description}} | `{{file:line}}` | {{Impact description}} | {{Fix recommendation}} |

### Observations

- {{Observation 1: Something notable but not necessarily a problem}}
- {{Observation 2: Pattern noticed across the codebase}}
- {{Observation 3: Potential improvement opportunity}}

## Detailed Analysis

### {{Section 1: e.g., "Database Queries"}}

{{Detailed analysis of this area.}}

**Specific issues found:**

```{{language}}
# Location: {{file:line}}
# Issue: {{description}}
{{problematic code}}
```

**Recommended fix:**

```{{language}}
{{fixed code}}
```

### {{Section 2: e.g., "Memory Usage"}}

{{Detailed analysis of this area.}}

## Metrics

| Metric | Before | After (projected) | Improvement |
|--------|--------|-------------------|-------------|
| {{Metric 1}} | {{Value}} | {{Value}} | {{%}} |
| {{Metric 2}} | {{Value}} | {{Value}} | {{%}} |

## Recommendations

Priority-ordered list of actions:

1. **Critical**: {{Action}} - {{Rationale}}
2. **High**: {{Action}} - {{Rationale}}
3. **Medium**: {{Action}} - {{Rationale}}
4. **Low**: {{Action}} - {{Rationale}}

## Next Steps

- [ ] {{Immediate action 1}}
- [ ] {{Immediate action 2}}
- [ ] {{Follow-up analysis needed}}

## Related

### Codebase

- [{{primary_file.rb}}](../../{{path/to/file.rb}}) - {{Primary file analyzed}}
- [{{related_file.rb}}](../../{{path/to/related.rb}}) - {{Related file with similar issues}}

### Related Documentation

- [{{Related Plan}}](../plans/{{YYYY-MM-DD}}-{{filename}}.md) - {{Plan to address these findings}}
- [{{Related Analysis}}](../analysis/{{YYYY-MM-DD}}-{{filename}}.md) - {{Previous or related analysis}}
