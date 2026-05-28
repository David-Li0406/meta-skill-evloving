# Key Trends Summary 2025-2026

Summary of major trends in Specification-Driven Development and documentation practices.

**Research Date:** 2026-01-19
**Sources:** Thoughtworks, Martin Fowler, AWS, Google Cloud, Microsoft, Red Hat, Pragmatic Engineer

---

## 2025-2026 Specification-Driven Development

1. **AI as specification partner** - LLMs help structure and complete specs, but humans remain accountable
2. **Bottleneck shift** - Implementation is commoditized; specification skills are premium
3. **Tool explosion** - 15+ major SDD platforms launched 2024-2025
4. **Workflow standardization** - Intent -> Spec -> Plan -> Execute -> Review pattern universal

## Living Documentation

1. **Docs-as-Code mainstream** - Version control, CI/CD for documentation
2. **LLM-optimized docs** - Markdown for AI assistants (Cursor, Copilot)
3. **Auto-generation mature** - API docs, code docs generated from source
4. **Developer portals** - Backstage, GitBook as central hubs

## Architecture Decisions

1. **ADRs standard practice** - Adopted across AWS, Google Cloud, Microsoft
2. **Immutability preferred** - New ADRs over editing existing
3. **Co-location with code** - Store in `docs/adr/` in repo
4. **Amazon-style reviews** - Silent reading before discussion

## API Development

1. **API-First mandatory** - Design before implementation
2. **OpenAPI 3.1** - JSON Schema alignment, webhooks support
3. **Contract testing** - Automated verification against spec
4. **Mock-first frontend** - Parallel development enabled

---

## All Sources

### Specification-Driven Development
- [Thoughtworks: Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler: SDD Tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Microsoft: Spec-Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- [JetBrains: Spec-Driven Approach](https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/)
- [Red Hat: SDD Quality](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality)
- [Scott Logic: Specification Renaissance](https://blog.scottlogic.com/2025/12/15/the-specification-renaissance-skills-and-mindset-for-spec-driven-development.html)

### Living Documentation
- [Augment Code: Auto Document](https://www.augmentcode.com/learn/auto-document-your-code-tools-and-best-practices)
- [Squarespace: Docs-as-Code Journey](https://engineering.squarespace.com/blog/2025/making-documentation-simpler-and-practical-our-docs-as-code-journey)
- [Mintlify](https://www.mintlify.com/)
- [GitBook: LLM-Ready Docs](https://gitbook.com/docs/publishing-documentation/llm-ready-docs)
- [Medium: Living Documentation](https://medium.com/@rasmus-haapaniemi/living-documentation-how-to-let-your-documentation-grow-naturally-and-be-self-sustainable-24feac57a041)

### Architecture Decision Records
- [AWS Architecture Blog: ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Google Cloud: ADR Overview](https://cloud.google.com/architecture/architecture-decision-records)
- [Microsoft: Azure ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [ADR GitHub](https://adr.github.io/)
- [UK GOV: ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)

### API-First Development
- [Baeldung: API First with Spring Boot](https://www.baeldung.com/spring-boot-openapi-api-first-development)
- [DevGuide: Contract-First](https://devguide.dev/blog/contract-first-api-development)
- [OpenAPI Specification 3.1](https://swagger.io/specification/)
- [openapi-stack](https://github.com/openapistack)
- [Fern: API-First Platforms](https://buildwithfern.com/post/api-first-development-platforms)

### Design Docs & RFCs
- [Pragmatic Engineer: RFCs and Design Docs](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs)
- [Pragmatic Engineer: RFC Examples](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design)
- [Industrial Empathy: Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)
- [Uber H3 RFC Template](https://github.com/uber/h3/blob/master/dev-docs/RFCs/rfc-template.md)
- [InnerSource: RFC Patterns](https://patterns.innersourcecommons.org/p/transparent-cross-team-decision-making-using-rfcs)

---

*Reference Document | Key Trends Summary 2025-2026 | Version 1.0*
