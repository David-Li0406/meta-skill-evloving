---
name: findatruck-ui-ux-polisher
description: Use this skill when the user asks to make FindATruck UI/UX better looking, smoother, faster, improve animations, reduce jank, improve perceived performance, polish interactions, or tighten design consistency without changing the brand.
---

# FindATruck UI/UX + Animation Polish

## Goal
Ship UI/UX polish that *feels premium* and *runs at 60fps*:
- smoother animations (no jank)
- faster perceived load
- consistent design system (spacing/typography/colors)
- zero random "AI-looking" styling
- keep the app simple + modular

## Non-negotiables (hard constraints)
1. **No brand drift**
   - Do not invent new colors "because it looks cool".
   - Use existing design tokens if they exist (Tailwind theme, CSS vars, globals.css).
   - If tokens do *not* exist, create a minimal token set and apply it consistently.
2. **Icons**
   - Prefer the project's custom icon set (the "icons we made").
   - Do not introduce new icon libraries unless the repo already uses them.
3. **Accessibility**
   - Respect `prefers-reduced-motion`.
   - All interactive elements must have keyboard/focus states.
4. **Performance**
   - Avoid heavy animation libs unless already in project.
   - Prefer CSS transforms/opacity; avoid layout-thrashing properties.

## When this skill is used
Run this workflow every time.

### Step 0 — Establish the baseline (before touching code)
- Identify the target pages/components (map, cards, filters, drawers, modals).
- Find the animation code paths (Framer Motion / CSS / GSAP / requestAnimationFrame).
- Collect **baseline**:
  - list the biggest components and where renders happen
  - note any obvious expensive loops, re-renders, or DOM-heavy markers
  - record any existing "animation gate" logic (networkSlow / userInteracted / zoom, etc.)

### Step 1 — Produce a tight "Polish Plan" (max 12 bullets)
For each bullet:
- what changes
- where (file/component)
- why (UX/perf)
- risk (low/med/high)

Prefer small, high-impact changes.

### Step 2 — Implement polish with strict engineering rules

#### A) Animation rules (must follow)
- Prefer **transform + opacity** animations only.
- Never animate: `width`, `height`, `top/left`, `box-shadow` (unless tiny + proven safe).
- Use easing that feels natural:
  - fast in, smooth out; no "floaty" durations.
- Cap durations:
  - micro-interactions: 120–220ms
  - drawers/modals: 220–360ms
- Add `prefers-reduced-motion`:
  - if reduced motion, disable non-essential animations and keep fades minimal.
- Add/keep an **animation gate**:
  - only animate if user has interacted OR device/network is safe
  - never animate heavy map markers while zoomed out / clustering
- If a component animates on scroll:
  - use IntersectionObserver
  - never bind expensive work directly to scroll events

#### B) React/Next rules (must follow)
- Kill unnecessary rerenders:
  - memoize derived data (`useMemo`)
  - memoize callbacks (`useCallback`) only when it actually helps
  - split heavy components; keep props stable
- Avoid "global state rerendering the whole page":
  - localize state to the smallest subtree possible
- Any list > 30 items:
  - consider virtualization (or pagination), but don't over-engineer
- Map markers:
  - cluster aggressively when zoomed out
  - keep marker DOM light
  - avoid per-marker React state if possible

#### C) Visual system rules (must follow)
- Use one spacing scale (e.g. 4/8/12/16/24/32).
- Use 2–3 type sizes per view (headline, body, caption).
- Consistent radii and shadows (don't mix random ones).
- States must be consistent:
  - hover, active, focus, disabled, loading
- Keep contrast readable:
  - text on gradients must remain crisp
- If you change backgrounds:
  - do it via tokens (CSS vars / Tailwind theme), not ad-hoc hex codes in components

### Step 3 — Verification (no skipping)
Run whatever scripts exist in package.json (don't guess names):
- lint
- typecheck
- build

Then do a manual smoke check:
- first load (no stutter)
- open/close drawers/modals quickly
- move through map zoom levels
- rapid filter toggles (no UI lag)
- reduced motion mode

### Step 4 — Output format to the user (required)
Deliver:
1. **What changed** (bullet list)
2. **Files touched**
3. **Perf/UX impact** (what got faster/smoother)
4. **Any follow-ups** (max 5)

## Common fixes to look for (fast wins)
- Skeletons/placeholder transitions that cause layout shifts → lock heights
- "Animating shadows" → replace with opacity fade + subtle transform
- Expensive calculations in render → move to memo or server
- Too many gradients + low contrast → simplify surfaces, stronger hierarchy
- Map marker rerenders on hover → separate hover layer or use CSS-only

## Example prompts that should trigger this skill
- "Make the animations smoother"
- "UI feels off-brand / too AI-ish"
- "Map is janky when zooming"
- "Make it feel more premium"
- "Speed it up without rewriting everything"
