---
name: design-suite:launchpad-audit
description: Check code against landing page design for brand violations and AI-generic defaults.
---

# launchpad audit

Check existing code against landing page design patterns.

## Usage

```
/design-suite:launchpad-audit <path>     # Audit specific file/directory
/design-suite:launchpad-audit            # Audit common UI paths
```

## What to Check

### Layer 1: System Violations (if `.launchpad/system.md` exists)

1. **Color violations**
   - Colors outside defined palette
   - Hardcoded colors instead of CSS variables
   - Example: `#6366f1` when palette uses `var(--brand)`

2. **Typography violations**
   - Fonts not matching defined system
   - Scale not matching hero/display definitions
   - Generic fonts where signature fonts expected

3. **Signature presence**
   - Verify the signature element exists
   - Check it's prominent, not buried
   - Ensure it matches the documented approach

### Layer 2: AI-Generic Defaults (always checked)

These are checked regardless of whether system.md exists:

1. **Gradient violations**
   - Purple-to-blue gradients (`from-purple-* to-blue-*`, `from-violet-* to-indigo-*`)
   - Indigo-to-purple variations
   - Any gradient that screams "AI-generated"

2. **Font violations**
   - Inter/Roboto/system fonts for headlines
   - No display font personality
   - Generic font stacks with no brand voice

3. **Layout violations**
   - Centered everything (no asymmetry)
   - Feature grids with generic icons
   - Same section rhythm throughout
   - Hero → Features → Testimonials → CTA template

4. **Decoration violations**
   - Floating blobs and abstract shapes
   - Meaningless gradients as backgrounds
   - Stock illustration patterns

5. **Color violations**
   - Gray backgrounds everywhere
   - Safe, non-committal palettes
   - Colors that could work for any company

## Report Format

```
Audit Results: src/components/

System Violations: (if system.md exists)
  Hero.tsx:8 - Color #6366f1 not in palette (use var(--brand))
  CTA.tsx:15 - Font "Inter" not in system (expected: "Clash Display")

AI-Generic Defaults:
  Hero.tsx:12 - Purple-to-blue gradient detected (from-purple-500 to-blue-600)
  Features.tsx:5 - Generic feature grid with icons
  layout.tsx:3 - Inter font for headlines (no personality)
  Page.tsx:20 - All sections centered (no asymmetry)

Suggestions:
  - Replace gradient with brand color or intentional palette choice
  - Rethink feature section: what makes YOUR features unique?
  - Choose a display font that commits to a personality
  - Introduce asymmetric layouts in at least 2 sections
```

**If no system.md and defaults found:**

```
No landing page system to audit against.

However, AI-generic defaults detected:
  [list of defaults found]

Suggestions:
1. Run /design-suite:launchpad-init → establish brand direction
2. Run /design-suite:launchpad-extract → create system from existing code

Then re-audit to catch system violations.
```

## Implementation

1. Check for system.md
2. Parse system rules if present
3. Read target files (tsx, jsx, css, scss)
4. Check against system rules (Layer 1)
5. Check against AI-generic patterns (Layer 2)
6. Report violations with specific suggestions
