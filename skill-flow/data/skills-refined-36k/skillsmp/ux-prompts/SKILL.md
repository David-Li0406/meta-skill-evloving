---
name: ux-prompts
description: This skill should be used when the user asks to "generate build prompts", "create implementation prompts", "break down the UX spec", "prepare prompts for v0/Bolt/Claude", "sequence the build tasks", or needs to transform UX specifications into sequential, self-contained prompts for UI generation tools.
---

# UX Spec to Build-Order Prompts

Transform detailed UX specifications into a sequence of self-contained prompts optimized for UI generation tools. Each prompt builds one discrete feature with full context included.

## When to Use

- User has a UX spec, PRD, or detailed feature documentation
- Output needs to feed into UI generation tools (v0, Bolt, Claude, etc.)
- User wants build-order sequencing (foundations → features → polish)
- Large specs that would overwhelm a single prompt

**Not for:** Quick component requests, already-atomic features, specs that fit in one prompt.

## Build Order Strategy

Generate prompts in this sequence:

| Phase | Contents | Why First |
|-------|----------|-----------|
| **1. Foundation** | Design tokens, shared types, base styles | Everything depends on these |
| **2. Layout Shell** | Page structure, navigation, panels | Container for all features |
| **3. Core Components** | Primary UI elements (cards, inputs, buttons) | Building blocks |
| **4. Interactions** | Drag-drop, selections, pickers | Depend on components |
| **5. States & Feedback** | Empty, loading, error, success states | Refinement layer |
| **6. Polish** | Animations, responsive, edge cases | Final layer |

## Extraction Process

### Step 1: Identify Atomic Units
List discrete buildable features:
- Each screen/view
- Each reusable component
- Each interaction pattern
- Each state variation

### Step 2: Map Dependencies
For each unit, note what it requires:
- "Cart drawer requires Cart Item component"
- "Checkout flow requires Address form"

### Step 3: Sequence by Dependencies
Order units so dependencies come first. Group tightly-coupled items into single prompts.

### Step 4: Write Self-Contained Prompts
For each prompt:
1. Re-state relevant context (no references to other prompts)
2. Include specific measurements from spec
3. Include all states
4. Include all interactions
5. Set explicit boundaries (what's excluded)

## Self-Containment Rules

Each prompt MUST include:
- Enough context to understand the feature in isolation
- All visual specs (colors, spacing, dimensions)
- All states that feature can have
- All interactions for that feature

Each prompt MUST NOT:
- Reference "see previous prompt" or "as described earlier"
- Assume knowledge from other prompts
- Leave specs vague ("appropriate styling")

## Prompt Structure Template

```markdown
## [Feature Name]

### Context
[What this is and where it fits in the app]

### Requirements
- [Specific dimensions, colors, spacing]
- [Layout structure]
- [Content elements]

### States
- Default: [description]
- Hover: [description]
- Loading: [description]
- Error: [description]
- [Other states]

### Interactions
- [Click behavior]
- [Hover behavior]
- [Keyboard support]

### Constraints
- This prompt includes: [list]
- This prompt does NOT include: [list]

### Verification
- [ ] [Testable criterion]
- [ ] [Testable criterion]
```

## Output Format

```markdown
# Build-Order Prompts: [Project Name]

## Overview
[1-2 sentence summary]

## Build Sequence
1. [Prompt name] - [brief description]
2. [Prompt name] - [brief description]
...

---

## Prompt 1: [Feature Name]
[Full self-contained prompt]

---

## Prompt 2: [Feature Name]
[Full self-contained prompt]
```

## Output Location

Write prompts to same directory as source UX spec:
- UX spec `feature-x-ux-spec.md` → output `feature-x-prompts.md`
- For sprint-based output: `sprints/sprint-1-foundation.md`, `sprints/sprint-2-components.md`

---

## Additional Resources

### Reference Files

For prompt quality and verification:
- **`references/quality-amplifiers.md`** — Specificity ladder, context density, extraction patterns
- **`references/verification-templates.md`** — Per-type verification checklists
- **`references/anti-patterns.md`** — Common mistakes and fixes

### Example Files

Working examples in `examples/`:
- **`component-prompt.md`** — Complete component prompt (Product Card)
- **`flow-prompt.md`** — Complete page/flow prompt (Checkout Flow)

---

## Quick Reference

### Quality Checklist

- [ ] Every measurement from spec captured
- [ ] Every state from spec captured
- [ ] Every interaction from spec captured
- [ ] No prompt references another prompt
- [ ] Build order respects dependencies
- [ ] Each prompt executable with zero context

### Specificity Ladder

| Level | Example |
|-------|---------|
| Vague | "Use appropriate spacing" |
| Better | "Use consistent spacing" |
| Good | "8px padding, 16px gap" |
| Excellent | "8px padding (var(--space-2)), 16px gap, matching card pattern" |

### Sprint Batching

| Risk | Prompt Types | Ship After |
|------|--------------|------------|
| Low | Tokens, types, utilities | Immediately |
| Medium | Components, animations | Unit tests |
| High | Checkout, auth, payments | E2E tests |

### Verification Footer by Type

| Type | Key Checks |
|------|------------|
| Component | Types, states, keyboard, dark mode |
| Page | E2E happy path, error states, responsive |
| Animation | 60fps, reduced motion, no blocking |
| Form | Validation, labels, autofill |
