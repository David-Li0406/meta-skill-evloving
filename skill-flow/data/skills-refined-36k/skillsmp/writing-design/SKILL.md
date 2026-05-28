---
name: writing-design
description: "Use when creating design documents, technical specs, architecture decisions, or system documentation. Covers structure, audience, and validation."
---

# Writing Design Documents

## No Code Policy

> **Design documents must be plain prose.** No code blocks, no schema definitions, no API examples. Describe architecture and decisions in written English.

Why:
- Designs should be accessible to all stakeholders
- Code creates false precision - designs should describe intent, not implementation
- Prose forces clear thinking about the "why" behind decisions

## Overview

Design documents capture decisions, trade-offs, and rationale BEFORE implementation. They prevent rework, align stakeholders, and create institutional knowledge.

## When to Use

- Planning new feature with multiple approaches
- Making architectural decisions
- Proposing system changes
- Documenting API contracts
- Recording technology choices

## Document Types

| Type | Purpose | Audience |
|------|---------|----------|
| **RFC** | Propose significant changes | Team, stakeholders |
| **ADR** | Record architecture decisions | Future developers |
| **Tech Spec** | Detail implementation approach | Implementers |
| **API Contract** | Define interface boundaries | Consumers, implementers |

---

## Structure Template

All design documents should be written in plain prose. Here are the key sections for each type:

### RFC (Request for Comments)

An RFC proposes significant changes and needs team buy-in.

**Header:** Title, status (Draft/Review/Accepted/Rejected), author, date, reviewers.

**Summary:** One or two paragraphs capturing the essence of the proposal. A busy reader should understand the key points from this alone.

**Problem Statement:** What problem are we solving? Why is it important now? What's the cost of not solving it?

**Goals and Non-Goals:** Explicitly state what we're trying to achieve AND what's out of scope. Non-goals prevent scope creep.

**Proposed Solution:** Describe the approach in prose. Use diagrams if helpful, but no code. Focus on the "what" and "why", not the "how".

**Alternatives Considered:** List other approaches you evaluated. For each, explain the pros, cons, and why it wasn't chosen. These should be genuine alternatives, not strawmen.

**Trade-offs:** What are we giving up with this approach? Be honest.

**Risks:** What could go wrong? For each risk, assess likelihood and impact, and describe the mitigation strategy.

**Open Questions:** What still needs to be resolved before implementation?

### ADR (Architecture Decision Record)

An ADR records a significant architectural decision for future reference.

**Header:** Number, title, status (Proposed/Accepted/Deprecated/Superseded), date, deciders.

**Context:** What situation or problem motivated this decision? Provide enough background that someone reading this later understands the constraints.

**Decision:** What did we decide? State it clearly in one or two sentences.

**Consequences:** What are the positive outcomes, negative trade-offs, and neutral side effects of this decision?

**Alternatives Not Chosen:** What other options were considered and why weren't they selected?

### Tech Spec

A tech spec details the implementation approach for a specific feature.

**Header:** Feature name, author, status, target version.

**Overview:** Brief description of what this feature does and why it matters.

**Requirements:** Functional requirements (what it must do) and non-functional requirements (performance, security, scalability targets).

**Design:** Describe the data model, API approach, and component architecture in prose. Explain how pieces fit together and data flows through the system.

**Testing Strategy:** How will we verify this works? Describe the approach for unit, integration, and end-to-end testing.

**Rollout Plan:** How will we deploy this? Describe phases if applicable.

**Monitoring:** What should we watch after deployment to ensure it's working correctly?

---

## Quality Checklist

### Content
- [ ] Problem is clearly stated
- [ ] Goals are measurable/verifiable
- [ ] Non-goals explicitly stated
- [ ] Alternatives genuinely considered (not strawmen)
- [ ] Trade-offs acknowledged honestly
- [ ] Risks identified with mitigations

### Structure
- [ ] Appropriate template for document type
- [ ] Sections complete (no TODOs in final)
- [ ] Diagrams where text is unclear
- [ ] References linked, not inline

### Audience
- [ ] Technical level appropriate for readers
- [ ] Jargon explained or avoided
- [ ] Executive summary for skimmers

### Review
- [ ] Self-reviewed before sharing
- [ ] Reviewed by someone not involved
- [ ] Open questions addressed or marked

---

## Common Mistakes

### 1. Writing After Implementation
**Wrong**: Document what you built
**Right**: Document decisions BEFORE building

### 2. Fake Alternatives
**Wrong**: "Do nothing" or obviously bad options
**Right**: Genuinely viable alternatives you considered

### 3. Missing Trade-offs
**Wrong**: Only listing benefits
**Right**: Honest assessment of what you're giving up

### 4. Too Much Detail
**Wrong**: Implementation code in design doc
**Right**: Enough detail to make decisions, not implement

### 5. Stale Documents
**Wrong**: Design doc never updated
**Right**: Update status, add learnings, link to ADRs

---

## Anti-patterns

**Solution disguised as problem:**

Bad: "We need to use Redis for caching." This states a solution, not a problem.

Good: "API response times exceed 500ms for dashboard queries, causing poor user experience." This describes the actual problem, leaving solution space open.

**Strawman alternatives:**

Bad: Listing "do nothing" or obviously terrible options just to make your preferred solution look good.

Good: Presenting genuine alternatives with honest trade-offs. For example, when solving slow API responses, real alternatives might be Redis (fast but operational overhead), in-memory caching (simple but doesn't scale), or CDN edge caching (fast but invalidation is complex). Each has genuine merit.

---

## Integration

**Related skills:** plan, brainstorm
**Triggers:** design, RFC, ADR, tech spec, architecture, proposal
