---
name: frontend-design
description: Use this skill when designing components, layouts, color schemes, typography, or creating aesthetic interfaces for web UI. It emphasizes design thinking and decision-making principles rather than fixed values.
---

# Frontend Design System

> **Philosophy:** Every pixel has purpose. Restraint is luxury. User psychology drives decisions.
> **Core Principle:** THINK, don't memorize. ASK, don't assume.

---

## 🎯 Selective Reading Rule (MANDATORY)

**Read REQUIRED files always, OPTIONAL only when needed:**

| File                                         | Status          | When to Read                      |
| -------------------------------------------- | --------------- | --------------------------------- |
| [ux-psychology.md](ux-psychology.md)         | 🔴 **REQUIRED** | Always read first!                |
| [color-system.md](color-system.md)           | ⚪ Optional     | Color/palette decisions           |
| [typography-system.md](typography-system.md) | ⚪ Optional     | Font selection/pairing            |
| [visual-effects.md](visual-effects.md)       | ⚪ Optional     | Glassmorphism, shadows, gradients |
| [animation-guide.md](animation-guide.md)     | ⚪ Optional     | Animation needed                  |
| [motion-graphics.md](motion-graphics.md)     | ⚪ Optional     | Lottie, GSAP, 3D                  |
| [decision-trees.md](decision-trees.md)       | ⚪ Optional     | Context templates                 |

> 🔴 **ux-psychology.md = ALWAYS READ. Others = only if relevant.**

---

## 🔧 Runtime Scripts

**Execute these for audits (don't read, just run):**

| Script                | Purpose                             | Usage                                       |
| --------------------- | ----------------------------------- | ------------------------------------------- |
| `scripts/ux_audit.py` | UX Psychology & Accessibility Audit | `python scripts/ux_audit.py <project_path>` |

---

## ⚠️ CRITICAL: ASK BEFORE ASSUMING (MANDATORY)

> **STOP! If the user's request is open-ended, DO NOT default to your favorites.**

### When User Prompt is Vague, ASK:

**Color not specified?** Ask:
> "What color palette do you prefer? (blue/green/orange/neutral/other?)"

**Style not specified?** Ask:
> "What style are you going for? (minimal/bold/retro/futuristic/organic?)"

**Layout not specified?** Ask:
> "Do you have a layout preference? (single column/grid/asymmetric/full-width?)"

### ⛔ DEFAULT TENDENCIES TO AVOID (ANTI-SAFE HARBOR):

| AI Default Tendency | Why It's Bad | Think Instead |
|---------------------|--------------|---------------|
| **Bento Grids (Modern Cliché)** | Used in every AI design | Why does this content NEED a grid? |
| **Hero Split (Left/Right)** | Predictable & Boring | How about Massive Typography or Vertical Narrative? |
| **Mesh/Aurora Gradients** | The "new" lazy background | What's a radical color pairing? |