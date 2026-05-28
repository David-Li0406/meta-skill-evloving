---
id: spec-writing
name: "Product Specification Writing"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Product Specification Writing

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #specification, #prd |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-spec-reviewer-agent |

---

## Problem

Product specs are either too vague or too prescriptive. Common issues:
- "Just make it work" (no guidance)
- 50-page documents nobody reads
- Mixing what and how
- No clear acceptance criteria

**The root cause:** No template that balances completeness with conciseness.

---

## Framework

### What is a Product Spec?

A product specification (PRD) defines WHAT to build and WHY, leaving HOW to the design/engineering process. It answers: "What problem are we solving and what does success look like?"

### Spec Components

| Section | Purpose | Length |
|---------|---------|--------|
| Overview | Context and summary | 1 paragraph |
| Problem | What we're solving | 1-2 paragraphs |
| Goals | Success metrics | 3-5 bullets |
| User Stories | Who and what | 3-10 stories |
| Requirements | What's needed | Detailed list |
| Non-Requirements | What's excluded | Explicit list |
| Open Questions | Unresolved issues | As needed |

### Spec Writing Process

#### Step 1: Understand the Context

**Before writing, answer:**
- Why are we building this?
- Who requested it?
- What happens if we don't build it?
- How does this fit the product strategy?

#### Step 2: Define the Problem

**Write clearly:**
- Who has this problem?
- What is the problem specifically?
- How do they solve it today?
- What's the impact?

#### Step 3: Set Goals and Non-Goals

**Goals (3-5):**
- What will success look like?
- How will we measure it?
- What outcomes matter?

**Non-Goals:**
- What are we NOT trying to do?
- What's explicitly out of scope?

#### Step 4: Write User Stories

**Template:**
```
As a [user type]
I want to [action]
So that [benefit]
```

**Tips:**
- Focus on user value
- Be specific about the user
- Include the "so that" (motivation)

#### Step 5: Detail Requirements

**Functional Requirements (FR):**
```
FR-1: The system shall [do X]
FR-2: The system shall [do Y]
```

**Non-Functional Requirements:**
- Performance
- Security
- Scalability
- Accessibility

#### Step 6: Define Acceptance Criteria

**For each major feature:**
```
Given [context]
When [action]
Then [expected result]
```

#### Step 7: Call Out Open Questions

List unresolved issues for discussion:
- Technical unknowns
- Business decisions pending
- User research gaps

---

## Templates

### Product Specification Template

```markdown
# [Feature Name] Specification

## Metadata
- **Author:** [Name]
- **Created:** [Date]
- **Status:** [Draft/Review/Approved]
- **Stakeholders:** [Names]

---

## Overview

[One paragraph summary: what are we building and why]

---

## Problem Statement

### Current Situation
[How things work today]

### Pain Points
1. [Pain 1]
2. [Pain 2]
3. [Pain 3]

### Impact
[What happens if we don't solve this]

---

## Goals

### Success Metrics
| Metric | Current | Target |
|--------|---------|--------|
| [Metric 1] | [X] | [Y] |
| [Metric 2] | [X] | [Y] |

### Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

### Non-Goals
- [Explicitly not X]
- [Explicitly not Y]

---

## User Stories

### Primary User: [Persona Name]

**US-1:** As a [user], I want to [action] so that [benefit].

**US-2:** As a [user], I want to [action] so that [benefit].

### Secondary User: [Persona Name]

**US-3:** As a [user], I want to [action] so that [benefit].

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | [Description] | Must |
| FR-2 | [Description] | Should |
| FR-3 | [Description] | Could |

### Non-Functional Requirements

| ID | Requirement | Criteria |
|----|-------------|----------|
| NFR-1 | Performance | [Specific metric] |
| NFR-2 | Security | [Specific requirement] |

---

## Acceptance Criteria

### [Feature 1]
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

### [Feature 2]
- [ ] Given [context], when [action], then [result]

---

## Out of Scope

| Item | Reason | Future? |
|------|--------|---------|
| [Feature] | [Why not included] | [Yes/No/Maybe] |

---

## Open Questions

| Question | Owner | Status |
|----------|-------|--------|
| [Question] | [Name] | Open |
| [Question] | [Name] | Resolved: [Answer] |

---

## Appendix

### Mockups/Wireframes
[Links or embedded images]

### Technical Notes
[Any relevant technical context]

### Related Documents
- [Link to design doc]
- [Link to research]
```

### Mini-Spec (Quick Features)

```markdown
# [Feature Name] Mini-Spec

**One-liner:** [What it does]
**Owner:** [Name]
**Target:** [Sprint/Date]

## Problem
[2-3 sentences]

## Solution
[2-3 sentences]

## Requirements
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

## Not Included
- [Explicit exclusion]

## Success Criteria
[How we know it works]
```

---

## Examples

### Example 1: Search Feature Spec

```markdown
# Product Search Specification

## Overview
Enable users to search products by keyword to find what they need quickly.

## Problem
Users browse through 500+ products manually. Average time to find: 3 minutes.
Support tickets: 20% are "can't find product."

## Goals
- Reduce time to find product from 3 min to 30 sec
- Reduce support tickets about finding products by 80%

## Non-Goals
- Advanced filters (separate feature)
- AI-powered recommendations
- Voice search

## User Stories
US-1: As a customer, I want to search by product name so I can find it quickly.
US-2: As a customer, I want to see search suggestions so I spell correctly.

## Requirements
- FR-1: Search bar visible on all pages (Must)
- FR-2: Results appear as user types (Must)
- FR-3: Show top 10 results with images (Should)
- FR-4: "No results" shows similar products (Could)

## Acceptance Criteria
- Given I'm on any page, I see a search bar
- When I type "chair", I see products with "chair" in title
- When I search with typo "chiar", I see "Did you mean: chair"
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mixing what and how | Spec = what; Design = how |
| No acceptance criteria | Every feature needs testable criteria |
| Missing non-goals | Explicitly state what's excluded |
| Too long | 1-3 pages for most features |
| No metrics | Define measurable success |
| Skipping open questions | Document unknowns |
| Writing alone | Collaborate with stakeholders |

---

## Related Methodologies

- **writing-specifications:** Writing Specifications
- **mvp-scoping:** MVP Scoping
- **use-case-mapping:** Use Case Mapping
- **requirements-elicitation:** Requirements Elicitation
- **requirements-documentation:** Requirements Documentation

---

## Agent

**faion-spec-reviewer-agent** helps with specifications. Invoke with:
- "Help me write a spec for [feature]"
- "Review my specification: [content]"
- "What's missing from this spec?"
- "Convert this idea into a spec: [description]"

---

*Methodology | Product | Version 1.0*
