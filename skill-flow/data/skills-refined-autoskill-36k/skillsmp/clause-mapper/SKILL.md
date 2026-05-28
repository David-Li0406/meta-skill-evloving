---
name: clause-mapper
description: Map LogiDocs features to ISO standard clauses and vice versa. Use when the user asks to "map clauses", "ISO coverage", "which clause", "compliance mapping", or needs to understand how platform features align with ISO 9001/14001/45001 requirements.
---

# Clause Mapper Skill

Map LogiDocs Certify features to ISO standard clauses, ensuring comprehensive coverage of certification requirements and clear traceability between platform capabilities and standard requirements.

## When to Use

- Determining which clause a feature addresses
- Identifying gaps in ISO coverage
- Creating clause-to-feature mapping documentation
- Validating feature completeness against standards
- Planning features to close compliance gaps

## ISO 9001:2015 Clause Reference

### Clause 4: Context of the Organization
| Sub-Clause | Requirement | Platform Feature |
|------------|-------------|------------------|
| 4.1 | Understanding organization context | Organization profile |
| 4.2 | Interested parties needs | Stakeholder register |
| 4.3 | QMS scope determination | Scope definition |
| 4.4 | QMS and processes | Process mapping |

### Clause 5: Leadership
| Sub-Clause | Requirement | Platform Feature |
|------------|-------------|------------------|
| 5.1 | Leadership commitment | MRM participation tracking |
| 5.2 | Quality policy | Policy document control |
| 5.3 | Roles and responsibilities | User roles, RACI matrix |

### Clause 6: Planning
| Sub-Clause | Requirement | Platform Feature |
|------------|-------------|------------------|
| 6.1 | Risks and opportunities | Risk register |
| 6.2 | Quality objectives | Objectives tracker |
| 6.3 | Planning of changes | Change management |

### Clause 7: Support
| Sub-Clause | Requirement | Platform Feature |
|------------|-------------|------------------|
| 7.1.1 | Resources - General | Resource planning |
| 7.1.2 | People | Training records |
| 7.1.3 | Infrastructure | Equipment register |
| 7.1.4 | Environment | Environment controls |
| 7.1.5 | Monitoring equipment | Calibration tracking |
| 7.1.6 | Organizational knowledge | Knowledge base |
| 7.2 | Competence | Competence matrix |
| 7.3 | Awareness | Training records |
| 7.4 | Communication | Communication log |
| 7.5 | Documented information | Document control |

### Clause 8: Operation
| Sub-Clause | Requirement | Platform Feature |
|------------|-------------|------------------|
| 8.1 | Operational planning | Process controls |
| 8.2 | Product requirements | Product specifications |
| 8.3 | Design and development | Design control |
| 8.4 | External providers | Supplier management |
| 8.5 | Production/service provision | Process records |
| 8.6 | Release of products | Release records |
| 8.7 | Nonconforming outputs | NCR management |

### Clause 9: Performance Evaluation
| Sub-Clause | Requirement | Platform Feature |
|------------|-------------|------------------|
| 9.1.1 | Monitoring general | KPI dashboard |
| 9.1.2 | Customer satisfaction | Feedback tracking |
| 9.1.3 | Analysis and evaluation | Analytics/reports |
| 9.2 | Internal audit | Audit management |
| 9.3 | Management review | MRM dashboard |

### Clause 10: Improvement
| Sub-Clause | Requirement | Platform Feature |
|------------|-------------|------------------|
| 10.1 | Improvement general | Improvement register |
| 10.2 | Nonconformity/corrective action | CAPA management |
| 10.3 | Continual improvement | Improvement tracking |

## Mapping Process

### Feature → Clause Mapping

When you have a feature and need to identify applicable clauses:

```markdown
## Feature: [Feature Name]

### Primary Clause
- **Number:** ISO 9001:2015 X.X
- **Title:** [Clause title]
- **Requirement:** [What the standard says]
- **How feature addresses:** [Specific alignment]

### Secondary Clauses
| Clause | Relevance |
|--------|-----------|
| X.X | [How it relates] |

### Coverage Assessment
- Full coverage: [What's fully addressed]
- Partial coverage: [What's partially addressed]
- Gap: [What's missing]
```

### Clause → Feature Mapping

When you have a clause and need to identify required features:

```markdown
## Clause: ISO 9001:2015 X.X - [Title]

### Requirement Summary
[What the standard requires]

### Auditor Expectations
[What evidence auditors look for]

### Required Platform Features
| Feature | Status | Notes |
|---------|--------|-------|
| [Feature] | Exists/Needed | ... |

### Evidence Examples
- [What records/evidence should exist]
```

## Coverage Analysis

### Full Coverage Matrix

Use this to assess overall platform coverage:

```markdown
## ISO 9001:2015 Coverage Analysis

### Summary
- Clauses with full coverage: X/Y
- Clauses with partial coverage: X/Y
- Clauses with no coverage: X/Y

### By Clause Section
| Section | Coverage | Priority Gaps |
|---------|----------|---------------|
| 4. Context | X% | ... |
| 5. Leadership | X% | ... |
| 6. Planning | X% | ... |
| 7. Support | X% | ... |
| 8. Operation | X% | ... |
| 9. Performance | X% | ... |
| 10. Improvement | X% | ... |

### Critical Gaps (Certification Blockers)
1. [Gap description] - Clause X.X
2. [Gap description] - Clause X.X

### Secondary Gaps (Minor NC Risk)
1. [Gap description] - Clause X.X
```

## Quick Reference Tables

### Document Types by Clause

| Clause | Required Documents |
|--------|-------------------|
| 4.3 | QMS Scope |
| 5.2 | Quality Policy |
| 6.2 | Quality Objectives |
| 7.1.5 | Calibration records |
| 7.2 | Competence records |
| 7.5 | Document register |
| 8.4 | Supplier evaluations |
| 9.2 | Audit program, reports |
| 9.3 | MRM minutes |
| 10.2 | NCR records, CAPA |

### Records Types by Clause

| Clause | Required Records |
|--------|-----------------|
| 7.1.5 | Calibration results |
| 7.2 | Training records |
| 8.2.3 | Contract review records |
| 8.4 | Supplier monitoring |
| 8.5.2 | Traceability records |
| 8.6 | Release records |
| 9.1.2 | Customer satisfaction data |
| 9.2 | Audit findings |
| 9.3 | MRM outputs |
| 10.2 | Nonconformity records |

## Output Format

### Single Feature Mapping
```markdown
## Clause Mapping: [Feature Name]

### Primary Alignment
**Clause:** ISO 9001:2015 X.X - [Title]
**Requirement:** [Summary]
**Feature addresses:** [How]

### Related Clauses
- X.X: [Relationship]

### Audit Questions Addressed
- "[Typical auditor question]"

### Evidence Produced
- [What records/evidence this creates]
```

### Gap Analysis Output
```markdown
## Clause Gap Analysis: [Area]

### Clauses Assessed
[List of clauses evaluated]

### Coverage Status
| Clause | Status | Feature | Gap |
|--------|--------|---------|-----|
| X.X | Full/Partial/None | [Feature] | [Gap] |

### Priority Actions
1. [Critical gap to close]
2. [Important gap]
3. [Nice to have]
```

## Related Agents

- `iso-expert` - Detailed clause interpretation
- `auditor-simulator` - Validate evidence meets requirements
