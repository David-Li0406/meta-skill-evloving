# FRD Template (Odyssey-Style)

Use this structure for generating Functional Requirements Documents. Adapt technology references to the project's actual stack. Apply Socratic questioning and Devil's Advocate analysis before generating.

## Pre-Generation Analysis

Before writing the FRD, complete the critical analysis phase:

1. **Read** [socratic-questions.md](socratic-questions.md) and apply to each epic
2. **Read** [devils-advocate-strategy.md](devils-advocate-strategy.md) and challenge major decisions
3. **Document** findings in Sections 2 (Strategic Context) and 12 (Assumptions & Risks)

## Template

```markdown
---
title: "[Product Name] - Functional Requirements Document"
description: "Comprehensive functional requirements for [Product Name]"
document_id: FRD-001
product: [Product Name]
date: [DD/MM/YYYY]
version: 1.0
author: [Author from PRD or user]
status: Draft
technology_stack: [Array extracted from PRD/FRD or specified by user]
---

# 1. Introduction

## 1.1 Purpose
This document specifies the functional requirements for [Product Name]. It serves as the authoritative source for implementation teams, providing detailed specifications derived from the PRD.

## 1.2 Scope
[Define what is included and explicitly excluded from this FRD]

## 1.3 Document Conventions

| Convention | Meaning |
|------------|---------|
| P0 | Critical priority - blocks release |
| P1 | High priority - required for release |
| P2 | Medium priority - desired for release |
| SHALL | Mandatory requirement |
| SHOULD | Strongly recommended requirement |
| MAY | Optional requirement |

## 1.4 References

| Document | Location | Version |
|----------|----------|---------|
| PRD | ./docs/PRD.md | [Version] |
| [Other docs] | [Path] | [Version] |

## 1.5 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Frontend | [Framework] | [Version] | [Purpose] |
| Backend | [Framework] | [Version] | [Purpose] |
| Database | [Database] | [Version] | [Purpose] |
| [Other] | [Technology] | [Version] | [Purpose] |

---

# 2. Strategic Context

## 2.1 Problem Statement
[Concise description of the problem with quantitative evidence from PRD]

## 2.2 Strategic Rationale
[Why this product/feature, why now, how it fits company strategy]

## 2.3 Key Assumptions (to validate)

| ID | Assumption | Validation Method | Status |
|----|------------|-------------------|--------|
| A-001 | [User assumption] | [How to test] | Unvalidated |
| A-002 | [Technical assumption] | [How to test] | Unvalidated |
| A-003 | [Business assumption] | [How to test] | Unvalidated |

## 2.4 Success Metrics

| Metric | Baseline | Target (3mo) | Target (6mo) | Measurement |
|--------|----------|--------------|--------------|-------------|
| [Leading indicator] | [Current] | [Target] | [Target] | [Method] |
| [Lagging indicator] | [Current] | [Target] | [Target] | [Method] |

---

# 3. User Roles and Personas

## 3.1 Primary User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| [Role Name] | [Description] | [Key permissions] |

## 3.2 Primary Persona: [Name]

**Demographics**: [Age, role, company context, tech proficiency]

**Goals**:
- [Primary goal]
- [Secondary goal]

**Pain Points**:
- [Current frustration 1]
- [Current frustration 2]

**Current Solutions**: [How they solve this today]

**Success Criteria**: [What makes this persona successful with the product]

## 3.3 Secondary Persona: [Name]
[Same structure as primary]

---

# 4. Functional Requirements — [Epic Name] (EP-01)

## 4.0 Epic Analysis

**Job-to-be-Done**: [What specific job does this epic address?]

**Evidence of Need**: [Quantitative/qualitative evidence this is a real problem]

**Alternatives Considered**:
| Approach | Pros | Cons | Why Not Chosen |
|----------|------|------|----------------|
| [Alternative 1] | [Pros] | [Cons] | [Reason] |
| [Alternative 2] | [Pros] | [Cons] | [Reason] |

## 4.1 FR-[ABBREV]-001: [Requirement Name]

| Priority | Dependencies | Tech Stack |
|----------|--------------|------------|
| P0 | None | [Relevant technologies from project stack] |

**Requirement:** System SHALL [specific behavioral requirement with measurable criteria].

**Functional Details:**
- [Detail 1 with specific behavior]
- [Detail 2 with edge cases]
- [Integration points]

**Business Rules:**
- BR-001: [Rule with specific logic]
- BR-002: [Rule with validation criteria]

**Acceptance Criteria:**

```
GIVEN: User is authenticated and on [specific page/state]
WHEN: User [performs specific action with parameters]
THEN: System [produces specific, measurable outcome]
  AND: [Additional outcome if applicable]
