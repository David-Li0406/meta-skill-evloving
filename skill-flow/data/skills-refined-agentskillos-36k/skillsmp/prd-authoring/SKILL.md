---
name: prd-authoring  
description: Generates a research-grade Product Requirements Document (PRD) defining problems, goals, scope, constraints, and success criteria. Use when creating or updating a PRD for a product or major initiative.  
metadata:  
  title: PRD Authoring Skill  
  tags: prd,product-requirements,documentation,research  
---

# Product Requirements Document (PRD) Authoring

## What is it?

This skill generates a high-quality Product Requirements Document (PRD) that establishes shared understanding across product, engineering, and leadership.

It emphasizes problem clarity, reasoning, and trade-offs, not feature lists or implementation details.

---

## Why Use It?

A well-authored PRD prevents costly misalignment and rework by establishing shared understanding upfront. Without clarity on problems, goals, and constraints, teams diverge—engineers build the wrong thing, leadership questions decisions, and products miss their mark.

This skill delivers:

- Alignment across disciplines: Product, engineering, and leadership speak the same language
- De-risked decision-making: Trade-offs and constraints are explicit, not hidden
- Reduced iteration cycles: Clear scope prevents "scope creep" and mid-project pivots
- Measurable outcomes: Success criteria anchor the work to business and user value
- Institutional knowledge: The reasoning behind the product remains documented for future reference

---

## When to Use This Skill

Use this skill when you need to:

- Define a new product or major initiative
- Reframe or correct an existing PRD
- Establish alignment before roadmap or feature planning
- Translate ambiguous ideas into a clear product definition

Do not use this skill for:

- feature-level specifications
- roadmap sequencing
- UI or UX design
- implementation planning

---

## How to Use It?

### Preparation Phase

1. Gather context: Collect existing research, user interviews, market data, or strategic direction
2. Identify stakeholders: Know who will review and be impacted by the PRD
3. Define constraints: Understand timeline, budget, technical debt, or organizational constraints upfront

### Authoring Phase

1. Start with the problem: Write out the user problem clearly before considering solutions
2. Reason through analytical dimensions: Work through each dimension systematically (see [Analytical Dimensions](#analytical-dimensions) below).
3. Make trade-offs explicit: Document what you're choosing and why—especially what you're not doing
4. Reference the template: Use `assets/prd.template.md` as your structural guide
5. Use visuals for complexity: Add Mermaid diagrams for workflows, user journeys, or system interactions that benefit from visual representation

### Review Phase

1. Share for feedback: Get input from product, engineering, and leadership early
2. Verify alignment: Ensure everyone has the same understanding of the problem and approach
3. Document decisions: Capture the reasoning behind major choices for future reference

### Output

Deliver a clean, neutral Markdown document suitable for long-term reference and artifact storage. The PRD is complete when stakeholders confirm shared understanding of the problem, goals, scope, and success criteria.

---

## Core Principles

When authoring a PRD, always prioritize:

1. User problems over solutions
2. Explicit assumptions
3. Clear goals and non-goals
4. Early acknowledgment of constraints
5. Measurable success criteria
6. Visual clarity (Use Mermaid diagrams for complex flows)

---

## Examples

PRDs vary significantly based on scope type. Here are three common patterns:

### Example 1: Product PRD (New Product Launch)

Problem: Teams disagree on which user segment to target first.  
What NOT to write: "Build a mobile app with social features and analytics."  
What TO write: "Freelance designers aged 25–40 struggle to showcase work across platforms. Success = 500 active users sharing portfolios within 90 days."  
Critical trade-off: Launch with portfolio-only features; defer social networking to v2 to reduce scope and risk.

### Example 2: Feature PRD (Addition to Existing Product)

Problem: Users request better search, but engineering has limited capacity.  
What NOT to write: "Add advanced filters and sorting options."  
What TO write: "Current search returns unranked results, forcing users to manually filter 50+ items. Goal: reduce search time from 5 min to 1 min. Success = 80% of searches complete within 10 clicks."  
Critical constraint: Use existing database; no new infrastructure. This narrows implementation options and scope significantly.

### Example 3: Platform PRD (Infrastructure/Enabling Tech)

Problem: Success is indirect; hard to measure impact on downstream products.  
What NOT to write: "Build an API layer for internal services."  
What TO write: "Slow API responses (avg 2s) block three product teams from shipping features. Goal: reduce latency to <500ms, enabling 5 new features across platforms within Q2."  
Success metric: Not adoption count, but product velocity unlocked—track how many downstream features shipped or launched faster.

---

## Observations & Learnings

Documented insights from implementations that enable 100× faster future repetitions:

### Common Mistakes & Fixes

- Mistake: Starting with solutions instead of problems → Fix: Always write the user problem statement first, then validate with stakeholders. This prevents building the wrong thing and saves 3-5 rounds of feedback.
- Mistake: Vague success criteria → Fix: Use measurable metrics (e.g., "reduce search time from 5 min to 1 min" not "improve performance"). Vague criteria lead to unclear validation and scope debates.
- Mistake: Missing trade-off documentation → Fix: Explicitly state what you're NOT doing and why. Hidden assumptions cause mid-project pivots when stakeholders discover "missing" features.
- Mistake: Skipping stakeholder alignment on constraints → Fix: Get leadership buy-in on timeline, budget, and technical constraints upfront. Unaligned expectations cause project delays and rework.

### Speed Accelerators

- Problem-first template: Use the examples above to avoid solution bias. Start every PRD with "Users struggle with X because Y" to focus on real needs.
- Reference existing PRDs: For similar features, inherit proven patterns from past documents. This reduces planning time by 60-80%.
- Constraint-first scoping: Define what's impossible or too expensive before detailing what's possible. This prevents over-scoping and maintains project velocity.
- Early cross-functional review: Share the problem statement and constraints with product, engineering, and leadership before detailed requirements. This catches misalignment early.

### Troubleshooting Patterns

- If stakeholders keep suggesting solutions: Redirect to "What problem would this solve?" to maintain problem focus.
- If success criteria feel abstract: Make them observable behaviors (e.g., "80% of users complete task in <10 clicks" vs "users are satisfied").
- If scope keeps expanding: Audit non-goals and ask "What would we remove if we had 30% less time?"
- If engineering pushback occurs: Check if constraints are clearly documented and trade-offs are explicit.

---

## Analytical Dimensions

Before writing the PRD, reason through:

- user context and motivation
- problem framing and urgency
- goals vs non-goals
- functional scope boundaries
- constraints and trade-offs
- risks and failure modes

These dimensions must be reflected in the final document.

---

## Output Structure

Unless otherwise specified, the PRD should follow the canonical structure defined in:

- `assets/prd.template.md`

Sections may be expanded or collapsed as appropriate, but the reasoning integrity must be preserved.

---

## Important Boundaries

This skill must not:

- ask clarification questions
- plan next workflow steps
- create tasks or tickets
- specify UI, UX, or technical architecture
- interact with users

All orchestration decisions belong to the calling agent.

---

## Output Expectations

The output should be:

- clean Markdown (ensure one blank line after every header)
- directly usable as a PRD artifact
- neutral and analytical in tone
- suitable for product, engineering, and leadership review
