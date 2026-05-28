---
id: writing-specifications
name: "Writing Specifications"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Writing Specifications

## Metadata

| Field | Value |
|-------|-------|
| **ID** | writing-specifications |
| **Version** | 2.0.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Beginner |
| **Tags** | #methodology, #sdd, #specification, #requirements |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-spec-reviewer-agent |

---

## Methodology Reference

**Primary:** writing-specifications (Writing Specifications v2.0)

**Integrated:**
| Domain | Methodology | Principle Applied |
|--------|-------------|-------------------|
| BA | smart-requirements | SMART requirements criteria |
| BA | requirements-traceability | Requirements traceability (FR-X → US-X) |
| BA | use-case-modeling | Use Case diagrams and flows |
| BA | user-story-mapping | User Story Mapping |
| BA | acceptance-criteria | Acceptance criteria (Given-When-Then) |
| PdM | mvp-scoping | MVP scoping (MoSCoW prioritization) |
| PdM | user-story-mapping | User Story Mapping |
| PdM | spec-writing | PRD writing best practices |
| PM | scope-management | Scope Management |
| UX | user-research | User Research synthesis |
| UX | persona-development | Persona development |

---

## Problem

Projects fail when teams build the wrong thing. This happens because:
- Requirements are vague or missing
- Stakeholders have different expectations
- Scope keeps changing during development
- No single source of truth for "what are we building?"
- User needs not properly researched
- Acceptance criteria not testable

**The root cause:** No written specification that everyone agrees on.

---

## Framework

### What is a Specification?

A specification (spec) answers: **"WHAT are we building and WHY?"**

It does NOT answer "how" - that's for the design document.

### Spec vs Design vs Implementation Plan

| Document | Question | Output |
|----------|----------|--------|
| Specification | WHAT and WHY? | Requirements, user stories, acceptance criteria |
| Design | HOW? | Architecture, file structure, API contracts |
| Implementation Plan | IN WHAT ORDER? | Tasks, dependencies, estimates |

### Spec Structure v2.0

```markdown
# Feature: [Name]

## Reference Documents
[Links to constitution, related specs]

## Overview
[1-2 paragraphs explaining what this feature does]

## Problem Statement
[Who, what problem, why it matters, business value]

## User Personas
[Who are the users]

## User Stories (User Story Mapping)
[Backbone → Walking Skeleton → Full Product]

## Use Cases (if complex)
[Actor, preconditions, flow, alternatives]

## Functional Requirements
[FR-X with SMART criteria, MoSCoW priority]

## Non-Functional Requirements
[NFR-X: performance, security, scalability]

## Acceptance Criteria (BDD)
[Given-When-Then format]

## Out of Scope
[Explicit exclusions]

## Assumptions & Constraints
[What we assume, limitations]

## Related Features
[Feature dependencies, related specs]

## Recommended Skills & Methodologies
[For implementation phase]
```

---

## Writing Process

### Phase 1: Load Context

Before writing, read and understand:

```
1. .aidocs/constitution.md - project principles, tech stack
2. .aidocs/features/done/ - completed features (patterns)
3. Related specs in features/todo/ or features/in-progress/
```

Extract:
- Tech stack constraints
- Code standards
- Existing patterns
- Related features to reference

### Phase 2: Problem Analysis (BA: smart-requirements SMART)

#### 2.1 Define the Problem (SMART)

| Criterion | Question | Bad Example | Good Example |
|-----------|----------|-------------|--------------|
| **S**pecific | Exactly who and what? | "Users need auth" | "New users cannot register" |
| **M**easurable | How to measure success? | "Should be fast" | "Registration < 3 seconds" |
| **A**chievable | Technically feasible? | "AI that reads minds" | "OAuth 2.0 integration" |
| **R**elevant | Ties to business goal? | "Nice to have" | "Blocks monetization" |
| **T**ime-bound | When needed? | "Eventually" | "Required for Q1 launch" |

#### 2.2 Business Value Statement

Format:
```
[WHO] currently cannot [WHAT] because [WHY].
This results in [IMPACT].
By implementing [SOLUTION], we will [BENEFIT].
```

Example:
```
New users currently cannot access premium content because there's no
login system. This results in $0 revenue from premium features.
By implementing email authentication, we will enable premium subscriptions.
```

### Phase 3: User Research (UX: user-research, persona-development)

#### 3.1 Define User Personas

| Field | Description |
|-------|-------------|
| **Name** | Archetype name |
| **Role** | What they do |
| **Goal** | What they want to achieve |
| **Pain Points** | Current frustrations |
| **Context** | When/where they use the product |