```

## 4.2 FR-[ABBREV]-002: [Requirement Name]
[Same structure as 4.1]

---

# 5. Functional Requirements — [Epic Name] (EP-02)
[Repeat section 4 structure for each epic, including Epic Analysis]

---

# 10. Requirements Traceability Matrix

| Req ID | Requirement | Priority | PRD Section | Epic | Test Case ID | Status |
|--------|-------------|----------|-------------|------|--------------|--------|
| FR-UP-001 | [Short name] | P0 | 3.1 | EP-01 | TC-UP-001 | Draft |
| FR-UP-002 | [Short name] | P1 | 3.2 | EP-01 | TC-UP-002 | Draft |

---

# 11. Non-Functional Requirements Summary

## 11.1 Performance Requirements

| NFR ID | Requirement | Target | Measurement |
|--------|-------------|--------|-------------|
| NFR-PERF-001 | Page load time | < 2s (P95) | Lighthouse/RUM |
| NFR-PERF-002 | API response time | < 200ms (P95) | APM |
| NFR-PERF-003 | Concurrent users | [Target from PRD] | Load testing |

## 11.2 Security Requirements

| NFR ID | Requirement | Implementation |
|--------|-------------|----------------|
| NFR-SEC-001 | Authentication | [Auth method from stack] |
| NFR-SEC-002 | Authorization | [RBAC/ABAC as per stack] |
| NFR-SEC-003 | Data encryption | TLS in transit, encryption at rest |

## 11.3 Scalability Requirements
[Horizontal/vertical scaling strategy based on architecture]

## 11.4 Availability & Reliability Requirements

| Metric | Target |
|--------|--------|
| Uptime SLA | [From PRD or 99.9%] |
| RPO | [From PRD or specify] |
| RTO | [From PRD or specify] |

---

# 12. Assumptions & Risks

## 12.1 Critical Assumptions

| ID | Assumption | Impact if Wrong | Validation Plan |
|----|------------|-----------------|-----------------|
| A-001 | [Assumption] | [Impact] | [How to validate] |

## 12.2 Risk Assessment

| Risk ID | Risk | Category | L | I | Mitigation | Contingency | Owner |
|---------|------|----------|---|---|------------|-------------|-------|
| R-001 | [Description] | Technical | H/M/L | H/M/L | [Strategy] | [Fallback] | [Name] |
| R-002 | [Description] | Market | H/M/L | H/M/L | [Strategy] | [Fallback] | [Name] |

**Categories**: Technical, Market, Operational, Execution, Compliance

## 12.3 Key Decisions & Trade-offs

Document major decisions challenged via Devil's Advocate:

### Decision 1: [Decision Statement]

**Original Rationale**: [Why this was chosen]

**Devil's Advocate Challenge**: [Strongest argument for alternative]

**Trade-offs Accepted**:
- We accept [risk/downside] in exchange for [benefit]

**Mitigations Added**:
- [Action to address valid concerns]

---

# 13. Use Cases

## UC-001: [Use Case Name]

**Primary Actor**: [Role]
**Preconditions**: [What must be true]
**Postconditions**: [What is true after]

**Primary Flow:**
1. User [action]
2. System [response]
3. User [action]
4. System [response]

**Alternative Flows:**
- 2a. If [condition]: [alternative path]

**Exception Flows:**
- E1. If [error]: [handling]

---

# 14. Open Questions

| ID | Question | Context | Owner | Due Date | Status |
|----|----------|---------|-------|----------|--------|
| Q-001 | [Question requiring stakeholder input] | [Why this matters] | [Name] | [Date] | Open |
| Q-002 | [Clarification needed from PRD] | [Gap identified] | [Name] | [Date] | Open |

**Note**: These questions were identified during FRD analysis and require resolution before implementation.

---

# 15. Glossary

| Term | Definition |
|------|------------|
| [Term] | [Definition] |

---

# 16. Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

## Style Guidelines

**Requirement Writing**:
- Start with "System SHALL/SHOULD/MAY"
- Be specific and measurable
- Include edge cases and error conditions
- Reference specific UI components or API endpoints (using project terminology)

**Priority Assignment**:
- P0: Feature doesn't work without it, security/compliance critical
- P1: Core user journey, significant user value
- P2: Enhancement, nice-to-have

**Acceptance Criteria**:
- Always Given/When/Then format
- Include specific values, not ranges
- Cover happy path and key error paths
- Make testable by QA without ambiguity

**Technology References**:
- Use actual technology names from the project's stack
- Don't assume any specific framework
- Extract stack details from PRD or ask user

**Critical Analysis**:
- Every epic must have an Epic Analysis subsection
- Document alternatives considered and why rejected
- Challenge assumptions - don't rubber-stamp PRD
- Flag gaps with specific questions in Section 14

## Epic Abbreviation Examples

| Epic | Abbreviation | Example FR |
|------|--------------|------------|
| User Profile | UP | FR-UP-001 |
| Job Discovery | JD | FR-JD-001 |
| Authentication | AU | FR-AU-001 |
| Dashboard | DB | FR-DB-001 |
| Notifications | NT | FR-NT-001 |
| Admin | AD | FR-AD-001 |
| Payments | PM | FR-PM-001 |
| Search | SR | FR-SR-001 |
| Reports | RP | FR-RP-001 |
| Settings | ST | FR-ST-001 |

## Red Flags to Watch For

When analyzing PRD, these responses suggest weak reasoning:

| Response in PRD | Translation | Action |
|-----------------|-------------|--------|
| "Everyone knows X" | Unvalidated assumption | Add to Section 12.1, demand evidence |
| "We've always done Y" | Habit, not strategy | Challenge in Section 12.3 |
| "There's no time to evaluate Z" | Avoiding analysis | Flag in Section 14 |
| "The team wants A" | Preference, not rationale | Ask "why?" in Section 14 |
| "Competitors do X" | Copying, not thinking | Challenge in Section 12.3 |
| Vague success metrics | Can't measure success | Flag in Section 14 |
| No evidence cited | Assumption-driven | Add to Section 12.1 |
