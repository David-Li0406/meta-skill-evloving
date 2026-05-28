---
name: julien-ref-document-organisation-methodology-in-a-repo
description: "Complete documentation organization methodology for repositories. Use when organizing docs, creating reports, naming files, structuring project documentation, or needing guidance on documentation types."
version: "1.0.0"
license: Apache-2.0
user-invocable: true
metadata:
  author: "Julien"
  category: "reference"
triggers:
  - "methodologie documentation"
  - "doc methodology"
  - "organiser la documentation"
  - "structure docs"
  - "nommage fichiers"
  - "creer un rapport"
  - "comment documenter"
  - "organisation repo"
  - "naming convention docs"
  - "documentation structure"
  - "file naming"
  - "report template"
  - "incident report"
  - "session report"
  - "guide template"
  - "audit template"
  - "living docs"
  - "yaml frontmatter"
  - "document types"
  - "docs folder structure"
---

# Documentation Organization Methodology

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-ref-document-organisation-methodology-in-a-repo" activated
```

## Objective

Document efficiently without repetition. Ensure traceability, reusability, and clarity.

## Core Principles

1. **DRY**: Avoid duplication, use cross-references
2. **Living docs**: Update rather than create new, archive obsolete content
3. **Targeted audience**: Humans | LLM | All + level (1-10)
4. **Actionable**: Concrete examples, reproducible commands

## Directory Structure

```
project/
├── docs/
│   ├── guides/                    # Evolving docs
│   └── rapports/                  # Event-based docs
└── README.md                       # Index
```

## Naming Conventions

### EVOLVING Documents (living docs)
**Types**: GUIDE, METHODOLOGIE, AUDIT, TROUBLESHOOTING
**Name**: `[TYPE]_[subject].md` (no date)
**Timestamp**: In content, per section

**Required YAML header**:
```yaml
---
title: "Guide X"
version: X.Y.Z
created: YYYY-MM-DD
updated: YYYY-MM-DD
authors: [...]
audience: ["Humans"|"LLM"|"All"]
level: "Beginner (1-3)" | "Intermediate (4-6)" | "Expert (7-10)"
status: "Active" | "Archived" | "Draft"
tags: [...]
related: [related files]
---
```

### EVENT-BASED Documents (snapshots)
**Types**: INCIDENT, SESSION, RECHERCHE, RECOMMANDATIONS, MIGRATION, PERFORMANCE, SECURITE
**Name**: `YYYY.MM.DD_HH.mm_[commit-short]_[TYPE]_[subject].md`
**File timestamp format**: `2025.10.14_12.33` (dots + underscores)

**Required metadata**:
```markdown
## Metadata
- **Date**: YYYY-MM-DD HH:MM
- **Commit**: abc1234 (7 chars)
- **Duration**: X hours (if applicable)
```

**Example file names**:
- `2025.10.14_12.33_a888861_RECHERCHE_design-system.md`
- `2025.10.13_14.30_a3f9c21_INCIDENT_nginx-404.md`
- `2025.10.15_09.00_7b2e8d4_SESSION_auth-implementation.md`

## Document Types

### INCIDENT (event-based)
**When**: Blocking problem resolved

**Structure**:
```markdown
# Incident: [Title]

## Metadata
- Date, Duration, Severity, Commit

## Summary
[2-3 sentences]

## Symptoms → Timeline → Cause → Solution → Prevention

## References
```

### SESSION (event-based)
**When**: Significant session (feature, refactor)

**Structure**:
```markdown
# Session: [Title]

## Metadata
- Date, Duration, Commits

## Objective → Achievements → Decisions → Problems → Modified Files → Tests → Next

## References
```

### GUIDE (evolving)
**When**: Reusable procedure

**Structure**:
```markdown
---
[Complete YAML header]
---

# Guide: [Title]

## Overview → Concepts → Step-by-step Procedure → Troubleshooting → Examples → References
```

### AUDIT (evolving or event-based)
**When**: Pre-intervention analysis

**Structure**:
```markdown
# Audit: [Title]

## Metadata

## Executive Summary
- Score, Risks, Recommendations

## Findings (🔴 Critical, 🟠 Major, 🟡 Minor)

## Prioritized Recommendations → Action Plan → References
```

### RECHERCHE (event-based)
**When**: Investigation, exploration, benchmark

**Structure**:
```markdown
# Research: [Title]

## Metadata
- Date, Objective, Duration

## Question → Methodology → Findings → Options → Comparison → Recommendation → References
```

### PEDAGOGIQUE (evolving)
**When**: Knowledge transfer

**Structure**:
```markdown
# [Concept] Explained (Level X/10)

## Metadata

## Overview → Analogy → Detailed Concept → Examples → Pitfalls → Going Further → Glossary
```

### RECOMMANDATIONS (event-based)
**When**: Important technical decision

**Structure**:
```markdown
# Recommendations: [Title]

