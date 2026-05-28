# Design Document Skill

> **Install:** `npx skills add diskd-ai/design-doc` | [skills.sh](https://skills.sh)

Create structured technical design documents that communicate system behavior, implementation approach, and acceptance criteria.

---

## Scope & Purpose

This skill provides guidance and templates for writing technical design documents, covering:

* Feature design specifications
* System architecture documents
* Technical requirements documents (TRD)
* Request for comments (RFC)
* Refactoring plans
* API designs
* Database schema designs

---

## When to Use This Skill

**Triggers:**
* "Write a design doc for X"
* "Design the Y feature"
* "Create a technical spec"
* "Plan the architecture for Z"
* Requests for TRD, RFC, or system design documents

**Use cases:**
* Planning new features before implementation
* Documenting system architecture decisions
* Creating refactoring proposals
* Specifying API contracts
* Designing database schemas
* Communicating technical decisions to stakeholders

---

## Quick Reference

### Template Sections

| Section | Purpose |
|---------|---------|
| Context and motivation | Problem statement, goals, non-goals |
| Implementation considerations | Constraints, design principles, trade-offs |
| High-level behavior | End-to-end system flow |
| Domain-specific sections | Adapted to feature type |
| Error handling and UX | Error surfacing and recovery |
| Future-proofing | Design for extensibility |
| Implementation outline | Step-by-step approach |
| Testing approach | Unit, integration, manual tests |
| Acceptance criteria | Testable conditions for "done" |

### Domain-Specific Section Guide

| Feature Type | Typical Sections |
|--------------|------------------|
| File processor | Discovery rules, Format validation, Output model |
| API/Service | Endpoint design, Request/response schemas, Auth |
| UI Feature | Component structure, State management, Rendering |
| Data pipeline | Input sources, Transformations, Output sinks |
| Integration | Protocol, Authentication, Error mapping |

---

## Workflow

1. **Gather context**: Understand the feature/system scope, constraints, and goals
2. **Draft structure**: Use template from `references/template.md`
3. **Fill sections**: Work through each section, asking clarifying questions as needed
4. **Review**: Ensure acceptance criteria are testable and implementation outline is actionable

---

## Skill Structure

```
design-doc/
  SKILL.md          # Skill definition and guidelines
  README.md         # This file (overview)
  references/       # Supporting documentation
    template.md     # Full template with section guidelines
```

---

## Writing Guidelines

* Use `---` underlines for section headers (Setext style)
* Write in present tense for behavior ("loads", "validates", "returns")
* Be specific: "max 100 chars" not "reasonable length"
* Include concrete examples where behavior varies
* Non-goals are as important as goals - prevent scope creep
* Acceptance criteria must be verifiable, not subjective

---

## Section Best Practices

### Context and Motivation
* State the problem clearly in 1-2 sentences
* Explain why now (what triggered this work)
* Goals should be measurable outcomes, not implementation details
* Non-goals prevent scope creep and set expectations

### High-Level Behavior
* Write as if explaining to a new team member
* Use bullet points for step-by-step flows
* Cover both happy path and edge cases

### Acceptance Criteria
Write as testable statements:
* "Given X, when Y, then Z"
* Include both positive and negative cases
* Reference specific behaviors from High-level behavior section

---

## Resources

* **Full template**: [references/template.md](references/template.md)
* **Skill definition**: [SKILL.md](SKILL.md)

---

## License

MIT
