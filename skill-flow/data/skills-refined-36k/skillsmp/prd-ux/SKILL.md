---
name: prd-ux
description: This skill should be used when the user asks to "create UX specs", "translate PRD to UX", "design user experience", "prepare for mockups", "create design handoff", or needs to transform product requirements into UX foundations. Uses 6 forced designer mindset passes before any visual specifications.
---

# PRD to UX Translation

Translate product requirements into UX foundations through **6 forced designer mindset passes**. Each pass asks questions that visual-first approaches skip.

**Core principle:** UX foundations come BEFORE visual specifications. Mental models, information architecture, and cognitive load analysis prevent "pretty but unusable" designs.

## The Iron Law

```
NO VISUAL SPECS UNTIL ALL 6 PASSES COMPLETE
```

**Not negotiable:**
- Don't mention colors, typography, or spacing until Pass 6 is done
- Don't describe screen layouts until information architecture is explicit
- Don't design components until affordances are mapped

**No exceptions for urgency:**
- "I'm in a hurry" → Passes take 5 minutes; fixing bad UX takes days
- "Just give me screens" → Screens without foundations need rework
- "Skip the analysis" → Analysis IS the value; screens are just output

## Output Location

Write UX spec to same directory as source PRD:
- PRD `feature-x.md` → output `feature-x-ux-spec.md`
- PRD `PRD.md` → output `UX-spec.md`

Always write to file for persistence and mockup tool handoff.

## The 6 Passes

Execute IN ORDER. Each pass produces required outputs before the next begins.

### Pass 1: User Intent & Mental Model

**Mindset:** "What does the user think is happening?"

**Force:**
- What does the user believe this system does?
- What are they trying to accomplish in one sentence?
- What wrong mental models are likely?

**Output:** Primary intent, likely misconceptions, UX principles to reinforce.

### Pass 2: Information Architecture

**Mindset:** "What exists, and how is it organized?"

**Force:**
1. Enumerate ALL concepts the user will encounter
2. Group into logical buckets
3. Classify each as: Primary / Secondary / Hidden

**Output:** Concept list, grouped structure, navigation hierarchy.

### Pass 3: Affordances & Action Clarity

**Mindset:** "What actions are obvious without explanation?"

**Force:**
- What is clickable?
- What looks editable?
- What looks like output (read-only)?
- What looks final vs in-progress?

**Output:** Action-signal mapping, affordance rules.

### Pass 4: Cognitive Load & Decision Minimization

**Mindset:** "Where will the user hesitate?"

**Identify:**
- Moments of choice (decisions required)
- Moments of uncertainty (unclear what to do)
- Moments of waiting (system processing)

**Apply:**
- Collapse decisions (fewer choices)
- Delay complexity (progressive disclosure)
- Introduce defaults (reduce decision burden)

**Output:** Friction points table, defaults list.

### Pass 5: State Design & Feedback

**Mindset:** "How does the system talk back?"

**For EACH major element, enumerate:**
- Empty
- Loading
- Success
- Partial
- Error

**For each state:** What does user see, understand, and can do?

**Output:** State matrix for each element/screen.

### Pass 6: Flow Integrity Check

**Mindset:** "Does this feel inevitable?"

**Check:**
- Where could users get lost?
- Where would a first-time user fail?
- What must be visible vs can be implied?

**Output:** Flow risks table, visibility decisions, UX constraints.

## THEN: Visual Specifications

Only after all 6 passes, create:
- Screen layouts
- Component specifications
- Design system
- Interaction specifications
- Responsive breakpoints

## Red Flags - STOP and Restart

| Violation | What You're Skipping |
|-----------|---------------------|
| Describing colors/fonts | All foundational passes |
| "The main screen shows..." | Pass 1-2 (mental model, IA) |
| Designing components before actions mapped | Pass 3 (affordances) |
| No friction point analysis | Pass 4 (cognitive load) |
| States only in component specs | Pass 5 (holistic state design) |
| No "where could they fail?" | Pass 6 (flow integrity) |

---

## Additional Resources

### Reference Files

For detailed techniques and patterns:
- **`references/pass-enhancements.md`** — Advanced techniques for each pass
- **`references/state-choreography.md`** — Transition design, feedback patterns
- **`references/affordance-patterns.md`** — Z-index, touch targets, component consolidation
- **`references/failure-modes.md`** — Error mapping, recovery paths

### Example Files

Working examples in `examples/`:
- **`complete-ux-spec.md`** — Full 6-pass example for a task manager

---

## Quick Reference

### Pass Output Summary

| Pass | Mindset | Key Output |
|------|---------|------------|
| 1 | What user thinks | Mental model, misconceptions |
| 2 | What exists | IA structure, navigation |
| 3 | What's obvious | Affordance mapping |
| 4 | Where hesitation | Friction points, defaults |
| 5 | How system responds | State matrices |
| 6 | Where they fail | Risk mitigation, constraints |

### State Design Quick Matrix

| State | User Sees | User Understands | User Can Do |
|-------|-----------|------------------|-------------|
| Empty | [Visual] | [Meaning] | [Actions] |
| Loading | [Visual] | [Meaning] | [Actions] |
| Success | [Visual] | [Meaning] | [Actions] |
| Partial | [Visual] | [Meaning] | [Actions] |
| Error | [Visual] | [Meaning] | [Actions] |

### Success Feedback Pattern

```
Action → Success indicator → Hold 300-500ms → Proceed
```
Users must SEE success before UI transitions.
