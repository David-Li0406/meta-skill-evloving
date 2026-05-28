---
name: hld
description: High Level Design (HLD) document creation for engineering design reviews
---

# Amazon High Level Design (HLD) Skill

Use this skill when creating comprehensive High Level Design documents for engineering design reviews. HLD documents provide the strategic technical vision that guides implementation while remaining accessible to stakeholders.

**Template:** See `docs/templates/hld-template.md` for the authoritative template structure.

## When to Use This Skill

- When documenting new system architecture for engineering review
- When creating formal design documentation for stakeholder alignment
- When translating product requirements into technical architecture
- When preparing for design review meetings

## Document Structure Summary

Create a ~6-page document (2500-3000 words) with these sections:

1. **Title & Metadata** - System name, author, date, version, status
2. **Overview** (1 page) - Executive summary, problem statement, goals, non-goals, success metrics
3. **Tenets/Principles** (½ page) - 4-6 design principles with examples
4. **Architecture** (2-2.5 pages) - System diagram, component responsibilities, data flow, API design, scale/performance, security
5. **Detailed Design Considerations** (1-1.5 pages) - Alternatives considered, failure modes, operational concerns (monitoring, deployment, cost)
6. **Risks & Open Questions** (½ page) - Dependencies, open questions, assumptions
7. **Next Steps** (½ page) - Validation activities, milestones, resource requirements

## Writing Style

| Aspect | Guideline |
|--------|-----------|
| **Format** | Full narrative paragraphs, not bullet-point dumps |
| **Tense** | Present tense - describe as if implemented |
| **Audience** | Intelligent VP who needs to understand quickly |
| **Jargon** | Define technical terms when first used |
| **Examples** | Use concrete examples to illustrate abstract concepts |
| **Customer** | Every section connects back to customer value |

## Quality Checklist

- [ ] Customer problem clearly articulated
- [ ] Tenets are actionable and referenced in decisions
- [ ] Architecture diagram accurately represents system (Mermaid)
- [ ] All alternatives documented with rationale
- [ ] Failure modes and mitigations addressed
- [ ] Dependencies and risks explicitly stated
- [ ] Next steps are concrete and assigned
- [ ] Word count: 2500-3000 words

## Output Location

```
docs/design/[system-name]-hld.md
```
