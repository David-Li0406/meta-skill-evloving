---
name: skill-report
description: "Skill coverage and health reporting for Bosun. Use when generating skill reports, analyzing skill coverage gaps, reviewing skill health metrics, or auditing reference completeness. Also use when planning skill improvements, reporting on plugin status, checking agent-to-skill mappings, identifying orphaned skills, or measuring skill quality over time. Essential for plugin maintainers and Bosun development planning."
---

# Skill Report

## Overview

Understanding skill coverage helps prioritize improvements. This skill guides generation of comprehensive reports on Bosun's skills - their health, coverage, and relationships.

**Core principle:** Measure what matters. Good metrics drive good decisions.

## The Reporting Process

### Phase 1: Inventory Collection

Gather data on all skills:

1. **Skill Enumeration**
   - List all skill directories in `skills/`
   - Parse each SKILL.md frontmatter
   - Count lines in each skill

2. **Reference Enumeration**
   - List all files in each `references/` directory
   - Parse SKILL.md for cited references
   - Identify missing and orphaned references

3. **Agent Mapping**
   - Parse each agent's `skills:` field
   - Map skills to agents
   - Identify orphaned skills

### Phase 2: Categorization

Organize skills by category:

1. **Domain-Specific**
   - security, architect, testing
   - performance, devops, docs-writer
   - project-auditor, threat-model, ux-ui

2. **Language-Specific**
   - golang, typescript, python
   - javascript, rust, java, csharp

3. **Cloud/Platform**
   - aws, gcp, azure

4. **Specialty**
   - seo-llm

### Phase 3: Metrics Calculation

Calculate health metrics:

1. **Coverage Metrics**
   - Total skills
   - Skills per category
   - Agent coverage (% of skills assigned)

2. **Quality Metrics**
   - Average SKILL.md line count
   - Skills approaching limit (>400 lines)
   - Reference completeness (cited vs existing)

3. **Gap Analysis**
   - Missing references
   - Orphaned skills
   - Thin skills (few references)

## Report Sections

### Summary Table

```markdown
| Metric | Value |
|--------|-------|
| Total Skills | 20 |
| Total References | 53 |
| Agent Coverage | 85% (17/20 assigned) |
| Reference Completeness | 78% (41/53 exist) |
| Avg Skill Lines | 245 |
```

### Skills by Category

```markdown
### Domain-Specific (9 skills)
| Skill | Lines | Refs | Agents |
|-------|-------|------|--------|
| security | 178 | 4 | security-agent |
| architect | 199 | 5 | quality-agent, architecture-agent |
| ... | ... | ... | ... |

### Language-Specific (7 skills)
| Skill | Lines | Refs | Agents |
|-------|-------|------|--------|
| golang | 271 | 4 | quality-agent, testing-agent |
| ... | ... | ... | ... |
```

### Issues Found

```markdown
### Missing References
- security: security-headers.md
- architect: api-design.md, architecture-patterns.md
- golang: effective-go.md

### Orphaned Skills (not assigned to agents)
- rust
- java
- csharp

### Skills Approaching Line Limit
- seo-llm: 329 lines (limit: 500)
```

### Recommendations

```markdown
1. **Create missing references** - 12 files cited but don't exist
2. **Assign orphaned skills** - Add to quality-agent or testing-agent
3. **Expand thin skills** - azure has only 1 reference
```

## Red Flags - STOP and Investigate

### Coverage Red Flags
```
- More than 20% of skills orphaned
- Any category with zero skills
- Skills with zero references
```

### Quality Red Flags
```
- Skills over 400 lines (approaching 500 limit)
- More missing references than existing
- Large gap between skill count and reference count
```

### Trend Red Flags
```
- Reference count decreasing over time
- Orphaned skills increasing
- New skills without references
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "The report is just numbers" | Numbers reveal health. Track them. |
| "Orphaned skills are fine" | Either use them or remove them. |
| "We'll add references later" | Track missing ones. Later is never. |
| "Coverage doesn't matter" | Uncovered areas are blind spots. |

## Report Checklist

Before finalizing a report:

- [ ] All skills enumerated
- [ ] All references counted
- [ ] Agent mappings verified
- [ ] Categories correctly assigned
- [ ] Missing references identified
- [ ] Orphaned skills listed
- [ ] Recommendations prioritized

## Quick Report Commands

```bash
# Count skills
ls -d skills/*/ | wc -l

# Count total references
find skills/*/references -name "*.md" | wc -l

# Lines per skill
wc -l skills/*/SKILL.md | sort -n

# References per skill
for s in skills/*/; do echo "$(basename $s): $(ls $s/references/*.md 2>/dev/null | wc -l)"; done

# Skills per agent
grep -h "^skills:" agents/*.md | tr '[],' '\n' | grep bosun | sort | uniq -c | sort -rn
```

## Output Formats

### Markdown (default)
Full formatted report as shown in Report Sections above.

### JSON
```json
{
  "generated": "2026-01-23",
  "summary": {
    "total_skills": 20,
    "total_references": 53,
    "agent_coverage_pct": 85
  },
  "skills": [
    {
      "name": "security",
      "category": "domain",
      "lines": 178,
      "references": 4,
      "agents": ["security-agent"]
    }
  ],
  "issues": {
    "missing_references": [...],
    "orphaned_skills": [...]
  }
}
```

## References

- CLAUDE.md for skill conventions
- `skill-validator` for validation rules
