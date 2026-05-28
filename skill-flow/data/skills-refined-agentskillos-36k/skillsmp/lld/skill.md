---
name: lld
description: Low Level Design (LLD) document creation with detailed implementation specifications
---

# Amazon Low Level Design (LLD) Skill

Use this skill when creating detailed technical specifications for software components. LLD documents bridge the gap between high-level architecture and actual code implementation, providing engineers with everything they need to build.

**Template:** See `docs/templates/lld-template.md` for the authoritative template structure.

## When to Use This Skill

- After HLD is approved and detailed implementation specs are needed
- When engineers need complete API specs, database schemas, and sequence diagrams
- When defining component interfaces and data flows
- When creating specifications detailed enough for immediate implementation

## Document Structure Summary

Create a ~6-page document (3000-3500 words) with these sections:

1. **Title & Metadata** - Component/service name, author, date, version, related HLD
2. **Introduction** (½ page) - Context, scope, audience, terminology
3. **Detailed Component Design** (2-3 pages) - Responsibilities, dependencies, interfaces, data flow, error handling, configuration
4. **Data Models & Schemas** (1-1.5 pages) - Entity definitions, database schemas, indexing strategy, serialization
5. **API Specifications** (1 page) - Complete endpoints with request/response examples, error codes, validation
6. **Sequence & State Diagrams** (½ page) - Key flows, state machines
7. **Operational Considerations** (½ page) - Monitoring metrics, logging, performance targets, deployment
8. **Open Issues/Assumptions** (½ page) - Issues, assumptions, prototyping needs

## Writing Style

| Aspect | Guideline |
|--------|-----------|
| **Language** | Clear, fact-driven narrative; technical precision for specs |
| **Tense** | Present tense, as if design exists |
| **Customer Focus** | Connect technical decisions to customer value |
| **Examples** | Include concrete examples (JSON, SQL, API calls) |
| **Tradeoffs** | Document rationale for design choices |

## Quality Checklist

- [ ] All components have clear responsibilities and boundaries
- [ ] Data flows are explicitly documented with state transitions
- [ ] APIs include complete request/response specifications
- [ ] Database schemas include proper indexing strategies
- [ ] Mermaid diagrams accurately represent system flows
- [ ] Error handling covers all failure scenarios
- [ ] Performance and monitoring requirements are specified
- [ ] Word count: 3000-3500 words

## Output Location

```
docs/design/[component-name]-lld.md
```
