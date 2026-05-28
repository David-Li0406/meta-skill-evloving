---
name: design-lab
description: Use this skill when you want to explore UI design options, redesign existing components, or create new UI with multiple approaches to compare.
---

# Design Lab Skill

This skill implements a complete design exploration workflow: conduct interviews, generate five distinct UI variations, collect feedback, refine designs, preview, and finalize.

## CRITICAL: Cleanup Behavior

**All temporary files MUST be deleted when the process ends, whether by:**
- User confirms final design → cleanup, then generate plan
- User aborts/cancels → cleanup immediately, no plan generated

**Never leave `.claude-design/` or `__design_lab` routes behind.** If the user says "cancel", "abort", "stop", or "nevermind" at any point, confirm and then delete all temporary artifacts.

---

## Phase 0: Preflight Detection

Before starting the interview, automatically detect:

### Package Manager
Check for lock files in the project root:
- `pnpm-lock.yaml` → use `pnpm`
- `yarn.lock` → use `yarn`
- `package-lock.json` → use `npm`
- `bun.lockb` → use `bun`

### Framework Detection
Check for config files:
- `next.config.js` or `next.config.mjs` or `next.config.ts` → **Next.js**
  - Check for `app/` directory → App Router
  - Check for `pages/` directory → Pages Router
- `vite.config.js` or `vite.config.ts` → **Vite**
- `remix.config.js` → **Remix**
- `nuxt.config.js` or `nuxt.config.ts` → **Nuxt**
- `astro.config.mjs` → **Astro**

### Styling System Detection
Check `package.json` dependencies and config files:
- `tailwind.config.js` or `tailwind.config.ts` → **Tailwind CSS**
- `@mui/material` in dependencies → **Material UI**
- `@chakra-ui/react` in dependencies → **Chakra UI**
- `antd` in dependencies → **Ant Design**
- `styled-components` in dependencies → **styled-components**
- `@emotion/react` in dependencies → **Emotion**
- `.css` or `.module.css` files → **CSS Modules**

### Design Memory Check
Look for existing Design Memory file:
- `docs/design-memory.md`
- `DESIGN_MEMORY.md`
- `.claude-design/design-memory.md`

If found, read it and use to prefill defaults and skip redundant questions.

### Visual Style Inference (CRITICAL)

**DO NOT use generic/predefined styles. Extract visual language from the project:**

**If Tailwind detected**, read `tailwind.config.js` or `tailwind.config.ts`:
```javascript
// Extract and use:
theme.colors      // Color palette
```