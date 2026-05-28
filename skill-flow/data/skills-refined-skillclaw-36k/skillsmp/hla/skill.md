---
name: hla
description: High Level Architecture (HLA) document creation for leadership review
---

# Amazon High Level Architecture (HLA) Skill

Use this skill when creating comprehensive architecture documents that follow Amazon's working backwards approach and narrative style. HLA documents are designed for senior leadership review and stakeholder alignment.

**Template:** See `docs/templates/hla-template.md` for the authoritative template structure.

## When to Use This Skill

- When documenting new microservice or system architecture
- When preparing architecture documents for leadership review
- When creating formal architecture documentation for complex distributed systems
- When presenting system architecture to stakeholders in Amazon's format

## Document Structure Summary

Create a ~6-page document (2500-3000 words) with these sections:

1. **Metadata** - Title, author, date, version, status
2. **Overview** (1 page) - Executive summary, customer problems, goals, non-goals
3. **Tenets/Principles** (½ page) - 4-6 guiding principles with tradeoffs
4. **Architecture Narrative** (2-3 pages) - System overview, Mermaid diagrams, component details, data flow, APIs, scale, availability, security
5. **Detailed Design Considerations** (1-1.5 pages) - Alternatives considered, failure modes, operational concerns
6. **Risks & Open Questions** (½ page) - Dependencies, open questions, assumptions
7. **Next Steps** (½ page) - Prototype plan, milestones, resource requirements

## Writing Style

| Requirement | Guideline |
|-------------|-----------|
| **Narrative** | Full paragraphs, not bullet-point lists |
| **Tense** | Present tense, as if system exists |
| **Clarity** | Plain English, define jargon |
| **Customer Focus** | Every decision ties to customer value |
| **Quantification** | Metrics wherever possible |
| **Assumptions** | Marked explicitly with **(Assumption)** |

## Quality Checklist

- [ ] Customer problems clearly articulated
- [ ] 4-6 actionable tenets included
- [ ] Architecture diagram present and accurate (Mermaid)
- [ ] Alternatives documented with rationale
- [ ] Failure modes and mitigations covered
- [ ] Open questions have owners and dates
- [ ] Next steps are concrete
- [ ] Word count: 2500-3000 words

## Output Location

```
docs/architecture/[system-name]-hla.md
```