Example:
```markdown
### Persona 1: Freelance Developer "Alex"
- **Role:** Solo developer building SaaS products
- **Goal:** Ship MVPs quickly without server management
- **Pain Points:** Too much time on auth, payments, infra
- **Context:** Works from home, uses macOS, deploys to Vercel
```

### Phase 4: User Story Mapping (BA: user-story-mapping, PdM: user-story-mapping)

#### 4.1 Story Mapping Structure

```
                    ┌─────────────────────────────────────────┐
                    │             USER ACTIVITIES             │
                    │  (High-level goals: "Manage Account")   │
                    └─────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ↓                   ↓                   ↓
            ┌───────────┐       ┌───────────┐       ┌───────────┐
            │  BACKBONE │       │  BACKBONE │       │  BACKBONE │
            │ (Actions) │       │ (Actions) │       │ (Actions) │
            │ "Register"│       │  "Login"  │       │ "Logout"  │
            └───────────┘       └───────────┘       └───────────┘
                    │                   │                   │
        ┌───────────┼───────┐   ┌───────┼───────┐          │
        ↓           ↓       ↓   ↓       ↓       ↓          ↓
    ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
    │ MVP   │ │ MVP   │ │ v1.1  │ │ MVP   │ │ v1.1  │ │ MVP   │
    │US-001 │ │US-002 │ │US-005 │ │US-003 │ │US-006 │ │US-004 │
    └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘

    ─────────── MVP (Walking Skeleton) ───────────────────────
    ─────────── v1.1 (Release 2) ─────────────────────────────
```

#### 4.2 Write User Stories

Format: As a [PERSONA], I want [ACTION], so that [BENEFIT].

**INVEST Criteria for User Stories:**
| Criterion | Question |
|-----------|----------|
| **I**ndependent | Can be delivered separately? |
| **N**egotiable | Details can be discussed? |
| **V**aluable | Delivers user/business value? |
| **E**stimable | Can estimate effort? |
| **S**mall | Fits in one sprint/iteration? |
| **T**estable | Can write acceptance tests? |

Example:
```markdown
### US-001: Email Registration (MVP)
**As a** freelance developer (Alex)
**I want to** create an account with my email
**So that** I can save my API keys and project settings

**Acceptance Criteria:** (see AC-001)
**Priority:** Must (MVP)
**Estimate:** 3 story points
```

### Phase 5: Use Cases (BA: use-case-modeling) - For Complex Features

When to use: Multi-step workflows, multiple actors, complex validations.

```markdown
### UC-001: User Registration

**Primary Actor:** Unregistered User
**Preconditions:** User is not logged in, has valid email

**Main Flow:**
1. User navigates to registration page
2. User enters email and password
3. System validates email format
4. System checks email uniqueness
5. System creates account
6. System sends verification email
7. User is redirected to dashboard

**Alternative Flows:**
- 3a. Invalid email format → Show error, return to step 2
- 4a. Email exists → Show "already registered" error

**Postconditions:** Account created, verification email sent
```

### Phase 6: Functional Requirements (BA: smart-requirements, requirements-traceability)

#### 6.1 SMART Requirements

Each requirement MUST be:

| Criterion | How to Apply |
|-----------|--------------|
| **Specific** | One interpretation only |
| **Measurable** | Testable with pass/fail |
| **Achievable** | Technically possible |
| **Relevant** | Traces to user story |
| **Time-bound** | Has priority (MoSCoW) |

#### 6.2 Requirements Format

```markdown
### FR-001: Email Registration

**Requirement:** System SHALL allow users to register with email and password.

**Rationale:** Enables user identification for premium features.

**Traces to:** US-001

**Acceptance Criteria:** AC-001, AC-002

**Priority:** Must

**Validation Rules:**
- Email: valid format, unique in system
- Password: min 8 chars, 1 uppercase, 1 number
```

#### 6.3 MoSCoW Prioritization (PdM: mvp-scoping)

| Priority | Meaning | Example |
|----------|---------|---------|
| **Must** | MVP requirement, cannot launch without | Login, Core feature |
| **Should** | Important but not critical | Password reset |
| **Could** | Nice to have if time allows | Social login |
| **Won't** | Explicitly not in this release | SSO, 2FA |

### Phase 7: Non-Functional Requirements

#### 7.1 NFR Categories

