---
name: design-suite:launchpad-status
description: Show current landing page design state including brand direction, colors, typography, and signature element.
---

# launchpad status

Show current landing page design state.

## What to Show

**If `.launchpad/system.md` exists:**

Display:
```
Landing Page System: [Project Name]

Brand Direction: [Bold & Playful / Minimal & Premium / etc]
Personality: [Key personality traits]

Color Palette:
- Brand: [value]
- Surface: [value]
- Ink: [value]
- Accent: [value]

Typography:
- Display: [font family]
- Body: [font family]
- Hero scale: [clamp value]

Signature Element: [The unforgettable moment]

Component Patterns:
- CTA: [description]
- Hero: [description]
- [other patterns...]

Animation Approach: [Reveal on scroll / Staggered entrance / etc]

Last updated: [from git or file mtime]
```

**If no system.md:**

```
No landing page system found.

Options:
1. Run /design-suite:launchpad-init → explore brand, build with craft
2. Run /design-suite:launchpad-extract → pull patterns from existing code
```

## Implementation

1. Read `.launchpad/system.md`
2. Parse brand direction, colors, typography, signature, patterns
3. Format and display
4. If no system, suggest next steps