## Metadata

## Context → Evaluated Options (Pros/Cons/Rating) → Decision Matrix → Recommendation → Risks → Next
```

### MIGRATION (event-based)
**When**: Tech/version/infra migration

**Structure**:
```markdown
# Migration: [Title]

## Metadata

## Objective → Before/After → Procedure → Verifications → Problems → Rollback Plan → Lessons → Follow-up
```

### PERFORMANCE (event-based)
**When**: Measurable optimization

**Structure**:
```markdown
# Performance: [Title]

## Metadata

## Summary → Before Metrics → Optimizations → After Metrics → Graphs → Recommendations → References
```

### SECURITE (event-based)
**When**: Security audit, vulnerabilities

**Structure**:
```markdown
# Security Audit: [Title]

⚠️ CONFIDENTIAL - DO NOT COMMIT WITH SENSITIVE DETAILS

## Metadata

## Summary → Vulnerabilities (🔴🟠🟡) → Best Practices → Remediation Plan → Verifications → References
```

## Workflow

**Create report when**:
- Session > 1h with significant changes → SESSION
- Blocking problem resolved → INCIDENT
- Investigation completed → RECHERCHE
- Technical decision → RECOMMANDATIONS
- New procedure → GUIDE (or update)
- Migration done → MIGRATION
- Measurable optimization → PERFORMANCE
- Vulnerability found → SECURITE

**Production**:
1. Choose type
2. Use template
3. Fill all sections
4. Name correctly
5. Add metadata
6. Reference in README
7. Commit

**Maintenance**:
- Guides: Update YAML header + content
- Reports: Immutable (create new if needed)

## Quality Checklist

### Content
- [ ] All sections filled
- [ ] No TODO/To complete
- [ ] Commands tested
- [ ] Paths correct
- [ ] Links valid

### Form
- [ ] Naming respected
- [ ] Metadata present
- [ ] Valid markdown
- [ ] Code blocks with language

### Context
- [ ] Audience identified
- [ ] Level adapted
- [ ] Cross-references

### Traceability
- [ ] Commits mentioned
- [ ] Files listed
- [ ] Clear timeline

## Common Formats

| Element | Format | Example |
|---------|--------|---------|
| Timestamp | ISO 8601 with timezone | `2025-10-14T14:32:15Z` |
| Commit | Short hash 7 chars | `abc1234` |
| Files | Clear absolute or relative paths | `./docs/guides/` |
| Links | Cross-references | `see GUIDE_X.md section Y` |

## Quick Reference Table

| Type | Category | Naming | When to Use |
|------|----------|--------|-------------|
| GUIDE | Evolving | `GUIDE_subject.md` | Reusable procedures |
| METHODOLOGIE | Evolving | `METHODOLOGIE_subject.md` | Process documentation |
| AUDIT | Evolving/Event | `AUDIT_subject.md` or timestamped | Pre-intervention analysis |
| TROUBLESHOOTING | Evolving | `TROUBLESHOOTING_subject.md` | Problem resolution guides |
| INCIDENT | Event | `YYYY.MM.DD_HH.mm_commit_INCIDENT_subject.md` | Blocking issues resolved |
| SESSION | Event | `YYYY.MM.DD_HH.mm_commit_SESSION_subject.md` | Significant work sessions |
| RECHERCHE | Event | `YYYY.MM.DD_HH.mm_commit_RECHERCHE_subject.md` | Investigations |
| RECOMMANDATIONS | Event | `YYYY.MM.DD_HH.mm_commit_RECOMMANDATIONS_subject.md` | Technical decisions |
| MIGRATION | Event | `YYYY.MM.DD_HH.mm_commit_MIGRATION_subject.md` | System migrations |
| PERFORMANCE | Event | `YYYY.MM.DD_HH.mm_commit_PERFORMANCE_subject.md` | Optimization work |
| SECURITE | Event | `YYYY.MM.DD_HH.mm_commit_SECURITE_subject.md` | Security audits |

## Skill Chaining

### Skills Required Before
- None (reference skill, can be invoked anytime)

### Input Expected
- Question about documentation organization
- Request to create a specific document type
- File naming guidance needed

### Output Produced
- Documentation methodology guidance
- Correct file naming convention
- Appropriate template structure

### Compatible Skills After
- Any skill that produces documentation
- `julien-dev-commit-message` - After creating documentation
- Document-specific skills for actual creation

### Called By
- Manual invocation when documentation guidance needed
- Any skill needing documentation structure reference

### Tools Used
- None (pure reference/guidance skill)

### Usage Example

```
User: "I need to document a 3-hour session where I fixed the authentication bug"
Claude: [Invokes skill, provides SESSION template with correct naming]
→ Creates: `2025.01.21_14.30_abc1234_SESSION_auth-bug-fix.md`
```

---

**Note**: This methodology should facilitate work, not complicate it. Use only relevant document types for your context.