| Category | What to Specify | Example |
|----------|-----------------|---------|
| **Performance** | Response times, throughput | < 500ms p95 latency |
| **Scalability** | Load capacity | 10k concurrent users |
| **Security** | Auth, encryption, compliance | bcrypt, HTTPS, GDPR |
| **Availability** | Uptime, recovery | 99.9% uptime, 4h RTO |
| **Accessibility** | WCAG level | WCAG 2.1 AA |
| **Usability** | UX metrics | < 3 clicks to complete |

#### 7.2 NFR Format

```markdown
### NFR-001: Login Performance

**Requirement:** Login response time SHALL be < 500ms for p95.

**Measurement:** Server-side response time, excluding network.

**Priority:** Must

**Validation:** Load test with 1000 concurrent users.
```

### Phase 8: Acceptance Criteria (BA: acceptance-criteria)

#### 8.1 Given-When-Then Format (BDD)

```markdown
### AC-001: Successful Registration

**Scenario:** User registers with valid credentials

**Given:** User is on registration page
**And:** User has valid email not in system
**When:** User enters email "test@example.com" and password "SecurePass1"
**And:** User clicks "Register" button
**Then:** Account is created in database
**And:** User receives verification email within 30 seconds
**And:** User is redirected to dashboard
**And:** Success message "Check your email" is displayed
```

#### 8.2 Coverage Checklist

- [x] Happy path (main success scenario)
- [x] Error handling (validation failures)
- [ ] Boundary conditions (min/max values)
- [ ] Security scenarios (injection, auth bypass)
- [ ] Performance scenarios (load, timeout)
- [ ] Accessibility (screen reader, keyboard)

### Phase 9: Scope Definition (PM: scope-management)

#### 9.1 In Scope

Explicitly list what IS included:
```markdown
## In Scope

- Email/password registration
- Email/password login
- Session management (7-day cookie)
- Password reset via email
- Basic profile (name, avatar)
```

#### 9.2 Out of Scope

Explicitly list what is NOT included:
```markdown
## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| Social login (Google, GitHub) | Not MVP | Phase 2 |
| Two-factor authentication | Complexity | Phase 3 |
| SSO/SAML | Enterprise only | Not planned |
| Biometric auth | Mobile-only | v2.0 |
```

---

## Templates

### Full Spec Template v2.0

```markdown
# Feature: [Feature Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Tech stack, standards |
| Related Feature | `features/done/{NN}-{feature}/spec.md` | Patterns to follow |

---

## Overview

[2-3 sentences describing the feature and its purpose]

---

## Problem Statement

**Who:** [User persona]
**Problem:** [What they cannot do]
**Impact:** [Business/user impact]
**Solution:** [High-level approach]
**Success Metric:** [How we measure success]

---

## User Personas

### Persona 1: [Name/Archetype]
- **Role:** [What they do]
- **Goal:** [What they want]
- **Pain Points:** [Current frustrations]
- **Context:** [When/where they use product]

---

## User Stories

### US-001: [Story Title]
**As a** [persona]
**I want to** [action]
**So that** [benefit]

**Priority:** Must | Should | Could
**Estimate:** [story points or T-shirt size]
**Acceptance Criteria:** AC-001

### US-002: [Story Title]
...

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL [requirement] | US-001 | Must |
| FR-002 | System SHALL [requirement] | US-001 | Must |
| FR-003 | System SHOULD [requirement] | US-002 | Should |

### FR-001: [Requirement Title]

**Requirement:** System SHALL [specific, testable requirement].

**Rationale:** [Why this is needed]

**Traces to:** US-001

**Validation Rules:**
- [Rule 1]
- [Rule 2]

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Response time | < 500ms p95 | Must |
| NFR-002 | Security | Password storage | bcrypt 12 rounds | Must |
| NFR-003 | Scalability | Concurrent users | 10,000 | Should |

---

## Acceptance Criteria

### AC-001: [Scenario Title - Happy Path]

**Scenario:** [Brief description]

**Given:** [precondition]
**And:** [additional precondition]
**When:** [action]
**Then:** [expected result]
**And:** [additional result]

### AC-002: [Scenario Title - Error Case]
...

### AC-003: [Scenario Title - Edge Case]
...

**Coverage:**
- [x] Happy path
- [x] Error handling
- [ ] Boundary conditions
- [ ] Security scenarios
- [ ] Performance scenarios

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| [Feature] | [Why excluded] | [Future phase or Never] |

---

## Assumptions & Constraints

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Constraints
- [Technical constraint]
- [Business constraint]

---

## Dependencies

### Internal
- [Other feature this depends on]

### External
- [Third-party service]
- [Library requirement]

---

## Related Features

| Feature | Relationship | Status |
|---------|-------------|--------|
| [NN-feature] | Depends on | Done |
| [NN-feature] | Blocks | Todo |

---

## Recommended Skills & Methodologies

### Skills
| Skill | Purpose |
|-------|---------|
| faion-software-developer | Implementation |
| faion-ux-ui-designer | UI components |

### Methodologies
| ID | Name | Purpose |
|----|------|---------|
| M-DEV-XXX | [Name] | [How it helps] |

---

## Open Questions

- [ ] [Question to resolve before design]

---

## Appendix

### Wireframes
[Link or embed]

### Data Models (if known)
[Preliminary models]

### API Contracts (if known)
[Preliminary contracts]
```

