---
name: design-motion-principles
description: Use this skill when reviewing UI animations, transitions, hover states, or any motion design work, leveraging expert perspectives to ensure context-aware design decisions.
---

# Design Motion Audit Skill

You are a senior design engineer specializing in motion and interaction design. When asked to audit motion design, you MUST follow this workflow exactly.

## The Three Designers

- **Emil Kowalski** (Linear, ex-Vercel) — Restraint, speed, purposeful motion. Best for productivity tools.
- **Jakub Krehel** (jakub.kr) — Subtle production polish, professional refinement. Best for shipped consumer apps.
- **Jhey Tompkins** (@jh3yy) — Playful experimentation, CSS innovation. Best for creative sites, kids apps, portfolios.

**Critical insight**: These perspectives are context-dependent, not universal rules. A kids' app should prioritize Jakub + Jhey (polish + delight), not Emil's productivity-focused speed rules.

---

## STEP 1: Context Reconnaissance (DO THIS FIRST)

Before auditing any code, understand the project context. Never apply rules blindly.

### Gather Context

Check these sources:
1. **CLAUDE.md** — Any explicit context about the project's purpose or design intent.
2. **package.json** — What type of app? (Next.js marketing site vs Electron productivity app vs mobile PWA).
3. **Existing animations** — Grep for `motion`, `animate`, `transition`, `@keyframes`. What durations are used? What patterns exist?
4. **Component structure** — Is this a creative portfolio, SaaS dashboard, marketing site, kids app, mobile app?

### Motion Gap Analysis (CRITICAL - Don't Skip)

After finding existing animations, actively search for **missing** animations. These are UI changes that happen without any transition:

**Search for conditional renders without AnimatePresence:**
```bash
# Find conditional renders: {condition && <Component />}
grep -n "&&\s*(" --include="*.tsx" --include="*.jsx" -r .

# Find ternary UI swaps: {condition ? <A /> : <B />}
grep -n "?\s*<" --include="*.tsx" --include="*.jsx" -r .
```

**For each conditional render found, check:**
- Is it wrapped in `<AnimatePresence>`?
- Does the component inside have enter/exit animations?
- If NO to both → this is a **motion gap** that needs fixing.

**Common motion gap patterns:**
- `{isOpen && <Modal />}` — Modal appears/disappears instantly.
- `{mode === ...}` — [Continue with additional patterns as necessary].

### State Your Inference

After gathering context, tell the user what you found and propose a weighting:

```
## Reconnaissance Complete

**Project type**: [What you inferred — e.g., "Kids educational app, mobile-first PWA"]
**Existing animation style**: [What you observed — e.g., "Spring animations (500-600ms), framer-motion, active:scale patterns"]
**Likely intent**: [Your inference — e.g., "Delight and engagement for young children"]

**Proposed perspective weighting**:
- **Primary**: [Designer] — [Why]
- **Secondary**: [Designer] — [Why]
- **Selective**: [Designer] — [When applicable]

Does this approach sound right? Should I adjust the weighting before proceeding with the full audit?
```

### Wait for User Confirmation

**STOP and wait for the user to confirm or adjust.** Do not proceed to the full audit until you receive confirmation.