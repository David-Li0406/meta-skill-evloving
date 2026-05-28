# Game Design Document (GDD) Template

## Introduction
This template is designed for an AI-driven game development team with two human roles: `Producer` and `Prompt Engineer`, and multiple AI agents (e.g., `Muse`, `Build`, `Patch`, `Pixel`, `Probe`, `Scribbler`, `Ship`).

It is written to be filled in collaboratively:
- The **Producer** is accountable for product decisions and final sign-off.
- The **Prompt Engineer** ensures prompts/templates are precise, repeatable, and auditable.
- AI agents **draft**, **iterate**, and **propose**; the Producer approves.

Use this as a living document: update it when the design changes, and link changes to the relevant `bd` issues/PRs.

---

## How to use this template
- **Fill the “Decisions” fields first**, then let AI agents propose options for everything else.
- Keep sections short and testable. Prefer measurable statements over prose.
- For every important change, add:
  - a `bd` comment summarizing the decision
  - the PR URL (if applicable)

**AI Delegation guidance**
- `Build` (Product Manager): creates/maintains an implementation plan (tracking issues + dependency graph).
- `Muse` (Designer): proposes mechanics, loops, balance, and variants.
- `Patch` (Implementation): prototypes systems and integration.
- `Pixel` (Art): proposes style + assets.
- `Probe` (QA): automated tests + telemetry/regression summaries.
- `Scribbler` (Docs): keeps this GDD and related docs aligned.
- `Ship` (DevOps): CI/build/release pipeline.

---

## 1. Feature / Game Summary

### 1.1 One-liner
**Decision (Producer):**
- <one sentence pitch>

**AI draft (Muse):**
- Provide 5 alternative pitches optimized for clarity and player fantasy.

### 1.2 Goals
**Decision (Producer):**
- Primary goal: <…>
- Secondary goals: <…>

**AI draft (Build + Muse):**
- Translate goals into milestone outcomes and player-visible behaviors.

### 1.3 Non-goals
**Decision (Producer):**
- <explicitly out of scope>

---

## 2. Player & Market

### 2.1 Target player
**Decision (Producer):**
- Audience: <…>
- Platform(s): <…>
- Session length: <…>
- Input device: <…>

**AI draft (Muse):**
- Provide 2–3 personas and their motivations.

### 2.2 Comparable games / inspirations
**AI draft (Muse):**
- List 3–7 references and what we borrow/avoid.

---

## 3. Vision & Pillars

### 3.1 Design pillars (3–5)
**Decision (Producer):**
- Pillar 1: <…>
- Pillar 2: <…>
- Pillar 3: <…>

**AI draft (Muse):**
- Provide pillar candidates and “pillar tests” (how we know we’re honoring them).

### 3.2 Success criteria (measurable)
**Decision (Producer):**
- <criteria with numbers/timeframes when possible>

**AI draft (Build + Probe):**
- Convert into measurable metrics and test plans.

---

## 4. Core Game Loop

### 4.1 Core loop
Describe the primary repeatable loop in 4–8 steps.

**Decision (Producer):**
1) <…>
2) <…>
3) <…>

**AI draft (Muse):**
- Provide 2–3 loop variants with tradeoffs.

### 4.2 Secondary loops
**AI draft (Muse):**
- Identify progression/meta/social/collection loops.

---

## 5. Mechanics & Systems

### 5.1 Controls & moment-to-moment play
**Decision (Producer):**
- Controls: <…>
- Fail state: <…>
- Win state: <…>

**AI draft (Muse):**
- Propose control schemes and accessibility considerations.

### 5.2 Systems list
Provide a list of major systems and the status of each.

| System | Purpose | Status (idea/prototype/implemented) | Owner agent |
|--------|---------|--------------------------------------|------------|
| <…>    | <…>     | <…>                                  | <Muse/Patch/etc> |

**AI draft (Build):**
- Break systems into tracking issues; add dependencies.

### 5.3 Tuning knobs
**Decision (Producer):**
- What parameters are intentionally tunable? <…>