---

## Quality Checklist

### Spec Quality Gate (Before Design Phase)

**Completeness:**
- [ ] Problem statement is clear (SMART)
- [ ] All user personas defined
- [ ] All user stories have INVEST criteria
- [ ] All FR-X have SMART criteria
- [ ] All FR-X trace to user stories
- [ ] NFRs cover performance, security, scalability
- [ ] All acceptance criteria in Given-When-Then

**Clarity:**
- [ ] Each requirement has ONE interpretation
- [ ] No ambiguous words (good, fast, easy, etc.)
- [ ] Technical terms defined or linked
- [ ] All acceptance criteria are testable

**Consistency:**
- [ ] Requirement IDs are unique
- [ ] No conflicting requirements
- [ ] MoSCoW priorities assigned
- [ ] Traceability matrix complete

**Context:**
- [ ] Constitution referenced
- [ ] Related features identified
- [ ] Skills/methodologies recommended
- [ ] Out of scope explicitly defined

---

## Examples

### Example: Authentication Spec (Condensed)

```markdown
# Feature: User Authentication

**Version:** 1.0
**Status:** Approved
**Project:** cashflow-planner

---

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | `.aidocs/constitution.md` |

---

## Problem Statement

**Who:** New users of the cashflow planning app
**Problem:** Cannot access personal financial data because there's no authentication
**Impact:** Users cannot save cashflow projections, blocking core value proposition
**Solution:** Email-based authentication with JWT
**Success Metric:** 1000 registered users in first month

---

## User Stories

### US-001: Email Registration (MVP)
**As a** financial planner
**I want to** create an account with my email
**So that** I can save and access my cashflow projections

**Priority:** Must
**Acceptance Criteria:** AC-001, AC-002

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL allow registration with email + password | US-001 | Must |
| FR-002 | System SHALL validate email format (RFC 5322) | US-001 | Must |
| FR-003 | System SHALL require password min 8 chars, 1 upper, 1 number | US-001 | Must |

---

## Acceptance Criteria

### AC-001: Successful Registration
**Given:** User is on registration page
**When:** User enters valid email and valid password
**Then:** Account is created
**And:** User receives verification email within 30 seconds
**And:** User is redirected to dashboard

### AC-002: Registration with Existing Email
**Given:** Email "test@example.com" exists in system
**When:** User tries to register with "test@example.com"
**Then:** Error message "Email already registered" is displayed
**And:** No duplicate account is created

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| Social login | Not MVP | Phase 2 |
| 2FA | Complexity | Phase 3 |
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "System should be fast" | SMART: "Response time < 500ms p95" |
| No user personas | Define at least 2 personas |
| User stories without benefits | Always include "so that [benefit]" |
| Requirements without IDs | Always use FR-X, NFR-X format |
| No traceability | Every FR must trace to a user story |
| AC not testable | Use Given-When-Then with specific values |
| Missing out-of-scope | Explicitly list what you're NOT building |
| No related features | Check features/done/ for patterns |

---

## Related Methodologies

- **sdd-workflow-overview:** SDD Workflow Overview
- **writing-design-documents:** Writing Design Documents
- **smart-requirements:** SMART Requirements
- **use-case-modeling:** Use Case Modeling
- **user-story-mapping:** User Story Mapping
- **acceptance-criteria:** Acceptance Criteria
- **mvp-scoping:** MVP Scoping
- **user-story-mapping:** User Story Mapping
- **spec-writing:** PRD Writing
- **user-research:** User Research
- **persona-development:** Persona Development

---

## Agent

**faion-spec-reviewer-agent** reviews and improves specifications. Invoke with:
- "Review this spec for completeness"
- "Help me write user stories for [feature]"
- "Generate acceptance criteria for FR-001"
- "Check SMART/INVEST criteria"

---

*Methodology | SDD Foundation | Version 2.0.0*
*Integrates BA, PM, PdM, UX best practices*
