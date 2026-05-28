---
name: mvp-prd
description: This skill should be used when the user asks to "create a PRD", "write requirements", "define an MVP", "spec out a feature", "plan a demo", "document product requirements", or needs to turn a rough idea into a structured product requirements document. Converts vague ideas into demo-grade PRDs with decision clarity.
---

# MVP to Demo PRD Generator

Transform rough MVP ideas into clear, demo-grade Product Requirements Documents. Optimize for decision clarity, not enterprise ceremony.

## Input Expectations

Accept from user:
- Rough MVP or demo descriptions
- Vague, incomplete, or "vibe-level" ideas
- Feature requests without context

Handling ambiguity:
- Infer missing details with reasonable assumptions
- Label all assumptions explicitly
- Avoid overengineering
- Optimize for believable demo, not production scale
- Ask maximum one clarifying question, then proceed

## Output Structure (7 Sections)

Generate a Demo Project PRD with exactly these sections:

### 1. One-Sentence Problem

Format:
> [User] struggles to [do X] because [reason], resulting in [impact].

Pick the single most demo-worthy problem if multiple exist.

### 2. Demo Goal (What Success Looks Like)

Include:
- What must work for demo success
- What outcome the demo should communicate
- Non-Goals (what is intentionally out of scope)

### 3. Target User (Role-Based)

Define one primary user role:
- Role / context
- Skill level
- Key constraint (time, knowledge, access)

Avoid personas or demographics.

### 4. Core Use Case (Happy Path)

Describe the single most important end-to-end flow:
- Start condition
- Step-by-step flow (numbered)
- End condition

If this flow works, the demo works.

### 5. Functional Decisions (What It Must Do)

Table format:

| ID | Function | Notes |
|----|----------|-------|

Rules:
- Phrase as capabilities, not implementation
- No "nice-to-haves"
- Keep the list tight

### 6. UX Decisions (What the Experience Is Like)

#### 6.1 Entry Point
How the user starts; what they see first.

#### 6.2 Inputs
What the user provides (if anything).

#### 6.3 Outputs
What the user receives and in what form.

#### 6.4 Feedback & States
How the system communicates: loading, success, failure, partial results.

#### 6.5 Errors (Minimum Viable Handling)
What happens when: input is invalid, system fails, user does nothing.

### 7. Data & Logic (At a Glance)

#### 7.1 Inputs
Where data comes from: user, API, static/mocked, generated.

#### 7.2 Processing
High-level logic only. Example: Input → transform → output.

#### 7.3 Outputs
Where results go: UI only, temporarily stored, logged.

## Content Guidelines

Include:
- Sharp, builder-friendly language
- Explicit assumptions with labels
- Decision rationale when non-obvious

Exclude:
- Architecture diagrams
- Tech stack decisions
- Pricing, monetization, GTM
- Long explanations
- Implementation details

## Output Location

Write PRD to a location the user specifies or use a sensible default:
- Example: `docs/prd.md` or `docs/features/feature-name.md`
- Clarification session: `docs/prd-clarification-session.md`

Ask user for preferred location if unclear.

## Completion Criteria

PRD is done when a builder could:
- Read it and build a demo without guessing
- Explain the product clearly to someone else
- Identify what's in scope vs out of scope

## Post-Generation

After generating sections 1-7, invoke the `prd-clarify` skill to refine requirements through structured questioning.

---

## Additional Resources

### Reference Files

For detailed planning and scope management:
- **`references/sprint-planning.md`** — Risk-based batching, prioritization, sprint sequencing
- **`references/scope-management.md`** — Creep prevention, expansion protocols, scope lock

### Example Files

Working examples in `examples/`:
- **`sample-prd.md`** — Complete PRD following the 7-section structure

---

## Quick Reference

### Risk Classification

| Risk Level | Examples | Ship Gate |
|------------|----------|-----------|
| Low | Types, configs, docs | Immediately |
| Medium | UI, styling, animations | Unit tests pass |
| High | Auth, payments, mutations | E2E tests pass |

### Priority Order

Bugs > Breaking Changes > Consistency > Polish > Performance

### Scope Expansion Protocol

| Expansion Size | Action |
|----------------|--------|
| Minor (<20%) | Add to current sprint |
| Moderate (20-50%) | Split to follow-up sprint |
| Major (>50%) | Pause, re-clarify, replan |

$ARGUMENTS