**AI draft (Muse + Probe):**
- Recommend tunables and safe ranges; propose automated regression checks.

---

## 6. Progression & Economy (if applicable)

### 6.1 Progression model
**Decision (Producer):**
- <levels/chapters/unlocks>

**AI draft (Muse):**
- Propose a progression curve and pacing assumptions.

### 6.2 Economy
**Decision (Producer):**
- Currencies/resources: <…>
- Sources/sinks: <…>

**AI draft (Muse + Build):**
- Identify risks (grind, inflation) and mitigation.

---

## 7. Content

### 7.1 Content types
**Decision (Producer):**
- <levels, enemies, items, quests, etc>

**AI draft (Muse + Pixel):**
- Suggest a content list and a production cadence.

### 7.2 Content pipeline
**Decision (Producer):**
- How is content created, validated, and shipped?

**AI draft (Build + Ship + Scribbler):**
- Propose a pipeline with quality gates and documentation hooks.

---

## 8. Art & Audio

### 8.1 Art direction
**Decision (Producer):**
- Style: <…>
- Constraints: <…>

**AI draft (Pixel):**
- Provide moodboard keywords, palette guidance (no hard-coded colors here), and asset list.

### 8.2 Audio direction
**Decision (Producer):**
- Music: <…>
- SFX: <…>

**AI draft (Muse):**
- Suggest audio cues per major event.

---

## 9. UX & UI

### 9.1 Key screens
**Decision (Producer):**
- Screens: <…>

**AI draft (Muse + Scribbler):**
- Draft user journeys and UX risks.

### 9.2 Accessibility
**Decision (Producer):**
- Accessibility requirements: <…>

---

## 10. Telemetry & QA

### 10.1 Telemetry
**Decision (Producer):**
- What events do we track and why?

**AI draft (Probe):**
- Propose event schema, dashboards, and alerting thresholds.

### 10.2 Automated testing (AI QA Agent)
**Decision (Producer):**
- Required automated checks: <…>

**AI draft (Probe):**
- Propose tests (unit/integration/smoke), plus regression scenarios.

### 10.3 Human playtesting (Producer)
**Decision (Producer):**
- Playtest plan: who/when/what we learn

**AI draft (Muse + Scribbler):**
- Provide playtest script and survey questions.

---

## 11. Technical Constraints & Integration

### 11.1 Constraints
**Decision (Producer):**
- Performance targets: <…>
- Platform constraints: <…>
- Dependencies: <…>

**AI draft (Patch + Ship):**
- Identify key risks and propose mitigations.

### 11.2 Architecture notes (optional)
**AI draft (Patch):**
- Sketch major modules and responsibilities.

---

## 12. Implementation Plan (bd tracking)

**Decision (Producer):**
- What is the delivery milestone for this feature/game?

**AI draft (Build):**
- Create the implementation plan as `bd` issues and dependencies.
- Ensure each issue has: description, acceptance criteria, owner agent, and links back to this GDD.

**Template fields**
- Epic / parent issue: <bd-id>
- Tracking issues:
  - <bd-id> — <title>
  - <bd-id> — <title>
- Dependency notes:
  - <bd-id> blocks <bd-id>

---

## 13. Risks, Decisions, Open Questions

### 13.1 Risks
| Risk | Impact | Likelihood | Mitigation | Owner |
|------|--------|------------|------------|-------|
| <…>  | <…>    | <…>        | <…>        | <Build/Muse/Patch/etc> |

### 13.2 Decisions log
| Date | Decision | Rationale | Link (bd/PR) |
|------|----------|-----------|--------------|
| <…>  | <…>      | <…>       | <…>          |

### 13.3 Open questions
- <…>

---

## 14. Acceptance Criteria
List concrete criteria for “done”.

**Decision (Producer):**
- [ ] <…>
- [ ] <…>

**AI draft (Probe + Scribbler):**
- Propose acceptance checks and how they’re verified.

---

## 15. Links
- bd epic/issue: <…>
- PR(s): <…>
- Related docs (Design, Implementation plan, Workflow, Team): <…>
