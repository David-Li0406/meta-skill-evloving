---
name: design-suite:launchpad-init
description: Build distinctive landing pages with craft and boldness. For marketing pages — not dashboards or multi-page apps.
---

## Required Reading — Do This First

Before writing any code, read the launchpad SKILL.md completely — the foundation, principles, and checks.

Do not skip this. The craft knowledge is in that file.

---

**Scope:** Landing pages, promotional sites, waitlist pages, product launches. Not dashboards or multi-page apps — use `/design-suite:workbench-init` for those.

## Stack

**React** — Component-based, flat composition for linear page flow.

**Tailwind CSS** — Utility-first, pure Tailwind (no external CSS).

**Framer Motion** (optional) — For scroll-triggered animations.

---

## Intent First — Answer Before Building

Before touching code, answer these out loud:

**What is the ONE action?** Not "explore." The verb. Sign up. Download. Buy. Join the waitlist. If you can't name it, stop.

**Who lands here?** Not "visitors." The actual person. Where did they come from? What's their skepticism? What's their desire?

**What must they feel?** Not "interested." The emotion. Urgency? Curiosity? Trust? FOMO? Excitement?

**What makes this unforgettable?** Not "good design." The moment. What will they remember tomorrow?

If you cannot answer these with specifics, stop and ask the user. Do not guess. Do not default.

---

## Before Writing Each Section

State the intent AND the technical approach:

```
Intent: [the ONE action, who lands here, what they must feel]
Brand world: [5+ concepts from this brand's territory]
Color world: [5+ colors that feel native to this brand]
Signature: [the one unforgettable element]
Rejecting: [3 defaults and what replaces them]

Direction: [approach that connects to the above]
```

Every choice must be explainable. If your answer is "it converts well" or "it's clean" — you haven't chosen. You've defaulted.

**The test:** If another AI given a similar prompt would produce the same output, you have failed.

---

## Communication

Be invisible. Don't announce modes or narrate process.

**Never say:** "Let me design a hero section...", "I'll add some social proof..."

**Instead:** Jump into work. Present the thinking, then the result.

---

## Suggest + Ask

Lead with your exploration and recommendation, then confirm:
```
"Brand world: [concepts from this brand's territory]
Color world: [colors that feel native]
Signature: [the unforgettable element]
Rejecting: [default] → [alternative], [default] → [alternative]

Direction: [approach that connects to the above]"

[AskUserQuestion: "Does that direction feel right?"]
```

---

## Flow

1. Read the launchpad SKILL.md (always — even if system.md exists)
2. Check if `.launchpad/system.md` exists
3. **If exists**: Apply established patterns from system.md
4. **If not**: Offer options:
   - Start fresh with brand exploration
   - Use a template as starting point (see `templates/` folder)
5. **Ask about optional stack** (for relevant project types):
   - Portfolio, product showcase, creative/agency, tech/gaming → Ask about Three.js
6. Assess brand, suggest direction, get confirmation, build
7. **Evaluate** — Run the mandate checks before showing
8. Offer to save

---

## Stack Options

After establishing direction, ask about optional stack components when relevant.

**For 3D/WebGL (ask on portfolios, product showcases, creative pages):**
```
"Does this project call for 3D elements, WebGL effects, or immersive visuals?"
```
→ If yes, include Three.js + React Three Fiber patterns
→ See `references/threejs-patterns.md` for implementation

**When to ask about Three.js:**
- Portfolio sites
- Product showcases with 3D viewer potential
- Creative/agency pages
- Tech/gaming landing pages

**When NOT to ask:**
- SaaS landing pages
- Waitlist/email capture pages
- Content-focused marketing pages

---

## The Checks

Before presenting, run these:

- **The generic test:** Could this page belong to any company in this space?
- **The scroll test:** Is there a reason to keep scrolling beyond "more content"?
- **The signature test:** Can you point to the one unforgettable element?
- **The feel test:** Does every section reinforce the stated emotion?
- **The action test:** Is the ONE action unmistakably clear?

If any check fails, iterate before showing.

---

## Avoid

- Purple-to-blue gradients — clearest sign of AI-generated
- Floating blobs and abstract shapes
- Inter/Roboto for headlines — no personality
- Centered everything — creates monotony
- Feature grids with generic icons
- Multiple competing CTAs
- Logo walls without context
- Stock illustrations
- Same section rhythm — predictable is forgettable

---

## After Every Task

Offer to save when you finish building:

"Want me to save these patterns to `.launchpad/system.md`?"

Include in system.md:
- Brand direction and personality
- Color palette (CSS variables)
- Typography choices
- The signature element
- Key component patterns
- Animation approach

Always offer — new patterns should be captured whether system.md exists or not.
